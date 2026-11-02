% Hecate G2000 PRO Volume — Manual
% Sumário

# Introdução {#introduction}

O Hecate G2000 PRO Volume faz o controle de volume do sistema mudar o volume da própria caixa de som USB Edifier Hecate G2000 PRO, pelo controle de hardware dela (**PCM Playback Volume**), em vez de baixar o som no computador.

Com a caixa como saída:

- A barra de volume do sistema mostra e muda o **volume da caixa**.
- As teclas de volume do teclado e os botões **+** e **−** da caixa mudam esse mesmo volume, e a barra acompanha.
- O mudo do sistema liga e desliga o **mudo da caixa** (**PCM Playback Switch**).
- O volume do computador (por software) fica sempre em **100%** e não aparece em nenhum controle.
- O volume de cada aplicativo continua funcionando como sempre.

Só a G2000 PRO (USB `35bb:b065`) é afetada; os outros dispositivos de áudio continuam como estão. Funciona em qualquer ambiente gráfico (GNOME, KDE Plasma e outros), porque todos usam o PipeWire. Não há programa rodando em segundo plano: são dois arquivos de configuração do PipeWire e do WirePlumber, mais o comando `hecate-g2000-pro-volume` para conferir e testar.

# Requisitos {#requirements}

- Linux com PipeWire e WirePlumber 0.5 ou mais novo. Para ver a versão: `wireplumber --version`.
- Python 3.11 ou mais novo, para o comando `hecate-g2000-pro-volume`.
- Os comandos `wpctl`, `pw-cli` e `amixer` (Debian e Ubuntu: pacotes `wireplumber`, `pipewire-bin` e `alsa-utils`). O pacote .deb já os instala.
- A caixa ligada ao computador pelo cabo USB.

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

## Ativar {#apply}

1. Reinicie o WirePlumber, ou saia da sessão e entre de novo:

```
systemctl --user restart wireplumber.service
```

2. Nas configurações de som, escolha a **HECATE G2000 PRO** como saída. A saída da caixa passa a se chamar "Estéreo analógico"; se antes ela estava como "Estéreo digital (IEC958)", a saída padrão pode ter ido para outro dispositivo. Se usa o Easy Effects, escolha a caixa também como saída dele.
3. Confira com `hecate-g2000-pro-volume status`: o resultado deve ser **Result: OK**.

![Configurações de som: a HECATE G2000 PRO como saída](configuracoes_som_saida.jpg)

# Uso {#usage}

## Volume e mudo da caixa {#volume}

Use a barra de volume do sistema, as teclas de volume do teclado ou os botões **+** e **−** da caixa. Todos mudam o mesmo volume: o da caixa. A barra mostra o volume da caixa e acompanha qualquer um deles. O mudo do sistema desliga o som na caixa.

![Barra de volume do sistema com a HECATE G2000 PRO](controle_volume_gnome.jpg)

## Volume de cada aplicativo {#app-volume}

No controle de volume por aplicativo (nas configurações de som, ou em programas como o pavucontrol), cada aplicativo continua com o seu próprio volume, ajustado no computador, como sempre. Ele se soma ao volume da caixa.

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

Baixa o volume em três passos abaixo do atual, liga o mudo e confere se o controle de hardware acompanha e se o volume por software fica em 100%. No fim, volta o volume e o mudo ao que estavam. O som nunca fica mais alto do que antes do teste; com o volume abaixo de 5%, o teste pede para aumentá-lo. Cada verificação aparece como **PASS** ou **FAIL**.

![Terminal: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Como funciona {#how-it-works}

- **O controle de volume da caixa.** Pela USB, a caixa oferece um controle de volume (esquerdo e direito) e um de mudo. O Linux os mostra como **PCM Playback Volume** e **PCM Playback Switch**.
- **Os botões da caixa.** A caixa também se apresenta ao computador como um teclado de mídia ("HECATE G2000 PRO Consumer Control"): os botões **+** e **−** enviam as teclas de volume. Por isso eles agem exatamente como as teclas de volume do teclado.
- **Perfil analógico.** O conjunto de perfis padrão do PipeWire oferece para a caixa também o perfil digital IEC958, que não usa o controle de volume dela: com ele, o volume era baixado no computador. A configuração deste projeto oferece só o perfil analógico, que usa o controle **PCM** da caixa para volume e mudo. Um perfil IEC958 escolhido antes é deixado de lado e o WirePlumber passa a usar o analógico sozinho.
- **Volume só na caixa.** O controle da caixa tem 148 degraus (0 a 147), de −28,37 dB a −0,94 dB. O PipeWire aplica a barra de volume direto nesses degraus, sem volume por software por cima.
- **Só esta caixa.** A regra do WirePlumber vale apenas para o dispositivo USB `35bb:b065`.
- **Arquivos.** Pacote .deb: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` e `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Instalação por usuário: os mesmos nomes em `~/.config/wireplumber/wireplumber.conf.d/` e `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Problemas comuns {#troubleshooting}

- **"The configuration is installed but not loaded yet."** O WirePlumber ainda não foi reiniciado: `systemctl --user restart wireplumber.service`.
- **Sem som depois de ativar.** A saída padrão foi para outro dispositivo. Escolha a HECATE G2000 PRO como saída (e no Easy Effects, se usar).
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
