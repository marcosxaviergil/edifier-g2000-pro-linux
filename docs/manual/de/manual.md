% Hecate G2000 PRO Volume — Handbuch
% Inhalt

# Einführung {#introduction}

Hecate G2000 PRO Volume sorgt dafür, dass die Lautstärkeregelung des Systems die Lautstärke des USB-Lautsprechers Edifier Hecate G2000 PRO selbst ändert, über dessen Hardware-Regler (**PCM Playback Volume**), statt den Ton im Computer abzusenken.

Mit dem Lautsprecher als Ausgabe:

- Der Lautstärkebalken des Systems zeigt und ändert die **Lautstärke des Lautsprechers**.
- Die Lautstärketasten der Tastatur und die Tasten **+** und **−** am Lautsprecher ändern dieselbe Lautstärke, und der Balken folgt.
- Die Stummschaltung des Systems schaltet die **Stummschaltung des Lautsprechers** ein und aus (**PCM Playback Switch**).
- Die Lautstärke des Computers (Software) bleibt immer bei **100 %** und erscheint in keinem Regler.
- Die Lautstärke jeder Anwendung funktioniert wie immer.

Nur der G2000 PRO (USB `35bb:b065`) ist betroffen; andere Audiogeräte bleiben, wie sie sind. Es funktioniert mit jeder Arbeitsumgebung (GNOME, KDE Plasma und andere), weil alle PipeWire verwenden. Es läuft kein Programm im Hintergrund: Es sind zwei Konfigurationsdateien für PipeWire und WirePlumber, dazu der Befehl `hecate-g2000-pro-volume` zum Prüfen und Testen.

# Voraussetzungen {#requirements}

- Linux mit PipeWire und WirePlumber 0.5 oder neuer. Version anzeigen: `wireplumber --version`.
- Python 3.11 oder neuer, für den Befehl `hecate-g2000-pro-volume`.
- Die Befehle `wpctl`, `pw-cli` und `amixer` (Debian und Ubuntu: Pakete `wireplumber`, `pipewire-bin` und `alsa-utils`). Das .deb-Paket installiert sie bereits.
- Der Lautsprecher ist über das USB-Kabel mit dem Computer verbunden.

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

## Aktivieren {#apply}

1. Starten Sie WirePlumber neu, oder melden Sie sich ab und wieder an:

```
systemctl --user restart wireplumber.service
```

2. Wählen Sie in den Toneinstellungen **HECATE G2000 PRO** als Ausgabe. Die Ausgabe des Lautsprechers ist jetzt die analoge Stereo-Ausgabe; war sie vorher die digitale Stereo-Ausgabe (IEC958), kann die Standardausgabe zu einem anderen Gerät gewechselt sein. Wenn Sie Easy Effects verwenden, wählen Sie den Lautsprecher auch dort als Ausgabe.
3. Prüfen Sie mit `hecate-g2000-pro-volume status`: Das Ergebnis muss **Result: OK** sein.

![Toneinstellungen: HECATE G2000 PRO als Ausgabe](configuracoes_som_saida.jpg)

# Verwendung {#usage}

## Lautstärke und Stummschaltung des Lautsprechers {#volume}

Verwenden Sie den Lautstärkebalken des Systems, die Lautstärketasten der Tastatur oder die Tasten **+** und **−** am Lautsprecher. Alle ändern dieselbe Lautstärke: die des Lautsprechers. Der Balken zeigt die Lautstärke des Lautsprechers und folgt jeder dieser Änderungen. Die Stummschaltung des Systems schaltet den Ton am Lautsprecher ab.

![Lautstärkebalken des Systems mit HECATE G2000 PRO](controle_volume_gnome.jpg)

## Lautstärke jeder Anwendung {#app-volume}

In der Lautstärkeregelung pro Anwendung (in den Toneinstellungen oder in Programmen wie pavucontrol) behält jede Anwendung ihre eigene Lautstärke, die wie immer im Computer eingestellt wird. Sie wirkt zusätzlich zur Lautstärke des Lautsprechers.

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

Senkt die Lautstärke in drei Schritten unter die aktuelle, schaltet stumm und prüft, dass der Hardware-Regler folgt und die Software-Lautstärke bei 100 % bleibt. Am Ende stellt es Lautstärke und Stummschaltung wieder her. Der Ton wird nie lauter als vor dem Test; bei einer Lautstärke unter 5 % bittet der Test, sie zu erhöhen. Jede Prüfung zeigt **PASS** oder **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Funktionsweise {#how-it-works}

- **Der Lautstärkeregler des Lautsprechers.** Über USB bietet der Lautsprecher einen Lautstärkeregler (links und rechts) und eine Stummschaltung. Linux zeigt sie als **PCM Playback Volume** und **PCM Playback Switch**.
- **Die Tasten am Lautsprecher.** Der Lautsprecher meldet sich beim Computer auch als Medientastatur ("HECATE G2000 PRO Consumer Control"): Die Tasten **+** und **−** senden die Lautstärketasten. Deshalb wirken sie genau wie die Lautstärketasten der Tastatur.
- **Analoges Profil.** Der Standard-Profilsatz von PipeWire bietet für den Lautsprecher auch das digitale Profil IEC958 an, das seinen Lautstärkeregler nicht nutzt: Damit wurde die Lautstärke im Computer abgesenkt. Die Konfiguration dieses Projekts bietet nur das analoge Profil an, das den **PCM**-Regler des Lautsprechers für Lautstärke und Stummschaltung nutzt. Ein früher gewähltes IEC958-Profil wird beiseitegelassen, und WirePlumber verwendet von selbst das analoge.
- **Lautstärke nur im Lautsprecher.** Der Regler des Lautsprechers hat 148 Stufen (0 bis 147), von −28,37 dB bis −0,94 dB. PipeWire wendet den Lautstärkebalken direkt auf diese Stufen an, ohne Software-Lautstärke darüber.
- **Nur dieser Lautsprecher.** Die WirePlumber-Regel gilt nur für das USB-Gerät `35bb:b065`.
- **Dateien.** .deb-Paket: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` und `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installation pro Benutzer: dieselben Namen in `~/.config/wireplumber/wireplumber.conf.d/` und `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Häufige Probleme {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber wurde noch nicht neu gestartet: `systemctl --user restart wireplumber.service`.
- **Kein Ton nach dem Aktivieren.** Die Standardausgabe ist zu einem anderen Gerät gewechselt. Wählen Sie HECATE G2000 PRO als Ausgabe (und in Easy Effects, falls Sie es verwenden).
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
