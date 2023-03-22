'''
import board
import digitalio

dirPin = digitalio.DigitalInOut(board.GP16) #define gpio
stepPin = digitalio.DigitalInOut(board.GP17) #define gpio
dirPin.direction = digitalio.Direction.INPUT #define as input pin
stepPin.direction = digitalio.Direction.INPUT #define as input pin

dirPin.pull = digitalio.Pull.UP
stepPin.pull = digitalio.Pull.UP
previousValue = True
while 1 == 1:
    if previousValue != stepPin.value:
        if stepPin.value == False:
            if dirPin.value == False:
                print("To the left, to the left!")
            else:
                print("To the right, to the right!")
        previousValue = stepPin.value
'''

from machine import Pin


#had re-wire pins as previously used pins used for comm between pico to pico
button_pin = Pin(20, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(21, Pin.IN, Pin.PULL_UP) #help identify which direction the knob is being turned in
step_pin = Pin(22, Pin.IN, Pin.PULL_UP) #help identify which direction the knob is being turned in




previous_value = True
button_down = False #part of debouncing

while True:
    if previous_value != step_pin.value():    
        if step_pin.value() == False:
            if direction_pin.value() == False:
                print("turn left")
            else:
                print("turn right")
        previous_value = step_pin.value()
    if button_pin.value() == False and not button_down:
        print ("button pushed")
        button_down = True
    if button_pin.value() == True and button_down:

        
