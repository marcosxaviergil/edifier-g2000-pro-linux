% Hecate G2000 PRO Volume — Handbuch
% Inhalt

# Einführung {#introduction}

Hecate G2000 PRO Volume sorgt dafür, dass die Lautstärkeregelung des Systems die Hardware-Lautstärke des USB-Lautsprechers Edifier Hecate G2000 PRO ändert, über den ALSA-Regler des Lautsprechers selbst (**PCM Playback Volume**), statt den Ton per Software abzusenken.

- Mit dem Lautsprecher als Ausgabe bleibt die Software-Lautstärke immer bei 100 %: Lautstärkeregler, Lautstärketasten und Stummschaltung des Systems ändern nur die Hardware des Lautsprechers.
- Es funktioniert mit jeder Arbeitsumgebung (GNOME, KDE Plasma und andere) und mit allen Anwendungen, weil alle PipeWire verwenden.
- Nur der G2000 PRO (USB `35bb:b065`) ist betroffen. Andere Audiogeräte bleiben, wie sie sind.
- Es läuft kein Programm im Hintergrund: Die Lösung ist eine Konfiguration für PipeWire und WirePlumber, dazu der Befehl `hecate-g2000-pro-volume` zum Prüfen und Testen.

# Voraussetzungen {#requirements}

- Linux mit PipeWire und WirePlumber 0.5 oder neuer. Getestet unter Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). Version anzeigen: `wireplumber --version`.
- Python 3.11 oder neuer, für den Befehl `hecate-g2000-pro-volume`.
- Die Befehle `wpctl`, `pw-cli` und `amixer` (Debian und Ubuntu: Pakete `wireplumber`, `pipewire-bin` und `alsa-utils`).

# Installation {#installation}

## Debian, Ubuntu und Derivate (.deb) {#install-deb}

1. Laden Sie `hecate-g2000-pro-volume_<Version>_all.deb` aus dem Release herunter.
2. Installieren Sie es mit apt, das auch die Abhängigkeiten installiert:

```
sudo apt install ./hecate-g2000-pro-volume_<Version>_all.deb
```

Das Paket installiert die Konfiguration für alle Benutzer des Computers.

## Andere Distributionen (.tar.gz) {#install-tarball}

1. Laden Sie `hecate-g2000-pro-volume-<Version>.tar.gz` aus dem Release herunter.
2. Entpacken Sie es und installieren Sie es für Ihren Benutzer, ohne root:

```
tar -xzf hecate-g2000-pro-volume-<Version>.tar.gz
cd hecate-g2000-pro-volume-<Version>
./hecate-g2000-pro-volume install
```

Gibt es schon eine Datei mit demselben Namen und anderem Inhalt, bleibt sie erhalten und die Installation bricht mit einer Meldung ab. Zum Ersetzen verwenden Sie `./hecate-g2000-pro-volume install --force`.

## Konfiguration anwenden {#apply}

1. Starten Sie WirePlumber neu, oder melden Sie sich ab und wieder an:

```
systemctl --user restart wireplumber.service
```

2. War der Lautsprecher im digitalen Profil (IEC958), bekommt seine Ausgabe einen neuen Namen, und die Standardausgabe kann zu einem anderen Gerät wechseln. Wählen Sie **HECATE G2000 PRO** einmal als Ausgabe in den Toneinstellungen. Wenn Sie Easy Effects verwenden, wählen Sie den Lautsprecher auch dort als Ausgabe.

![Toneinstellungen: HECATE G2000 PRO als Ausgabe](configuracoes_som_saida.jpg)

# Verwendung {#usage}

Verwenden Sie Lautstärkeregler, Lautstärketasten und Stummschaltung wie immer. Jede Änderung geht direkt an die Hardware-Lautstärke des Lautsprechers.

![Lautstärkeregler des Systems mit HECATE G2000 PRO](controle_volume_gnome.jpg)

## Installation prüfen: status {#status}

```
hecate-g2000-pro-volume status
```

Zeigt, wo die Konfiguration installiert ist, ob WirePlumber sie geladen hat, das aktive Profil, die Systemlautstärke, die Hardware-Regler des Lautsprechers und die Software-Lautstärke. Ändert nichts. Endet mit **Result: OK**, wenn alles stimmt; sonst sagt jede **Problem:**-Zeile, was zu tun ist.

![Terminal: hecate-g2000-pro-volume status](terminal_status.jpg)

## Lautsprecher testen: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Senkt die Lautstärke in drei Schritten unter die aktuelle, schaltet stumm und prüft, dass der Hardware-Regler folgt und die Software-Lautstärke bei 100 % bleibt. Am Ende stellt es Lautstärke und Stummschaltung wieder her. Der Ton wird nie lauter als vor dem Test. Jede Prüfung zeigt **PASS** oder **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Funktionsweise {#how-it-works}

