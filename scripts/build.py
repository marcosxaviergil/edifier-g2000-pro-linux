"""Build dist/: the Debian package and the tarball for other distributions.

- hecate-g2000-pro-volume_<version>_all.deb: the configuration in the distribution data directory
  (/usr/share/wireplumber/wireplumber.conf.d and /usr/share/alsa-card-profile/mixer/profile-sets,
  the paths WirePlumber and PipeWire's ALSA card profile code read; see src/hecate_volume/files.py),
  the command in /usr/bin, its code in /usr/share/hecate-g2000-pro-volume, copyright, changelog, man page.
- hecate-g2000-pro-volume-<version>.tar.gz: the command and the configuration, installed per user
  with `./hecate-g2000-pro-volume install` (no root).

Reproducible: every file gets the SOURCE_DATE_EPOCH time (default: the time of the last git commit),
owner root, mode 0644 or 0755, in sorted order; gzip and dpkg-deb get the same time.

    python3 -B scripts/build.py   # needs dpkg-deb (package dpkg)
"""

import datetime
import gzip
import hashlib
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "hecate_volume"
DIST = ROOT / "dist"
PACKAGE = "hecate-g2000-pro-volume"
sys.path.insert(0, str(ROOT / "src"))
from hecate_volume import __version__, files  # noqa: E402 - the version and file layout of the code itself

LAUNCHER = '''#!{python}
"""{package}: see `{package} --help` and the manual."""

import sys

sys.dont_write_bytecode = True  # no __pycache__ next to the code, which may belong to root
sys.path.insert(0, {library})

from hecate_volume.cli import main  # noqa: E402

sys.exit(main())
'''
DESCRIPTION = """\
Edifier Hecate G2000 PRO: system volume drives the hardware volume
 Configuration for PipeWire and WirePlumber that makes the system volume and
 mute of the Edifier Hecate G2000 PRO USB speaker (USB 35bb:b065) change the
 speaker's own ALSA PCM controls, with no software volume on top. Other audio
 devices are not changed.
 .
 Includes hecate-g2000-pro-volume, a command to check the configuration
 (status) and to test that the hardware follows the system volume (diagnose)."""


def fail(message):
    sys.exit(f"build: {message}")


def source_date_epoch():
    """SOURCE_DATE_EPOCH, else the last commit time, else the date of this version in CHANGELOG.md."""
    if os.environ.get("SOURCE_DATE_EPOCH", "").isdigit():
        return int(os.environ["SOURCE_DATE_EPOCH"])
    try:
        result = subprocess.run(["git", "log", "-1", "--format=%ct"], cwd=ROOT, capture_output=True, text=True)  # noqa: S603, S607
        if result.stdout.strip().isdigit():
            return int(result.stdout.strip())
    except FileNotFoundError:
        pass
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(rf"^## \[{re.escape(__version__)}\] - (\d{{4}}-\d{{2}}-\d{{2}})$", text, re.M)
    if not match:
        fail(f"CHANGELOG.md has no '## [{__version__}] - YYYY-MM-DD' line and git has no commit")
    return int(datetime.datetime.fromisoformat(match[1]).replace(tzinfo=datetime.UTC).timestamp())


def code_files():
    """(path relative to the package, path) of the code and configuration; no caches."""
    found = []
    for path in sorted(SOURCE.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            found.append((path.relative_to(SOURCE), path))
    return found


def gzip_bytes(data, epoch):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="wb", compresslevel=9, mtime=epoch, filename="") as stream:
        stream.write(data)
    return out.getvalue()


def debian_changelog(epoch):
    """A one-entry Debian changelog for this native package (the history is in CHANGELOG.md)."""
    from email.utils import formatdate

    return (
        f"{PACKAGE} ({__version__}) unstable; urgency=medium\n\n"
        f"  * Release {__version__}. History: CHANGELOG.md in the source.\n\n"
        f" -- {debian_fields()['maintainer']}  {formatdate(epoch, localtime=False)}\n"
    )


def debian_fields():
    """[tool.debian] of pyproject.toml: maintainer, depends, recommends."""
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["debian"]


