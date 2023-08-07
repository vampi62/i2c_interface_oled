# i2c_interface_oled

## description

interface via un écran oled et boutons de navigation, pour un raspberry en n'utilisant que le port I2C.  

les pages sont paramétrer dans le fichier config_lcd.py, creer une page ou ajouter une section en suivant les instruction ci-dessous.  

## installation

cloner le projet dans le dossier /opt/  

```bash
cd /opt/
git clone https://github.com/vampi62/i2c_interface_oled.git
sudo chmod 755 -R /opt/i2c_interface_oled
sudo chown root:root -R /opt/i2c_interface_oled
```
lancer le script d'installation
```bash
cd install
sudo ./install_service.sh
```
un fichier uninstall_service.sh est disponible pour supprimer le service si vous le souhaitez.

## Documentation pour l'édition du fichier config  

### Ajouter une nouvelle page  
Pour ajouter une nouvelle page, suivez ces étapes :  

Définissez une nouvelle liste vide pour la page, par exemple pX = [], où X est le numéro de la page.  

### Ajoutez des composants à la nouvelle liste pX. Chaque composant est représenté par une liste avec le format suivant :  

pX.append(['text à afficher', numéro_de_page, nav_ou_commande, [commande_à_exécuter, affichage_si_0, affichage_si_1, [fonction_personnalisée, option1, option2]], [commande_si_bouton, option1_si_info_1, option2_si_info_0]])  
text à afficher : Remplacez par le texte à afficher pour le composant.  
numéro_de_page : si nav_ou_commande est True, remplacez par le numéro de la page vers laquelle le composant doit rediriger. Sinon, mettre de 1 à 3 selon le type de composant.(1 = button, 2 = info, 3 = info+button)  
nav_ou_commande : Mettez True si le composant est un élément de navigation, False si c'est un bouton, un capteur ou un interrupteur.  
commande_à_exécuter : Remplacez par la commande à exécuter si le composant est une commande.  
affichage_si_0 : Remplacez par le texte à afficher lorsque la commande retourne 0.  
affichage_si_1 : Remplacez par le texte à afficher lorsque la commande retourne 1.  
fonction_personnalisée : Remplacez par la fonction personnalisée à exécuter si le composant en possède une. (ex: mqtt)  
option1 et option2 : Remplacez par les options pour la fonction personnalisée, le cas échéant.  

Une fois que la nouvelle page pX est définie avec tous ses composants, ajoutez-la à la liste page : page.append(pX).  
n'oublier pas d'ajouter le lien de navigation dans la liste nav : nav.append("menu/Yname") où Yname est le nom de la page.  


### Ajouter une redirection  
Une redirection est obtenue en créant un composant qui dirige vers une autre page lorsqu'il est cliqué. Pour ajouter une redirection :

Créez un nouveau composant avec le nom souhaité et définissez numéro_de_page comme le numéro de la page cible.  
Mettez nav_ou_commande à True.  
Laissez les champs commande_à_exécuter et les autres vides.  



### Ajouter un bouton  
Pour ajouter un bouton :  

Créez un nouveau composant avec le nom souhaité.  
Mettez nav_ou_commande à False.  
Laissez les champs commande_à_exécuter et les autres vides.  
Définissez commande_si_bouton avec la commande à exécuter lorsque le bouton est cliqué.  



### Ajouter un capteur  
Pour ajouter un capteur :  

Créez un nouveau composant avec le nom souhaité.  
Mettez nav_ou_commande à False.  
Définissez commande_à_exécuter avec la commande qui récupère les données du capteur.  
Laissez les autres champs vides car ils seront utilisés pour afficher les données du capteur.  



### Ajouter un Interrupteur  
Pour ajouter un interrupteur avec une commande qui récupère une information, suivez ces étapes :  

Créez un nouveau composant avec le nom souhaité.  
Mettez nav_ou_commande à False.  
Définissez commande_à_exécuter avec la commande qui récupère l'information pour l'interrupteur (par exemple, l'état actuel de l'interrupteur).  
Laissez les autres champs vides, car ils seront utilisés pour afficher l'état de l'interrupteur.  
Définissez commande_si_bouton avec la commande à exécuter lorsque l'interrupteur est activé ou désactivé. Utilisez option1_si_info_1 pour l'action lorsque l'interrupteur est activé et option2_si_info_0 pour l'action lorsque l'interrupteur est désactivé.  