- **Eigener Profilsatz.** Der Standard-Profilsatz von PipeWire bietet für den Lautsprecher auch das digitale Profil IEC958 an, dessen Mixer-Pfad keinen Lautstärkeregler hat: Damit ist jede Lautstärkeänderung reine Software. Die Konfiguration dieses Projekts bietet nur das analoge Profil an, dessen Pfad den **PCM**-Regler des Lautsprechers für Lautstärke und Stummschaltung nutzt.
- **Gespeichertes Profil.** Ein früher gespeichertes IEC958-Profil wird ignoriert, weil es nicht mehr existiert; WirePlumber wählt das analoge von selbst.
- **Nur Hardware.** Der Treiber meldet die Lautstärke des Lautsprechers von −28,37 dB bis −0,94 dB. Da das Maximum negativ ist, verwirft PipeWire diese Dezibel-Angabe und wendet die Lautstärke nur auf die 148 Hardware-Stufen (0 bis 147) an, ohne Software-Lautstärke darüber.
- **Nur dieser Lautsprecher.** Die WirePlumber-Regel gilt nur für das USB-Gerät `35bb:b065`.
- **Dateien.** .deb-Paket: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` und `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installation pro Benutzer: dieselben Namen in `~/.config/wireplumber/wireplumber.conf.d/` und `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Einschränkungen {#limitations}

- **Tasten am Lautsprecher.** Taste und Lautstärkeregler am Lautsprecher selbst sind eine eigene Einstellung: ALSA sieht sie nicht, und die Systemlautstärke folgt ihnen nicht.
- **Lautstärke 0 %.** Entspricht Hardware-Stufe 0. Ob diese Stufe völlige Stille ist, wurde nicht geprüft; für Stille verwenden Sie die Stummschaltung.
- **Digitale Ausgabe.** Das Profil IEC958 erscheint für diesen Lautsprecher nicht mehr.
- **WirePlumber 0.4.** Nicht unterstützt: Es verwendet ein anderes Konfigurationsformat (Lua).
- **Ohne PipeWire.** Systeme nur mit PulseAudio wurden nicht getestet und werden nicht unterstützt.
- **Ohne systemd.** Starten Sie WirePlumber so neu, wie Ihre Distribution es vorsieht, oder melden Sie sich ab und wieder an.

# Häufige Probleme {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber wurde noch nicht neu gestartet: `systemctl --user restart wireplumber.service`.
- **Kein Ton nach der Installation.** Die Standardausgabe ist zu einem anderen Gerät gewechselt, weil sich der Name der Lautsprecherausgabe geändert hat. Wählen Sie HECATE G2000 PRO als Ausgabe (und in Easy Effects, falls Sie es verwenden).
- **"PipeWire does not see the speaker."** Prüfen Sie das USB-Kabel und ob der Lautsprecher eingeschaltet ist.
- **"wpctl is not installed"** (oder `pw-cli`, `amixer`). Installieren Sie das in der Meldung genannte Paket.
- **Eine Datei erscheint in status als "different".** Es gab schon eine Datei mit demselben Namen und anderem Inhalt. Prüfen Sie sie und führen Sie, wenn sie ersetzt werden darf, `hecate-g2000-pro-volume install --force` aus.
- **diagnose zeigt FAIL.** Führen Sie `hecate-g2000-pro-volume status` aus und lösen Sie zuerst die angezeigten **Problem:**-Zeilen.

# Deinstallieren {#uninstall}

- .deb-Paket: `sudo apt remove hecate-g2000-pro-volume`
- Installation pro Benutzer: `./hecate-g2000-pro-volume uninstall` (eine Datei mit anderem Inhalt bleibt erhalten; `--force` entfernt sie)

Starten Sie danach WirePlumber neu: `systemctl --user restart wireplumber.service`. Der Lautsprecher kehrt zum Standardverhalten von PipeWire zurück.

# Datenschutz und Sicherheit {#privacy}

Das Projekt sammelt, speichert und sendet keine personenbezogenen Daten und nutzt kein Netzwerk. Der Befehl liest nur den Audiozustand mit `wpctl`, `pw-cli` und `amixer` und schreibt oder löscht bei `install` und `uninstall` die zwei Konfigurationsdateien in Ihrem persönlichen Ordner. `diagnose` ändert die Lautstärke für einige Sekunden und stellt sie dann wieder her. Details in `docs/PRIVACIDADE.md` des Projekts.
