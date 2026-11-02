"""hecate-g2000-pro-volume: install, check and test the G2000 PRO hardware volume configuration."""

import argparse
import os
import sys
import time

from . import __version__, files, pipewire

ACTIVE_PROFILE = "output:analog-stereo"
RESTART = "systemctl --user restart wireplumber.service"
WAIT_STEPS, WAIT_SECONDS = 12, 0.25  # up to 3 s for WirePlumber to apply a volume


def is_installed(items):
    """True when one scope has both files with this version's content."""
    for scope in ("user", "system"):
        states = [item.state for item in items if item.scope == scope]
        if states and all(state == "current" for state in states):
            return True
    return False


def is_unity(values):
    return bool(values) and all(abs(value - 1.0) < 0.001 for value in values)


def status(audio, environ, out):
    items = files.inspect(files.user_base(environ), "user") + files.inspect(files.SYSTEM_BASE, "system")
    print(f"hecate-g2000-pro-volume {__version__}", file=out)
    print("Configuration files:", file=out)
    for item in items:
        print(f"  {item.scope:<6} {item.state:<9} {item.path}", file=out)
    speaker = audio.find_speaker()
    problems = []
    if not is_installed(items):
        problems.append("The configuration is not installed. Run: hecate-g2000-pro-volume install")
    if speaker is None:
        problems.append("PipeWire does not see the speaker (USB 35bb:b065). Connect it and turn it on.")
    else:
        print(f"Speaker: sink {speaker.sink_id} ({speaker.sink_name}), ALSA card {speaker.card}", file=out)
        print(f"  Profile set: {speaker.profile_set or '(default)'}", file=out)
        print(f"  Active profile: {speaker.profile}", file=out)
        volume, muted = audio.volume(speaker)
        hardware, switch = audio.hardware(speaker)
        soft = audio.props(speaker).get("softVolumes", [])
        print(f"  System volume: {volume:.2f}{' (muted)' if muted else ''}", file=out)
        print(f"  Hardware: {pipewire.VOLUME_CONTROL} {hardware}, {pipewire.SWITCH_CONTROL} {switch}", file=out)
        print(f"  Software volume: {', '.join(f'{value:.2f}' for value in soft) or 'unknown'}", file=out)
        if is_installed(items) and speaker.profile_set != files.PROFILE_SET:
            problems.append(f"The configuration is installed but not loaded yet. Run: {RESTART}")
        elif speaker.profile_set == files.PROFILE_SET and speaker.profile != ACTIVE_PROFILE:
            problems.append(
                f"The speaker uses the profile {speaker.profile}. "
                "In Settings > Sound, choose HECATE G2000 PRO as the output."
            )
        elif speaker.profile == ACTIVE_PROFILE and not is_unity(soft):
            problems.append("Software volume is not 100%. Run: hecate-g2000-pro-volume diagnose")
    for problem in problems:
        print(f"Problem: {problem}", file=out)
    if not problems:
        print("Result: OK. The system volume drives the speaker's hardware volume.", file=out)
    return 1 if problems else 0


def volumes_below(current):
    """Three different volumes below the current one, or None when it is too low for that.

    Testing only below the current volume keeps the promise that the test never plays louder.
    """
    wanted = [round(current * share, 2) for share in (0.75, 0.5, 0.25)]
    if len(set(wanted)) < 3 or wanted[-1] < 0.01:
        return None
    return wanted


def wait_for(audio, speaker, volume, sleep):
    for _ in range(WAIT_STEPS):
        sleep(WAIT_SECONDS)
        if f"{audio.volume(speaker)[0]:.2f}" == f"{volume:.2f}":
            return


