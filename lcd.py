#!/usr/bin/env python3
#sudo pip install pyudev
#sudo pip install Adafruit_SSD1306
#sudo pip install Adafruit_GPIO
#sudo pip install smbus2
#sudo pip install pi-ina219
#sudo apt install mosquitto-clients

import smbus
import time
import json
import subprocess
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#from ina219 import INA219,DeviceRangeError
#from multiprocessing import Process
#import pyudev

## ------ config ------ ##
from config_lcd import page,nav

## ------ init var ------ ##
encoding = 'utf-8'
RST = None
PCF8574=0x20
pageactive = 0
position_x = 0
top_display = -2
x_display = 0
offset_y_display = [0,9,17,25]
anti_act = 0
veillescreen = 0
veille_tempo = 2000
command_info_value = []
command_info_txt = []
tempo_actu_screen = 0
custom_return = ''
move = False
nav_histo = []
## ------ init lib ------ ##

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
b=smbus.SMBus(1)
b.write_byte(PCF8574, 0xff)

disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def process_exec(command):
    try:
        returncommand = subprocess.check_output(command, shell = True, timeout = 2 )
        if returncommand == b'':
            returncommand = "N/A"
        returncommand = returncommand.decode(encoding)
    except:
        returncommand = "N/A"
    return returncommand

## gestion des pages
def pagechange(sens,active,position):
    if sens:
        if page[active][position].get('actionCommande') != None:
            action(active,position)
        if page[active][position].get('destinationPage') != None:
            nav_histo.append([active,position])
            return page[active][position]['destinationPage'],0
        return active,position
    else: # retour
        if len(nav_histo) > 0:
            page_return = [nav_histo[len(nav_histo)-1][0],nav_histo[len(nav_histo)-1][1]]
            del nav_histo[len(nav_histo)-1]
            return page_return[0],page_return[1]
        else:
            return active,position

## execution command des boutons
def action(active,position):
    if page[active][position]['actionCommande'].get('ifResult') != None:
        for x in range(0, len(page[active][position]['actionCommande']['ifResult'])):
            if page[active][position]['actionCommande']['ifResult'][x][0] == command_info_value[position] or x == len(page[active][position]['actionCommande']['ifResult'])-1:
                process_exec(page[active][position]['actionCommande']['commande'] + page[active][position]['actionCommande']['ifResult'][x][1])
                break
    else:
        process_exec(page[active][position]['actionCommande']['commande'])
    getcommand()
    printpage()

## affichage de la page
def printpage():
    global veillescreen
    global command_info_value
    global command_info_txt
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if veillescreen < veille_tempo:
        draw.text((x_display, top_display + offset_y_display[0]),  str(" " + nav[pageactive]),  font=font, fill=255)
        offset_select = get_offset(position_x)
        for x in range(0, 3):
            if x+offset_select < len(page[pageactive]):
                if x+offset_select == position_x:
                    selection_x = "*"
                else:
                    selection_x = " "
                draw.text((x_display, top_display + offset_y_display[x+1]),  selection_x + " " + page[pageactive][x+offset_select]['txt'] + command_info_txt[x+offset_select],  font=font, fill=255)
    disp.image(image)
    disp.display()

## offset selecteur
def get_offset(x):
    if x > 2:
        return x-2
    else:
        return 0


## recuperation des commandes info
def getcommand():
    global command_info_value
    global command_info_txt
    command_info_value = []
    command_info_txt = []
    for x in range(0, len(page[pageactive])):
        command_info_value.append("")
        command_info_txt.append("")
    for x in range(0, len(page[pageactive])):
        if page[pageactive][x].get('infoCommande') != None:
            command_info_value[x] = process_exec(page[pageactive][x]['infoCommande']['commande'])
            if command_info_value[x] == "N/A":
                command_info_txt[x] = "N/A"
                continue
            if page[pageactive][x]['infoCommande'].get('type') != None:
                if page[pageactive][x]['infoCommande']['type'] == "json":
                    try:
                        command_info_value[x] = json.loads(command_info_value[x])[page[pageactive][x]['infoCommande']['tag']]
                    except:
                        command_info_value[x] = "N/A - json"
                        command_info_txt[x] = "N/A - json"
                        continue
            command_info_value[x] = str(command_info_value[x])
            if page[pageactive][x]['infoCommande'].get('txtResultLiteral') != None:
                valFound = False
                for y in range(0, len(page[pageactive][x]['infoCommande']['txtResultLiteral'])):
                    if page[pageactive][x]['infoCommande']['txtResultLiteral'][y][0] == command_info_value[x]:
                        command_info_txt[x] = page[pageactive][x]['infoCommande']['txtResultLiteral'][y][1]
                        valFound = True
                        break
                if not valFound:
                    command_info_txt[x] = command_info_value[x]
            else:
                command_info_txt[x] = command_info_value[x]
            if page[pageactive][x]['infoCommande'].get('suffixe') != None:
                command_info_txt[x] += page[pageactive][x]['infoCommande'].get('suffixe')
                

## lecture des boutons
def read_pin_pcf():
    global anti_act
    global move
    global veillescreen
    global tempo_actu_screen
    global position_x
    global pageactive
    pins = b.read_byte(PCF8574)
    if (pins & 0x08) == 0: # haut
        if anti_act == 0:
            anti_act = 10
            if veillescreen < veille_tempo:
                if position_x > 0:
                    position_x -= 1
            veillescreen = 0
            move = True
    else:
        if anti_act == 10:
            anti_act = 0
    if (pins & 0x02) == 0: # droite
        if anti_act == 0:
            anti_act = 11
            if veillescreen < veille_tempo:
                pageactive,position_x = pagechange(True,pageactive,position_x)
            veillescreen = 0
            tempo_actu_screen = 0
    else:
        if anti_act == 11:
            anti_act = 0
    if (pins & 0x04) == 0: # gauche
        if anti_act == 0:
            anti_act = 12
            if veillescreen < veille_tempo:
                pageactive,position_x = pagechange(False,pageactive,position_x)
            veillescreen = 0
            tempo_actu_screen = 0
    else:
        if anti_act == 12:
            anti_act = 0
    if (pins & 0x01) == 0: # bas
        if anti_act == 0:
            anti_act = 13
            if veillescreen < veille_tempo:
                if position_x < len(page[pageactive])-1:
                    position_x += 1
            veillescreen = 0
            move = True
    else:
        if anti_act == 13:
            anti_act = 0
    time.sleep(0.01)
#    if (pins & 0x10) == 0:
#    if (pins & 0x20) == 0:
#    if (pins & 0x40) == 0:
#    if (pins & 0x80) == 0:
def run():
    global anti_act
    global move
    global veillescreen
    global tempo_actu_screen
    while 1:
        read_pin_pcf()
        if tempo_actu_screen == 0:
            getcommand()
            printpage()
            tempo_actu_screen +=1
        elif tempo_actu_screen > 150:
            tempo_actu_screen = 0
        else:
            tempo_actu_screen +=1
            veillescreen += 1
        if move:
            printpage()
            move = False

if __name__ == '__main__':
    run()
