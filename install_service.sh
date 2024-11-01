#!/bin/sh

repertoire_script=$(dirname "$(readlink -f "$0")")

service_file="/etc/systemd/system/i2cpythonlcd.service"
echo "[Unit]
Description=ecran oled en i2c

[Service]
Type=simple
WorkingDirectory=$repertoire_script
ExecStart=python main.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target" | sudo tee $service_file

sudo systemctl daemon-reload

sudo systemctl enable i2cpythonlcd

sudo systemctl start i2cpythonlcd

sudo systemctl status i2cpythonlcd