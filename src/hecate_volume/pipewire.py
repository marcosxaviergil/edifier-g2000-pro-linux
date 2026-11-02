"""Read and change the G2000 PRO through wpctl, pw-cli and amixer.

Only the command-line tools of WirePlumber, PipeWire and alsa-utils are used, with the output
formats recorded on Debian 13 (WirePlumber 0.5.8, PipeWire 1.4.2; see tests/fixtures). The speaker is
found by its USB ids on the PipeWire device (``device.vendor.id``, ``device.product.id``), never by
node name or ALSA card number, which change between machines and reboots.
"""

import os
import re
import subprocess
from dataclasses import dataclass

VENDOR_ID, PRODUCT_ID = "0x35bb", "0xb065"
VOLUME_CONTROL, SWITCH_CONTROL = "PCM Playback Volume", "PCM Playback Switch"
PACKAGES = {"wpctl": "wireplumber", "pw-cli": "pipewire-bin", "amixer": "alsa-utils"}  # Debian and Ubuntu
TIMEOUT = 10  # seconds; wpctl waits forever for WirePlumber when the session manager is down


class AudioError(Exception):
    """A command failed or printed something unexpected; the message says what to check."""


@dataclass(frozen=True)
class Item:
    id: str
    name: str


@dataclass(frozen=True)
class Speaker:
    device_id: str
    sink_id: str
    sink_name: str
    card: str  # ALSA card number, for amixer -c
    profile: str  # active profile, e.g. "output:analog-stereo"
    profile_set: str  # device.profile-set, "" when the default profile set is used


def run_command(args, runner=subprocess.run):
    """stdout of one command. The C locale keeps numbers with a decimal point; the timeout keeps a hang short."""
    env = {**os.environ, "LC_ALL": "C"}
    try:
        done = runner(args, capture_output=True, text=True, timeout=TIMEOUT, env=env, check=False)
    except FileNotFoundError:
        package = PACKAGES.get(args[0], args[0])
        message = f"{args[0]} is not installed. Install the package that provides it ({package} on Debian)."
        raise AudioError(message) from None
    except subprocess.TimeoutExpired:
        raise AudioError(
            f"{' '.join(args)} did not answer in {TIMEOUT} s. "
            "Check that WirePlumber is running: systemctl --user status wireplumber.service"
        ) from None
    if done.returncode != 0:
        detail = (done.stderr or done.stdout).strip().splitlines()[-1:] or ["no output"]
        raise AudioError(f"{' '.join(args)} failed: {detail[0]}")
    return done.stdout


SECTION = re.compile(r"^[\s│├└─]*(Devices|Sinks|Sources|Filters|Streams):")
ITEM = re.compile(r"^[\s│]*\*?\s*(\d+)\.\s+(\S+)")


def parse_status(text):
    """{"Devices": [Item], "Sinks": [Item]} from ``wpctl status -n``, Audio part only."""
    found, block, section = {"Devices": [], "Sinks": []}, None, None
    for line in text.splitlines():
        if line and not line[0].isspace():
            block, section = line.strip(), None  # "Audio", "Video", "Settings", "PipeWire ..."
            continue
        header = SECTION.match(line)
        if header:
            section = header[1]
            continue
        item = ITEM.match(line)
        if block == "Audio" and section in found and item:
            found[section].append(Item(item[1], item[2]))
    return found


def parse_inspect(text):
    """Properties of ``wpctl inspect ID``: lines ``key = "value"``, some marked with ``*``."""
    return dict(re.findall(r'^[\s*]*([\w.:-]+) = "(.*)"$', text, re.M))


def _values_after(text, key):
    """The value lines that follow ``Prop: key ...:<key> (...)`` in pw-cli output."""
    lines = text.splitlines()
    for number, line in enumerate(lines):
        if re.search(rf":{re.escape(key)} \(\d+\)", line):
            values = []
            for following in lines[number + 1 :]:
                if "Prop: key" in following:
                    break
                values.append(following.strip())
            return values
    return []