def copyright_file():
    """debian/copyright (DEP-5) from LICENSE: the MIT license is called Expat there."""
    lines = (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()
    holders = [line.removeprefix("Copyright (c) ") for line in lines if line.startswith("Copyright (c) ")]
    if not holders:
        fail("LICENSE has no 'Copyright (c) ' line")
    last = max(number for number, line in enumerate(lines) if line.startswith("Copyright (c) "))
    body = "\n".join(f" {line}" if line.strip() else " ." for line in "\n".join(lines[last + 1 :]).strip().splitlines())
    copyright_lines = "\n           ".join(holders)
    return (
        "Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n"
        f"Upstream-Name: {PACKAGE}\n\n"
        "Files: *\n"
        f"Copyright: {copyright_lines}\n"
        "License: Expat\n"
        f"{body}\n"
    )


def stage_deb(stage, epoch):
    """The package tree below `stage`."""
    library = pathlib.Path("usr/share") / PACKAGE
    for relative, path in code_files():
        target = stage / library / "hecate_volume" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    for target in files.targets(stage / "usr/share").values():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(files.SOURCES[target.name][0], target)
    launcher = stage / "usr/bin" / PACKAGE
    launcher.parent.mkdir(parents=True)
    launcher.write_text(LAUNCHER.format(python="/usr/bin/python3", package=PACKAGE, library=repr(f"/{library}")))
    docs = stage / "usr/share/doc" / PACKAGE
    docs.mkdir(parents=True)
    (docs / "copyright").write_text(copyright_file())
    (docs / "changelog.gz").write_bytes(gzip_bytes(debian_changelog(epoch).encode(), epoch))
    shutil.copyfile(ROOT / "README.md", docs / "README.md")
    man = stage / "usr/share/man/man1" / f"{PACKAGE}.1.gz"
    man.parent.mkdir(parents=True)
    man.write_bytes(gzip_bytes((ROOT / "docs" / f"{PACKAGE}.1").read_bytes(), epoch))
    normalize(stage, executables={launcher}, epoch=epoch)
    control_dir = stage / "DEBIAN"
    control_dir.mkdir()
    payload = sorted(path for path in stage.rglob("*") if path.is_file() and "DEBIAN" not in path.parts)
    size = sum(path.stat().st_size for path in payload)
    control = debian_fields()
    (control_dir / "control").write_text(
        f"Package: {PACKAGE}\nVersion: {__version__}\nArchitecture: all\nMaintainer: {control['maintainer']}\n"
        f"Installed-Size: {(size + 1023) // 1024}\nDepends: {control['depends']}\nRecommends: {control['recommends']}\n"
        f"Section: sound\nPriority: optional\nDescription: {DESCRIPTION}\n"
    )
    (control_dir / "md5sums").write_text(
        "".join(f"{hashlib.md5(path.read_bytes()).hexdigest()}  {path.relative_to(stage)}\n" for path in payload)  # noqa: S324 - dpkg format
    )
    normalize(control_dir, executables=set(), epoch=epoch)


def normalize(base, executables, epoch):
    for path in [base, *base.rglob("*")]:
        if path.is_dir():
            path.chmod(0o755)
        else:
            path.chmod(0o755 if path in executables else 0o644)
        os.utime(path, (epoch, epoch), follow_symlinks=False)


def build_deb(epoch):
    stage = DIST / "deb-root"
    shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir(parents=True)
    stage_deb(stage, epoch)
    out = DIST / f"{PACKAGE}_{__version__}_all.deb"
    env = {**os.environ, "SOURCE_DATE_EPOCH": str(epoch)}
    command = ["dpkg-deb", "--root-owner-group", "-Zxz", "--build", str(stage), str(out)]
    try:
        subprocess.run(command, check=True, env=env, capture_output=True, text=True)  # noqa: S603, S607
    except FileNotFoundError:
        fail("dpkg-deb is missing. Debian/Ubuntu: it comes with the dpkg package")
    except subprocess.CalledProcessError as error:
        fail(f"dpkg-deb failed: {error.stderr.strip()}")
    shutil.rmtree(stage)
    return out


def build_tarball(epoch):
    top = f"{PACKAGE}-{__version__}"
    entries = [(f"{top}/lib/hecate_volume/{relative}", path.read_bytes(), 0o644) for relative, path in code_files()]
    launcher = LAUNCHER.format(
        python="/usr/bin/env python3",
        package=PACKAGE,
        library='str(__import__("pathlib").Path(__file__).resolve().parent / "lib")',
    )
    entries.append((f"{top}/{PACKAGE}", launcher.encode(), 0o755))
    for name in ("README.md", "LICENSE", "CHANGELOG.md"):
        entries.append((f"{top}/{name}", (ROOT / name).read_bytes(), 0o644))
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w", format=tarfile.PAX_FORMAT) as archive:
        folders = {str(parent) for name, _, _ in entries for parent in pathlib.PurePosixPath(name).parents}
        for name in sorted(folders - {"."}):
            info = tarfile.TarInfo(name)
            info.type, info.mode, info.mtime = tarfile.DIRTYPE, 0o755, epoch
            archive.addfile(info)
        for name, content, mode in sorted(entries):
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(content), mode, epoch
            archive.addfile(info, io.BytesIO(content))
    out = DIST / f"{top}.tar.gz"
    out.write_bytes(gzip_bytes(data.getvalue(), epoch))
    return out


def main():
    epoch = source_date_epoch()
    DIST.mkdir(exist_ok=True)
    built = [build_deb(epoch), build_tarball(epoch)]
    for path in built:
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
