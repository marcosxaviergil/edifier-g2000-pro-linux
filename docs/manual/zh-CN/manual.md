% Hecate G2000 PRO Volume — 手册
% 目录

# 简介 {#introduction}

Hecate G2000 PRO Volume 让系统音量控制改变 USB 音箱 Edifier Hecate G2000 PRO 本身的音量。它使用音箱的硬件控件（**PCM Playback Volume**），而不是在电脑里降低声音。

以音箱为输出时：

- 系统音量条显示并改变**音箱的音量**。
- 键盘的音量键和音箱上的 **+**、**−** 按钮改变的是同一个音量，音量条会随之变化。
- 系统静音会打开或关闭**音箱的静音**（**PCM Playback Switch**）。
- 电脑的（软件）音量始终保持 **100%**，不会出现在任何控件中。
- 每个应用程序的音量照常使用。

只影响 G2000 PRO（USB `35bb:b065`）；其他音频设备保持不变。适用于任何桌面环境（GNOME、KDE Plasma 等），因为它们都使用 PipeWire。没有在后台运行的程序：只有两个 PipeWire 和 WirePlumber 配置文件，外加用于检查和测试的命令 `hecate-g2000-pro-volume`。

# 系统要求 {#requirements}

- 带有 PipeWire 和 WirePlumber 0.5 或更高版本的 Linux。查看版本：`wireplumber --version`。
- Python 3.11 或更高版本，用于 `hecate-g2000-pro-volume` 命令。
- 命令 `wpctl`、`pw-cli` 和 `amixer`（Debian 和 Ubuntu：软件包 `wireplumber`、`pipewire-bin` 和 `alsa-utils`）。.deb 软件包会一并安装它们。
- 音箱通过 USB 线连接到电脑。

# 安装 {#installation}

## Debian、Ubuntu 及其衍生版（.deb） {#install-deb}

1. 从发布页下载 `hecate-g2000-pro-volume_<版本>_all.deb`。
2. 用 apt 安装，它也会安装依赖：

```
sudo apt install ./hecate-g2000-pro-volume_<版本>_all.deb
```

该软件包为这台电脑的所有用户安装配置。

## 其他发行版（.tar.gz） {#install-tarball}

1. 从发布页下载 `hecate-g2000-pro-volume-<版本>.tar.gz`。
2. 解压，并为当前用户安装，无需 root：

```
tar -xzf hecate-g2000-pro-volume-<版本>.tar.gz
cd hecate-g2000-pro-volume-<版本>
./hecate-g2000-pro-volume install
```

如果已经存在同名但内容不同的文件，该文件会被保留，安装会停止并显示提示。要替换它，请使用 `./hecate-g2000-pro-volume install --force`。

## 启用 {#apply}

1. 重启 WirePlumber，或注销后重新登录：

```
systemctl --user restart wireplumber.service
```

2. 在声音设置中把 **HECATE G2000 PRO** 选为输出。音箱的输出会变成模拟立体声；如果之前是数字立体声（IEC958），默认输出可能已转到其他设备。如果使用 Easy Effects，也要把音箱选为它的输出。
3. 用 `hecate-g2000-pro-volume status` 检查：结果应为 **Result: OK**。

![声音设置：选择 HECATE G2000 PRO 作为输出](configuracoes_som_saida.jpg)

# 使用 {#usage}

## 音箱的音量和静音 {#volume}

使用系统音量条、键盘音量键或音箱上的 **+**、**−** 按钮。它们改变的都是同一个音量：音箱的音量。音量条显示音箱的音量，并随任何一种操作变化。系统静音会关闭音箱的声音。

![使用 HECATE G2000 PRO 时的系统音量条](controle_volume_gnome.jpg)

## 每个应用程序的音量 {#app-volume}

在按应用程序调节音量的控件中（声音设置里，或 pavucontrol 等程序），每个应用程序照常拥有自己的音量，在电脑中调节。它叠加在音箱的音量之上。

## 检查安装：status {#status}

```
hecate-g2000-pro-volume status
```

显示配置的安装位置、WirePlumber 是否已加载配置、当前配置文件、系统音量、音箱的硬件控件和软件音量。不做任何更改。一切正常时以 **Result: OK** 结尾；否则每一行 **Problem:** 都会说明该怎么做。

![终端：hecate-g2000-pro-volume status](terminal_status.jpg)

## 测试音箱：diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

把音量分三步降到当前音量以下，打开静音，并检查硬件控件是否跟随变化、软件音量是否保持 100%。最后把音量和静音恢复原样。声音不会比测试前更大；音量低于 5% 时，测试会要求先调高音量。每项检查显示 **PASS** 或 **FAIL**。

![终端：hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# 工作原理 {#how-it-works}

- **音箱的音量控件。** 音箱通过 USB 提供一个音量控件（左、右声道）和一个静音控件。Linux 将它们显示为 **PCM Playback Volume** 和 **PCM Playback Switch**。
- **音箱的按钮。** 音箱同时以多媒体键盘（"HECATE G2000 PRO Consumer Control"）的身份出现在电脑上：**+** 和 **−** 按钮发送的是音量键。因此它们的作用与键盘音量键完全相同。
- **模拟配置文件。** PipeWire 的默认配置文件集也为音箱提供数字配置文件 IEC958，它不使用音箱的音量控件：使用它时，音量是在电脑里降低的。本项目的配置只提供模拟配置文件，它使用音箱的 **PCM** 控件来控制音量和静音。之前选择的 IEC958 配置文件会被搁置，WirePlumber 会自动使用模拟配置文件。
- **音量只在音箱上。** 音箱的控件有 148 档（0 到 147），从 −28.37 dB 到 −0.94 dB。PipeWire 把音量条直接应用到这些档位上，不再叠加软件音量。
- **仅此音箱。** WirePlumber 规则只适用于 USB 设备 `35bb:b065`。
- **文件。** .deb 软件包：`/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` 和 `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`。按用户安装：同名文件位于 `~/.config/wireplumber/wireplumber.conf.d/` 和 `~/.config/alsa-card-profile/mixer/profile-sets/`。

# 常见问题 {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber 还没有重启：`systemctl --user restart wireplumber.service`。
- **启用后没有声音。** 默认输出转到了其他设备。请把 HECATE G2000 PRO 选为输出（如果使用 Easy Effects，也在其中选择）。
- **"PipeWire does not see the speaker."** 请检查 USB 线以及音箱是否已开机。
- **"wpctl is not installed"**（或 `pw-cli`、`amixer`）。请安装提示中给出的软件包。
- **status 中某个文件显示为 "different"。** 已经存在同名但内容不同的文件。请检查它；如果可以替换，运行 `hecate-g2000-pro-volume install --force`。
- **diagnose 显示 FAIL。** 运行 `hecate-g2000-pro-volume status`，先解决它显示的 **Problem:** 行。

# 卸载 {#uninstall}

- .deb 软件包：`sudo apt remove hecate-g2000-pro-volume`
- 按用户安装：`./hecate-g2000-pro-volume uninstall`（内容不同的文件会被保留；`--force` 会删除它）

然后重启 WirePlumber：`systemctl --user restart wireplumber.service`。音箱会恢复 PipeWire 的默认行为。

# 隐私与安全 {#privacy}

本项目不收集、不保存、不发送个人数据，也不使用网络。该命令只用 `wpctl`、`pw-cli` 和 `amixer` 读取音频状态；在 `install` 和 `uninstall` 中，它只写入或删除您主文件夹中的两个配置文件。`diagnose` 会在几秒内改变音量，然后恢复原样。详情见项目中的 `docs/PRIVACIDADE.md`。
