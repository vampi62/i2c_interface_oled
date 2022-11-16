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
from ina219 import INA219,DeviceRangeError
#from multiprocessing import Process
import pyudev

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
printmeno = ['','','']
tempo_actu_screen = 0
custom_return = ''
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

## ------ config ------ ##
# 0 = button, 1 = info, 2 = info+button
# format : ['name',page si nav_ou_commande=false ,nav_ou_commande,['command','affichage si 0','affichage si 1',['func custom','option1','option2']],['command_button','option1 si info=1','option2 si info=0']]

nav_histo = []
p0 = []
p1 = []
p2 = []
p3 = []
p4 = []
page = []

p0.append(['energie',1,True,['','','',['','','']],['','','','']])
p0.append(['gestion',2,True,['','','',['','','']],['','','','']])
p0.append(['resource',3,True,['','','',['','','']],['','','','']])
p0.append(['temperature',4,True,['','','',['','','']],['','','','']])

p1.append(['prise_1 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/multi_labo -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l1']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/multi_labo/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l1\\": \\"OFF\\" }\"','\"{ \\"state_l1\\": \\"ON\\" }\"','']])
p1.append(['prise_2 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/multi_labo -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l2']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/multi_labo/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l2\\": \\"OFF\\" }\"','\"{ \\"state_l2\\": \\"ON\\" }\"','']])
p1.append(['prise_3 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/multi_labo -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l3']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/multi_labo/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l3\\": \\"OFF\\" }\"','\"{ \\"state_l3\\": \\"ON\\" }\"','']])
p1.append(['prise_4 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/multi_labo -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l4']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/multi_labo/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l4\\": \\"OFF\\" }\"','\"{ \\"state_l4\\": \\"ON\\" }\"','']])
p1.append(['usb     :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/multi_labo -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l5']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/multi_labo/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l5\\": \\"OFF\\" }\"','\"{ \\"state_l5\\": \\"ON\\" }\"','']])

p2.append(['wifi driver',1,False,['','','',['','','']],['python restoredrive.py','','','']])
p2.append(['fsck sd',1,False,['','','',['','','']],['python repare.py','','','','']])
p2.append(['ping gateway',1,False,['','','',['','','']],['python ping.py','','','']])
p2.append(['redemarrage',1,False,['','','',['','','']],['python redemarrage.py','','','','']])
p2.append(['arret',1,False,['','','',['','','']],['python arret.py','','','','']])

p3.append(['IP   :',2,False,['hostname -I | cut -d\' \' -f1','','',['','','']],['','','','']])
p3.append(['TEMP :',2,False,['vcgencmd measure_temp | cut -b 6-12','','',['','','']],['','','','']])
p3.append(['CPU  :',2,False,["top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)*10}'",'','',['','','']],['','','','']])
p3.append(['RAM  :',2,False,["free -m | awk 'NR==2{printf \"%s/%sMB \", $3,$2 }'",'','',['','','']],['','','','']])
p3.append(['DISK :',2,False,["df -h | grep 'root' | awk '{print $3 \"/\" $2 \" \" $5}'",'','',['','','']],['','','','']])

p4.append(['TEMP :',2,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/temp_labo -u zigbee -P jee4mqt2sub -C 1','','',['mqtt','temp','temperature']],['','','','']])
p4.append(['HUMI :',2,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/temp_labo -u zigbee -P jee4mqt2sub -C 1','','',['mqtt','humi','humidity']],['','','','']])

page.append(p0)
page.append(p1)
page.append(p2)
page.append(p3)
page.append(p4)

nav = ["menu","menu/energie","menu/gestion","menu/resource","menu/temperature"]

## ------ code custom ------ ##
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

## ------ code generic ------ ## -- ne rien changer --

## gestion des pages
def pagechange(sens,active,position):
    if sens:
        if page[active][position][3]:
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
            returncommand = subprocess.check_output(page[active][position][3][0], shell = True )
           # return page[active][position][0] + str(returncommand)
        if page[active][position][1] == 3:
            returncommand = action(active,position,False)
            if returncommand == page[active][position][0] + page[active][position][3][2]:
                returncommand = subprocess.check_output(page[active][position][4][0] + page[active][position][4][1], shell = True )
            elif returncommand == page[active][position][0] + page[active][position][3][1]:
                returncommand = subprocess.check_output(page[active][position][4][0] + page[active][position][4][2], shell = True )
           # return page[active][position][0] + str(returncommand)

def printpage():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if veillescreen < veille_tempo:
        draw.text((x_display, top_display + offset_y_display[0]),  str(" " + nav[pageactive]),  font=font, fill=255)
        for x in range(0, 3):
            draw.text((x_display, top_display + offset_y_display[x+1]),  printmeno[x],  font=font, fill=255)
    disp.image(image)
    disp.display()

def getcommand():
    if position_x > 2:
        offset_select = position_x-2
    else:
        offset_select = 0
    for x in range(0, 3):
        printmeno[x] = ''
        if x+offset_select < len(page[pageactive]):
            if x+offset_select == position_x:
                selection_x = "*"
            else:
                selection_x = " "
            printmeno[x] = selection_x + " " + action(pageactive,offset_select+x,False)

def read_pin_pcf():
    pins = b.read_byte(PCF8574)
    if (pins & 0x08) == 0: # haut
        if anti_act == 0:
            anti_act = 10
            if veillescreen < veille_tempo:
                if position_x > 0:
                    position_x -= 1
            veillescreen = 0
            tempo_actu_screen = 0
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
            tempo_actu_screen = 0
    else:
        if anti_act == 13:
            anti_act = 0
    time.sleep(0.01)
#    if (pins & 0x10) == 0:
#    if (pins & 0x20) == 0:
#    if (pins & 0x40) == 0:
#    if (pins & 0x80) == 0:
def run():
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

if __name__ == '__main__':
    run()
