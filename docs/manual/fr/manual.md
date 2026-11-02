% Hecate G2000 PRO Volume — Manuel
% Sommaire

# Introduction {#introduction}

Hecate G2000 PRO Volume fait en sorte que le réglage du volume du système change le volume de l'enceinte USB Edifier Hecate G2000 PRO elle-même, par son contrôle matériel (**PCM Playback Volume**), au lieu de baisser le son dans l'ordinateur.

Avec l'enceinte comme sortie :

- La barre de volume du système affiche et change le **volume de l'enceinte**.
- Les touches de volume du clavier et les boutons **+** et **−** de l'enceinte changent ce même volume, et la barre suit.
- La sourdine du système active et désactive la **sourdine de l'enceinte** (**PCM Playback Switch**).
- Le volume de l'ordinateur (logiciel) reste toujours à **100 %** et n'apparaît dans aucun réglage.
- Le volume de chaque application fonctionne comme d'habitude.

Seule la G2000 PRO (USB `35bb:b065`) est concernée ; les autres périphériques audio restent tels quels. Cela fonctionne avec n'importe quel bureau (GNOME, KDE Plasma et autres), car ils utilisent tous PipeWire. Aucun programme ne tourne en arrière-plan : ce sont deux fichiers de configuration de PipeWire et de WirePlumber, plus la commande `hecate-g2000-pro-volume` pour vérifier et tester.

# Prérequis {#requirements}

- Linux avec PipeWire et WirePlumber 0.5 ou plus récent. Pour voir la version : `wireplumber --version`.
- Python 3.11 ou plus récent, pour la commande `hecate-g2000-pro-volume`.
- Les commandes `wpctl`, `pw-cli` et `amixer` (Debian et Ubuntu : paquets `wireplumber`, `pipewire-bin` et `alsa-utils`). Le paquet .deb les installe déjà.
- L'enceinte reliée à l'ordinateur par le câble USB.

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

## Activer {#apply}

1. Redémarrez WirePlumber, ou fermez la session et rouvrez-la :

```
systemctl --user restart wireplumber.service
```

2. Dans les paramètres du son, choisissez **HECATE G2000 PRO** comme sortie. La sortie de l'enceinte devient la sortie stéréo analogique ; si elle était avant la sortie stéréo numérique (IEC958), la sortie par défaut a pu passer à un autre périphérique. Si vous utilisez Easy Effects, choisissez aussi l'enceinte comme sa sortie.
3. Vérifiez avec `hecate-g2000-pro-volume status` : le résultat doit être **Result: OK**.

![Paramètres du son : HECATE G2000 PRO comme sortie](configuracoes_som_saida.jpg)

# Utilisation {#usage}

## Volume et sourdine de l'enceinte {#volume}

Utilisez la barre de volume du système, les touches de volume du clavier ou les boutons **+** et **−** de l'enceinte. Tous changent le même volume : celui de l'enceinte. La barre affiche le volume de l'enceinte et suit chacun d'eux. La sourdine du système coupe le son dans l'enceinte.

![Barre de volume du système avec HECATE G2000 PRO](controle_volume_gnome.jpg)

## Volume de chaque application {#app-volume}

Dans le réglage du volume par application (dans les paramètres du son, ou dans des programmes comme pavucontrol), chaque application garde son propre volume, réglé dans l'ordinateur, comme d'habitude. Il s'ajoute au volume de l'enceinte.

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

Baisse le volume en trois étapes sous le volume actuel, active la sourdine et vérifie que le contrôle matériel suit et que le volume logiciel reste à 100 %. À la fin, remet le volume et la sourdine comme avant. Le son ne devient jamais plus fort qu'avant le test ; avec un volume inférieur à 5 %, le test demande de l'augmenter. Chaque vérification affiche **PASS** ou **FAIL**.

![Terminal : hecate-g2000-pro-volume diagnose](terminal_diagnose.jpg)

# Fonctionnement {#how-it-works}

- **Le contrôle de volume de l'enceinte.** Par USB, l'enceinte propose un contrôle de volume (gauche et droite) et une sourdine. Linux les affiche comme **PCM Playback Volume** et **PCM Playback Switch**.
- **Les boutons de l'enceinte.** L'enceinte se présente aussi à l'ordinateur comme un clavier multimédia (« HECATE G2000 PRO Consumer Control ») : les boutons **+** et **−** envoient les touches de volume. C'est pourquoi ils agissent exactement comme les touches de volume du clavier.
- **Profil analogique.** Le jeu de profils par défaut de PipeWire propose aussi pour l'enceinte le profil numérique IEC958, qui n'utilise pas son contrôle de volume : avec lui, le volume était baissé dans l'ordinateur. La configuration de ce projet ne propose que le profil analogique, qui utilise le contrôle **PCM** de l'enceinte pour le volume et la sourdine. Un profil IEC958 choisi auparavant est laissé de côté, et WirePlumber utilise seul le profil analogique.
- **Volume uniquement dans l'enceinte.** Le contrôle de l'enceinte a 148 crans (0 à 147), de −28,37 dB à −0,94 dB. PipeWire applique la barre de volume directement à ces crans, sans volume logiciel par-dessus.
- **Cette enceinte uniquement.** La règle de WirePlumber ne s'applique qu'au périphérique USB `35bb:b065`.
- **Fichiers.** Paquet .deb : `/usr/share/wireplumber/wireplumber.conf.d/60-edifier-hecate-g2000-pro.conf` et `/usr/share/alsa-card-profile/mixer/profile-sets/edifier-hecate-g2000-pro.conf`. Installation par utilisateur : les mêmes noms dans `~/.config/wireplumber/wireplumber.conf.d/` et `~/.config/alsa-card-profile/mixer/profile-sets/`.

# Problèmes courants {#troubleshooting}

- **"The configuration is installed but not loaded yet."** WirePlumber n'a pas encore été redémarré : `systemctl --user restart wireplumber.service`.
- **Pas de son après l'activation.** La sortie par défaut est passée à un autre périphérique. Choisissez HECATE G2000 PRO comme sortie (et dans Easy Effects, si vous l'utilisez).
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
