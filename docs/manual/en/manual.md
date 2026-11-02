% Hecate G2000 PRO Volume — Manual
% Contents

# Introduction {#introduction}

Hecate G2000 PRO Volume makes the system volume control change the volume of the Edifier Hecate G2000 PRO USB speaker itself, through the speaker's hardware control (**PCM Playback Volume**), instead of lowering the sound in the computer.

With the speaker as the output:

- The system volume bar shows and changes the **speaker's volume**.
- The keyboard volume keys and the speaker's **+** and **−** buttons change that same volume, and the bar follows.
- The system mute turns the **speaker's mute** on and off (**PCM Playback Switch**).
- The computer's (software) volume always stays at **100%** and does not appear in any control.
- Each application's volume keeps working as always.

Only the G2000 PRO (USB `35bb:b065`) is affected; other audio devices stay as they are. It works with any desktop (GNOME, KDE Plasma and others), because they all use PipeWire. Nothing runs in the background: it is two PipeWire and WirePlumber configuration files, plus the `hecate-g2000-pro-volume` command to check and test.

# Requirements {#requirements}

- Linux with PipeWire and WirePlumber 0.5 or newer. To see the version: `wireplumber --version`.
- Python 3.11 or newer, for the `hecate-g2000-pro-volume` command.
- The `wpctl`, `pw-cli` and `amixer` commands (Debian and Ubuntu: packages `wireplumber`, `pipewire-bin` and `alsa-utils`). The .deb package already installs them.
- The speaker connected to the computer by the USB cable.

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

## Activate {#apply}

1. Restart WirePlumber, or log out and log in again:

```
systemctl --user restart wireplumber.service
```

2. In the sound settings, choose **HECATE G2000 PRO** as the output. The speaker's output is now the analog stereo one ("Analog Stereo"); if it was "Digital Stereo (IEC958)" before, the default output may have moved to another device. If you use Easy Effects, choose the speaker as its output too.
3. Check with `hecate-g2000-pro-volume status`: the result must be **Result: OK**.

![Sound settings: HECATE G2000 PRO as the output](configuracoes_som_saida.jpg)

# Usage {#usage}

## Speaker volume and mute {#volume}

Use the system volume bar, the keyboard volume keys or the speaker's **+** and **−** buttons. All of them change the same volume: the speaker's. The bar shows the speaker's volume and follows any of them. The system mute silences the speaker.

![System volume bar with HECATE G2000 PRO](controle_volume_gnome.jpg)

## Each application's volume {#app-volume}

In the per-application volume control (in the sound settings, or in programs such as pavucontrol), each application keeps its own volume, adjusted in the computer, as always. It adds to the speaker's volume.

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

Lowers the volume in three steps below the current one, mutes, and checks that the hardware control follows and that the software volume stays at 100%. At the end, it sets the volume and mute back to what they were. The sound never gets louder than before the test; with the volume below 5%, the test asks you to raise it. Each check shows **PASS** or **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# How it works {#how-it-works}

- **The speaker's volume control.** Over USB, the speaker offers one volume control (left and right) and one mute. Linux shows them as **PCM Playback Volume** and **PCM Playback Switch**.
- **The speaker's buttons.** The speaker also presents itself to the computer as a media keyboard ("HECATE G2000 PRO Consumer Control"): the **+** and **−** buttons send the volume keys. That is why they act exactly like the keyboard volume keys.
- **Analog profile.** PipeWire's default profile set also offers the digital IEC958 profile for the speaker, which does not use its volume control: with it, the volume was lowered in the computer. This project's configuration offers only the analog profile, which uses the speaker's **PCM** control for volume and mute. An IEC958 profile chosen before is set aside, and WirePlumber uses the analog one by itself.
- **Volume only in the speaker.** The speaker's control has 148 steps (0 to 147), from −28.37 dB to −0.94 dB. PipeWire applies the volume bar straight to these steps, with no software volume on top.
- **Only this speaker.** The WirePlumber rule applies only to the USB device `35bb:b065`.
- **Files.** .deb package: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` and `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Per-user installation: the same names in `~/.config/wireplumber/wireplumber.conf.d/` and `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Troubleshooting {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber was not restarted yet: `systemctl --user restart wireplumber.service`.
- **No sound after activating.** The default output moved to another device. Choose HECATE G2000 PRO as the output (and in Easy Effects, if you use it).
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
