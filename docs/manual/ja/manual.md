% Hecate G2000 PRO Volume — マニュアル
% 目次

# はじめに {#introduction}

Hecate G2000 PRO Volume は、システムの音量調整で USB スピーカー Edifier Hecate G2000 PRO 自体の音量を変更できるようにします。コンピューター側で音を小さくするのではなく、スピーカーのハードウェアコントロール（**PCM Playback Volume**）を使います。

スピーカーを出力にしているとき:

- システムの音量バーは **スピーカーの音量** を表示し、変更します。
- キーボードの音量キーとスピーカーの **+**・**−** ボタンも同じ音量を変更し、バーもそれに追従します。
- システムのミュートは **スピーカーのミュート**（**PCM Playback Switch**）をオン・オフします。
- コンピューター側（ソフトウェア）の音量は常に **100%** のままで、どのコントロールにも表示されません。
- アプリケーションごとの音量はこれまでどおり使えます。

対象は G2000 PRO（USB `35bb:b065`）だけで、ほかのオーディオデバイスはそのままです。どのデスクトップ（GNOME、KDE Plasma など）でも動作します。どれも PipeWire を使っているからです。バックグラウンドで動くプログラムはありません。PipeWire と WirePlumber の設定ファイル 2 つと、確認・テスト用のコマンド `hecate-g2000-pro-volume` だけです。

# 必要なもの {#requirements}

- PipeWire と WirePlumber 0.5 以降を備えた Linux。バージョンの確認: `wireplumber --version`。
- `hecate-g2000-pro-volume` コマンド用の Python 3.11 以降。
- コマンド `wpctl`、`pw-cli`、`amixer`（Debian と Ubuntu ではパッケージ `wireplumber`、`pipewire-bin`、`alsa-utils`）。.deb パッケージがこれらもインストールします。
- USB ケーブルでコンピューターにつないだスピーカー。

# インストール {#installation}

## Debian、Ubuntu とその派生（.deb） {#install-deb}

1. リリースから `hecate-g2000-pro-volume_<バージョン>_all.deb` をダウンロードします。
2. 依存パッケージも一緒に入る apt でインストールします。

```
sudo apt install ./hecate-g2000-pro-volume_<バージョン>_all.deb
```

このパッケージは、コンピューターのすべてのユーザー向けに設定をインストールします。

## その他のディストリビューション（.tar.gz） {#install-tarball}

1. リリースから `hecate-g2000-pro-volume-<バージョン>.tar.gz` をダウンロードします。
2. 展開して、root なしで自分のユーザー向けにインストールします。

```
tar -xzf hecate-g2000-pro-volume-<バージョン>.tar.gz
cd hecate-g2000-pro-volume-<バージョン>
./hecate-g2000-pro-volume install
```

同じ名前で内容の違うファイルがすでにある場合、そのファイルは残され、インストールはメッセージを出して止まります。置き換えるには `./hecate-g2000-pro-volume install --force` を使います。

## 有効にする {#apply}

1. WirePlumber を再起動するか、ログアウトしてもう一度ログインします。

```
systemctl --user restart wireplumber.service
```

2. サウンド設定で **HECATE G2000 PRO** を出力に選びます。スピーカーの出力はアナログステレオになります。以前がデジタルステレオ（IEC958）だった場合、既定の出力が別のデバイスに移っていることがあります。Easy Effects を使っている場合は、その出力にもスピーカーを選びます。
3. `hecate-g2000-pro-volume status` で確認します。結果は **Result: OK** になるはずです。

![サウンド設定: 出力に HECATE G2000 PRO を選択](configuracoes_som_saida.jpg)

# 使い方 {#usage}

## スピーカーの音量とミュート {#volume}

システムの音量バー、キーボードの音量キー、スピーカーの **+**・**−** ボタンのどれを使ってもかまいません。どれも同じ音量、つまりスピーカーの音量を変更します。バーはスピーカーの音量を表示し、どの操作にも追従します。システムのミュートはスピーカーの音を消します。

![HECATE G2000 PRO を使ったシステムの音量バー](controle_volume_gnome.jpg)

## アプリケーションごとの音量 {#app-volume}

アプリケーションごとの音量調整（サウンド設定や pavucontrol などのプログラム）では、各アプリケーションがこれまでどおりコンピューター側で調整される独自の音量を持ちます。この音量はスピーカーの音量に重ねて適用されます。

