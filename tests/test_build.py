"""scripts/build.py: what the .deb and the tarball contain, and that two builds are identical."""

import hashlib
import importlib.util
import io
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock

from support import ROOT

from hecate_volume import __version__

spec = importlib.util.spec_from_file_location("build", ROOT / "scripts" / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

NEEDS_DPKG = unittest.skipUnless(shutil.which("dpkg-deb"), "dpkg-deb not installed (package dpkg)")


class Build(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patch = mock.patch.object(build, "DIST", pathlib.Path(self.tmp.name))
        patch.start()
        self.addCleanup(patch.stop)
        self.epoch = 1793577600

    @NEEDS_DPKG
    def test_deb_contents_and_control(self):
        deb = build.build_deb(self.epoch)
        self.assertEqual(deb.name, f"hecate-g2000-pro-volume_{__version__}_all.deb")
        listing = subprocess.run(["dpkg-deb", "--contents", deb], capture_output=True, text=True, check=True).stdout
        paths = {line.split()[-1].removeprefix(".") for line in listing.splitlines()}
        for expected in (
            "/usr/bin/hecate-g2000-pro-volume",
            "/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf",
            "/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf",
            "/usr/share/hecate-g2000-pro-volume/hecate_volume/cli.py",
            "/usr/share/doc/hecate-g2000-pro-volume/copyright",
            "/usr/share/doc/hecate-g2000-pro-volume/changelog.gz",
            "/usr/share/man/man1/hecate-g2000-pro-volume.1.gz",
        ):
            self.assertIn(expected, paths)
        self.assertFalse([path for path in paths if "__pycache__" in path or path.endswith(".pyc")])
        self.assertTrue(all(" root/root " in line for line in listing.splitlines()), "owned by root")
        field = lambda name: subprocess.run(  # noqa: E731
            ["dpkg-deb", "--field", deb, name], capture_output=True, text=True, check=True
        ).stdout.strip()
        self.assertEqual(field("Version"), __version__)
        self.assertEqual(field("Architecture"), "all")
        self.assertIn("wireplumber (>= 0.5)", field("Depends"))

    @NEEDS_DPKG
    def test_installed_command_runs_from_its_package_tree(self):
        root = pathlib.Path(self.tmp.name, "root")
        subprocess.run(["dpkg-deb", "-x", build.build_deb(self.epoch), root], check=True)
        launcher = (root / "usr/bin/hecate-g2000-pro-volume").read_text()
        self.assertTrue(launcher.startswith("#!/usr/bin/python3\n"))
        self.assertIn("'/usr/share/hecate-g2000-pro-volume'", launcher)
        # The same launcher, pointed at the extracted tree instead of /usr/share.
        extracted = repr(str(root / "usr/share/hecate-g2000-pro-volume"))
        local = launcher.replace("'/usr/share/hecate-g2000-pro-volume'", extracted)
        result = subprocess.run(["python3", "-c", local, "--version"], capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.strip(), f"hecate-g2000-pro-volume {__version__}")

    def test_tarball_installs_for_the_user(self):
        tarball = build.build_tarball(self.epoch)
        with tarfile.open(tarball) as archive:
            members = {member.name: member for member in archive.getmembers()}
            top = f"hecate-g2000-pro-volume-{__version__}"
            self.assertEqual(members[f"{top}/hecate-g2000-pro-volume"].mode, 0o755)
            self.assertTrue(all(member.mtime == self.epoch and member.uid == 0 for member in members.values()))
            safe = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}  # PEP 706, Python 3.11.4+
            archive.extractall(self.tmp.name, **safe)  # noqa: S202 - our own tarball, data filter when available
        config = pathlib.Path(self.tmp.name, "config")
        env = {**os.environ, "XDG_CONFIG_HOME": str(config)}
        command = [pathlib.Path(self.tmp.name, top, "hecate-g2000-pro-volume"), "install"]
        result = subprocess.run(command, capture_output=True, text=True, env=env, check=True)
        self.assertEqual(result.stdout.count("Installed "), 2)
        self.assertTrue((config / "wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf").is_file())

    @NEEDS_DPKG
    def test_two_builds_are_identical(self):
        def digests():
            built = [build.build_deb(self.epoch), build.build_tarball(self.epoch)]
            return [hashlib.sha256(path.read_bytes()).hexdigest() for path in built]

        self.assertEqual(digests(), digests())

    def test_copyright_is_dep5_with_the_license_text(self):
        text = build.copyright_file()
        self.assertTrue(text.startswith("Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/"))
        self.assertIn("Copyright: 2026 Marcos Xavier", text)
        self.assertIn("License: Expat", text)
        self.assertIn(' THE SOFTWARE IS PROVIDED "AS IS"', text)

    def test_one_version_everywhere(self):
        import tomllib

        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        self.assertEqual(project["version"], __version__)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(changelog, rf"(?m)^## \[{__version__}\] - \d{{4}}-\d{{2}}-\d{{2}}$")
        manpage = (ROOT / "docs" / "hecate-g2000-pro-volume.1").read_text(encoding="utf-8")
        self.assertIn(f'"hecate-g2000-pro-volume {__version__}"', manpage)

    def test_gzip_is_deterministic(self):
        self.assertEqual(build.gzip_bytes(b"x", 5), build.gzip_bytes(b"x", 5))
        self.assertEqual(io.BytesIO(build.gzip_bytes(b"x", 5)).read(2), b"\x1f\x8b")


if __name__ == "__main__":
    unittest.main()
