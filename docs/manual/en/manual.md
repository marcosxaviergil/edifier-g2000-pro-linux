% Hecate G2000 PRO Volume — Manual
% Contents

# Introduction {#introduction}

Hecate G2000 PRO Volume makes the system volume control change the hardware volume of the Edifier Hecate G2000 PRO USB speaker, through the speaker's own ALSA control (**PCM Playback Volume**), instead of lowering the sound in software.

- With the speaker as the output, the software volume always stays at 100%: the volume control, the volume keys and the system mute change only the speaker's hardware.
- It works with any desktop (GNOME, KDE Plasma and others) and with every application, because they all use PipeWire.
- Only the G2000 PRO (USB `35bb:b065`) is affected. Other audio devices stay as they are.
- Nothing runs in the background: the solution is PipeWire and WirePlumber configuration, plus the `hecate-g2000-pro-volume` command to check and test it.

# Requirements {#requirements}

- Linux with PipeWire and WirePlumber 0.5 or newer. Tested on Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). To see the version: `wireplumber --version`.
- Python 3.11 or newer, for the `hecate-g2000-pro-volume` command.
- The `wpctl`, `pw-cli` and `amixer` commands (Debian and Ubuntu: packages `wireplumber`, `pipewire-bin` and `alsa-utils`).

# Installation {#installation}

## Debian, Ubuntu and derivatives (.deb) {#install-deb}

1. Download `hecate-g2000-pro-volume_<version>_all.deb` from the release.
2. Install it with apt, which also installs the dependencies:

```
sudo apt install ./hecate-g2000-pro-volume_<version>_all.deb
```

The package installs the configuration for every user of the computer.

## Other distributions (.tar.gz) {#install-tarball}

1. Download `hecate-g2000-pro-volume-<version>.tar.gz` from the release.
2. Extract it and install for your user, without root:

```
tar -xzf hecate-g2000-pro-volume-<version>.tar.gz
cd hecate-g2000-pro-volume-<version>
./hecate-g2000-pro-volume install
```

If a file with the same name and other content already exists, it is kept and the installation stops with a message. To replace it, use `./hecate-g2000-pro-volume install --force`.

## Apply the configuration {#apply}

1. Restart WirePlumber, or log out and log in again:

```
systemctl --user restart wireplumber.service
```

2. If the speaker was on the digital profile (IEC958), its output gets a new name and the default output may move to another device. Choose **HECATE G2000 PRO** once as the output in the sound settings. If you use Easy Effects, choose the speaker as its output too.

![Sound settings: HECATE G2000 PRO as the output](configuracoes_som_saida.jpg)

# Usage {#usage}

Use the volume control, the volume keys and mute as always. Every change goes straight to the speaker's hardware volume.

![System volume control with HECATE G2000 PRO](controle_volume_gnome.jpg)

## Check the installation: status {#status}

```
hecate-g2000-pro-volume status
```

Shows where the configuration is installed, whether WirePlumber loaded it, the active profile, the system volume, the speaker's hardware controls and the software volume. Changes nothing. It ends with **Result: OK** when everything is right; otherwise each **Problem:** says what to do.

![Terminal: hecate-g2000-pro-volume status](terminal_status.jpg)

## Test the speaker: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Lowers the volume in three steps below the current one, mutes, and checks that the hardware control follows and that the software volume stays at 100%. At the end, it sets the volume and mute back to what they were. The sound never gets louder than before the test. Each check shows **PASS** or **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# How it works {#how-it-works}

- **Own profile set.** PipeWire's default profile set also offers the digital IEC958 profile for the speaker, whose mixer path has no volume control: with it, every volume change is software only. This project's configuration offers only the analog profile, whose path uses the speaker's **PCM** control for volume and mute.
- **Stored profile.** An IEC958 profile stored before is ignored, because it no longer exists; WirePlumber picks the analog one by itself.
- **Hardware only.** The driver reports the speaker's volume from −28.37 dB to −0.94 dB. As the maximum is negative, PipeWire disregards this decibel information and applies the volume only to the 148 hardware steps (0 to 147), with no software volume on top.
- **Only this speaker.** The WirePlumber rule applies only to the USB device `35bb:b065`.
- **Files.** .deb package: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` and `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Per-user installation: the same names in `~/.config/wireplumber/wireplumber.conf.d/` and `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Limitations {#limitations}

- **Speaker buttons.** The speaker's own volume button and control are a separate adjustment: ALSA does not see them, and the system volume does not follow what they do.
- **0% volume.** It is hardware step 0. Whether that step is complete silence was not verified; for silence, use mute.
- **Digital output.** The IEC958 profile no longer appears for this speaker.
- **WirePlumber 0.4.** Not supported: it uses another configuration format (Lua).
- **No PipeWire.** Systems with PulseAudio only were not tested and are not supported.
- **No systemd.** Restart WirePlumber the way your distribution does, or log out and log in again.

# Troubleshooting {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber was not restarted yet: `systemctl --user restart wireplumber.service`.
- **No sound after installing.** The default output moved to another device, because the name of the speaker's output changed. Choose HECATE G2000 PRO as the output (and in Easy Effects, if you use it).
- **"PipeWire does not see the speaker."** Check the USB cable and that the speaker is on.
- **"wpctl is not installed"** (or `pw-cli`, `amixer`). Install the package the message names.
- **A file shows as "different" in status.** A file with the same name and other content already existed. Check it and, if it can be replaced, run `hecate-g2000-pro-volume install --force`.
- **diagnose shows FAIL.** Run `hecate-g2000-pro-volume status` and solve the **Problem:** lines it shows first.

# Uninstall {#uninstall}

- .deb package: `sudo apt remove hecate-g2000-pro-volume`
- Per-user installation: `./hecate-g2000-pro-volume uninstall` (a file with other content is kept; `--force` removes it)

Then restart WirePlumber: `systemctl --user restart wireplumber.service`. The speaker goes back to PipeWire's default behavior.

# Privacy and security {#privacy}

The project does not collect, store or send personal data, and does not use the network. The command only reads the audio state with `wpctl`, `pw-cli` and `amixer` and, in `install` and `uninstall`, writes or deletes the two configuration files in your home folder. `diagnose` changes the volume for a few seconds and sets it back. Details in the project's `docs/PRIVACIDADE.md`.
