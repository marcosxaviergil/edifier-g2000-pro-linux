"""Parsing the recorded outputs of wpctl, pw-cli and amixer, and finding the G2000 PRO."""

import unittest

from support import G2000_SINK, FakeSystem, fixture

from hecate_volume import pipewire


class Parsing(unittest.TestCase):
    def test_status_lists_audio_devices_and_sinks_only(self):
        found = pipewire.parse_status(fixture("wpctl_status.txt"))
        self.assertEqual([item.id for item in found["Devices"]], ["48", "50", "51"])
        sinks = {item.id: item.name for item in found["Sinks"]}
        self.assertEqual(sinks["45"], f"{G2000_SINK}.iec958-stereo")
        self.assertEqual(set(sinks), {"43", "45", "92"}, "Video sinks and stream ports are not audio sinks")

    def test_inspect_reads_every_property_with_or_without_the_star(self):
        props = pipewire.parse_inspect(fixture("wpctl_inspect_node.txt"))
        self.assertEqual(props["device.id"], "50")  # line starts with "  * "
        self.assertEqual(props["alsa.card"], "5")  # line starts with spaces only
        self.assertEqual(props["device.profile.description"], "Estéreo digital (IEC958)")

    def test_profile_name(self):
        self.assertEqual(pipewire.parse_profile(fixture("pw_cli_profile.txt")), "output:iec958-stereo")

    def test_props_floats_with_a_decimal_comma_or_point(self):
        comma = pipewire.parse_props(fixture("pw_cli_props.txt"))
        self.assertEqual(comma["softVolumes"], [1.0, 1.0])
        self.assertEqual(comma["channelVolumes"], [0.20024, 0.20024])
        self.assertIs(comma["softMute"], False)
        point = pipewire.parse_props(fixture("pw_cli_props.txt").replace(",", "."))
        self.assertEqual(point, comma)

    def test_amixer_values(self):
        self.assertEqual(pipewire.parse_amixer(fixture("amixer_volume.txt")), ["117", "117"])

    def test_volume_with_and_without_mute(self):
        self.assertEqual(pipewire.parse_volume("Volume: 0.40"), (0.40, False))
        self.assertEqual(pipewire.parse_volume("Volume: 0.01 [MUTED]"), (0.01, True))
        with self.assertRaises(pipewire.AudioError):
            pipewire.parse_volume("Translate ID error")


class Finding(unittest.TestCase):
    def test_finds_the_speaker_by_usb_ids_not_by_name_or_card_number(self):
        audio = pipewire.Audio(FakeSystem())
        speaker = audio.find_speaker()
        self.assertEqual((speaker.device_id, speaker.sink_id, speaker.card), ("50", "45", "5"))
        self.assertEqual(speaker.profile, "output:analog-stereo")

    def test_speaker_missing(self):
        self.assertIsNone(pipewire.Audio(FakeSystem(connected=False)).find_speaker())

    def test_reads_the_hardware_controls_by_name(self):
        system = FakeSystem(hardware=86)
        audio = pipewire.Audio(system)
        speaker = audio.find_speaker()
        self.assertEqual(audio.hardware(speaker), ([86, 86], "on"))
        self.assertIn(["amixer", "-c", "5", "cget", "name=PCM Playback Volume"], system.calls)


class Commands(unittest.TestCase):
    def test_every_command_runs_with_the_c_locale_and_a_timeout(self):
        seen = {}

        def fake_run(args, **options):
            seen.update(options)

            class Done:
                returncode, stdout, stderr = 0, "Volume: 0.50\n", ""

            return Done()

        out = pipewire.run_command(["wpctl", "get-volume", "45"], runner=fake_run)
        self.assertEqual(out, "Volume: 0.50\n")
        self.assertEqual(seen["env"]["LC_ALL"], "C")
        self.assertGreater(seen["timeout"], 0)
        self.assertFalse(seen.get("shell", False))

    def test_missing_program_explains_which_package_has_it(self):
        def missing(args, **options):
            raise FileNotFoundError(args[0])

        with self.assertRaises(pipewire.AudioError) as caught:
            pipewire.run_command(["pw-cli", "info"], runner=missing)
        self.assertIn("pw-cli", str(caught.exception))
        self.assertIn("pipewire", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
