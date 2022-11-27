#!/usr/bin/env python3
import subprocess
import smbus
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
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

DEVICE_BUS = 1
DEVICE_ADDR = 0x17
top_display = -2
x_display = 0
offset_y_display = [0,9,17,25]

draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x_display, top_display + offset_y_display[0]),  str(" - message - "),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[1]),  str("arret"),  font=font, fill=255)
draw.text((x_display, top_display + offset_y_display[2]),  str("en cours"),  font=font, fill=255)
disp.image(image)
disp.display()
bus = smbus.SMBus(DEVICE_BUS)
bus.write_byte_data(DEVICE_ADDR, 24,30)
returncommand = subprocess.check_output('sudo shutdown -h now', shell = True)