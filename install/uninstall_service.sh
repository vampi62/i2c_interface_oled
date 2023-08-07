#!/bin/sh
sudo systemctl stop i2cpythonlcd
sudo systemctl disable i2cpythonlcd
sudo rm /etc/systemd/system/i2cpythonlcd.service
sudo systemctl daemon-reload