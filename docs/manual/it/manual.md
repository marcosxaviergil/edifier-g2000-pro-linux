% Hecate G2000 PRO Volume — Manuale
% Indice

# Introduzione {#introduction}

Hecate G2000 PRO Volume fa sì che il controllo del volume del sistema cambi il volume dell'altoparlante USB Edifier Hecate G2000 PRO stesso, tramite il suo controllo hardware (**PCM Playback Volume**), invece di abbassare il suono nel computer.

Con l'altoparlante come uscita:

- La barra del volume del sistema mostra e cambia il **volume dell'altoparlante**.
- I tasti del volume della tastiera e i pulsanti **+** e **−** dell'altoparlante cambiano lo stesso volume, e la barra li segue.
- Il muto del sistema attiva e disattiva il **muto dell'altoparlante** (**PCM Playback Switch**).
- Il volume del computer (software) resta sempre al **100%** e non appare in nessun controllo.
- Il volume di ogni applicazione continua a funzionare come sempre.

Riguarda solo la G2000 PRO (USB `35bb:b065`); gli altri dispositivi audio restano come sono. Funziona con qualsiasi desktop (GNOME, KDE Plasma e altri), perché usano tutti PipeWire. Nessun programma gira in background: sono due file di configurazione di PipeWire e WirePlumber, più il comando `hecate-g2000-pro-volume` per verificare e provare.

# Requisiti {#requirements}

- Linux con PipeWire e WirePlumber 0.5 o successivo. Per vedere la versione: `wireplumber --version`.
- Python 3.11 o successivo, per il comando `hecate-g2000-pro-volume`.
- I comandi `wpctl`, `pw-cli` e `amixer` (Debian e Ubuntu: pacchetti `wireplumber`, `pipewire-bin` e `alsa-utils`). Il pacchetto .deb li installa già.
- L'altoparlante collegato al computer con il cavo USB.

# Installazione {#installation}

## Debian, Ubuntu e derivate (.deb) {#install-deb}

1. Scarichi `hecate-g2000-pro-volume_<versione>_all.deb` dalla release.
2. Lo installi con apt, che installa anche le dipendenze:

```
sudo apt install ./hecate-g2000-pro-volume_<versione>_all.deb
```

Il pacchetto installa la configurazione per tutti gli utenti del computer.

## Altre distribuzioni (.tar.gz) {#install-tarball}

1. Scarichi `hecate-g2000-pro-volume-<versione>.tar.gz` dalla release.
2. Lo estragga e lo installi per il suo utente, senza root:

```
tar -xzf hecate-g2000-pro-volume-<versione>.tar.gz
cd hecate-g2000-pro-volume-<versione>
./hecate-g2000-pro-volume install
```

Se esiste già un file con lo stesso nome e un contenuto diverso, viene mantenuto e l'installazione si ferma con un messaggio. Per sostituirlo, usi `./hecate-g2000-pro-volume install --force`.

## Attivare {#apply}

1. Riavvii WirePlumber, oppure esca dalla sessione e rientri:

```
systemctl --user restart wireplumber.service
```

2. Nelle impostazioni audio, scelga **HECATE G2000 PRO** come uscita. L'uscita dell'altoparlante diventa quella stereo analogica; se prima era quella stereo digitale (IEC958), l'uscita predefinita può essere passata a un altro dispositivo. Se usa Easy Effects, scelga l'altoparlante anche come sua uscita.
3. Verifichi con `hecate-g2000-pro-volume status`: il risultato deve essere **Result: OK**.

![Impostazioni audio: HECATE G2000 PRO come uscita](configuracoes_som_saida.jpg)

# Uso {#usage}

## Volume e muto dell'altoparlante {#volume}

Usi la barra del volume del sistema, i tasti del volume della tastiera o i pulsanti **+** e **−** dell'altoparlante. Tutti cambiano lo stesso volume: quello dell'altoparlante. La barra mostra il volume dell'altoparlante e segue ognuno di essi. Il muto del sistema spegne il suono nell'altoparlante.

![Barra del volume del sistema con HECATE G2000 PRO](controle_volume_gnome.jpg)

## Volume di ogni applicazione {#app-volume}

Nel controllo del volume per applicazione (nelle impostazioni audio, o in programmi come pavucontrol), ogni applicazione mantiene il proprio volume, regolato nel computer, come sempre. Si somma al volume dell'altoparlante.

