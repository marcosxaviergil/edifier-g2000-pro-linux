# Fontes

Cada linha de configuração e cada comando foi conferido na documentação oficial ou no código-fonte das
versões usadas no teste: **PipeWire 1.4.2** (tag `1.4.2`) e **WirePlumber 0.5.8** (tag `0.5.8`), lidos
nos espelhos oficiais `github.com/PipeWire/pipewire` e `github.com/PipeWire/wireplumber`.

## Conjunto de perfis (`edifier-hecate-g2000-pro.conf`)

| Linha | Fonte |
| --- | --- |
| formato `[General]`, `auto-profiles`, `[Mapping]`, `device-strings`, `channel-map`, `paths-output`, `direction`, `priority` | cabeçalho de `spa/plugins/alsa/mixer/profile-sets/default.conf` |
| `device-strings = front:%f`, `channel-map = left,right`, `paths-output`, `priority = 15` | `[Mapping analog-stereo]` do mesmo `default.conf`; `api.alsa.path = "front:5"` no teste real |
| `paths-output = analog-output` (e não os outros caminhos analógicos) | `paths/analog-output.conf.common`: `[Element PCM] switch = mute, volume = merge`; o comentário do mesmo arquivo explica o `merge` (hardware primeiro, depois o resto) |
| não usar `element-output` | `acp/alsa-mixer.c` `pa_alsa_path_synthesize()` não define descrição; `path_verify()` (que define) só roda em caminho lido de arquivo; `acp/compat.c:123` `pa_assert(data->description)`; queda real no teste |
| IEC958 sem volume | `paths/iec958-stereo-output.conf`: só `[Element IEC958] switch = mute` |
| volume só no hardware | `acp/alsa-mixer.c` 1657–1663 (dB com máximo negativo é desativado); `acp/acp.c` ramo sem dB (`dev->real_volume = r`, sem `soft_volume`); log real do teste |
| mudo no hardware | `acp/acp.c`: mudo por software só se `soft_mixer` ou se o caminho não tiver mudo; o PCM tem `switch = mute` |
| onde o arquivo é procurado | `acp/compat.c` `get_data_path()`: `ACP_PROFILES_DIR`, `$XDG_CONFIG_HOME/alsa-card-profile/mixer/profile-sets`, `/etc/alsa-card-profile/...`, `PA_ALSA_DATA_DIR` (`meson.build`: `datadir/alsa-card-profile/mixer` = `/usr/share/...`) |

## Regra do WirePlumber (`60-edifier-hecate-g2000-pro.conf`)

| Linha | Fonte |
| --- | --- |
| `monitor.alsa.rules`, `matches`, `actions`, `update-props` | WirePlumber `docs/rst/daemon/configuration/alsa.rst` |
| `device.profile-set` | mesmo arquivo: "select a custom ACP profile-set name for the device. This can be configured in UDev rules, but it can also be specified here"; lido em `acp/acp.c` (`device.profile-set`) |
| várias chaves no mesmo objeto = todas precisam bater | PipeWire `doc/dox/config/pipewire-jack.conf.5.md`: "all keys must match the value" |
| `device.vendor.id = "0x35bb"`, `device.product.id = "0xb065"` | `spa/plugins/alsa/alsa-udev.c` (`"0x%04x"` a partir de `ID_VENDOR_ID`/`ID_MODEL_ID`); valores reais do `wpctl inspect` e do `udevadm info` |
| sintaxe SPA-JSON | `conf_file.rst` (separadores opcionais; `#` é comentário) |
| pasta `wireplumber.conf.d` (usuário e sistema) | `modifying_configuration.rst`; `daemon/locations.rst` (`$XDG_CONFIG_HOME`, `$XDG_CONFIG_DIRS`, `$XDG_DATA_DIRS`) |
| perfil salvo ignorado quando some | `src/scripts/device/state-profile.lua` linhas 43–53; ordem `find-stored-profile` → `find-preferred-profile` → `find-best-profile` |
| reiniciar | unidade `wireplumber.service` (`daemon/running.rst`) |

## Comandos usados pelo `hecate-g2000-pro-volume`

| Comando | Fonte |
| --- | --- |
| `wpctl status -n`, `inspect`, `get-volume`, `set-volume`, `set-mute` | `wpctl(1)` (WirePlumber); `set-volume` grava na rota do dispositivo (`modules/module-mixer-api.c`) |
| `pw-cli enum-params ID Profile` / `Props` | `pw-cli(1)` (PipeWire) |
| `amixer -c N cget name=...` | `amixer(1)` (alsa-utils); leitura e escrita comprovadas no relatório de testes |
| pacotes `wireplumber`, `pipewire-bin`, `alsa-utils`, `pulseaudio-utils` (pactl) | packages.debian.org (trixie) |

## Empacotamento e CI

| Item | Fonte |
| --- | --- |
| `dpkg-deb --root-owner-group`, `SOURCE_DATE_EPOCH` | `dpkg-deb(1)`; reproducible-builds.org |
| `debian/copyright` (DEP-5, MIT = Expat) | Debian copyright-format 1.0 |
| lintian | sem erros nem avisos (lintian 2.117, `--pedantic -I` sem achados) |
| workflows, actions fixadas por SHA, release por tag | projeto de referência `opendeck-uno-overlays` (mesmo autor), adaptado |
