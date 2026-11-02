% Hecate G2000 PRO Volume — Manuel
% Sommaire

# Introduction {#introduction}

Hecate G2000 PRO Volume fait en sorte que le réglage du volume du système change le volume matériel de l'enceinte USB Edifier Hecate G2000 PRO, par le contrôle ALSA de l'enceinte elle-même (**PCM Playback Volume**), au lieu de baisser le son par logiciel.

- Avec l'enceinte comme sortie, le volume logiciel reste toujours à 100 % : le réglage du volume, les touches de volume et la sourdine du système ne changent que le matériel de l'enceinte.
- Cela fonctionne avec n'importe quel bureau (GNOME, KDE Plasma et autres) et avec toutes les applications, car elles utilisent toutes PipeWire.
- Seule la G2000 PRO (USB `35bb:b065`) est concernée. Les autres périphériques audio restent tels quels.
- Aucun programme ne tourne en arrière-plan : la solution est une configuration de PipeWire et de WirePlumber, plus la commande `hecate-g2000-pro-volume` pour la vérifier et la tester.

# Prérequis {#requirements}

- Linux avec PipeWire et WirePlumber 0.5 ou plus récent. Testé sous Debian 13 (PipeWire 1.4.2, WirePlumber 0.5.8). Pour voir la version : `wireplumber --version`.
- Python 3.11 ou plus récent, pour la commande `hecate-g2000-pro-volume`.
- Les commandes `wpctl`, `pw-cli` et `amixer` (Debian et Ubuntu : paquets `wireplumber`, `pipewire-bin` et `alsa-utils`).

# Installation {#installation}

## Debian, Ubuntu et dérivées (.deb) {#install-deb}

1. Téléchargez `hecate-g2000-pro-volume_<version>_all.deb` depuis la release.
2. Installez-le avec apt, qui installe aussi les dépendances :

```
sudo apt install ./hecate-g2000-pro-volume_<version>_all.deb
```

Le paquet installe la configuration pour tous les utilisateurs de l'ordinateur.

## Autres distributions (.tar.gz) {#install-tarball}

1. Téléchargez `hecate-g2000-pro-volume-<version>.tar.gz` depuis la release.
2. Extrayez-le et installez-le pour votre utilisateur, sans root :

```
tar -xzf hecate-g2000-pro-volume-<version>.tar.gz
cd hecate-g2000-pro-volume-<version>
./hecate-g2000-pro-volume install
```

Si un fichier du même nom avec un autre contenu existe déjà, il est conservé et l'installation s'arrête avec un message. Pour le remplacer, utilisez `./hecate-g2000-pro-volume install --force`.

## Appliquer la configuration {#apply}

1. Redémarrez WirePlumber, ou fermez la session et rouvrez-la :

```
systemctl --user restart wireplumber.service
```

2. Si l'enceinte était sur le profil numérique (IEC958), sa sortie change de nom et la sortie par défaut peut passer à un autre périphérique. Choisissez **HECATE G2000 PRO** une fois comme sortie dans les paramètres du son. Si vous utilisez Easy Effects, choisissez aussi l'enceinte comme sa sortie.

![Paramètres du son : HECATE G2000 PRO comme sortie](configuracoes_som_saida.jpg)

# Utilisation {#usage}

Utilisez le réglage du volume, les touches de volume et la sourdine comme d'habitude. Chaque changement va directement au volume matériel de l'enceinte.

![Réglage du volume du système avec HECATE G2000 PRO](controle_volume_gnome.jpg)

## Vérifier l'installation : status {#status}

```
hecate-g2000-pro-volume status
```

Affiche où la configuration est installée, si WirePlumber l'a chargée, le profil actif, le volume du système, les contrôles matériels de l'enceinte et le volume logiciel. Ne change rien. Se termine par **Result: OK** quand tout est correct ; sinon, chaque ligne **Problem:** indique quoi faire.

![Terminal : hecate-g2000-pro-volume status](terminal_status.jpg)

## Tester l'enceinte : diagnose {#diagnose}

```
hecate-g2000-pro-volume diagnose
```

