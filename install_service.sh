#!/bin/sh

# Chemin complet vers le fichier Python # repertoire du fichier bash
repertoire_script=$(dirname "$(readlink -f "$0")")

# Créer le fichier de service
service_file="/etc/systemd/system/i2cpythonlcd.service"
echo "[Unit]
Description=ecran oled en i2c

[Service]
Type=simple
WorkingDirectory=$repertoire_script
ExecStart=python lcd.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target" | sudo tee $service_file

# Charger le service
sudo systemctl daemon-reload

# Activer le service pour qu'il démarre au démarrage du système
sudo systemctl enable i2cpythonlcd

# Démarrer le service
sudo systemctl start i2cpythonlcd

# Vérifier le statut du service
sudo systemctl status i2cpythonlcd