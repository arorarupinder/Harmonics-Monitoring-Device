from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
from rotary_display import new_threshold

i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))

oled = SSD1306_I2C(width=128, height=64, i2c=i2c)

#def show_threshold(val):
oled.init_display()
oled.text("The set threshold is:", new_threshold,1,1)
oled.show()
sleep(1)
