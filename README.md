# i2c_interface_oled

## description

script ecrit en python pour generer une interface via un écran oled et des boutons de navigation, pour un raspberry en n'utilisant que le port I2C.

les pages sont parametrer dans le fichier config_lcd.py, creer une page ou ajouter une section en suivant les instruction ci-dessous.

1 - si vous voulez creer une nouvelle page ajouter une nouvelle table:

* __p..numero de page = []__

* exemple : p5 = []

2 - ajouter un __page.append(p..numero de page)__  à la fin du script

3 - dans la table "nav" tout en bas du fichier config_lcd ajoutter un titre a cette page

4 - ajouter des infos

4.1 - le premier champs contient le nom qui sera afficher

4.2 - valuer bool true si le champs permet d'aller sur une autre page

4.3.1 - si true le champs suivant comptient la page de destination

4.3.2 - si false le champs suivant comptient le type de bouton - 1 = button, 2 = info, 3 = info+button

4.4.1 - tableau dont le premier champs comptient la commande qui sera effectuer regulièrement par la page

4.4.2 - le 2eme et 3eme champs contienne les texte afficher si le retour de la commande est compris entre 0 et 1

4.4.3 - le 4eme champs est une autre table qui doit être traité par une fonction custom que vous aurait integrer dans le code

4.5.1 - tableau dont le premier champs comptient la commande qui sera effectuer à l'appuie du bouton (si selectionner)

4.5.2 - le 2eme et 3eme champs contienne des parties qui seront ajouter à la commande en fonction du retour de la commande dans le champs 3 si le retour de la commande est compris entre 0 et 1 (si le bouton est sur le type 3)

p..numero de page.append(['nom',bool false si navigation ,nav_ou_commande,['command','affichage si 0','affichage si 1',['func custom','option1','option2']],['command_button','option1 si info=1','option2 si info=0']])

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

