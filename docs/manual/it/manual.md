% Hecate G2000 PRO Volume — Manuale
% Indice

# Introduzione {#introduction}

Hecate G2000 PRO Volume fa sì che il controllo del volume del sistema cambi il volume fisico dell'altoparlante USB Edifier Hecate G2000 PRO, tramite il controllo ALSA dell'altoparlante stesso (**PCM Playback Volume**), invece di abbassare il suono via software.

- Con l'altoparlante come uscita, il volume software resta sempre al 100%: il controllo del volume, i tasti del volume e il muto del sistema agiscono solo sull'hardware dell'altoparlante.
- Funziona con qualsiasi desktop (GNOME, KDE Plasma e altri) e con tutte le applicazioni, perché usano tutte PipeWire.
- Riguarda solo la G2000 PRO (USB `35bb:b065`). Gli altri dispositivi audio restano come sono.
- Nessun programma gira in background: la soluzione è una configurazione di PipeWire e WirePlumber, più il comando `hecate-g2000-pro-volume` per verificarla e provarla.

# Requisiti {#requirements}

- Linux con PipeWire e WirePlumber 0.5 o successivo. Provato su Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). Per vedere la versione: `wireplumber --version`.
- Python 3.11 o successivo, per il comando `hecate-g2000-pro-volume`.
- I comandi `wpctl`, `pw-cli` e `amixer` (Debian e Ubuntu: pacchetti `wireplumber`, `pipewire-bin` e `alsa-utils`).

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

## Applicare la configurazione {#apply}

1. Riavvii WirePlumber, oppure esca dalla sessione e rientri:

```
systemctl --user restart wireplumber.service
```

2. Se l'altoparlante era sul profilo digitale (IEC958), la sua uscita cambia nome e l'uscita predefinita può passare a un altro dispositivo. Scelga **HECATE G2000 PRO** una volta come uscita nelle impostazioni audio. Se usa Easy Effects, scelga l'altoparlante anche come sua uscita.

![Impostazioni audio: HECATE G2000 PRO come uscita](configuracoes_som_saida.jpg)

# Uso {#usage}

Usi il controllo del volume, i tasti del volume e il muto come sempre. Ogni modifica va direttamente al volume fisico dell'altoparlante.

![Controllo del volume del sistema con HECATE G2000 PRO](controle_volume_gnome.jpg)

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

Abbassa il volume in tre passi sotto quello attuale, attiva il muto e verifica che il controllo hardware segua e che il volume software resti al 100%. Alla fine riporta il volume e il muto com'erano. Il suono non diventa mai più forte di prima della prova. Ogni verifica appare come **PASS** o **FAIL**.

![Terminale: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Come funziona {#how-it-works}

- **Insieme di profili proprio.** L'insieme di profili predefinito di PipeWire offre per l'altoparlante anche il profilo digitale IEC958, il cui percorso del mixer non ha un controllo del volume: con esso, ogni regolazione del volume è solo software. La configurazione di questo progetto offre solo il profilo analogico, il cui percorso usa il controllo **PCM** dell'altoparlante per volume e muto.
- **Profilo salvato.** Un profilo IEC958 salvato in precedenza viene ignorato, perché non esiste più; WirePlumber sceglie da solo quello analogico.
- **Solo hardware.** Il driver indica il volume dell'altoparlante da −28,37 dB a −0,94 dB. Poiché il massimo è negativo, PipeWire scarta questa informazione in decibel e applica il volume solo ai 148 passi dell'hardware (da 0 a 147), senza volume software sopra.
- **Solo questo altoparlante.** La regola di WirePlumber vale solo per il dispositivo USB `35bb:b065`.
- **File.** Pacchetto .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` e `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installazione per utente: gli stessi nomi in `~/.config/wireplumber/wireplumber.conf.d/` e `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Limitazioni {#limitations}

- **Tasti dell'altoparlante.** Il tasto e il controllo del volume dell'altoparlante sono una regolazione separata: ALSA non li vede e il volume del sistema non segue ciò che fanno.
- **Volume 0%.** Corrisponde al passo 0 dell'hardware. Non è stato verificato se quel passo sia silenzio totale; per il silenzio, usi il muto.
- **Uscita digitale.** Il profilo IEC958 non appare più per questo altoparlante.
- **WirePlumber 0.4.** Non supportato: usa un altro formato di configurazione (Lua).
- **Senza PipeWire.** I sistemi solo con PulseAudio non sono stati provati e non sono supportati.
- **Senza systemd.** Riavvii WirePlumber nel modo previsto dalla sua distribuzione, oppure esca dalla sessione e rientri.

# Problemi comuni {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber non è ancora stato riavviato: `systemctl --user restart wireplumber.service`.
- **Nessun suono dopo l'installazione.** L'uscita predefinita è passata a un altro dispositivo, perché il nome dell'uscita dell'altoparlante è cambiato. Scelga HECATE G2000 PRO come uscita (e in Easy Effects, se lo usa).
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
