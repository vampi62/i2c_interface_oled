# i2c_interface_oled

## Description

Interface via un écran OLED et boutons de navigation pour un Raspberry en n'utilisant que le port I2C. Les pages sont paramétrées dans le fichier `config_lcd.py`. Créez une page ou ajoutez une section en suivant les instructions ci-dessous.

## Installation

Clonez le projet dans le dossier `/opt/` :

```bash
cd /opt
git clone https://github.com/vampi62/i2c_interface_oled.git
sudo chmod 755 -R /opt/i2c_interface_oled
sudo chown root:root -R /opt/i2c_interface_oled
```

Lancez le script d'installation :

```bash
sudo ./install_service.sh
```

Un fichier `uninstall_service.sh` est disponible pour supprimer le service si vous le souhaitez.

## Documentation pour l'édition du fichier config

### Ajouter une nouvelle page

Pour ajouter une nouvelle page, suivez ces étapes :

1. Définissez une nouvelle liste vide pour la page, par exemple `pX = []`, où `X` est le numéro de la page.
2. Ajoutez des composants à la nouvelle liste `pX`. Chaque composant est représenté par un dictionnaire avec le format suivant :

```python
pX.append({
    'txt': 'prise_1 :',
    'destinationPage': 1,
    'infoCommande': {
        'commande': 'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1',
        'tag': 'state_l1',
        'type': 'json',
        'txtResultLiteral': [['1', 'ON'], ['0', 'OFF']],
        'suffixe': ' °C'
    },
    'actionCommande': {
        'commande': 'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ',
        'ifResult': [['OFF', '"{ \\"state_l1\\": \\"ON\\" }"'], ['ON', '"{ \\"state_l1\\": \\"OFF\\" }"']]
    }
})
```

Seul le champ `"txt"` est obligatoire, les autres peuvent être laissés absents en fonction de votre besoin.

- `txt` : le texte à afficher pour le composant.
- `destinationPage` : le numéro de la page vers laquelle le composant doit naviguer lorsqu'il est cliqué.
- `infoCommande` : la commande qui récupère les données du capteur.
  - `commande` : la commande à exécuter pour récupérer les données du capteur (obligatoire pour `infoCommande`).
  - `type` : le type de données à traiter (`'json'` seul type disponible pour le moment).
  - `tag` : le tag à rechercher dans la sortie JSON de la commande (champ obligatoire si `type` : `'json'`).
  - `txtResultLiteral` : une liste de listes qui contient les valeurs à afficher pour chaque résultat possible. Si non présent ou aucune valeur ne correspond, alors la valeur retournée par la commande est affichée telle quelle.
    - Par exemple, si la commande renvoie 0 ou 1, vous pouvez définir `txtResultLiteral` comme `[['0', 'OFF'], ['1', 'ON']]` pour afficher `OFF` lorsque la commande renvoie 0 et `ON` lorsque la commande renvoie 1.
  - `suffixe` : le suffixe à ajouter à la valeur récupérée.
- `actionCommande` : la commande à exécuter lorsque le composant est cliqué.
  - `commande` : la commande à exécuter (obligatoire pour `actionCommande`).
  - `ifResult` : une liste de listes qui contient les valeurs à comparer avec le résultat de la commande `infoCommande`. Si le résultat de la commande `infoCommande` correspond à l'une des valeurs de la liste en position `[0]`, alors la commande sera exécutée avec l'argument en position `[1]`. Si aucune valeur ne correspond, alors le dernier paramètre dans la liste sera envoyé.
    - Par exemple, si la commande `infoCommande` renvoie 0 ou 1, vous pouvez définir `ifResult` comme `[['0', '"{ \\"state_l1\\": \\"ON\\" }"'], ['1', '"{ \\"state_l1\\": \\"OFF\\" }"']]` pour exécuter la commande avec l'argument `"{ \\"state_l1\\": \\"ON\\" }"` lorsque la commande `infoCommande` renvoie 0 et avec l'argument `"{ \\"state_l1\\": \\"OFF\\" }"` lorsque la commande `infoCommande` renvoie 1.

3. Une fois que la nouvelle page `pX` est définie avec tous ses composants, ajoutez-la à la liste `page` : `page.append(pX)`.
4. N'oubliez pas d'ajouter le lien de navigation dans la liste `nav` : `nav.append("menu/Yname")` où `Yname` est le nom de la page.

## Matériel

- 1 - PCB (schéma disponible en ressources)
- 1 - 3D (fichier STL disponible en ressources)
- 1 - écran OLED I2C 128 x 64 Pixel 0.96 Pouce, SSD1306 ([amazon : lot de 5](https://www.amazon.fr/gp/product/B08FD643VZ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- 1 - PCF8574T ([amazon : lot de 5](https://www.amazon.fr/5-pi%C3%A8ces-PCF8574T-PCF8574-SOP16/dp/B0BFX2DV8R/ref=sr_1_11?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=37VWEWKKIXPDK&keywords=PCF8574T&qid=1669558592&qu=eyJxc2MiOiIyLjUyIiwicXNhIjoiMi4wNCIsInFzcCI6IjEuODQifQ%3D%3D&sprefix=pcf8574t%2Caps%2C56&sr=8-11))
- 6 - résistances SMD 1K Ohm
- 4 - boutons poussoirs SMT
- 2 - connecteurs 4*1 pin dupont

## Ressources

- PCB : https://oshwlab.com/vadidi62/pi_oled__display
- STL : https://www.thingiverse.com/thing:5661212
- STL compatible : https://www.thingiverse.com/thing:4249203
- Script Python : https://github.com/vampi62/i2c_interface_oled

## Images d'exemple d'affichage

![gestion](https://github.com/vampi62/i2c_interface_oled/assets/104321401/cf43119e-e68e-4253-b3ea-c2c7cc74781a)
![menu](https://github.com/vampi62/i2c_interface_oled/assets/104321401/4cc85f9a-1c58-44fa-a93d-17ebc9c95dcb)
![ip](https://github.com/vampi62/i2c_interface_oled/assets/104321401/e961bb2d-ff13-4272-8741-93fe7bb70591)
