"""Installing the two configuration files for one user, and the files themselves."""

import pathlib
import re
import tempfile
import unittest

from support import ROOT

from hecate_volume import files


class Locations(unittest.TestCase):
    def test_user_base_follows_xdg_config_home(self):
        self.assertEqual(files.user_base({"XDG_CONFIG_HOME": "/x/cfg", "HOME": "/home/u"}), pathlib.Path("/x/cfg"))
        for unusable in ("", "relative/dir"):  # XDG Base Directory spec: ignore empty or relative values
            with self.subTest(value=unusable):
                base = files.user_base({"XDG_CONFIG_HOME": unusable, "HOME": "/home/u"})
                self.assertEqual(base, pathlib.Path("/home/u/.config"))

    def test_sources_are_the_files_in_the_repository(self):
        for source, _ in files.SOURCES.values():
            self.assertTrue(source.is_relative_to(ROOT / "src" / "hecate_volume" / "config"))
            self.assertTrue(source.is_file())

    def test_destinations_are_the_paths_wireplumber_and_acp_read(self):
        found = {str(path) for path in files.targets(pathlib.Path("/usr/share")).values()}
        self.assertEqual(
            found,
            {
                "/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf",
                "/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf",
            },
        )


class UserInstall(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def states(self):
        return [item.state for item in files.inspect(self.base, "user")]

    def test_install_then_uninstall(self):
        self.assertEqual(self.states(), ["missing", "missing"])
        self.assertEqual(len(files.install_user(self.base)), 2)
        self.assertEqual(self.states(), ["current", "current"])
        self.assertEqual(files.install_user(self.base), [], "a second install changes nothing")
        self.assertEqual(len(files.uninstall_user(self.base)), 2)
        self.assertEqual(self.states(), ["missing", "missing"])

    def test_a_file_with_other_content_is_kept_unless_forced(self):
        target = files.targets(self.base)[files.WIREPLUMBER_RULE]
        target.parent.mkdir(parents=True)
        target.write_text("# my own rule\n")
        with self.assertRaises(files.InstallError):
            files.install_user(self.base)
        self.assertEqual(target.read_text(), "# my own rule\n", "nothing replaced")
        self.assertFalse(files.targets(self.base)[files.PROFILE_SET].exists(), "nothing half-installed")
        with self.assertRaises(files.InstallError):
            files.uninstall_user(self.base)
        self.assertTrue(target.exists())
        files.install_user(self.base, force=True)
        self.assertEqual(self.states(), ["current", "current"])

    def test_no_temporary_file_is_left(self):
        files.install_user(self.base)
        leftovers = [path for path in self.base.rglob(".*.tmp")]
        self.assertEqual(leftovers, [])


class ConfigurationFiles(unittest.TestCase):
    """The content that the tests on the reference machine validated (see docs/TESTING.md)."""

    def test_profile_set_offers_only_the_analog_output_through_the_analog_output_path(self):
        text = files.SOURCES[files.PROFILE_SET][0].read_text(encoding="utf-8")
        body = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith(";")]
        self.assertEqual(
            body,
            [
                "[General]",
                "auto-profiles = yes",
                "[Mapping analog-stereo]",
                "device-strings = front:%f",
                "channel-map = left,right",
                "paths-output = analog-output",
                "direction = output",
                "priority = 15",
            ],
        )
        # element-output builds a path without a description: WirePlumber 0.5.8 aborts (compat.c:123)
        self.assertNotIn("element-output", body[5])

    def test_wireplumber_rule_matches_only_the_usb_ids_and_names_the_profile_set(self):
        text = files.SOURCES[files.WIREPLUMBER_RULE][0].read_text(encoding="utf-8")
        code = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
        self.assertEqual(
            re.findall(r"(device\.[\w.-]+) = \"([^\"]*)\"", code),
            [
                ("device.vendor.id", "0x35bb"),
                ("device.product.id", "0xb065"),
                ("device.profile-set", files.PROFILE_SET),
            ],
        )
        self.assertIn("monitor.alsa.rules", code)
        self.assertEqual(code.count("{"), code.count("}"))
        self.assertEqual(code.count("["), code.count("]"))


if __name__ == "__main__":
    unittest.main()