def parse_profile(text):
    """Name of the active profile in ``pw-cli enum-params ID Profile``."""
    for value in _values_after(text, "Profile:name"):
        match = re.fullmatch(r'String "(.*)"', value)
        if match:
            return match[1]
    raise AudioError("pw-cli did not show the active profile name.")


def parse_props(text):
    """mute, softMute (bool) and channelVolumes, softVolumes (floats) from ``pw-cli enum-params ID Props``."""
    props = {}
    for key in ("mute", "softMute"):
        values = _values_after(text, f"Props:{key}")
        if values:
            props[key] = values[0] == "Bool true"
    for key in ("channelVolumes", "softVolumes"):
        floats = [value.split()[1] for value in _values_after(text, f"Props:{key}") if value.startswith("Float ")]
        props[key] = [float(number.replace(",", ".")) for number in floats]
    return props


def parse_amixer(text):
    """The values of ``amixer cget``: ``: values=117,117`` -> ["117", "117"]."""
    match = re.search(r"^\s*: values=(.*)$", text, re.M)
    if not match:
        raise AudioError("amixer did not show the control values.")
    return match[1].split(",")


def parse_volume(text):
    """(volume, muted) from ``wpctl get-volume ID``: ``Volume: 0.40`` or ``Volume: 0.40 [MUTED]``."""
    match = re.match(r"Volume: (\d+(?:\.\d+)?)( \[MUTED\])?", text.strip())
    if not match:
        raise AudioError(f"wpctl get-volume printed something unexpected: {text.strip()[:80]}")
    return float(match[1]), bool(match[2])


class Audio:
    """The commands the CLI needs, run through ``run`` (a list of arguments -> stdout)."""

    def __init__(self, run=run_command):
        self.run = run

    def find_speaker(self):
        """The G2000 PRO and its sink, or None when PipeWire has no such device or sink."""
        status = parse_status(self.run(["wpctl", "status", "-n"]))
        device = None
        for item in status["Devices"]:
            props = parse_inspect(self.run(["wpctl", "inspect", item.id]))
            if (props.get("device.vendor.id"), props.get("device.product.id")) == (VENDOR_ID, PRODUCT_ID):
                device = (item.id, props)
                break
        if device is None:
            return None
        device_id, device_props = device
        for item in status["Sinks"]:
            props = parse_inspect(self.run(["wpctl", "inspect", item.id]))
            if props.get("device.id") == device_id:
                return Speaker(
                    device_id=device_id,
                    sink_id=item.id,
                    sink_name=item.name,
                    card=props.get("alsa.card", device_props.get("alsa.card", "")),
                    profile=parse_profile(self.run(["pw-cli", "enum-params", device_id, "Profile"])),
                    profile_set=device_props.get("device.profile-set", ""),
                )
        return None

    def volume(self, speaker):
        return parse_volume(self.run(["wpctl", "get-volume", speaker.sink_id]))

    def set_volume(self, speaker, volume):
        self.run(["wpctl", "set-volume", speaker.sink_id, f"{volume:.2f}"])

    def set_mute(self, speaker, muted):
        self.run(["wpctl", "set-mute", speaker.sink_id, "1" if muted else "0"])

    def props(self, speaker):
        return parse_props(self.run(["pw-cli", "enum-params", speaker.sink_id, "Props"]))

    def hardware(self, speaker):
        """([volume per channel], switch "on"/"off") of the speaker's PCM controls, read by control name."""
        volume = parse_amixer(self.run(["amixer", "-c", speaker.card, "cget", f"name={VOLUME_CONTROL}"]))
        switch = parse_amixer(self.run(["amixer", "-c", speaker.card, "cget", f"name={SWITCH_CONTROL}"]))
        return [int(value) for value in volume], switch[0]
