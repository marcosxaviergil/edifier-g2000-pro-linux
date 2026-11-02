% Hecate G2000 PRO Volume — 설명서
% 목차

# 소개 {#introduction}

Hecate G2000 PRO Volume은 시스템 볼륨 조절이 USB 스피커 Edifier Hecate G2000 PRO의 하드웨어 볼륨을 바꾸도록 합니다. 소프트웨어로 소리를 줄이는 대신 스피커 자체의 ALSA 컨트롤(**PCM Playback Volume**)을 사용합니다.

- 스피커를 출력으로 쓰는 동안 소프트웨어 볼륨은 항상 100%로 유지됩니다. 볼륨 슬라이더, 볼륨 키, 시스템 음소거는 스피커의 하드웨어만 바꿉니다.
- 모든 데스크톱 환경(GNOME, KDE Plasma 등)과 모든 애플리케이션에서 동작합니다. 모두 PipeWire를 사용하기 때문입니다.
- G2000 PRO(USB `35bb:b065`)에만 적용됩니다. 다른 오디오 장치는 그대로입니다.
- 백그라운드에서 실행되는 프로그램은 없습니다. PipeWire와 WirePlumber 설정, 그리고 확인과 테스트를 위한 `hecate-g2000-pro-volume` 명령이 전부입니다.

# 요구 사항 {#requirements}

- PipeWire와 WirePlumber 0.5 이상이 있는 Linux. Debian 13(PipeWire 1.4.2, WirePlumber 0.5.8)에서 테스트했습니다. 버전 확인: `wireplumber --version`.
- `hecate-g2000-pro-volume` 명령을 위한 Python 3.11 이상.
- `wpctl`, `pw-cli`, `amixer` 명령(Debian과 Ubuntu: 패키지 `wireplumber`, `pipewire-bin`, `alsa-utils`).

# 설치 {#installation}

## Debian, Ubuntu 및 파생 배포판(.deb) {#install-deb}

1. 릴리스에서 `hecate-g2000-pro-volume_<버전>_all.deb`를 내려받습니다.
2. 의존 패키지도 함께 설치하는 apt로 설치합니다.

```
sudo apt install ./hecate-g2000-pro-volume_<버전>_all.deb
```

이 패키지는 컴퓨터의 모든 사용자를 위해 설정을 설치합니다.

## 기타 배포판(.tar.gz) {#install-tarball}

1. 릴리스에서 `hecate-g2000-pro-volume-<버전>.tar.gz`를 내려받습니다.
2. 압축을 풀고 root 없이 내 사용자용으로 설치합니다.

```
tar -xzf hecate-g2000-pro-volume-<버전>.tar.gz
cd hecate-g2000-pro-volume-<버전>
./hecate-g2000-pro-volume install
```

이름은 같고 내용이 다른 파일이 이미 있으면 그 파일은 그대로 두고, 설치는 메시지를 표시하며 멈춥니다. 교체하려면 `./hecate-g2000-pro-volume install --force`를 사용합니다.

## 설정 적용 {#apply}

1. WirePlumber를 다시 시작하거나, 로그아웃한 뒤 다시 로그인합니다.

```
systemctl --user restart wireplumber.service
```

2. 스피커가 디지털 프로필(IEC958)을 쓰고 있었다면 출력 이름이 바뀌고 기본 출력이 다른 장치로 넘어갈 수 있습니다. 소리 설정에서 **HECATE G2000 PRO**를 한 번 출력으로 선택하세요. Easy Effects를 쓴다면 그 출력도 스피커로 선택하세요.

![소리 설정: 출력으로 HECATE G2000 PRO 선택](configuracoes_som_saida.jpg)

# 사용 {#usage}

볼륨 슬라이더, 볼륨 키, 음소거를 평소처럼 사용하세요. 모든 변경은 스피커의 하드웨어 볼륨으로 바로 전달됩니다.

![HECATE G2000 PRO를 쓸 때의 시스템 볼륨 슬라이더](controle_volume_gnome.jpg)

## 설치 확인: status {#status}

```
hecate-g2000-pro-volume status
```

설정이 설치된 위치, WirePlumber가 설정을 불러왔는지, 활성 프로필, 시스템 볼륨, 스피커의 하드웨어 컨트롤, 소프트웨어 볼륨을 보여 줍니다. 아무것도 바꾸지 않습니다. 모두 정상이면 **Result: OK**로 끝나고, 그렇지 않으면 각 **Problem:** 줄이 해야 할 일을 알려 줍니다.

![터미널: hecate-g2000-pro-volume status](terminal_status.jpg)

## 스피커 테스트: diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

볼륨을 현재보다 낮게 세 단계로 내리고 음소거한 뒤, 하드웨어 컨트롤이 따라오는지와 소프트웨어 볼륨이 100%로 유지되는지 확인합니다. 마지막에 볼륨과 음소거를 원래대로 되돌립니다. 테스트 전보다 소리가 커지는 일은 없습니다. 각 확인 항목은 **PASS** 또는 **FAIL**로 표시됩니다.

