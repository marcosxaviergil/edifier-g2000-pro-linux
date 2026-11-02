# Arquitetura

## Requisito

Com a Edifier Hecate G2000 PRO como saída: o volume geral do sistema (ganho por software) fica em 100%,
e toda mudança de volume feita pelo usuário altera o volume físico da caixa pelo ALSA. Deve funcionar em
qualquer Linux, não só em sistemas configurados como o de teste.

**Interpretação adotada** (apresentada ao autor antes da implementação, que então pediu o projeto): "volume do sistema em 100%" é
o ganho por software do PipeWire (`softVolumes`) fixo em 1,0; o controle de volume do sistema continua
mostrando e mudando o nível, que vai para o hardware. Manter o controle visualmente travado em 100%
impediria a tecla de aumentar volume de gerar qualquer evento.

## Solução

```
Barra de volume / teclas do teclado / botões + e − da caixa (teclas HID "Consumer Control") / mudo
        │  (todos usam o PipeWire)
        ▼
WirePlumber 0.5 ── regra 60-edifier-hecate-g2000-pro.conf
        │            device.vendor.id = 0x35bb, device.product.id = 0xb065
        │            → device.profile-set = edifier-hecate-g2000-pro.conf
        ▼
PipeWire ACP (alsa-card-profile) ── conjunto de perfis só com analog-stereo
        │            paths-output = analog-output → [Element PCM] volume = merge, switch = mute
        │            dB com máximo negativo → desativado → volume só nos degraus do hardware
        ▼
ALSA: PCM Playback Volume (0–147), PCM Playback Switch
        ▼
HECATE G2000 PRO (USB Audio, Jieli Technology)
```

Não há processo próprio rodando: o PipeWire já sabe aplicar o volume no hardware quando o caminho de
mixer do perfil ativo tem um elemento de volume. O problema era só o perfil: o IEC958 (escolhido e salvo
no sistema de teste) usa `iec958-stereo-output.conf`, que só tem `[Element IEC958] switch = mute`.

## Decisões

| Decisão | Motivo (evidência em [SOURCES.md](SOURCES.md) e [TESTING.md](TESTING.md)) |
| --- | --- |
| Conjunto de perfis próprio, só com `analog-stereo` | Funciona com perfil salvo ou não: `state-profile.lua` só usa o perfil salvo se ele existir na lista; com o IEC958 fora da lista, vale a prioridade (`find-best-profile.lua`). Uma regra de prioridade (`device.profile.priority.rules`) perderia para o perfil salvo |
| `paths-output = analog-output`, não `element-output = PCM` | `element-output` cria um caminho sem descrição e o WirePlumber 0.5.8 aborta (`compat.c:123`), visto no teste |
| Regra pelo ID USB, não pelo nome | `device.vendor.id`/`device.product.id` vêm do udev e não mudam entre máquinas; nomes e número da placa mudam |
| Sem `api.alsa.ignore-dB` | O PipeWire já desativa o dB porque o máximo informado (−0,94 dB) é negativo (`alsa-mixer.c` 1657–1663); o resultado é só hardware, comprovado (`softVolumes` 1,0) |
| Arquivos em `/usr/share` no .deb, `~/.config` por usuário | Locais lidos pelo WirePlumber (`$XDG_DATA_DIRS`, `$XDG_CONFIG_HOME`) e pelo ACP (`get_data_path()` em `compat.c`) |
| Comando em Python só com biblioteca padrão | Sem dependências; usa `wpctl`, `pw-cli` e `amixer` (os mesmos dos testes) com `LC_ALL=C` e tempo-limite |
| CI na imagem `node:22-bookworm-slim` | A mesma do projeto de referência nos mesmos runners: a action de checkout precisa de Node.js no container do Forgejo |

## Alternativas descartadas

| Alternativa | Por que não |
| --- | --- |
| Extensão GNOME | Só GNOME, quebra a cada versão do GNOME Shell e é redundante: o controle nativo já move o hardware |
| Serviço que intercepta o volume e devolve o controle para 100% | Com o controle em 100%, a tecla de aumentar não gera evento; o controle "pularia" de volta; disputa com o PipeWire |
| Aplicativo GTK4 | Desnecessário: a interface de volume do próprio desktop já funciona |
| Portar o software do Windows / engenharia reversa USB | O controle ALSA já funciona (relatório de testes) |
| Regra udev `ACP_PROFILE_SET` | Mecanismo do próprio PipeWire, mas não testado aqui; a propriedade `device.profile-set` do WirePlumber foi testada |

## Módulos do comando

| Módulo | Responsabilidade |
| --- | --- |
| `hecate_volume/pipewire.py` | Executa `wpctl`/`pw-cli`/`amixer` e interpreta as saídas; acha a caixa pelo ID USB. Recebe a função que executa comandos, o que permite os testes com saídas gravadas |
| `hecate_volume/files.py` | Onde ficam os dois arquivos (usuário e sistema), instalar e remover por usuário sem sobrescrever arquivo alheio |
| `hecate_volume/cli.py` | `status`, `diagnose`, `install`, `uninstall` e as mensagens |
