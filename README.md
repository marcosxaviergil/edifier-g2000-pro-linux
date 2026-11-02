# Hecate G2000 PRO Volume

O controle de volume do sistema muda o **volume físico** da caixa USB Edifier Hecate G2000 PRO, pelo
controle ALSA da própria caixa (`PCM Playback Volume`), em vez de baixar o som por software. Com a caixa
como saída, o volume por software fica sempre em 100%.

- Funciona em qualquer distribuição Linux com PipeWire e WirePlumber 0.5+, em qualquer ambiente gráfico
  (GNOME, KDE Plasma…), com as teclas de volume e com todos os aplicativos.
- Só a G2000 PRO (USB `35bb:b065`) é afetada.
- Nenhum programa em segundo plano: são dois arquivos de configuração, mais o comando
  `hecate-g2000-pro-volume` para conferir (`status`) e testar (`diagnose`).

Manual completo (PDF, 9 idiomas) em cada release: `Hecate-G2000-PRO-Volume-<versão>-Manual.pdf`.

## Instalação

**Debian, Ubuntu e derivados:**

```sh
sudo apt install ./hecate-g2000-pro-volume_<versão>_all.deb
```

**Qualquer outra distribuição** (por usuário, sem root):

```sh
tar -xzf hecate-g2000-pro-volume-<versão>.tar.gz
cd hecate-g2000-pro-volume-<versão>
./hecate-g2000-pro-volume install
```

**Depois, nos dois casos:**

```sh
systemctl --user restart wireplumber.service
```

Se a caixa estava no perfil digital (IEC958), escolha a HECATE G2000 PRO uma vez como saída nas
configurações de som (e no Easy Effects, se usar): o nome da saída muda.

## Uso

Use o controle e as teclas de volume como sempre. Para conferir e testar:

```sh
hecate-g2000-pro-volume status     # mostra o estado; não muda nada; termina em "Result: OK"
hecate-g2000-pro-volume diagnose   # baixa o volume por alguns segundos e confere o hardware (PASS/FAIL)
```

## Como funciona

O conjunto de perfis padrão do PipeWire também oferece para a caixa o perfil IEC958, cujo caminho de
mixer não tem controle de volume (volume só por software). Este projeto instala:

| Arquivo | O que faz |
| --- | --- |
| [`edifier-hecate-g2000-pro.conf`](src/hecate_volume/config/alsa-card-profile/edifier-hecate-g2000-pro.conf) | Conjunto de perfis só com a saída analógica, cujo caminho (`analog-output`) usa o controle **PCM** da caixa para volume e mudo |
| [`60-edifier-hecate-g2000-pro.conf`](src/hecate_volume/config/wireplumber/60-edifier-hecate-g2000-pro.conf) | Regra do WirePlumber: esse conjunto de perfis só para o USB `35bb:b065` |

O driver informa o volume de −28,37 dB a −0,94 dB; com máximo negativo o PipeWire desconsidera os
decibéis e aplica o volume só nos 148 degraus do hardware. Detalhes, evidências e decisões em
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) e [docs/TESTING.md](docs/TESTING.md).

## Limitações

- Os botões da própria caixa são um ajuste separado, invisível ao ALSA.
- O volume 0% é o degrau 0 do hardware (não verificado se é silêncio; use o mudo).
- WirePlumber 0.4 (configuração em Lua) e sistemas só com PulseAudio não são suportados.

## Desenvolvimento

Requisitos: Python 3.11+, `dpkg-deb`, `lintian`, `python3-pyflakes`, `weasyprint`, `fontconfig`,
`fonts-dejavu-core` e `fonts-noto-cjk` (Debian: `sudo apt install ...`). `make tools` lista o que falta.

```sh
make check    # tools + lint + testes + build (.deb, .tar.gz, lintian) + manual
make test     # só os testes (unittest)
make build    # dist/*.deb e dist/*.tar.gz, com lintian
make manual   # dist/Hecate-G2000-PRO-Volume-<versão>-Manual.pdf
PYTHONPATH=src python3 -m hecate_volume status   # o comando direto do código-fonte
```

```
src/hecate_volume/        comando (cli.py, pipewire.py, files.py) e os dois arquivos de configuração
tests/                    unittest: comando, configuração, build, CI, releases, manual (fixtures = saídas reais)
scripts/                  build.py, build_manual.py, forgejo_release.py, github_release.py, forge.py
docs/manual/<idioma>/     manual em pt-BR, en, es, it, de, ja, zh-CN, ko, fr (imagens: docs/manual/imagens)
.forgejo/ e .github/      workflows: só tag v* dispara teste, build e release
```

| Documento | Conteúdo |
| --- | --- |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | arquitetura, decisões e alternativas descartadas |
| [docs/TESTING.md](docs/TESTING.md) | testes automáticos e os testes reais com a caixa |
| [docs/SOURCES.md](docs/SOURCES.md) | documentação e código-fonte que embasam cada linha de configuração |
| [docs/SKILLS.md](docs/SKILLS.md) | skills do projeto aplicadas e onde |
| [docs/AUDIT.md](docs/AUDIT.md) | auditoria final do repositório |
| [docs/FORGEJO.md](docs/FORGEJO.md), [docs/GITHUB.md](docs/GITHUB.md) | envio, CI e releases |
| [docs/PRIVACIDADE.md](docs/PRIVACIDADE.md), [docs/TERMOS.md](docs/TERMOS.md) | privacidade e termos de uso |

## Nova versão

Suba `__version__` em `src/hecate_volume/__init__.py` e `version` em `pyproject.toml`, acrescente a seção
no `CHANGELOG.md`, faça o commit e envie a tag `v<versão>`: cada forja testa, gera e publica a release.

## Licença

MIT. Veja [LICENSE](LICENSE).