![터미널: hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# 동작 방식 {#how-it-works}

- **전용 프로필 세트.** PipeWire의 기본 프로필 세트는 이 스피커에 디지털 프로필 IEC958도 제공하는데, 그 믹서 경로에는 볼륨 컨트롤이 없어서 모든 볼륨 조절이 소프트웨어로만 이루어집니다. 이 프로젝트의 설정은 아날로그 프로필만 제공하며, 그 경로는 스피커의 **PCM** 컨트롤을 볼륨과 음소거에 사용합니다.
- **저장된 프로필.** 예전에 저장된 IEC958 프로필은 더 이상 존재하지 않으므로 무시되고, WirePlumber가 알아서 아날로그 프로필을 선택합니다.
- **하드웨어만 사용.** 드라이버는 스피커 볼륨을 −28.37 dB에서 −0.94 dB로 보고합니다. 최댓값이 음수이므로 PipeWire는 이 데시벨 정보를 쓰지 않고, 하드웨어의 148단계(0~147)에만 볼륨을 적용하며 그 위에 소프트웨어 볼륨을 더하지 않습니다.
- **이 스피커에만 적용.** WirePlumber 규칙은 USB 장치 `35bb:b065`에만 적용됩니다.
- **파일.** .deb 패키지: `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf`와 `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. 사용자별 설치: 같은 이름으로 `~/.config/wireplumber/wireplumber.conf.d/`와 `~/.config/alsa-card-profile/mixer/profile-sets/`에 있습니다.

# 제한 사항 {#limitations}

- **스피커 버튼.** 스피커 자체의 볼륨 버튼과 조절기는 별도의 조절입니다. ALSA는 이를 볼 수 없고, 시스템 볼륨도 그 변화를 따라가지 않습니다.
- **볼륨 0%.** 하드웨어의 0단계에 해당합니다. 이 단계가 완전한 무음인지는 확인하지 않았습니다. 무음이 필요하면 음소거를 사용하세요.
- **디지털 출력.** 이 스피커에는 IEC958 프로필이 더 이상 나타나지 않습니다.
- **WirePlumber 0.4.** 지원하지 않습니다. 다른 설정 형식(Lua)을 사용하기 때문입니다.
- **PipeWire 없음.** PulseAudio만 있는 시스템은 테스트하지 않았으며 지원하지 않습니다.
- **systemd 없음.** 사용하는 배포판의 방법으로 WirePlumber를 다시 시작하거나, 로그아웃한 뒤 다시 로그인하세요.

# 자주 묻는 문제 {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber를 아직 다시 시작하지 않았습니다: `systemctl --user restart wireplumber.service`.
- **설치 후 소리가 나지 않음.** 스피커 출력의 이름이 바뀌어 기본 출력이 다른 장치로 넘어갔습니다. HECATE G2000 PRO를 출력으로 선택하세요(Easy Effects를 쓴다면 거기서도).
- **"PipeWire does not see the speaker."** USB 케이블과 스피커 전원이 켜져 있는지 확인하세요.
- **"wpctl is not installed"**(또는 `pw-cli`, `amixer`). 메시지에 나온 패키지를 설치하세요.
- **status에서 파일이 "different"로 표시됨.** 이름은 같고 내용이 다른 파일이 이미 있었습니다. 내용을 확인하고 교체해도 된다면 `hecate-g2000-pro-volume install --force`를 실행하세요.
- **diagnose가 FAIL을 표시함.** `hecate-g2000-pro-volume status`를 실행하고, 표시되는 **Problem:** 줄을 먼저 해결하세요.

# 제거 {#uninstall}

- .deb 패키지: `sudo apt remove hecate-g2000-pro-volume`
- 사용자별 설치: `./hecate-g2000-pro-volume uninstall`(내용이 다른 파일은 그대로 두며, `--force`를 쓰면 삭제합니다)

그다음 WirePlumber를 다시 시작하세요: `systemctl --user restart wireplumber.service`. 스피커는 PipeWire의 기본 동작으로 돌아갑니다.

# 개인정보 보호와 보안 {#privacy}

이 프로젝트는 개인 데이터를 수집, 저장, 전송하지 않으며 네트워크를 사용하지 않습니다. 명령은 `wpctl`, `pw-cli`, `amixer`로 오디오 상태를 읽기만 하고, `install`과 `uninstall`에서는 홈 폴더의 설정 파일 두 개를 쓰거나 지웁니다. `diagnose`는 몇 초 동안 볼륨을 바꾼 뒤 원래대로 되돌립니다. 자세한 내용은 프로젝트의 `docs/PRIVACIDADE.md`를 참고하세요.
