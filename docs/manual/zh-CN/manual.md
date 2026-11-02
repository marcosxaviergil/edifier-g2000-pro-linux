% Hecate G2000 PRO Volume — 手册
% 目录

# 简介 {#introduction}

Hecate G2000 PRO Volume 让系统音量控制直接改变 USB 音箱 Edifier Hecate G2000 PRO 的硬件音量。它使用音箱自身的 ALSA 控件（**PCM Playback Volume**），而不是用软件降低声音。

- 以音箱为输出时，软件音量始终保持 100%：音量滑块、音量键和系统静音只改变音箱的硬件。
- 适用于任何桌面环境（GNOME、KDE Plasma 等）和所有应用程序，因为它们都使用 PipeWire。
- 只影响 G2000 PRO（USB `35bb:b065`）。其他音频设备保持不变。
- 没有在后台运行的程序：方案就是 PipeWire 和 WirePlumber 的配置，外加用于检查和测试的命令 `hecate-g2000-pro-volume`。

# 系统要求 {#requirements}

- 带有 PipeWire 和 WirePlumber 0.5 或更高版本的 Linux。已在 Debian 13（PipeWire 1.4.2、WirePlumber 0.5.8）上测试。查看版本：`wireplumber --version`。
- Python 3.11 或更高版本，用于 `hecate-g2000-pro-volume` 命令。
- 命令 `wpctl`、`pw-cli` 和 `amixer`（Debian 和 Ubuntu：软件包 `wireplumber`、`pipewire-bin` 和 `alsa-utils`）。

# 安装 {#installation}

## Debian、Ubuntu 及其衍生版（.deb） {#install-deb}

1. 从发布页下载 `hecate-g2000-pro-volume_<版本>_all.deb`。
2. 用 apt 安装，它也会安装依赖：

```
sudo apt install ./hecate-g2000-pro-volume_<版本>_all.deb
```

该软件包为这台计算机的所有用户安装配置。

## 其他发行版（.tar.gz） {#install-tarball}

1. 从发布页下载 `hecate-g2000-pro-volume-<版本>.tar.gz`。
2. 解压，并为当前用户安装，无需 root：

```
tar -xzf hecate-g2000-pro-volume-<版本>.tar.gz
cd hecate-g2000-pro-volume-<版本>
./hecate-g2000-pro-volume install
```

如果已经存在同名但内容不同的文件，该文件会被保留，安装会停止并显示提示。要替换它，请使用 `./hecate-g2000-pro-volume install --force`。

## 应用配置 {#apply}

1. 重启 WirePlumber，或注销后重新登录：

```
systemctl --user restart wireplumber.service
```

2. 如果音箱原先使用数字配置文件（IEC958），它的输出会改名，默认输出可能会转到其他设备。请在声音设置中把 **HECATE G2000 PRO** 选为输出一次。如果使用 Easy Effects，也要把音箱选为它的输出。

![声音设置：选择 HECATE G2000 PRO 作为输出](configuracoes_som_saida.jpg)

# 使用 {#usage}

像平常一样使用音量滑块、音量键和静音。每次更改都会直接作用于音箱的硬件音量。

![使用 HECATE G2000 PRO 时的系统音量滑块](controle_volume_gnome.jpg)

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

把音量分三步降到当前音量以下，打开静音，并检查硬件控件是否跟随变化、软件音量是否保持 100%。最后把音量和静音恢复原样。声音不会比测试前更大。每项检查显示 **PASS** 或 **FAIL**。

![终端：hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# 工作原理 {#how-it-works}

- **专用配置文件集。** PipeWire 的默认配置文件集也为音箱提供数字配置文件 IEC958，其混音器路径没有音量控件：使用它时，所有音量调整都只是软件调整。本项目的配置只提供模拟配置文件，其路径使用音箱的 **PCM** 控件来控制音量和静音。
- **已保存的配置文件。** 之前保存的 IEC958 配置文件会被忽略，因为它已不存在；WirePlumber 会自动选择模拟配置文件。
- **仅硬件。** 驱动报告音箱音量范围为 −28.37 dB 到 −0.94 dB。由于最大值为负，PipeWire 不使用这一分贝信息，只把音量应用到硬件的 148 个档位（0 到 147），不再叠加软件音量。
- **仅此音箱。** WirePlumber 规则只适用于 USB 设备 `35bb:b065`。
- **文件。** .deb 软件包：`/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` 和 `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`。按用户安装：同名文件位于 `~/.config/wireplumber/wireplumber.conf.d/` 和 `~/.config/alsa-card-profile/mixer/profile-sets/`。

# 限制 {#limitations}

- **音箱按键。** 音箱自身的音量按键和旋钮是单独的调节：ALSA 看不到它们，系统音量也不会跟随它们的变化。
- **0% 音量。** 对应硬件的第 0 档。尚未验证这一档是否完全无声；需要静音时请使用静音。
- **数字输出。** 此音箱不再显示 IEC958 配置文件。
- **WirePlumber 0.4。** 不支持：它使用另一种配置格式（Lua）。
- **没有 PipeWire。** 只有 PulseAudio 的系统未经测试，也不受支持。
- **没有 systemd。** 请按您的发行版的方式重启 WirePlumber，或注销后重新登录。

# 常见问题 {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber 还没有重启：`systemctl --user restart wireplumber.service`。
- **安装后没有声音。** 由于音箱输出的名称变了，默认输出转到了其他设备。请把 HECATE G2000 PRO 选为输出（如果使用 Easy Effects，也在其中选择）。
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