## インストールの確認: status {#status}

```
hecate-g2000-pro-volume status
```

設定のインストール場所、WirePlumber が読み込んだかどうか、有効なプロファイル、システム音量、スピーカーのハードウェアコントロール、ソフトウェア音量を表示します。何も変更しません。すべて正しければ **Result: OK** で終わります。そうでなければ、各 **Problem:** の行がすべきことを示します。

![端末: hecate-g2000-pro-volume status](terminal_status.jpg)

## スピーカーのテスト: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

音量を現在より下に 3 段階下げ、ミュートし、ハードウェアコントロールが追従することと、ソフトウェア音量が 100% のままであることを確認します。最後に音量とミュートを元に戻します。テスト前より音が大きくなることはありません。音量が 5% 未満のときは、上げるように求めます。各確認は **PASS** または **FAIL** と表示されます。

![端末: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# しくみ {#how-it-works}

- **スピーカーの音量コントロール。** スピーカーは USB を通じて、音量コントロール（左右）とミュートを 1 つずつ提供します。Linux ではそれぞれ **PCM Playback Volume** と **PCM Playback Switch** と表示されます。
- **スピーカーのボタン。** スピーカーはコンピューターに対してメディアキーボード（「HECATE G2000 PRO Consumer Control」）としても認識されます。**+**・**−** ボタンは音量キーを送ります。そのため、キーボードの音量キーとまったく同じように動作します。
- **アナログプロファイル。** PipeWire の既定のプロファイルセットは、このスピーカーにデジタルの IEC958 プロファイルも提供します。このプロファイルはスピーカーの音量コントロールを使わないため、音量はコンピューター側で下げられていました。このプロジェクトの設定はアナログプロファイルだけを提供し、スピーカーの **PCM** コントロールを音量とミュートに使います。以前に選ばれていた IEC958 プロファイルは使われなくなり、WirePlumber が自動でアナログを使います。
- **音量はスピーカー側だけ。** スピーカーのコントロールは 148 段階（0〜147）、−28.37 dB から −0.94 dB です。PipeWire は音量バーをこの段階に直接適用し、その上にソフトウェア音量を重ねません。
- **このスピーカーだけ。** WirePlumber のルールは USB デバイス `35bb:b065` だけに適用されます。
- **ファイル。** .deb パッケージ: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` と `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`。ユーザーごとのインストール: 同じ名前で `~/.config/wireplumber/wireplumber.conf.d/` と `~/.config/alsa-card-profile/mixer/profile-sets/` に置かれます。

# よくある問題 {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber がまだ再起動されていません: `systemctl --user restart wireplumber.service`。
- **有効にした後に音が出ない。** 既定の出力が別のデバイスに移りました。HECATE G2000 PRO を出力に選んでください（Easy Effects を使っている場合はそちらでも）。
- **"PipeWire does not see the speaker."** USB ケーブルと、スピーカーの電源が入っていることを確認してください。
- **"wpctl is not installed"**（または `pw-cli`、`amixer`）。メッセージに書かれたパッケージをインストールしてください。
- **status でファイルが "different" と表示される。** 同じ名前で内容の違うファイルがすでにありました。内容を確認し、置き換えてよければ `hecate-g2000-pro-volume install --force` を実行してください。
- **diagnose が FAIL を表示する。** `hecate-g2000-pro-volume status` を実行し、表示された **Problem:** の行を先に解決してください。

# アンインストール {#uninstall}

- .deb パッケージ: `sudo apt remove hecate-g2000-pro-volume`
- ユーザーごとのインストール: `./hecate-g2000-pro-volume uninstall`（内容の違うファイルは残されます。`--force` で削除します）

その後、WirePlumber を再起動します: `systemctl --user restart wireplumber.service`。スピーカーは PipeWire の既定の動作に戻ります。

# プライバシーとセキュリティ {#privacy}

このプロジェクトは個人データを収集、保存、送信せず、ネットワークも使いません。コマンドは `wpctl`、`pw-cli`、`amixer` でオーディオの状態を読むだけで、`install` と `uninstall` ではホームフォルダーにある 2 つの設定ファイルを書き込みまたは削除します。`diagnose` は数秒間音量を変え、元に戻します。詳しくはプロジェクトの `docs/PRIVACIDADE.md` を参照してください。
