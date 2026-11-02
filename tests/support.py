"""Test helpers: the repository on sys.path, the recorded command outputs and a fake audio system.

``FakeSystem`` answers the same commands the CLI runs (wpctl, pw-cli, amixer), with the output
formats recorded on the reference machine (tests/fixtures). It models what the tests on that machine
showed: with the analog profile, volume and mute reach the hardware control and the software volume
stays 1.0; with the IEC958 profile, the hardware control never changes and only software volume moves.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "src"))

G2000_DEVICE = "alsa_card.usb-Jieli_Technology_HECATE_G2000_PRO_4150353335393909-01"
G2000_SINK = "alsa_output.usb-Jieli_Technology_HECATE_G2000_PRO_4150353335393909-01"


def fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


class FakeSystem:
    """A PipeWire session with one G2000 PRO (device 50, sink 45, ALSA card 5)."""

    def __init__(self, profile="analog-stereo", profile_set="", volume=0.4, hardware=59, connected=True):
        self.profile, self.profile_set, self.connected = profile, profile_set, connected
        self.volume, self.muted = volume, False
        self.hardware, self.switch = hardware, "on"
        self.calls = []

    def __call__(self, args):
        self.calls.append(list(args))
        command, *rest = args
        handler = {"wpctl": self.wpctl, "pw-cli": self.pw_cli, "amixer": self.amixer}[command]
        return handler(rest)

    # wpctl

    def wpctl(self, args):
        verb = args[0]
        if verb == "status":
            return self.status()
        if verb == "inspect":
            return self.inspect(args[1])
        if verb == "get-volume":
            return f"Volume: {self.volume:.2f}" + (" [MUTED]" if self.muted else "")
        if verb == "set-volume":
            self.volume = float(args[2])
            if self.profile == "analog-stereo":
                self.hardware = round(self.volume * 147)
            return ""
        if verb == "set-mute":
            self.muted = args[2] == "1"
            if self.profile == "analog-stereo":
                self.switch = "off" if self.muted else "on"
            return ""
        raise AssertionError(f"unexpected wpctl call {args}")

    def status(self):
        text = fixture("wpctl_status.txt")
        if not self.connected:
            lines = [line for line in text.splitlines() if "Jieli" not in line]
            return "\n".join(lines) + "\n"
        return text.replace(".iec958-stereo [vol", f".{self.profile} [vol")

    def inspect(self, object_id):
        if object_id == "50":
            text = fixture("wpctl_inspect_device.txt")
            if self.profile_set:
                text = text.replace(
                    '    device.product.id = "0xb065"\n',
                    f'    device.product.id = "0xb065"\n    device.profile-set = "{self.profile_set}"\n',
                )
            return text
        if object_id == "45":
            return fixture("wpctl_inspect_node.txt").replace("iec958-stereo", self.profile)
        return f'id {object_id}, type PipeWire:Interface:Device\n    device.api = "alsa"\n'

    # pw-cli

    def pw_cli(self, args):
        assert args[0] == "enum-params", args
        object_id, param = args[1], args[2]
        if param == "Profile" and object_id == "50":
            return fixture("pw_cli_profile.txt").replace("output:iec958-stereo", f"output:{self.profile}")
        if param == "Props" and object_id == "45":
            soft = 1.0 if self.profile == "analog-stereo" else self.volume**3
            channel = self.volume**3 if self.profile == "analog-stereo" else 1.0
            text = fixture("pw_cli_props.txt").replace("0,200240", f"{channel:.6f}".replace(".", ","))
            return text.replace("1,000000", f"{soft:.6f}".replace(".", ","))
        raise AssertionError(f"unexpected pw-cli call {args}")

    # amixer

    def amixer(self, args):
        assert args[:2] == ["-c", "5"] and args[2] == "cget", args
        if args[3] == "name=PCM Playback Volume":
            return fixture("amixer_volume.txt").replace("117,117", f"{self.hardware},{self.hardware}")
        if args[3] == "name=PCM Playback Switch":
            return (
                "numid=2,iface=MIXER,name='PCM Playback Switch'\n"
                "  ; type=BOOLEAN,access=rw------,values=1\n"
                f"  : values={self.switch}\n"
            )
        raise AssertionError(f"unexpected amixer call {args}")
