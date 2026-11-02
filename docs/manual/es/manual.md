% Hecate G2000 PRO Volume — Manual
% Índice

# Introducción {#introduction}

Hecate G2000 PRO Volume hace que el control de volumen del sistema cambie el volumen físico del altavoz USB Edifier Hecate G2000 PRO, mediante el control ALSA del propio altavoz (**PCM Playback Volume**), en lugar de bajar el sonido por software.

- Con el altavoz como salida, el volumen por software queda siempre en 100 %: el control de volumen, las teclas de volumen y el silencio del sistema cambian solo el hardware del altavoz.
- Funciona con cualquier escritorio (GNOME, KDE Plasma y otros) y con todas las aplicaciones, porque todas usan PipeWire.
- Solo afecta a la G2000 PRO (USB `35bb:b065`). Los demás dispositivos de audio siguen como están.
- No hay ningún programa en segundo plano: la solución es configuración de PipeWire y WirePlumber, más el comando `hecate-g2000-pro-volume` para comprobarla y probarla.

# Requisitos {#requirements}

- Linux con PipeWire y WirePlumber 0.5 o posterior. Probado en Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). Para ver la versión: `wireplumber --version`.
- Python 3.11 o posterior, para el comando `hecate-g2000-pro-volume`.
- Los comandos `wpctl`, `pw-cli` y `amixer` (Debian y Ubuntu: paquetes `wireplumber`, `pipewire-bin` y `alsa-utils`).

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

## Aplicar la configuración {#apply}

1. Reinicie WirePlumber, o cierre la sesión y vuelva a entrar:

```
systemctl --user restart wireplumber.service
```

2. Si el altavoz estaba en el perfil digital (IEC958), su salida cambia de nombre y la salida predeterminada puede pasar a otro dispositivo. Elija **HECATE G2000 PRO** una vez como salida en la configuración de sonido. Si usa Easy Effects, elija también el altavoz como su salida.

![Configuración de sonido: HECATE G2000 PRO como salida](configuracoes_som_saida.jpg)

# Uso {#usage}

Use el control de volumen, las teclas de volumen y el silencio como siempre. Cada cambio va directamente al volumen físico del altavoz.

![Control de volumen del sistema con HECATE G2000 PRO](controle_volume_gnome.jpg)

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

Baja el volumen en tres pasos por debajo del actual, activa el silencio y comprueba que el control de hardware lo sigue y que el volumen por software queda en 100 %. Al final, devuelve el volumen y el silencio a como estaban. El sonido nunca sube por encima de lo que estaba antes de la prueba. Cada comprobación aparece como **PASS** o **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Cómo funciona {#how-it-works}

- **Conjunto de perfiles propio.** El conjunto de perfiles predeterminado de PipeWire ofrece para el altavoz también el perfil digital IEC958, cuya ruta de mezclador no tiene control de volumen: con él, todo ajuste de volumen es por software. La configuración de este proyecto ofrece solo el perfil analógico, cuya ruta usa el control **PCM** del altavoz para volumen y silencio.
- **Perfil guardado.** Un perfil IEC958 guardado antes se ignora, porque deja de existir; WirePlumber elige el analógico por sí mismo.
- **Solo hardware.** El controlador informa el volumen del altavoz de −28,37 dB a −0,94 dB. Como el máximo es negativo, PipeWire descarta esa información en decibelios y aplica el volumen solo en los 148 pasos del hardware (0 a 147), sin volumen por software encima.
- **Solo este altavoz.** La regla de WirePlumber se aplica únicamente al dispositivo USB `35bb:b065`.
- **Archivos.** Paquete .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` y `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Instalación por usuario: los mismos nombres en `~/.config/wireplumber/wireplumber.conf.d/` y `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Limitaciones {#limitations}

- **Botones del altavoz.** El botón y el control de volumen del propio altavoz son un ajuste aparte: ALSA no los ve y el volumen del sistema no sigue lo que hacen.
- **Volumen 0 %.** Corresponde al paso 0 del hardware. No se verificó si ese paso es silencio total; para silencio, use el silencio.
- **Salida digital.** El perfil IEC958 deja de aparecer para este altavoz.
- **WirePlumber 0.4.** No es compatible: usa otro formato de configuración (Lua).
- **Sin PipeWire.** Los sistemas solo con PulseAudio no se probaron y no son compatibles.
- **Sin systemd.** Reinicie WirePlumber de la forma que use su distribución, o cierre la sesión y vuelva a entrar.

# Problemas comunes {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber aún no se reinició: `systemctl --user restart wireplumber.service`.
- **Sin sonido después de instalar.** La salida predeterminada pasó a otro dispositivo, porque el nombre de la salida del altavoz cambió. Elija HECATE G2000 PRO como salida (y en Easy Effects, si lo usa).
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