## Verificare l'installazione: status {#status}

```
hecate-g2000-pro-volume status
```

Mostra dove è installata la configurazione, se WirePlumber l'ha caricata, il profilo attivo, il volume del sistema, i controlli hardware dell'altoparlante e il volume software. Non cambia nulla. Termina con **Result: OK** quando tutto è a posto; altrimenti ogni **Problem:** dice cosa fare.

![Terminale: hecate-g2000-pro-volume status](terminal_status.jpg)

## Provare l'altoparlante: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Abbassa il volume in tre passi sotto quello attuale, attiva il muto e verifica che il controllo hardware segua e che il volume software resti al 100%. Alla fine riporta il volume e il muto com'erano. Il suono non diventa mai più forte di prima della prova; con il volume sotto il 5%, la prova chiede di alzarlo. Ogni verifica appare come **PASS** o **FAIL**.

![Terminale: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Come funziona {#how-it-works}

- **Il controllo del volume dell'altoparlante.** Tramite USB, l'altoparlante offre un controllo del volume (sinistro e destro) e uno del muto. Linux li mostra come **PCM Playback Volume** e **PCM Playback Switch**.
- **I pulsanti dell'altoparlante.** L'altoparlante si presenta al computer anche come tastiera multimediale ("HECATE G2000 PRO Consumer Control"): i pulsanti **+** e **−** inviano i tasti del volume. Per questo agiscono esattamente come i tasti del volume della tastiera.
- **Profilo analogico.** L'insieme di profili predefinito di PipeWire offre per l'altoparlante anche il profilo digitale IEC958, che non usa il suo controllo del volume: con esso il volume veniva abbassato nel computer. La configurazione di questo progetto offre solo il profilo analogico, che usa il controllo **PCM** dell'altoparlante per volume e muto. Un profilo IEC958 scelto in precedenza viene messo da parte e WirePlumber usa da solo quello analogico.
- **Volume solo nell'altoparlante.** Il controllo dell'altoparlante ha 148 passi (da 0 a 147), da −28,37 dB a −0,94 dB. PipeWire applica la barra del volume direttamente a questi passi, senza volume software sopra.
- **Solo questo altoparlante.** La regola di WirePlumber vale solo per il dispositivo USB `35bb:b065`.
- **File.** Pacchetto .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` e `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installazione per utente: gli stessi nomi in `~/.config/wireplumber/wireplumber.conf.d/` e `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Problemi comuni {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber non è ancora stato riavviato: `systemctl --user restart wireplumber.service`.
- **Nessun suono dopo l'attivazione.** L'uscita predefinita è passata a un altro dispositivo. Scelga HECATE G2000 PRO come uscita (e in Easy Effects, se lo usa).
- **"PipeWire does not see the speaker."** Controlli il cavo USB e che l'altoparlante sia acceso.
- **"wpctl is not installed"** (oppure `pw-cli`, `amixer`). Installi il pacchetto indicato nel messaggio.
- **Un file appare come "different" in status.** Esisteva già un file con lo stesso nome e un contenuto diverso. Lo controlli e, se può essere sostituito, esegua `hecate-g2000-pro-volume install --force`.
- **diagnose mostra FAIL.** Esegua `hecate-g2000-pro-volume status` e risolva prima le righe **Problem:** che mostra.

# Disinstallare {#uninstall}

- Pacchetto .deb: `sudo apt remove hecate-g2000-pro-volume`
- Installazione per utente: `./hecate-g2000-pro-volume uninstall` (un file con un contenuto diverso viene mantenuto; `--force` lo rimuove)

Poi riavvii WirePlumber: `systemctl --user restart wireplumber.service`. L'altoparlante torna al comportamento predefinito di PipeWire.

# Privacy e sicurezza {#privacy}

Il progetto non raccoglie, non salva e non invia dati personali, e non usa la rete. Il comando legge solo lo stato dell'audio con `wpctl`, `pw-cli` e `amixer` e, con `install` e `uninstall`, scrive o cancella i due file di configurazione nella sua cartella personale. `diagnose` cambia il volume per qualche secondo e poi lo riporta com'era. Dettagli in `docs/PRIVACIDADE.md` del progetto.