def diagnose(audio, out, sleep=time.sleep):
    speaker = audio.find_speaker()
    if speaker is None:
        print("Problem: PipeWire does not see the speaker (USB 35bb:b065). Connect it and turn it on.", file=out)
        return 1
    original, was_muted = audio.volume(speaker)
    steps = volumes_below(original)
    if steps is None:
        print(f"Problem: the volume ({original:.2f}) is too low to test below it. Raise it to 5% or more.", file=out)
        return 1
    print(f"Testing sink {speaker.sink_id}, profile {speaker.profile}, ALSA card {speaker.card}.", file=out)
    print("The volume goes down for a few seconds, then back to where it was.", file=out)
    rows, muted_switch = [], None
    try:
        for volume in steps:
            audio.set_volume(speaker, volume)
            wait_for(audio, speaker, volume, sleep)
            hardware, _ = audio.hardware(speaker)
            soft = audio.props(speaker).get("softVolumes", [])
            rows.append((volume, hardware, soft))
            print(f"  volume {volume:.2f} -> hardware {hardware}, software {soft}", file=out)
        audio.set_mute(speaker, True)
        sleep(1)
        muted_switch = audio.hardware(speaker)[1]
        print(f"  mute on -> {pipewire.SWITCH_CONTROL} {muted_switch}", file=out)
    finally:
        audio.set_volume(speaker, original)
        audio.set_mute(speaker, was_muted)
    print(f"Restored: volume {original:.2f}{', muted' if was_muted else ''}.", file=out)
    firsts = [hardware[0] for _, hardware, _ in rows]
    checks = [
        ("Hardware volume follows the system volume", all(a > b for a, b in zip(firsts, firsts[1:], strict=False))),
        ("Software volume stays at 100%", all(is_unity(soft) for _, _, soft in rows)),
        ("Mute switches the hardware off", muted_switch == "off"),
    ]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {name}", file=out)
    return 0 if all(passed for _, passed in checks) else 1


def install(environ, force, out):
    if is_installed(files.inspect(files.SYSTEM_BASE, "system")):
        print("Already installed for the whole system by the package. Nothing to do.", file=out)
        return 0
    written = files.install_user(files.user_base(environ), force=force)
    for path in written:
        print(f"Installed {path}", file=out)
    if not written:
        print("Already installed for this user. Nothing changed.", file=out)
        return 0
    print(f"To apply, run: {RESTART}", file=out)
    print("Then choose HECATE G2000 PRO once as the output: its name in the list changes.", file=out)
    return 0


def uninstall(environ, force, out):
    removed = files.uninstall_user(files.user_base(environ), force=force)
    for path in removed:
        print(f"Removed {path}", file=out)
    if removed:
        print(f"To apply, run: {RESTART}", file=out)
    else:
        print("Nothing installed for this user.", file=out)
    if any(item.state != "missing" for item in files.inspect(files.SYSTEM_BASE, "system")):
        print("The system package still provides the configuration: sudo apt remove hecate-g2000-pro-volume", file=out)
    return 0


def parser():
    main_parser = argparse.ArgumentParser(
        prog="hecate-g2000-pro-volume",
        description="Edifier Hecate G2000 PRO: the system volume drives the speaker's hardware volume.",
    )
    main_parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = main_parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="show the configuration and the speaker's state (changes nothing)")
    commands.add_parser("diagnose", help="lower the volume for a few seconds and check the hardware follows")
    for name, verb in (("install", "install"), ("uninstall", "remove")):
        command = commands.add_parser(name, help=f"{verb} the configuration for this user (no root needed)")
        command.add_argument("--force", action="store_true", help="also replace or remove a file with other content")
    return main_parser


def main(argv=None, audio=None, environ=None, out=sys.stdout):
    arguments = parser().parse_args(argv)
    environ = os.environ if environ is None else environ
    audio = pipewire.Audio() if audio is None else audio
    try:
        if arguments.command == "status":
            return status(audio, environ, out)
        if arguments.command == "diagnose":
            return diagnose(audio, out)
        action = install if arguments.command == "install" else uninstall
        return action(environ, arguments.force, out)
    except (files.InstallError, pipewire.AudioError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