Baisse le volume en trois étapes sous le volume actuel, active la sourdine et vérifie que le contrôle matériel suit et que le volume logiciel reste à 100 %. À la fin, remet le volume et la sourdine comme avant. Le son ne devient jamais plus fort qu'avant le test. Chaque vérification affiche **PASS** ou **FAIL**.

![Terminal : hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Fonctionnement {#how-it-works}

- **Jeu de profils propre.** Le jeu de profils par défaut de PipeWire propose aussi pour l'enceinte le profil numérique IEC958, dont le chemin de mixage n'a pas de contrôle de volume : avec lui, tout réglage du volume est purement logiciel. La configuration de ce projet ne propose que le profil analogique, dont le chemin utilise le contrôle **PCM** de l'enceinte pour le volume et la sourdine.
- **Profil enregistré.** Un profil IEC958 enregistré auparavant est ignoré, car il n'existe plus ; WirePlumber choisit seul le profil analogique.
- **Matériel uniquement.** Le pilote indique le volume de l'enceinte de −28,37 dB à −0,94 dB. Comme le maximum est négatif, PipeWire écarte cette information en décibels et applique le volume uniquement aux 148 crans matériels (0 à 147), sans volume logiciel par-dessus.
- **Cette enceinte uniquement.** La règle de WirePlumber ne s'applique qu'au périphérique USB `35bb:b065`.
- **Fichiers.** Paquet .deb : `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` et `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installation par utilisateur : les mêmes noms dans `~/.config/wireplumber/wireplumber.conf.d/` et `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Limitations {#limitations}

- **Boutons de l'enceinte.** Le bouton et le réglage de volume de l'enceinte elle-même sont un réglage séparé : ALSA ne les voit pas, et le volume du système ne suit pas ce qu'ils font.
- **Volume 0 %.** Correspond au cran 0 du matériel. Il n'a pas été vérifié si ce cran est un silence total ; pour le silence, utilisez la sourdine.
- **Sortie numérique.** Le profil IEC958 n'apparaît plus pour cette enceinte.
- **WirePlumber 0.4.** Non pris en charge : il utilise un autre format de configuration (Lua).
- **Sans PipeWire.** Les systèmes avec PulseAudio seul n'ont pas été testés et ne sont pas pris en charge.
- **Sans systemd.** Redémarrez WirePlumber comme le prévoit votre distribution, ou fermez la session et rouvrez-la.

# Problèmes courants {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber n'a pas encore été redémarré : `systemctl --user restart wireplumber.service`.
- **Pas de son après l'installation.** La sortie par défaut est passée à un autre périphérique, car le nom de la sortie de l'enceinte a changé. Choisissez HECATE G2000 PRO comme sortie (et dans Easy Effects, si vous l'utilisez).
- **"PipeWire does not see the speaker."** Vérifiez le câble USB et que l'enceinte est allumée.
- **"wpctl is not installed"** (ou `pw-cli`, `amixer`). Installez le paquet indiqué dans le message.
- **Un fichier apparaît comme "different" dans status.** Un fichier du même nom avec un autre contenu existait déjà. Vérifiez-le et, s'il peut être remplacé, lancez `hecate-g2000-pro-volume install --force`.
- **diagnose affiche FAIL.** Lancez `hecate-g2000-pro-volume status` et résolvez d'abord les lignes **Problem:** qu'il affiche.

# Désinstaller {#uninstall}

- Paquet .deb : `sudo apt remove hecate-g2000-pro-volume`
- Installation par utilisateur : `./hecate-g2000-pro-volume uninstall` (un fichier avec un autre contenu est conservé ; `--force` le supprime)

Ensuite, redémarrez WirePlumber : `systemctl --user restart wireplumber.service`. L'enceinte revient au comportement par défaut de PipeWire.

# Confidentialité et sécurité {#privacy}

Le projet ne collecte, n'enregistre et n'envoie aucune donnée personnelle, et n'utilise pas le réseau. La commande lit seulement l'état audio avec `wpctl`, `pw-cli` et `amixer` et, avec `install` et `uninstall`, écrit ou supprime les deux fichiers de configuration de votre dossier personnel. `diagnose` change le volume pendant quelques secondes puis le remet comme avant. Détails dans `docs/PRIVACIDADE.md` du projet.
