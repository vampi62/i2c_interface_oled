#!/usr/bin/env python3
import smbus
import json
import subprocess
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

class lcd:
    def __init__(self, pcf_address, lcd_address, offset_y_display:list, encoding:str) -> None:
        self.bus=smbus.SMBus(1)
        self.bus.write_byte(pcf_address, 0xff)
        self.pcf_address = pcf_address
        self.lcd = {}
        self.lcd['address'] = lcd_address
        self.lcd['display'] = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.lcd['width'] = self.lcd['display'].width
        self.lcd['height'] = self.lcd['display'].height
        self.lcd['display'].begin()
        self.lcd['display'].clear()
        self.lcd['display'].display()
        self.lcd['image'] = Image.new('1', (self.lcd['width'], self.lcd['height']))
        self.lcd['draw'] = ImageDraw.Draw(self.lcd['image'])
        self.lcd['font'] = ImageFont.load_default()
        self.lcd['offset_y_display'] = offset_y_display
        self.lcd['start_x_display'] = 0
        self.lcd['start_top_display'] = -2
        self.active_page = 0
        self.position = 0
        self.command_info_value = []
        self.command_info_txt = []
        self.encoding = encoding
        self.nav_histo = []
        self.nav = []
        self.page = []
        self.in_sleep = False
        self.key = 0
        self.custom_page = {}

    ## exec custom page
    def exec_custom(self,script:str) -> None:
        if self.custom_page.get(script) == None:
            return
        is_running = True
        custom_page = 0
        next_custom_page = 0
        while is_running:
            if next_custom_page != 0:
                custom_page = next_custom_page
                next_custom_page = 0
            if self.custom_page[script][custom_page] == None:
                return
            self.lcd['draw'].rectangle((0,0,self.lcd['width'],self.lcd['height']), outline=0, fill=0)
            self.lcd['draw'].text((self.lcd['start_x_display'], self.lcd['start_top_display'] + self.lcd['offset_y_display'][0]),  str(" " + self.custom_page[script][custom_page]['nav']),  font=self.lcd['font'], fill=255)
            if self.custom_page[script][custom_page].get('txt') != None:
                for x in range(0, min(len(self.custom_page[script][custom_page]['txt']), 3)):
                    self.lcd['draw'].text((self.lcd['start_x_display'], self.lcd['start_top_display'] + self.lcd['offset_y_display'][x+1]),  " " + self.custom_page[script][custom_page]['txt'][x],  font=self.lcd['font'], fill=255)
            self.lcd['display'].image(self.lcd['image'])
            self.lcd['display'].display()
            if self.custom_page[script][custom_page].get('command') != None:
                if self.custom_page[script][custom_page]['command'].get('cmd') != None:
                    if self.custom_page[script][custom_page]['command'].get('cwd') != None:
                        value = self.process_exec(self.custom_page[script][custom_page]['command']['cmd'],self.custom_page[script][custom_page]['command']['cwd'])
                    else:
                        value = self.process_exec(self.custom_page[script][custom_page]['command']['cmd'])
                    if self.custom_page[script][custom_page]['command']["result"].get(value):
                        next_custom_page = self.custom_page[script][custom_page]['command']["result"][value]
            if self.custom_page[script][custom_page].get('wait') != None:
                time.sleep(self.custom_page[script][custom_page]['wait'])
            if self.custom_page[script][custom_page].get('goto') != None and next_custom_page == 0:
                next_custom_page = self.custom_page[script][custom_page]['goto']
            if self.custom_page[script][custom_page].get('exit') != None:
                is_running = False

    ## exec command
    def process_exec(self,command:str,cwd:str=None) -> str:
        try:
            if cwd != None:
                returncommand = subprocess.check_output(command, cwd=cwd, shell = True)
            else:
                returncommand = subprocess.check_output(command, shell = True, timeout = 2 )
            if returncommand == b'':
                returncommand = "N/A"
            returncommand = str(returncommand.decode(self.encoding))
        except:
            returncommand = "N/A"
        return returncommand

    ## change page
    def page_change(self,sens:bool):
        if sens: # right button
            if self.page[self.active_page][self.position].get('actionCommande') != None:
                self.action()
            if self.page[self.active_page][self.position].get('destinationPage') != None:
                self.nav_histo.append([self.active_page,self.position])
                tmp_page = self.active_page
                self.active_page = self.page[tmp_page][self.position]['destinationPage']
                if self.page[tmp_page][self.position].get('destinationPosition') != None:
                    self.position = self.page[tmp_page][self.position]['destinationPosition']
                else:
                    self.position = 0
        else: # left button
            if len(self.nav_histo) > 0:
                page_return = [self.nav_histo[len(self.nav_histo)-1][0],self.nav_histo[len(self.nav_histo)-1][1]]
                del self.nav_histo[len(self.nav_histo)-1]
                self.active_page = page_return[0]
                self.position = page_return[1]
        self.command_info_value = []
        self.command_info_txt = []
        for x in range(0, len(self.page[self.active_page])):
            self.command_info_value.append("")
            self.command_info_txt.append("")
        self.get_command()

    ## exec action command
    def action(self) -> None:
        if self.page[self.active_page][self.position]['actionCommande'].get('customPage'):
            self.exec_custom(self.page[self.active_page][self.position]['actionCommande'].get('customPage'))
        else:
            if self.page[self.active_page][self.position]['actionCommande'].get('ifResult') != None:
                for x in range(0, len(self.page[self.active_page][self.position]['actionCommande']['ifResult'])):
                    if self.page[self.active_page][self.position]['actionCommande']['ifResult'][x][0] == self.command_info_value[self.position] or x == len(self.page[self.active_page][self.position]['actionCommande']['ifResult'])-1:
                        self.process_exec(self.page[self.active_page][self.position]['actionCommande']['commande'] + self.page[self.active_page][self.position]['actionCommande']['ifResult'][x][1])
                        break
            else:
                self.process_exec(self.page[self.active_page][self.position]['actionCommande']['commande'])
        self.get_command()
        self.print_page()

    ## show page
    def print_page(self) -> None:
        if self.in_sleep:
            return
        self.lcd['draw'].rectangle((0,0,self.lcd['width'],self.lcd['height']), outline=0, fill=0)
        self.lcd['draw'].text((self.lcd['start_x_display'], self.lcd['start_top_display'] + self.lcd['offset_y_display'][0]),  str(" " + self.nav[self.active_page]),  font=self.lcd['font'], fill=255)
        offset_select = self.get_offset(self.position)
        for x in range(0, 3):
            if x+offset_select < len(self.page[self.active_page]):
                if x+offset_select == self.position:
                    selection_x = "*"
                else:
                    selection_x = " "
                self.lcd['draw'].text((self.lcd['start_x_display'], self.lcd['start_top_display'] + self.lcd['offset_y_display'][x+1]),  selection_x + " " + self.page[self.active_page][x+offset_select]['txt'] + self.command_info_txt[x+offset_select],  font=self.lcd['font'], fill=255)
        self.lcd['display'].image(self.lcd['image'])
        self.lcd['display'].display()

    ## offset pointer
    def get_offset(self,x:int) -> int:
        if x > 2:
            return x-2
        else:
            return 0

    ## exec info command
    def get_command(self) -> None:
        if self.in_sleep:
            return
        for x in range(0, len(self.page[self.active_page])):
            self.command_info_value.append("")
            self.command_info_txt.append("")
        for x in range(0, len(self.page[self.active_page])):
            if self.page[self.active_page][x].get('infoCommande') != None:
                self.command_info_value[x] = self.process_exec(self.page[self.active_page][x]['infoCommande']['commande'])
                if self.command_info_value[x] == "N/A":
                    self.command_info_txt[x] = "N/A"
                    continue
                if self.page[self.active_page][x]['infoCommande'].get('type') != None:
                    if self.page[self.active_page][x]['infoCommande']['type'] == "json":
                        try:
                            self.command_info_value[x] = json.loads(self.command_info_value[x])[self.page[self.active_page][x]['infoCommande']['tag']]
                        except:
                            self.command_info_value[x] = "N/A - json"
                            self.command_info_txt[x] = "N/A - json"
                            continue
                self.command_info_value[x] = str(self.command_info_value[x])
                if self.page[self.active_page][x]['infoCommande'].get('txtResultLiteral') != None:
                    valFound = False
                    for y in range(0, len(self.page[self.active_page][x]['infoCommande']['txtResultLiteral'])):
                        if self.page[self.active_page][x]['infoCommande']['txtResultLiteral'][y][0] == self.command_info_value[x]:
                            self.command_info_txt[x] = self.page[self.active_page][x]['infoCommande']['txtResultLiteral'][y][1]
                            valFound = True
                            break
                    if not valFound:
                        self.command_info_txt[x] = self.command_info_value[x]
                else:
                    self.command_info_txt[x] = self.command_info_value[x]
                if self.page[self.active_page][x]['infoCommande'].get('suffixe') != None:
                    self.command_info_txt[x] += self.page[self.active_page][x]['infoCommande'].get('suffixe')

    ## load page
    def init_page(self,page:list,nav:list,custom_page:dict) -> None:
        self.nav = nav
        self.page = page
        self.custom_page = custom_page
        self.get_command()
        self.print_page()

    ## sleep screen
    def sleep_screen(self) -> None:
        self.in_sleep = True
        self.lcd['display'].clear()
        self.lcd['display'].display()

    ## read button
    def read_pin_pcf(self) -> None: # return True if a key is pressed
        pins = self.bus.read_byte(self.pcf_address)
        if (pins & 0x08) == 0: # top
            if self.key == 1:
                return
            if self.in_sleep:
                self.in_sleep = False
                self.key = 1
                return
            if self.position > 0:
                self.position -= 1
            self.key = 1
            return
        if (pins & 0x02) == 0: # right
            if self.key == 2:
                return
            if self.in_sleep:
                self.in_sleep = False
                self.key = 2
                return
            self.page_change(True)
            self.key = 2
            return
        if (pins & 0x04) == 0: # left
            if self.key == 3:
                return
            if self.in_sleep:
                self.in_sleep = False
                self.key = 3
                return
            self.page_change(False)
            self.key = 3
            return
        if (pins & 0x01) == 0: # bottom
            if self.key == 4:
                return
            if self.in_sleep:
                self.in_sleep = False
                self.key = 4
                return
            if self.position < len(self.page[self.active_page])-1:
                self.position += 1
            self.key = 4
            return
        self.key = 0
        return
    #    if (pins & 0x10) == 0:
    #    if (pins & 0x20) == 0:
    #    if (pins & 0x40) == 0:
    #    if (pins & 0x80) == 0: