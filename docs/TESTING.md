# Testes

```sh
make check   # tools + lint + testes + build (lintian) + manual
make test    # só unittest
```

Requisitos: Python 3.11+; para os testes de build, `dpkg-deb`; para os do PDF, `weasyprint` e
`fonts-noto-cjk` (sem eles esses testes são pulados com aviso).

## Testes automáticos

| Arquivo | Cobre |
| --- | --- |
| `tests/test_pipewire.py` | interpretação das saídas **reais** gravadas (`tests/fixtures`): `wpctl status -n` (só Audio; Video e portas de fluxo ignorados), `wpctl inspect` (com e sem `*`), perfil ativo, `Props` com vírgula ou ponto decimal, `amixer cget`, `get-volume` com `[MUTED]`; achar a caixa pelo ID USB; ler os controles por nome; todo comando com `LC_ALL=C`, tempo-limite e sem shell; programa ausente explica o pacote |
| `tests/test_files.py` | `XDG_CONFIG_HOME` (vazio ou relativo é ignorado, como manda a especificação); destinos; instalar/remover; arquivo com outro conteúdo mantido sem `--force` e nada instalado pela metade; nenhum temporário sobra; conteúdo exato do conjunto de perfis validado na caixa (e sem `element-output`); regra do WirePlumber só com os IDs USB e o nome do conjunto |
| `tests/test_cli.py` | `status` OK, não instalado, instalado mas WirePlumber não reiniciado, caixa desconectada, e não muda nada; `diagnose` PASS no perfil analógico, FAIL no IEC958, nunca mais alto que antes, restaura volume e mudo mesmo com erro no meio; `install` com o pacote do sistema presente não faz nada; conflito → código 2; `--version` |
| `tests/test_build.py` | conteúdo do .deb (caminhos, dono root, sem `__pycache__`), campos de controle, comando instalado roda a partir da árvore do pacote, tarball instala por usuário, dois builds idênticos (reprodutível), copyright DEP-5 |
| `tests/test_release.py` | releases contra emuladores locais das APIs do Forgejo e do GitHub: substitui a release da mesma tag, anexa os 3 arquivos, SHA-256 nas notas, não publica se a tag mudou (`BUILD_COMMIT`), rascunho → anexos → publicação no GitHub, recusa tag errada/token ausente/HTTP sem TLS antes de qualquer pedido, User-Agent padrão do Python recusado, token fora da saída |
| `tests/test_ci.py` | todo comando dos workflows e do `make tools` existe na imagem ou na lista do apt; GitHub com os mesmos passos do Forgejo (só checkout e release mudam); só tag `v*`; actions fixadas por SHA; `permissions: {}` e escrita só em `contents`; `make build` roda lintian |
| `tests/test_manual.py` | README da raiz com uma seção por idioma (os 9, na ordem, com o índice de links, as mesmas 4 partes, os mesmos comandos e links que existem); manual: 9 idiomas na ordem pedida, mesma estrutura de títulos, mesmas imagens e mesmos comandos que o pt-BR; toda imagem listada em `docs/manual/imagens/README.md`; comandos citados existem; placeholder visível; lista numerada continua depois de bloco de código; nome de imagem inseguro recusado; carregador recusa arquivo fora de `docs/manual`; capa com os 9 idiomas; PDF com um marcador por idioma e todo link interno com destino |

O `FakeSystem` (`tests/support.py`) reproduz o que os testes reais mostraram: no perfil analógico o
volume e o mudo chegam ao hardware e o volume por software fica 1,0; no IEC958 o hardware não muda.
Ele não é o PipeWire: os testes provam que o comando interpreta e reage a essas saídas, não como o
PipeWire de outra versão se comporta.

## Testes reais com a caixa (02/11/2026)

Máquina: Debian 13, GNOME, PipeWire 1.4.2, WirePlumber 0.5.8, Easy Effects ativo. Relatório completo no
projeto ("Relatório técnico de testes — PipeWire e WirePlumber").

| Teste | Resultado |
| --- | --- |
| Perfil IEC958 (salvo pelo WirePlumber), volume 1.00 → 0.10 | som baixou, `PCM Playback Volume` ficou 147,147: **só software** |
| Diagnóstico | perfis: off, analog-stereo (6500), iec958-stereo (5500), iec958-ac3-surround-51, pro-audio; perfil salvo `output:iec958-stereo`; USB 35bb:b065; controles PCM Volume e PCM Switch |
| Troca manual para analog-stereo (`wpctl set-profile`) | rota analógica não foi ativada a tempo; volume não aplicado; saída padrão foi para outro dispositivo: inconclusivo |
| Conjunto de perfis com `element-output = PCM` | WirePlumber abortou (`'data->description' failed at compat.c:123`); restaurado à mão |
| **Conjunto de perfis com `paths-output = analog-output` + regra do WirePlumber** | perfis off, analog-stereo, pro-audio; IEC958 salvo ignorado; rota `analog-output`; 1.00→147, 0.70→103, 0.50→74, 0.30→44, 0.20→29, 0.10→15, 0.05→7, 0.01→1; `softVolumes` 1,0 em todas; mudo → `PCM Playback Switch` off; teclas e controle do GNOME mudaram o hardware (0.24→36, 0.58→86, 0.90→133, 1.00→147); restauração completa |

Log do WirePlumber no teste: `The decibel volume range for element 'PCM' (-2837 dB - -94 dB) has
negative maximum. Disabling the decibel range.`

## O que não foi testado

| Item | Situação |
| --- | --- |
| Arquivos nas pastas do sistema (`/usr/share`), via .deb | mesmo mecanismo, outra pasta da busca; conferir com `hecate-g2000-pro-volume status` depois de instalar |
| Outras distribuições, outras versões do PipeWire/WirePlumber 0.5.x | não testado |
| Se o degrau 0 do hardware é silêncio | não verificado |
| PulseAudio sem PipeWire | não suportado |

## Depois de instalar o .deb (conferência na máquina real)

```sh
sudo apt install ./hecate-g2000-pro-volume_1.0.0_all.deb
systemctl --user restart wireplumber.service
hecate-g2000-pro-volume status      # esperado: "Result: OK"
hecate-g2000-pro-volume diagnose    # esperado: 3 x PASS
```
