#!/usr/bin/env python3
PCF8574=0x20
offset_y_display = [0,9,17,25]
sleep_timer = 2000
encoding = 'utf-8'

import time
from config_lcd import page,nav
from lcd import lcd
from custom import custom

def run():
    screen1 = lcd(PCF8574,None,offset_y_display,encoding)
    previus_key = 0
    sleep_count = 0
    timer_auto_refresh = 0
    screen1.init_page(page,nav,custom)
    while 1:
        screen1.read_pin_pcf()
        if screen1.in_sleep: # if screen is in sleep mode
            time.sleep(0.1)
        else:
            if screen1.key != 0 and previus_key == 0: # if a button is pressed and no button was pressed before
                screen1.print_page()
                previus_key = screen1.key
                timer_auto_refresh = 0
                sleep_count = 0
            elif previus_key != 0 and screen1.key == 0: # if no button is pressed
                previus_key = 0
            if timer_auto_refresh > 150: # auto refresh
                screen1.get_command()
                screen1.print_page()
                timer_auto_refresh = 0
            if sleep_count > sleep_timer:
                screen1.sleep_screen()
                sleep_count = 0
            timer_auto_refresh +=1
            sleep_count += 1
            time.sleep(0.01)

if __name__ == '__main__':
    run()
