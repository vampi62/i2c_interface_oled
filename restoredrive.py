#!/usr/bin/env python3
import subprocess
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

top_display = -2
x_display = 0
offset_y_display = [0,9,17,25]

draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x_display, top_display + offset_y_display[0]),  str(" - message - "),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[1]),  str("compilation driver"),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[3]),  str("  0%"),  font=font, fill=255)
disp.image(image)
disp.display()

returncommand = subprocess.check_output('sudo dkms add .', cwd="/home/vampilab/rtl8192eu-linux-driver/", shell = True)
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x_display, top_display + offset_y_display[0]),  str(" - message - "),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[1]),  str("installation driver"),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[3]),  str(" 50%"),  font=font, fill=255)
disp.image(image)
disp.display()

returncommand = subprocess.check_output('sudo dkms install rtl8192eu/1.0', cwd="/home/vampilab/rtl8192eu-linux-driver/", shell = True)
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x_display, top_display + offset_y_display[0]),  str(" - message - "),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[1]),  str("installation terminer"),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[3]),  str("100%"),  font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(5)