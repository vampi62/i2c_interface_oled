#!/usr/bin/env python3
#sudo pip install pyudev
#sudo pip install Adafruit_SSD1306
#sudo pip install Adafruit_GPIO
#sudo pip install smbus2
#sudo pip install pi-ina219
#sudo apt install mosquitto-clients

import smbus
import time
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

## ------ custom ------ ##

def custom_index(active,position):
    if page[active][position][3][3][0] == 'mqtt':
        return mqtt(page[active][position][3][0],page[active][position][3][3][1],page[active][position][3][3][2])

def mqtt(mqtt_command,mqtt_type,mqtt_recherche):
    returncommand = subprocess.check_output(mqtt_command, shell = True )
    returncommand = returncommand.decode(encoding)
    off = returncommand.find(mqtt_recherche)
    if mqtt_type == "prise":
        if returncommand[off+11] == "O" and returncommand[off+12] == "N":
            return "1"
        elif returncommand[off+11] == "O" and returncommand[off+12] == "F":
            return "0"
        else:
            return "inconnue"
    elif mqtt_type == "temp" or mqtt_type == "humi":
        if mqtt_type == "temp":
            off += 13
        elif mqtt_type == "humi":
            off += 10
        temp = ""
        for a in range(15):
            if returncommand[off+a] == ",":
                break
            temp += returncommand[off+a]
        if mqtt_type == "temp":
            temp += "°C"
        elif mqtt_type == "humi":
            temp += " %"
        return temp

## -- ne rien changer apres cette ligne, l'ajout de fonction doit se faire dans la section au dessus et l'ajout de page ou d'action dans le fichier config_lcd.py -- ##

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
printmeno = []
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

## ------ code generic ------ ## 

## gestion des pages
def pagechange(sens,active,position):
    if sens:
        if page[active][position][2]:
            if page[active][position][4][0] != '':
                action(active,position,True)
            nav_histo.append([active,position])
            return page[active][position][1],0
        else:
            action(active,position,True)
            return active,position
    else:
        if len(nav_histo) > 0:
            page_return = [nav_histo[len(nav_histo)-1][0],nav_histo[len(nav_histo)-1][1]]
            del nav_histo[len(nav_histo)-1]
            return page_return[0],page_return[1]
        else:
            return active,position

## convertie la sortie binaire d'une commande en texte pret definie
def conversion_return(active,position,returncommand):
    if returncommand == "0":
        return page[active][position][3][1]
    elif returncommand == "1":
        return page[active][position][3][2]
    else:
        return returncommand

## execution command des boutons
def action(active,position,typeact):
    if not typeact: ## info
        if page[active][position][2]:
            return page[active][position][0]
        else:
            if page[active][position][1] == 2:
                if not page[active][position][3][3][0] == '': # si custom function
                    returncommand = custom_index(active,position)
                else:
                    returncommand = subprocess.check_output(page[active][position][3][0], shell = True )
                    returncommand = returncommand.decode(encoding)
                returncommand = conversion_return(active,position,returncommand)
                return page[active][position][0] + str(returncommand)
            elif page[active][position][1] == 3:
                if not page[active][position][3][3][0] == '': # si custom function
                    returncommand = custom_index(active,position)
                else:
                    returncommand = subprocess.check_output(page[active][position][3][0], shell = True )
                    returncommand = returncommand.decode(encoding)
                returncommand = conversion_return(active,position,returncommand)
                return page[active][position][0] + str(returncommand)
            else:
                return page[active][position][0]
    else: ## buton
        if page[active][position][1] == 1:
            returncommand = subprocess.check_output(page[active][position][4][0], shell = True )
           # return page[active][position][0] + str(returncommand)
        if page[active][position][1] == 3:
            returncommand = action(active,position,False)
            if returncommand == page[active][position][0] + page[active][position][3][2]:
                returncommand = subprocess.check_output(page[active][position][4][0] + page[active][position][4][1], shell = True )
            elif returncommand == page[active][position][0] + page[active][position][3][1]:
                returncommand = subprocess.check_output(page[active][position][4][0] + page[active][position][4][2], shell = True )
            getcommand()
            printpage()
           # return page[active][position][0] + str(returncommand)

def printpage():
    global veillescreen
    global printmeno
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
                draw.text((x_display, top_display + offset_y_display[x+1]),  selection_x + " " + printmeno[x+offset_select],  font=font, fill=255)
    disp.image(image)
    disp.display()

def get_offset(x):
    if x > 2:
        return x-2
    else:
        return 0

def getcommand():
    global printmeno
    printmeno = []
    for x in range(0, len(page[pageactive])):
        printmeno.append("")
    for x in range(0, len(page[pageactive])):
        printmeno[x] = action(pageactive,x,False)

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
