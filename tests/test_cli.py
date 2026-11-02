"""The four commands against the fake audio system and temporary configuration directories."""

import io
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from support import ROOT, FakeSystem

from hecate_volume import __version__, cli, files, pipewire


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.environ = {"XDG_CONFIG_HOME": str(root / "config"), "HOME": str(root)}
        patch = mock.patch.object(files, "SYSTEM_BASE", root / "usr-share")
        patch.start()
        self.addCleanup(patch.stop)
        self.addCleanup(self.tmp.cleanup)

    def run_cli(self, *argv, system=None):
        out = io.StringIO()
        code = cli.main(list(argv), audio=pipewire.Audio(system or FakeSystem()), environ=self.environ, out=out)
        return code, out.getvalue()


class Status(Base):
    def test_ok_when_installed_loaded_and_analog(self):
        self.run_cli("install")
        code, text = self.run_cli("status", system=FakeSystem(profile_set=files.PROFILE_SET))
        self.assertEqual(code, 0, text)
        self.assertIn("Result: OK", text)
        self.assertIn("Software volume: 1.00, 1.00", text)

    def test_not_installed(self):
        code, text = self.run_cli("status", system=FakeSystem(profile="iec958-stereo"))
        self.assertEqual(code, 1)
        self.assertIn("not installed", text)

    def test_installed_but_wireplumber_not_restarted(self):
        self.run_cli("install")
        code, text = self.run_cli("status", system=FakeSystem(profile="iec958-stereo"))
        self.assertEqual(code, 1)
        self.assertIn("systemctl --user restart wireplumber.service", text)

    def test_speaker_disconnected(self):
        code, text = self.run_cli("status", system=FakeSystem(connected=False))
        self.assertEqual(code, 1)
        self.assertIn("does not see the speaker", text)

    def test_status_changes_nothing(self):
        system = FakeSystem()
        self.run_cli("status", system=system)
        verbs = {call[1] for call in system.calls if call[0] == "wpctl"}
        self.assertLessEqual(verbs, {"status", "inspect", "get-volume"})


class Diagnose(unittest.TestCase):
    def run_diagnose(self, system):
        out = io.StringIO()
        code = cli.diagnose(pipewire.Audio(system), out, sleep=lambda seconds: None)
        return code, out.getvalue()

    def test_passes_with_the_analog_profile_and_restores_volume_and_mute(self):
        system = FakeSystem(volume=0.40)
        code, text = self.run_diagnose(system)
        self.assertEqual(code, 0, text)
        self.assertEqual(text.count("PASS"), 3)
        self.assertEqual((system.volume, system.muted), (0.40, False))
        self.assertEqual(system.hardware, round(0.40 * 147))

    def test_fails_with_the_iec958_profile_where_volume_is_software_only(self):
        system = FakeSystem(profile="iec958-stereo", volume=1.0, hardware=147)
        code, text = self.run_diagnose(system)
        self.assertEqual(code, 1)
        self.assertIn("FAIL: Hardware volume follows the system volume", text)
        self.assertIn("FAIL: Software volume stays at 100%", text)

    def test_never_plays_louder_than_before(self):
        system = FakeSystem(volume=0.20)
        self.run_diagnose(system)
        asked = [float(call[3]) for call in system.calls if call[:2] == ["wpctl", "set-volume"]]
        self.assertTrue(all(volume <= 0.20 for volume in asked), asked)

    def test_restores_even_when_a_reading_fails(self):
        system = FakeSystem(volume=0.60)
        audio = pipewire.Audio(system)
        failing = mock.patch.object(audio, "props", side_effect=pipewire.AudioError("pw-cli failed"))
        with failing, self.assertRaises(pipewire.AudioError):
            cli.diagnose(audio, io.StringIO(), sleep=lambda seconds: None)
        self.assertEqual((system.volume, system.muted), (0.60, False))

    def test_volumes_below(self):
        self.assertEqual(cli.volumes_below(0.40), [0.3, 0.2, 0.1])
        self.assertEqual(cli.volumes_below(0.04), [0.03, 0.02, 0.01])
        self.assertIsNone(cli.volumes_below(0.03))

    def test_too_low_volume_is_not_tested_and_nothing_changes(self):
        system = FakeSystem(volume=0.0)
        code, text = self.run_diagnose(system)
        self.assertEqual(code, 1)
        self.assertIn("too low", text)
        self.assertFalse([call for call in system.calls if call[1] in ("set-volume", "set-mute")])


class InstallCommand(Base):
    def test_install_prints_how_to_apply(self):
        code, text = self.run_cli("install")
        self.assertEqual(code, 0)
        self.assertEqual(text.count("Installed "), 2)
        self.assertIn("systemctl --user restart wireplumber.service", text)

    def test_install_does_nothing_when_the_package_provides_the_files(self):
        files.install_user(files.SYSTEM_BASE)  # same layout as the .deb below /usr/share
        code, text = self.run_cli("install")
        self.assertEqual(code, 0)
        self.assertIn("Nothing to do", text)
        self.assertFalse(pathlib.Path(self.environ["XDG_CONFIG_HOME"], "wireplumber").exists())

    def test_conflict_is_an_error_with_exit_code_2(self):
        target = files.targets(files.user_base(self.environ))[files.WIREPLUMBER_RULE]
        target.parent.mkdir(parents=True)
        target.write_text("# mine\n")
        with mock.patch("sys.stderr", new_callable=io.StringIO) as err:
            code, _ = self.run_cli("install")
        self.assertEqual(code, 2)
        self.assertIn("install --force", err.getvalue())

    def test_uninstall(self):
        self.run_cli("install")
        code, text = self.run_cli("uninstall")
        self.assertEqual((code, text.count("Removed ")), (0, 2))


class Program(unittest.TestCase):
    def test_module_runs_and_reports_its_version(self):
        result = subprocess.run(
            [sys.executable, "-B", "-m", "hecate_volume", "--version"],
            cwd=ROOT / "src",
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), f"hecate-g2000-pro-volume {__version__}")


if __name__ == "__main__":
    unittest.main()
