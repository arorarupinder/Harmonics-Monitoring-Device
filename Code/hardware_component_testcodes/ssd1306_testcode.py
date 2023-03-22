from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(21), sda = Pin(20), freq = 200000)
#for fast mode use 400000 (default), slow mode use 100000
#I2C(0) as default which loads GP8 and GP9

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0) #clear whatever on display
oled.text("Hello World", 0, 0)

oled.show()