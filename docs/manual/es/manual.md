% Hecate G2000 PRO Volume — Manual
% Índice

# Introducción {#introduction}

Hecate G2000 PRO Volume hace que el control de volumen del sistema cambie el volumen del propio altavoz USB Edifier Hecate G2000 PRO, mediante su control de hardware (**PCM Playback Volume**), en lugar de bajar el sonido en el ordenador.

Con el altavoz como salida:

- La barra de volumen del sistema muestra y cambia el **volumen del altavoz**.
- Las teclas de volumen del teclado y los botones **+** y **−** del altavoz cambian ese mismo volumen, y la barra lo sigue.
- El silencio del sistema activa y desactiva el **silencio del altavoz** (**PCM Playback Switch**).
- El volumen del ordenador (por software) queda siempre en **100 %** y no aparece en ningún control.
- El volumen de cada aplicación sigue funcionando como siempre.

Solo afecta a la G2000 PRO (USB `35bb:b065`); los demás dispositivos de audio siguen como están. Funciona con cualquier escritorio (GNOME, KDE Plasma y otros), porque todos usan PipeWire. No hay ningún programa en segundo plano: son dos archivos de configuración de PipeWire y WirePlumber, más el comando `hecate-g2000-pro-volume` para comprobar y probar.

# Requisitos {#requirements}

- Linux con PipeWire y WirePlumber 0.5 o posterior. Para ver la versión: `wireplumber --version`.
- Python 3.11 o posterior, para el comando `hecate-g2000-pro-volume`.
- Los comandos `wpctl`, `pw-cli` y `amixer` (Debian y Ubuntu: paquetes `wireplumber`, `pipewire-bin` y `alsa-utils`). El paquete .deb ya los instala.
- El altavoz conectado al ordenador con el cable USB.

# Instalación {#installation}

## Debian, Ubuntu y derivadas (.deb) {#install-deb}

1. Descargue `hecate-g2000-pro-volume_<versión>_all.deb` de la release.
2. Instálelo con apt, que también instala las dependencias:

```
sudo apt install ./hecate-g2000-pro-volume_<versión>_all.deb
```

El paquete instala la configuración para todos los usuarios del equipo.

## Otras distribuciones (.tar.gz) {#install-tarball}

1. Descargue `hecate-g2000-pro-volume-<versión>.tar.gz` de la release.
2. Extráigalo e instálelo para su usuario, sin root:

```
tar -xzf hecate-g2000-pro-volume-<versión>.tar.gz
cd hecate-g2000-pro-volume-<versión>
./hecate-g2000-pro-volume install
```

Si ya existe un archivo con el mismo nombre y otro contenido, se conserva y la instalación se detiene con un mensaje. Para reemplazarlo, use `./hecate-g2000-pro-volume install --force`.

## Activar {#apply}

1. Reinicie WirePlumber, o cierre la sesión y vuelva a entrar:

```
systemctl --user restart wireplumber.service
```

2. En la configuración de sonido, elija **HECATE G2000 PRO** como salida. La salida del altavoz pasa a ser la estéreo analógica; si antes era la estéreo digital (IEC958), la salida predeterminada puede haber pasado a otro dispositivo. Si usa Easy Effects, elija también el altavoz como su salida.
3. Compruébelo con `hecate-g2000-pro-volume status`: el resultado debe ser **Result: OK**.

![Configuración de sonido: HECATE G2000 PRO como salida](configuracoes_som_saida.jpg)

# Uso {#usage}

## Volumen y silencio del altavoz {#volume}

Use la barra de volumen del sistema, las teclas de volumen del teclado o los botones **+** y **−** del altavoz. Todos cambian el mismo volumen: el del altavoz. La barra muestra el volumen del altavoz y sigue a cualquiera de ellos. El silencio del sistema apaga el sonido en el altavoz.

![Barra de volumen del sistema con HECATE G2000 PRO](controle_volume_gnome.jpg)

## Volumen de cada aplicación {#app-volume}

En el control de volumen por aplicación (en la configuración de sonido, o en programas como pavucontrol), cada aplicación conserva su propio volumen, ajustado en el ordenador, como siempre. Se suma al volumen del altavoz.

