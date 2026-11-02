% Hecate G2000 PRO Volume — マニュアル
% 目次

# はじめに {#introduction}

Hecate G2000 PRO Volume は、システムの音量調整で USB スピーカー Edifier Hecate G2000 PRO のハードウェア音量を変更できるようにします。ソフトウェアで音を小さくするのではなく、スピーカー自身の ALSA コントロール（**PCM Playback Volume**）を使います。

- スピーカーを出力にしているとき、ソフトウェア音量は常に 100% のままです。音量スライダー、音量キー、システムのミュートは、スピーカーのハードウェアだけを変更します。
- どのデスクトップ（GNOME、KDE Plasma など）でも、すべてのアプリケーションでも動作します。どれも PipeWire を使っているからです。
- 対象は G2000 PRO（USB `35bb:b065`）だけです。ほかのオーディオデバイスはそのままです。
- バックグラウンドで動くプログラムはありません。PipeWire と WirePlumber の設定に加えて、確認とテスト用のコマンド `hecate-g2000-pro-volume` があるだけです。

# 必要なもの {#requirements}

- PipeWire と WirePlumber 0.5 以降を備えた Linux。Debian 13（PipeWire 1.4.2、WirePlumber 0.5.8）でテスト済みです。バージョンの確認: `wireplumber --version`。
- `hecate-g2000-pro-volume` コマンド用の Python 3.11 以降。
- コマンド `wpctl`、`pw-cli`、`amixer`（Debian と Ubuntu ではパッケージ `wireplumber`、`pipewire-bin`、`alsa-utils`）。

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

## 設定を反映する {#apply}

1. WirePlumber を再起動するか、ログアウトしてもう一度ログインします。

```
systemctl --user restart wireplumber.service
```

2. スピーカーがデジタルプロファイル（IEC958）だった場合、出力の名前が変わり、既定の出力が別のデバイスに移ることがあります。サウンド設定で **HECATE G2000 PRO** を一度出力として選んでください。Easy Effects を使っている場合は、その出力にもスピーカーを選びます。

![サウンド設定: 出力に HECATE G2000 PRO を選択](configuracoes_som_saida.jpg)

# 使い方 {#usage}

音量スライダー、音量キー、ミュートをいつもどおり使います。変更はすべてスピーカーのハードウェア音量に直接届きます。

![HECATE G2000 PRO を使ったシステムの音量スライダー](controle_volume_gnome.jpg)

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

音量を現在より下に 3 段階下げ、ミュートし、ハードウェアコントロールが追従することと、ソフトウェア音量が 100% のままであることを確認します。最後に音量とミュートを元に戻します。テスト前より音が大きくなることはありません。各確認は **PASS** または **FAIL** と表示されます。

![端末: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# しくみ {#how-it-works}

- **専用のプロファイルセット。** PipeWire の既定のプロファイルセットは、このスピーカーにデジタルの IEC958 プロファイルも提供します。そのミキサーパスには音量コントロールがないため、音量の変更はすべてソフトウェアになります。このプロジェクトの設定はアナログプロファイルだけを提供し、そのパスはスピーカーの **PCM** コントロールを音量とミュートに使います。
- **保存されたプロファイル。** 以前に保存された IEC958 プロファイルは、もう存在しないため無視され、WirePlumber が自動でアナログを選びます。
- **ハードウェアのみ。** ドライバーはスピーカーの音量を −28.37 dB から −0.94 dB と報告します。最大値が負なので、PipeWire はこのデシベル情報を使わず、ハードウェアの 148 段階（0〜147）だけに音量を適用し、上にソフトウェア音量を重ねません。
- **このスピーカーだけ。** WirePlumber のルールは USB デバイス `35bb:b065` だけに適用されます。
- **ファイル。** .deb パッケージ: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` と `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`。ユーザーごとのインストール: 同じ名前で `~/.config/wireplumber/wireplumber.conf.d/` と `~/.config/alsa-card-profile/mixer/profile-sets/` に置かれます。

# 制限事項 {#limitations}

- **スピーカーのボタン。** スピーカー本体の音量ボタンとつまみは別の調整です。ALSA からは見えず、システム音量はその操作に追従しません。
- **音量 0%。** ハードウェアの 0 段階に当たります。この段階が完全な無音かどうかは確認していません。無音にするにはミュートを使ってください。
- **デジタル出力。** このスピーカーでは IEC958 プロファイルが表示されなくなります。
- **WirePlumber 0.4。** 対応していません。別の設定形式（Lua）を使うためです。
- **PipeWire なし。** PulseAudio だけのシステムはテストしておらず、対応していません。
- **systemd なし。** お使いのディストリビューションの方法で WirePlumber を再起動するか、ログアウトしてもう一度ログインしてください。

# よくある問題 {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber がまだ再起動されていません: `systemctl --user restart wireplumber.service`。
- **インストール後に音が出ない。** スピーカーの出力名が変わったため、既定の出力が別のデバイスに移りました。HECATE G2000 PRO を出力に選んでください（Easy Effects を使っている場合はそちらでも）。
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
