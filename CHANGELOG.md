# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Versões: [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-11-02

Primeira versão.

### Adicionado

- Conjunto de perfis (ACP) para a Edifier Hecate G2000 PRO (USB `35bb:b065`) só com a saída analógica:
  o caminho `analog-output` usa o controle **PCM** da caixa, então o volume e o mudo do sistema mudam
  `PCM Playback Volume` e `PCM Playback Switch`, sem volume por software.
- Regra do WirePlumber 0.5 que aplica esse conjunto de perfis só a esse dispositivo USB.
- Com a caixa como saída, a barra de volume do sistema mostra e muda o volume da caixa; as teclas de
  volume e os botões **+**/**−** da caixa (que ela envia ao computador como teclas de mídia) mudam o
  mesmo volume; o ganho por software da saída fica em 100%; o volume de cada aplicativo continua por software.
- Comando `hecate-g2000-pro-volume` (Python 3.11+, só biblioteca padrão): `status`, `diagnose`,
  `install` e `uninstall` (por usuário, sem root).
- Pacote `.deb` (configuração para todo o sistema) e `.tar.gz` (instalação por usuário em qualquer distribuição).
- README da raiz e manual em PDF em 9 idiomas: português (Brasil), inglês, espanhol, italiano, alemão, japonês, chinês
  simplificado, coreano e francês.
- Workflows do Forgejo Actions e do GitHub Actions: testes, build, lintian, manual e release por tag `v*`.

### Validado

- Debian 13, PipeWire 1.4.2, WirePlumber 0.5.8, com a caixa real (ver `docs/TESTING.md`):
  volume do sistema 1.00 → 0.01 levou o `PCM Playback Volume` de 147 a 1; volume por software 1,0 em
  todas as medições; mudo do sistema desligou `PCM Playback Switch`; teclas e controle do GNOME
  mudaram o controle de hardware; os botões da caixa chegam ao sistema como teclas de volume
  ("HECATE G2000 PRO Consumer Control") e mudaram o volume do sistema.