## Comprobar la instalación: status {#status}

```
hecate-g2000-pro-volume status
```

Muestra dónde está instalada la configuración, si WirePlumber la cargó, el perfil activo, el volumen del sistema, los controles de hardware del altavoz y el volumen por software. No cambia nada. Termina con **Result: OK** cuando todo está bien; si no, cada **Problem:** indica qué hacer.

![Terminal: hecate-g2000-pro-volume status](terminal_status.jpg)

## Probar el altavoz: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Baja el volumen en tres pasos por debajo del actual, activa el silencio y comprueba que el control de hardware lo sigue y que el volumen por software queda en 100 %. Al final, devuelve el volumen y el silencio a como estaban. El sonido nunca sube por encima de lo que estaba antes de la prueba; con el volumen por debajo del 5 %, la prueba pide subirlo. Cada comprobación aparece como **PASS** o **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Cómo funciona {#how-it-works}

- **El control de volumen del altavoz.** Por USB, el altavoz ofrece un control de volumen (izquierdo y derecho) y uno de silencio. Linux los muestra como **PCM Playback Volume** y **PCM Playback Switch**.
- **Los botones del altavoz.** El altavoz también se presenta al ordenador como un teclado multimedia ("HECATE G2000 PRO Consumer Control"): los botones **+** y **−** envían las teclas de volumen. Por eso actúan exactamente como las teclas de volumen del teclado.
- **Perfil analógico.** El conjunto de perfiles predeterminado de PipeWire ofrece para el altavoz también el perfil digital IEC958, que no usa su control de volumen: con él, el volumen se bajaba en el ordenador. La configuración de este proyecto ofrece solo el perfil analógico, que usa el control **PCM** del altavoz para volumen y silencio. Un perfil IEC958 elegido antes se deja de lado y WirePlumber usa el analógico por sí mismo.
- **Volumen solo en el altavoz.** El control del altavoz tiene 148 pasos (0 a 147), de −28,37 dB a −0,94 dB. PipeWire aplica la barra de volumen directamente a esos pasos, sin volumen por software encima.
- **Solo este altavoz.** La regla de WirePlumber se aplica únicamente al dispositivo USB `35bb:b065`.
- **Archivos.** Paquete .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` y `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Instalación por usuario: los mismos nombres en `~/.config/wireplumber/wireplumber.conf.d/` y `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Problemas comunes {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber aún no se reinició: `systemctl --user restart wireplumber.service`.
- **Sin sonido después de activar.** La salida predeterminada pasó a otro dispositivo. Elija HECATE G2000 PRO como salida (y en Easy Effects, si lo usa).
- **"PipeWire does not see the speaker."** Revise el cable USB y que el altavoz esté encendido.
- **"wpctl is not installed"** (o `pw-cli`, `amixer`). Instale el paquete que indica el mensaje.
- **Un archivo aparece como "different" en status.** Ya existía un archivo con el mismo nombre y otro contenido. Revíselo y, si se puede reemplazar, ejecute `hecate-g2000-pro-volume install --force`.
- **diagnose muestra FAIL.** Ejecute `hecate-g2000-pro-volume status` y resuelva primero las líneas **Problem:** que muestre.

# Desinstalar {#uninstall}

- Paquete .deb: `sudo apt remove hecate-g2000-pro-volume`
- Instalación por usuario: `./hecate-g2000-pro-volume uninstall` (un archivo con otro contenido se conserva; `--force` lo elimina)

Después, reinicie WirePlumber: `systemctl --user restart wireplumber.service`. El altavoz vuelve al comportamiento predeterminado de PipeWire.

# Privacidad y seguridad {#privacy}

El proyecto no recoge, no guarda ni envía datos personales, y no usa la red. El comando solo lee el estado del audio con `wpctl`, `pw-cli` y `amixer` y, en `install` y `uninstall`, escribe o borra los dos archivos de configuración de su carpeta personal. `diagnose` cambia el volumen unos segundos y lo devuelve a como estaba. Detalles en `docs/PRIVACIDADE.md` del proyecto.
