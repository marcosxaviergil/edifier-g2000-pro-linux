% Hecate G2000 PRO Volume — Manual
% Sumário

# Introdução {#introduction}

O Hecate G2000 PRO Volume faz o controle de volume do sistema mudar o volume físico da caixa de som USB Edifier Hecate G2000 PRO, pelo controle ALSA da própria caixa (**PCM Playback Volume**), em vez de baixar o som por software.

- Com a caixa como saída, o volume por software fica sempre em 100%: o controle de volume, as teclas de volume e o mudo do sistema mexem só no hardware da caixa.
- Vale para qualquer ambiente gráfico (GNOME, KDE Plasma e outros) e para todos os aplicativos, porque todos usam o PipeWire.
- Só a G2000 PRO (USB `35bb:b065`) é afetada. Os outros dispositivos de áudio continuam como estão.
- Não há programa rodando em segundo plano: a solução é configuração do PipeWire e do WirePlumber, mais o comando `hecate-g2000-pro-volume` para conferir e testar.

# Requisitos {#requirements}

- Linux com PipeWire e WirePlumber 0.5 ou mais novo. Testado no Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). Para ver a versão: `wireplumber --version`.
- Python 3.11 ou mais novo, para o comando `hecate-g2000-pro-volume`.
- Os comandos `wpctl`, `pw-cli` e `amixer` (Debian e Ubuntu: pacotes `wireplumber`, `pipewire-bin` e `alsa-utils`).

# Instalação {#installation}

## Debian, Ubuntu e derivados (.deb) {#install-deb}

1. Baixe `hecate-g2000-pro-volume_<versão>_all.deb` da release.
2. Instale com o apt, que também instala as dependências:

```
sudo apt install ./hecate-g2000-pro-volume_<versão>_all.deb
```

O pacote instala a configuração para todos os usuários do computador.

## Outras distribuições (.tar.gz) {#install-tarball}

1. Baixe `hecate-g2000-pro-volume-<versão>.tar.gz` da release.
2. Extraia e instale para o seu usuário, sem root:

```
tar -xzf hecate-g2000-pro-volume-<versão>.tar.gz
cd hecate-g2000-pro-volume-<versão>
./hecate-g2000-pro-volume install
```

Se já existir um arquivo com o mesmo nome e outro conteúdo, ele é mantido e a instalação para com uma mensagem. Para substituí-lo, use `./hecate-g2000-pro-volume install --force`.

## Aplicar a configuração {#apply}

1. Reinicie o WirePlumber, ou saia da sessão e entre de novo:

```
systemctl --user restart wireplumber.service
```

2. Se a caixa estava no perfil digital (IEC958), a saída dela muda de nome e a saída padrão pode passar para outro dispositivo. Escolha a **HECATE G2000 PRO** uma vez como saída nas configurações de som. Se usa o Easy Effects, escolha a caixa também como saída dele.

![Configurações de som: a HECATE G2000 PRO como saída](configuracoes_som_saida.jpg)

# Uso {#usage}

Use o controle de volume, as teclas de volume e o mudo como sempre. Cada mudança vai direto para o volume físico da caixa.

![Controle de volume do sistema com a HECATE G2000 PRO](controle_volume_gnome.jpg)

## Conferir a instalação: status {#status}

```
hecate-g2000-pro-volume status
```

Mostra onde a configuração está instalada, se o WirePlumber a carregou, o perfil ativo, o volume do sistema, os controles de hardware da caixa e o volume por software. Não muda nada. Termina com **Result: OK** quando está tudo certo; senão, cada **Problem:** diz o que fazer.

![Terminal: hecate-g2000-pro-volume status](terminal_status.jpg)

## Testar a caixa: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Baixa o volume em três passos abaixo do atual, liga o mudo e confere se o controle de hardware acompanha e se o volume por software fica em 100%. No fim, volta o volume e o mudo ao que estavam. O som nunca fica mais alto do que antes do teste. Cada verificação aparece como **PASS** ou **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Como funciona {#how-it-works}

- **Conjunto de perfis próprio.** O conjunto de perfis padrão do PipeWire oferece para a caixa também o perfil digital IEC958, cujo caminho de mixer não tem controle de volume: com ele, todo ajuste de volume é por software. A configuração deste projeto oferece só o perfil analógico, cujo caminho usa o controle **PCM** da caixa para volume e mudo.
- **Perfil salvo.** Um perfil IEC958 salvo antes é ignorado, porque deixa de existir; o WirePlumber escolhe o analógico sozinho.
- **Só hardware.** O driver informa o volume da caixa de −28,37 dB a −0,94 dB. Como o máximo é negativo, o PipeWire desconsidera essa informação em decibéis e aplica o volume só nos 148 degraus do hardware (0 a 147), sem volume por software por cima.
- **Só esta caixa.** A regra do WirePlumber vale apenas para o dispositivo USB `35bb:b065`.
- **Arquivos.** Pacote .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` e `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Instalação por usuário: os mesmos nomes em `~/.config/wireplumber/wireplumber.conf.d/` e `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Limitações {#limitations}

- **Botões da caixa.** O botão e o controle de volume da própria caixa são um ajuste separado: o ALSA não os enxerga, e o volume do sistema não acompanha o que eles fazem.
- **Volume 0%.** Corresponde ao degrau 0 do hardware. Não foi verificado se esse degrau é silêncio total; para silêncio, use o mudo.
- **Saída digital.** O perfil IEC958 deixa de aparecer para esta caixa.
- **WirePlumber 0.4.** Não é suportado: ele usa outro formato de configuração (Lua).
- **Sem PipeWire.** Sistemas só com PulseAudio não foram testados e não são suportados.
- **Sem systemd.** Reinicie o WirePlumber pelo meio que a sua distribuição usa, ou saia da sessão e entre de novo.

# Problemas comuns {#troubleshooting}

- **"The configuration is installed but not loaded yet."** O WirePlumber ainda não foi reiniciado: `systemctl --user restart wireplumber.service`.
- **Sem som depois de instalar.** A saída padrão foi para outro dispositivo, porque o nome da saída da caixa mudou. Escolha a HECATE G2000 PRO como saída (e no Easy Effects, se usar).
- **"PipeWire does not see the speaker."** Confira o cabo USB e se a caixa está ligada.
- **"wpctl is not installed"** (ou `pw-cli`, `amixer`). Instale o pacote indicado na mensagem.
- **Um arquivo aparece como "different" no status.** Já existia um arquivo com o mesmo nome e outro conteúdo. Confira-o e, se puder ser substituído, rode `hecate-g2000-pro-volume install --force`.
- **diagnose mostra FAIL.** Rode `hecate-g2000-pro-volume status` e resolva primeiro os **Problem:** que ele mostrar.

# Desinstalar {#uninstall}

- Pacote .deb: `sudo apt remove hecate-g2000-pro-volume`
- Instalação por usuário: `./hecate-g2000-pro-volume uninstall` (um arquivo com outro conteúdo é mantido; `--force` o remove)

Depois, reinicie o WirePlumber: `systemctl --user restart wireplumber.service`. A caixa volta ao comportamento padrão do PipeWire.

# Privacidade e segurança {#privacy}

O projeto não coleta, não grava e não envia dados pessoais, e não acessa a rede. O comando só lê o estado do áudio com `wpctl`, `pw-cli` e `amixer` e, no `install` e no `uninstall`, grava ou apaga os dois arquivos de configuração da sua pasta pessoal. O `diagnose` muda o volume por alguns segundos e o devolve ao que estava. Detalhes em `docs/PRIVACIDADE.md` do projeto.
