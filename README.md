# Hecate G2000 PRO Volume — código-fonte

[Português (Brasil)](#português-brasil) · [English](#english) · [Español](#español) ·
[Italiano](#italiano) · [Deutsch](#deutsch) · [日本語](#日本語) · [简体中文](#简体中文) ·
[한국어](#한국어) · [Français](#français)

## Português (Brasil)

Configuração do PipeWire e do WirePlumber que faz o controle de volume do sistema mudar o volume
físico da caixa USB Edifier Hecate G2000 PRO (controle ALSA `PCM Playback Volume`), com o volume por
software sempre em 100%. Só a G2000 PRO (USB `35bb:b065`) é afetada. Este repositório tem a
configuração, o comando `hecate-g2000-pro-volume`, os testes e o build. Para **usar**, leia o manual
em PDF anexado a cada release (9 idiomas).

### Estrutura

```text
src/hecate_volume/config/    os dois arquivos de configuração (conjunto de perfis ACP e regra do WirePlumber)
src/hecate_volume/           comando hecate-g2000-pro-volume: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: saídas reais de wpctl, pw-cli e amixer
scripts/                     build.py (.deb e .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   o mesmo CI no Forgejo e no GitHub, só em tag de versão (v*)
docs/                        arquitetura, testes, fontes, skills, auditoria, Forgejo, GitHub, privacidade
docs/manual/<idioma>/manual.md, docs/manual/imagens/   fonte do manual em PDF e capturas de tela
```

### Comandos

```sh
make tools   # lista o que falta instalar (o mesmo que a imagem do CI tem)
make check   # tools, lint (pyflakes, ruff se houver), testes, build com lintian, manual
make build   # dist/hecate-g2000-pro-volume_<versão>_all.deb e dist/hecate-g2000-pro-volume-<versão>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<versão>-Manual.pdf, os 9 idiomas num arquivo
```

Requisitos de desenvolvimento: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` e,
para o manual, `weasyprint`, `fontconfig`, `fonts-dejavu-core` e `fonts-noto-cjk` (apt). Opcional:
`ruff`. Detalhes em [docs/TESTING.md](docs/TESTING.md).

### Documentação

- [Arquitetura](docs/ARCHITECTURE.md): solução, decisões e alternativas descartadas.
- [Testes](docs/TESTING.md): testes automáticos e os testes reais com a caixa.
- [Fontes](docs/SOURCES.md): documentação oficial e código que embasam cada linha de configuração.
- [Skills](docs/SKILLS.md): skills do projeto aplicadas em cada área. [Auditoria](docs/AUDIT.md).
- [Privacidade](docs/PRIVACIDADE.md) e [Termos](docs/TERMOS.md).
- [Manual](docs/manual/): fonte do PDF por idioma; imagens em [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) e [GitHub](docs/GITHUB.md): CI, envio e releases por tag. [Histórico](CHANGELOG.md).

### Licença

MIT ([LICENSE](LICENSE)).

## English

PipeWire and WirePlumber configuration that makes the system volume control change the hardware
volume of the Edifier Hecate G2000 PRO USB speaker (ALSA control `PCM Playback Volume`), with the
software volume always at 100%. Only the G2000 PRO (USB `35bb:b065`) is affected. This repository
holds the configuration, the `hecate-g2000-pro-volume` command, the tests and the build. To **use**
it, read the PDF manual attached to every release (9 languages).

### Structure

```text
src/hecate_volume/config/    the two configuration files (ACP profile set and WirePlumber rule)
src/hecate_volume/           hecate-g2000-pro-volume command: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: real output of wpctl, pw-cli and amixer
scripts/                     build.py (.deb and .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   the same CI on Forgejo and GitHub, on version tags only (v*)
docs/                        architecture, tests, sources, skills, audit, Forgejo, GitHub, privacy
docs/manual/<language>/manual.md, docs/manual/imagens/   source of the PDF manual and screenshots
```

### Commands

```sh
make tools   # lists what is missing (the same the CI image has)
make check   # tools, lint (pyflakes, ruff if present), tests, build with lintian, manual
make build   # dist/hecate-g2000-pro-volume_<version>_all.deb and dist/hecate-g2000-pro-volume-<version>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<version>-Manual.pdf, all 9 languages in one file
```

Development requirements: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` and, for
the manual, `weasyprint`, `fontconfig`, `fonts-dejavu-core` and `fonts-noto-cjk` (apt). Optional:
`ruff`. Details in [docs/TESTING.md](docs/TESTING.md).

### Documentation

The documents below are in Portuguese; the manual is in 9 languages.

- [Architecture](docs/ARCHITECTURE.md): solution, decisions and rejected alternatives.
- [Tests](docs/TESTING.md): automated tests and the real tests with the speaker.
- [Sources](docs/SOURCES.md): official documentation and code behind every configuration line.
- [Skills](docs/SKILLS.md): the project's skills applied in each area. [Audit](docs/AUDIT.md).
- [Privacy](docs/PRIVACIDADE.md) and [Terms](docs/TERMOS.md).
- [Manual](docs/manual/): PDF source per language; images in [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) and [GitHub](docs/GITHUB.md): CI, pushing and releases by tag. [Changelog](CHANGELOG.md).

### License

MIT ([LICENSE](LICENSE)).

## Español

Configuración de PipeWire y WirePlumber que hace que el control de volumen del sistema cambie el
volumen físico del altavoz USB Edifier Hecate G2000 PRO (control ALSA `PCM Playback Volume`), con el
volumen por software siempre en 100 %. Solo afecta a la G2000 PRO (USB `35bb:b065`). Este
repositorio contiene la configuración, el comando `hecate-g2000-pro-volume`, las pruebas y el build.
Para **usarlo**, lea el manual en PDF adjunto a cada release (9 idiomas).

### Estructura

```text
src/hecate_volume/config/    los dos archivos de configuración (conjunto de perfiles ACP y regla de WirePlumber)
src/hecate_volume/           comando hecate-g2000-pro-volume: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: salidas reales de wpctl, pw-cli y amixer
scripts/                     build.py (.deb y .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   el mismo CI en Forgejo y GitHub, solo con etiqueta de versión (v*)
docs/                        arquitectura, pruebas, fuentes, skills, auditoría, Forgejo, GitHub, privacidad
docs/manual/<idioma>/manual.md, docs/manual/imagens/   fuente del manual en PDF y capturas de pantalla
```

### Comandos

```sh
make tools   # lista lo que falta instalar (lo mismo que tiene la imagen del CI)
make check   # tools, lint (pyflakes, ruff si está), pruebas, build con lintian, manual
make build   # dist/hecate-g2000-pro-volume_<versión>_all.deb y dist/hecate-g2000-pro-volume-<versión>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<versión>-Manual.pdf, los 9 idiomas en un archivo
```

Requisitos de desarrollo: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` y, para el
manual, `weasyprint`, `fontconfig`, `fonts-dejavu-core` y `fonts-noto-cjk` (apt). Opcional: `ruff`.
Detalles en [docs/TESTING.md](docs/TESTING.md).

### Documentación

Los documentos siguientes están en portugués; el manual está en 9 idiomas.

- [Arquitectura](docs/ARCHITECTURE.md): solución, decisiones y alternativas descartadas.
- [Pruebas](docs/TESTING.md): pruebas automáticas y las pruebas reales con el altavoz.
- [Fuentes](docs/SOURCES.md): documentación oficial y código que respaldan cada línea de configuración.
- [Skills](docs/SKILLS.md): skills del proyecto aplicadas en cada área. [Auditoría](docs/AUDIT.md).
- [Privacidad](docs/PRIVACIDADE.md) y [Términos](docs/TERMOS.md).
- [Manual](docs/manual/): fuente del PDF por idioma; imágenes en [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) y [GitHub](docs/GITHUB.md): CI, envío y releases por etiqueta. [Historial](CHANGELOG.md).

### Licencia

MIT ([LICENSE](LICENSE)).

## Italiano

Configurazione di PipeWire e WirePlumber che fa sì che il controllo del volume del sistema cambi il
volume fisico dell'altoparlante USB Edifier Hecate G2000 PRO (controllo ALSA `PCM Playback Volume`),
con il volume software sempre al 100%. Riguarda solo la G2000 PRO (USB `35bb:b065`). Questo
repository contiene la configurazione, il comando `hecate-g2000-pro-volume`, i test e il build. Per
**usarlo**, legga il manuale in PDF allegato a ogni release (9 lingue).

### Struttura

```text
src/hecate_volume/config/    i due file di configurazione (insieme di profili ACP e regola di WirePlumber)
src/hecate_volume/           comando hecate-g2000-pro-volume: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: output reali di wpctl, pw-cli e amixer
scripts/                     build.py (.deb e .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   lo stesso CI su Forgejo e GitHub, solo con tag di versione (v*)
docs/                        architettura, test, fonti, skill, audit, Forgejo, GitHub, privacy
docs/manual/<lingua>/manual.md, docs/manual/imagens/   sorgente del manuale in PDF e schermate
```

### Comandi

```sh
make tools   # elenca cosa manca da installare (lo stesso dell'immagine del CI)
make check   # tools, lint (pyflakes, ruff se presente), test, build con lintian, manuale
make build   # dist/hecate-g2000-pro-volume_<versione>_all.deb e dist/hecate-g2000-pro-volume-<versione>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<versione>-Manual.pdf, le 9 lingue in un file
```

Requisiti di sviluppo: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` e, per il
manuale, `weasyprint`, `fontconfig`, `fonts-dejavu-core` e `fonts-noto-cjk` (apt). Facoltativo:
`ruff`. Dettagli in [docs/TESTING.md](docs/TESTING.md).

### Documentazione

I documenti seguenti sono in portoghese; il manuale è in 9 lingue.

- [Architettura](docs/ARCHITECTURE.md): soluzione, decisioni e alternative scartate.
- [Test](docs/TESTING.md): test automatici e i test reali con l'altoparlante.
- [Fonti](docs/SOURCES.md): documentazione ufficiale e codice alla base di ogni riga di configurazione.
- [Skill](docs/SKILLS.md): skill del progetto applicate in ogni area. [Audit](docs/AUDIT.md).
- [Privacy](docs/PRIVACIDADE.md) e [Termini](docs/TERMOS.md).
- [Manuale](docs/manual/): sorgente del PDF per lingua; immagini in [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) e [GitHub](docs/GITHUB.md): CI, invio e release per tag. [Cronologia](CHANGELOG.md).

### Licenza

MIT ([LICENSE](LICENSE)).

## Deutsch

Konfiguration für PipeWire und WirePlumber, mit der die Lautstärkeregelung des Systems die
Hardware-Lautstärke des USB-Lautsprechers Edifier Hecate G2000 PRO ändert (ALSA-Regler
`PCM Playback Volume`), während die Software-Lautstärke immer bei 100 % bleibt. Nur der G2000 PRO
(USB `35bb:b065`) ist betroffen. Dieses Repository enthält die Konfiguration, den Befehl
`hecate-g2000-pro-volume`, die Tests und den Build. Zur **Verwendung** lesen Sie das PDF-Handbuch,
das jedem Release beiliegt (9 Sprachen).

### Struktur

```text
src/hecate_volume/config/    die zwei Konfigurationsdateien (ACP-Profilsatz und WirePlumber-Regel)
src/hecate_volume/           Befehl hecate-g2000-pro-volume: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: echte Ausgaben von wpctl, pw-cli und amixer
scripts/                     build.py (.deb und .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   dasselbe CI auf Forgejo und GitHub, nur bei Versions-Tags (v*)
docs/                        Architektur, Tests, Quellen, Skills, Audit, Forgejo, GitHub, Datenschutz
docs/manual/<Sprache>/manual.md, docs/manual/imagens/   Quelle des PDF-Handbuchs und Bildschirmfotos
```

### Befehle

```sh
make tools   # listet, was fehlt (dasselbe wie im CI-Image)
make check   # tools, Lint (pyflakes, ruff falls vorhanden), Tests, Build mit lintian, Handbuch
make build   # dist/hecate-g2000-pro-volume_<Version>_all.deb und dist/hecate-g2000-pro-volume-<Version>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<Version>-Manual.pdf, alle 9 Sprachen in einer Datei
```

Entwicklungsvoraussetzungen: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` und für
das Handbuch `weasyprint`, `fontconfig`, `fonts-dejavu-core` und `fonts-noto-cjk` (apt). Optional:
`ruff`. Details in [docs/TESTING.md](docs/TESTING.md).

### Dokumentation

Die folgenden Dokumente sind auf Portugiesisch; das Handbuch gibt es in 9 Sprachen.

- [Architektur](docs/ARCHITECTURE.md): Lösung, Entscheidungen und verworfene Alternativen.
- [Tests](docs/TESTING.md): automatische Tests und die echten Tests mit dem Lautsprecher.
- [Quellen](docs/SOURCES.md): offizielle Dokumentation und Code hinter jeder Konfigurationszeile.
- [Skills](docs/SKILLS.md): die Skills des Projekts je Bereich. [Audit](docs/AUDIT.md).
- [Datenschutz](docs/PRIVACIDADE.md) und [Nutzungsbedingungen](docs/TERMOS.md).
- [Handbuch](docs/manual/): PDF-Quelle je Sprache; Bilder in [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) und [GitHub](docs/GITHUB.md): CI, Hochladen und Releases per Tag. [Änderungen](CHANGELOG.md).

### Lizenz

MIT ([LICENSE](LICENSE)).

## 日本語

USB スピーカー Edifier Hecate G2000 PRO のハードウェア音量（ALSA コントロール `PCM Playback Volume`）を
システムの音量調整で変更できるようにする、PipeWire と WirePlumber の設定です。ソフトウェア音量は常に
100% のままです。対象は G2000 PRO（USB `35bb:b065`）だけです。このリポジトリには、設定、
`hecate-g2000-pro-volume` コマンド、テスト、ビルドが含まれます。**使い方**は、各リリースに添付された
PDF マニュアル（9 言語）を参照してください。

### 構成

```text
src/hecate_volume/config/    2 つの設定ファイル（ACP プロファイルセットと WirePlumber のルール）
src/hecate_volume/           hecate-g2000-pro-volume コマンド: status、diagnose、install、uninstall
tests/                       unittest。tests/fixtures: wpctl、pw-cli、amixer の実際の出力
scripts/                     build.py（.deb と .tar.gz）、build_manual.py（PDF）、forgejo_release.py、github_release.py
.forgejo/workflows/, .github/workflows/   Forgejo と GitHub で同じ CI。バージョンタグ（v*）のときだけ実行
docs/                        アーキテクチャ、テスト、出典、スキル、監査、Forgejo、GitHub、プライバシー
docs/manual/<言語>/manual.md, docs/manual/imagens/   PDF マニュアルの原稿とスクリーンショット
```

### コマンド

```sh
make tools   # 足りないものを一覧表示（CI イメージと同じ内容）
make check   # tools、lint（pyflakes、あれば ruff）、テスト、lintian 付きビルド、マニュアル
make build   # dist/hecate-g2000-pro-volume_<バージョン>_all.deb と dist/hecate-g2000-pro-volume-<バージョン>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<バージョン>-Manual.pdf（9 言語を 1 ファイルに）
```

開発に必要なもの: Python 3.11 以降、`make`、`dpkg-deb`、`lintian`、`python3-pyflakes`、マニュアル用に
`weasyprint`、`fontconfig`、`fonts-dejavu-core`、`fonts-noto-cjk`（apt）。任意: `ruff`。詳しくは
[docs/TESTING.md](docs/TESTING.md) にあります。

### ドキュメント

以下の文書はポルトガル語です。マニュアルは 9 言語です。

- [アーキテクチャ](docs/ARCHITECTURE.md): 解決策、判断、採用しなかった案。
- [テスト](docs/TESTING.md): 自動テストと、スピーカーでの実機テスト。
- [出典](docs/SOURCES.md): 設定の各行の根拠となる公式ドキュメントとソースコード。
- [スキル](docs/SKILLS.md): 分野ごとに適用したプロジェクトのスキル。[監査](docs/AUDIT.md)。
- [プライバシー](docs/PRIVACIDADE.md) と [利用規約](docs/TERMOS.md)。
- [マニュアル](docs/manual/): 言語ごとの PDF の原稿。画像は [docs/manual/imagens](docs/manual/imagens/README.md)。
- [Forgejo](docs/FORGEJO.md) と [GitHub](docs/GITHUB.md): CI、送信、タグによるリリース。[変更履歴](CHANGELOG.md)。

### ライセンス

MIT（[LICENSE](LICENSE)）。

## 简体中文

PipeWire 和 WirePlumber 的配置，让系统音量控制改变 USB 音箱 Edifier Hecate G2000 PRO 的硬件音量
（ALSA 控件 `PCM Playback Volume`），软件音量始终保持 100%。只影响 G2000 PRO（USB `35bb:b065`）。
本仓库包含配置、`hecate-g2000-pro-volume` 命令、测试和构建。**使用方法**请阅读每个发布版附带的
PDF 手册（9 种语言）。

### 结构

```text
src/hecate_volume/config/    两个配置文件（ACP 配置文件集和 WirePlumber 规则）
src/hecate_volume/           hecate-g2000-pro-volume 命令：status、diagnose、install、uninstall
tests/                       unittest；tests/fixtures：wpctl、pw-cli 和 amixer 的真实输出
scripts/                     build.py（.deb 和 .tar.gz）、build_manual.py（PDF）、forgejo_release.py、github_release.py
.forgejo/workflows/, .github/workflows/   Forgejo 和 GitHub 上相同的 CI，只在版本标签（v*）时运行
docs/                        架构、测试、来源、技能、审计、Forgejo、GitHub、隐私
docs/manual/<语言>/manual.md, docs/manual/imagens/   PDF 手册的源文件和截图
```

### 命令

```sh
make tools   # 列出缺少的软件（与 CI 镜像相同）
make check   # tools、lint（pyflakes，有 ruff 时也运行）、测试、带 lintian 的构建、手册
make build   # dist/hecate-g2000-pro-volume_<版本>_all.deb 和 dist/hecate-g2000-pro-volume-<版本>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<版本>-Manual.pdf，9 种语言合为一个文件
```

开发要求：Python 3.11+、`make`、`dpkg-deb`、`lintian`、`python3-pyflakes`，手册还需要 `weasyprint`、
`fontconfig`、`fonts-dejavu-core` 和 `fonts-noto-cjk`（apt）。可选：`ruff`。详情见
[docs/TESTING.md](docs/TESTING.md)。

### 文档

以下文档为葡萄牙语；手册有 9 种语言。

- [架构](docs/ARCHITECTURE.md)：方案、决策和放弃的替代方案。
- [测试](docs/TESTING.md)：自动测试和使用音箱的实机测试。
- [来源](docs/SOURCES.md)：每一行配置所依据的官方文档和源代码。
- [技能](docs/SKILLS.md)：各领域应用的项目技能。[审计](docs/AUDIT.md)。
- [隐私](docs/PRIVACIDADE.md) 和 [条款](docs/TERMOS.md)。
- [手册](docs/manual/)：各语言的 PDF 源文件；图片在 [docs/manual/imagens](docs/manual/imagens/README.md)。
- [Forgejo](docs/FORGEJO.md) 和 [GitHub](docs/GITHUB.md)：CI、推送和按标签发布。[更新记录](CHANGELOG.md)。

### 许可证

MIT（[LICENSE](LICENSE)）。

## 한국어

시스템 볼륨 조절이 USB 스피커 Edifier Hecate G2000 PRO의 하드웨어 볼륨(ALSA 컨트롤
`PCM Playback Volume`)을 바꾸도록 하는 PipeWire와 WirePlumber 설정입니다. 소프트웨어 볼륨은 항상
100%로 유지됩니다. G2000 PRO(USB `35bb:b065`)에만 적용됩니다. 이 저장소에는 설정,
`hecate-g2000-pro-volume` 명령, 테스트, 빌드가 들어 있습니다. **사용법**은 각 릴리스에 첨부된 PDF
설명서(9개 언어)를 참고하세요.

### 구조

```text
src/hecate_volume/config/    두 개의 설정 파일(ACP 프로필 세트와 WirePlumber 규칙)
src/hecate_volume/           hecate-g2000-pro-volume 명령: status, diagnose, install, uninstall
tests/                       unittest; tests/fixtures: wpctl, pw-cli, amixer의 실제 출력
scripts/                     build.py(.deb와 .tar.gz), build_manual.py(PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   Forgejo와 GitHub의 같은 CI, 버전 태그(v*)에서만 실행
docs/                        아키텍처, 테스트, 출처, 스킬, 감사, Forgejo, GitHub, 개인정보 보호
docs/manual/<언어>/manual.md, docs/manual/imagens/   PDF 설명서 원본과 스크린샷
```

### 명령

```sh
make tools   # 설치가 필요한 항목 목록(CI 이미지와 동일)
make check   # tools, lint(pyflakes, 있으면 ruff), 테스트, lintian을 포함한 빌드, 설명서
make build   # dist/hecate-g2000-pro-volume_<버전>_all.deb와 dist/hecate-g2000-pro-volume-<버전>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<버전>-Manual.pdf, 9개 언어를 한 파일로
```

개발 요구 사항: Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes`, 그리고 설명서를 위해
`weasyprint`, `fontconfig`, `fonts-dejavu-core`, `fonts-noto-cjk`(apt). 선택: `ruff`. 자세한 내용은
[docs/TESTING.md](docs/TESTING.md)에 있습니다.

### 문서

아래 문서는 포르투갈어로 되어 있으며, 설명서는 9개 언어로 제공됩니다.

- [아키텍처](docs/ARCHITECTURE.md): 해결 방법, 결정, 채택하지 않은 대안.
- [테스트](docs/TESTING.md): 자동 테스트와 스피커를 사용한 실제 테스트.
- [출처](docs/SOURCES.md): 설정의 각 줄을 뒷받침하는 공식 문서와 소스 코드.
- [스킬](docs/SKILLS.md): 분야별로 적용한 프로젝트 스킬. [감사](docs/AUDIT.md).
- [개인정보 보호](docs/PRIVACIDADE.md)와 [이용 약관](docs/TERMOS.md).
- [설명서](docs/manual/): 언어별 PDF 원본, 이미지는 [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md)와 [GitHub](docs/GITHUB.md): CI, 전송, 태그별 릴리스. [변경 기록](CHANGELOG.md).

### 라이선스

MIT([LICENSE](LICENSE)).

## Français

Configuration de PipeWire et de WirePlumber qui fait en sorte que le réglage du volume du système
change le volume matériel de l'enceinte USB Edifier Hecate G2000 PRO (contrôle ALSA
`PCM Playback Volume`), avec le volume logiciel toujours à 100 %. Seule la G2000 PRO
(USB `35bb:b065`) est concernée. Ce dépôt contient la configuration, la commande
`hecate-g2000-pro-volume`, les tests et le build. Pour l'**utiliser**, lisez le manuel PDF joint à
chaque release (9 langues).

### Structure

```text
src/hecate_volume/config/    les deux fichiers de configuration (jeu de profils ACP et règle WirePlumber)
src/hecate_volume/           commande hecate-g2000-pro-volume : status, diagnose, install, uninstall
tests/                       unittest ; tests/fixtures : sorties réelles de wpctl, pw-cli et amixer
scripts/                     build.py (.deb et .tar.gz), build_manual.py (PDF), forgejo_release.py, github_release.py
.forgejo/workflows/, .github/workflows/   le même CI sur Forgejo et GitHub, seulement sur tag de version (v*)
docs/                        architecture, tests, sources, skills, audit, Forgejo, GitHub, confidentialité
docs/manual/<langue>/manual.md, docs/manual/imagens/   source du manuel PDF et captures d'écran
```

### Commandes

```sh
make tools   # liste ce qui manque (la même chose que l'image du CI)
make check   # tools, lint (pyflakes, ruff si présent), tests, build avec lintian, manuel
make build   # dist/hecate-g2000-pro-volume_<version>_all.deb et dist/hecate-g2000-pro-volume-<version>.tar.gz
make manual  # dist/Hecate-G2000-PRO-Volume-<version>-Manual.pdf, les 9 langues dans un fichier
```

Prérequis de développement : Python 3.11+, `make`, `dpkg-deb`, `lintian`, `python3-pyflakes` et,
pour le manuel, `weasyprint`, `fontconfig`, `fonts-dejavu-core` et `fonts-noto-cjk` (apt).
Facultatif : `ruff`. Détails dans [docs/TESTING.md](docs/TESTING.md).

### Documentation

Les documents ci-dessous sont en portugais ; le manuel existe en 9 langues.

- [Architecture](docs/ARCHITECTURE.md) : solution, décisions et alternatives écartées.
- [Tests](docs/TESTING.md) : tests automatiques et tests réels avec l'enceinte.
- [Sources](docs/SOURCES.md) : documentation officielle et code derrière chaque ligne de configuration.
- [Skills](docs/SKILLS.md) : skills du projet appliquées dans chaque domaine. [Audit](docs/AUDIT.md).
- [Confidentialité](docs/PRIVACIDADE.md) et [Conditions](docs/TERMOS.md).
- [Manuel](docs/manual/) : source du PDF par langue ; images dans [docs/manual/imagens](docs/manual/imagens/README.md).
- [Forgejo](docs/FORGEJO.md) et [GitHub](docs/GITHUB.md) : CI, envoi et releases par tag. [Historique](CHANGELOG.md).

### Licence

MIT ([LICENSE](LICENSE)).