Exemple :  
Supposons que vous souhaitez ajouter un interrupteur pour contrôler une lampe. Voici comment procéder :  
Créez un nouveau composant pour l'interrupteur :  

['Lampe :', 3, False, ['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_lampe -u zigbee -P jee4mqt2sub -C 1', 'OFF', 'ON', ['mqtt', 'lampe', 'etat']], ['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_lampe/set -u zigbee -P jee4mqt2sub -m ', '{"etat": "OFF"}', '{"etat": "ON"}']]  
Le composant s'appelle "Lampe".  
Le numéro de page est 3, mais puisque nav_ou_commande est False, c'est le type de composant qui est détecté, donc 3 signifie que c'est un interrupteur.  
nav_ou_commande est False.  
La commande commande_à_exécuter est mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_lampe -u zigbee -P jee4mqt2sub -C 1, qui récupère l'état actuel de la lampe via MQTT.  
L'affichage lorsque l'interrupteur est désactivé est "OFF" (affichage_si_0).  
L'affichage lorsque l'interrupteur est activé est "ON" (affichage_si_1).  
La commande à exécuter lorsque l'interrupteur est activé est mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_lampe/set -u zigbee -P jee4mqt2sub -m {"etat": "ON"} (commande_si_bouton avec option1_si_info_1).  
La commande à exécuter lorsque l'interrupteur est désactivé est mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_lampe/set -u zigbee -P jee4mqt2sub -m {"etat": "OFF"} (commande_si_bouton avec option2_si_info_0).  
Exemple :  
Supposons que vous souhaitiez ajouter une nouvelle page appelée 'paramètres'. Voici comment procéder :  

Définissez une nouvelle liste pour la page : p5 = []  
Ajoutez des composants à la nouvelle page :  

p5.append(['Réglage 1 :', 2, False, ['commande', 'on', 'off', ['', '', '']], ['', '', '']])  
p5.append(['Réglage 2 :', 2, False, ['commande', 'actif', 'inactif', ['', '', '']], ['', '', '']])  
Ajoutez la nouvelle page à la liste page : page.append(p5)  
Ajoutez un nouveau lien de navigation à la liste nav : nav.append("menu/paramètres")  
N'oubliez pas de remplacer 'commande', 'Réglage 1', 'Réglage 2' et les autres espaces réservés par de véritables commandes et des noms appropriés pour vos nouveaux composants.  

p..numerodepage.append(['nom',bool false si navigation ,nav_ou_commande,['command','affichage si 0','affichage si 1',['func custom','option1','option2']],['command_button','option1 si info=1','option2 si info=0']])  


## materiel

* 1 - PCB (schema disponible en ressources)

* 1 - 3D (fichier STL disponible en ressources)

* 1 - écran OLED I2C 128 x 64 Pixel 0.96 Pouce, SSD1306

[amazon : lot de 5](https://www.amazon.fr/gp/product/B08FD643VZ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

* 1 - PCF8574T

[amazon : lot de 5](https://www.amazon.fr/5-pi%C3%A8ces-PCF8574T-PCF8574-SOP16/dp/B0BFX2DV8R/ref=sr_1_11?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=37VWEWKKIXPDK&keywords=PCF8574T&qid=1669558592&qu=eyJxc2MiOiIyLjUyIiwicXNhIjoiMi4wNCIsInFzcCI6IjEuODQifQ%3D%3D&sprefix=pcf8574t%2Caps%2C56&sr=8-11)

* 6 - resistance SMD 1K Ohm

* 4 - bouton poussoir SMT

* 2 - 4*1 connecteur pin dupont

## ressources

PCB : https://oshwlab.com/vadidi62/pi_oled__display

STL : https://www.thingiverse.com/thing:5661212

STL compatible : https://www.thingiverse.com/thing:4249203

script PYTHON : https://github.com/vampi62/i2c_interface_oled

## image exemple d'affichage
![gestion](https://github.com/vampi62/i2c_interface_oled/assets/104321401/cf43119e-e68e-4253-b3ea-c2c7cc74781a)
![menu](https://github.com/vampi62/i2c_interface_oled/assets/104321401/4cc85f9a-1c58-44fa-a93d-17ebc9c95dcb)
![ip](https://github.com/vampi62/i2c_interface_oled/assets/104321401/e961bb2d-ff13-4272-8741-93fe7bb70591)

