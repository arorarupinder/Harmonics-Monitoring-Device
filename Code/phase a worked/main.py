
# uart central & rotary_display integrated
from easy_comms import Easy_comms
from ulab import numpy as np
from machine import Pin, I2C, ADC, Timer
from os import listdir
from ssd1306 import SSD1306_I2C
from time import sleep
import time
import machine
import struct
import math




def thd_fft_calc(received_data):
    i_fund = received_data[1]
    i_harmonics = received_data[2:]

    # calculate THD from FFT input
    thd_fft = math.sqrt(sum([n**2 for n in i_harmonics]) - i_fund**2) / i_fund
    
    return thd_fft

#import RPi.GPIO as GPIO

#UART read from peripherals
com1 = Easy_comms(0,9600)
com2 = Easy_comms(1,9600)
led = Pin(25, Pin.OUT)
counter = 0


# flags to keep track of whether data has been received
#data5_received = False
#data4_received = False
data2_received = False

while True:

    # read from com2
    if not data2_received:
        data2 = com2.read()
        if data2 is not None:
            slave_id, received_data = data2
            if slave_id == 2:
                data2_received = True
              
# Inside the main while loop

    if data2_received:  # Moved this block outside the if statement
        print("adctimer2 data:", end=" ")
        for value in received_data:
            print(value, end=" ")
        print()  # print a newline character to separate the output for each received message
        # toggle led for 15sec
        
        

        led.value(1)
        sleep(5)
        led.value(0)
        sleep(5)
        counter += 1
        data2_received = False  # Reset the flag
        
        # call thd_fft_calc() function here
        thd_fft = thd_fft_calc(received_data)
        print("Phase A THD :", thd_fft, "%")

    if counter >= 1:
        break
   

def thd_thresh_calc(received_data):
    #fundamental from fft input
    i_fund=received_data[1]

    #converting string to int
    i_thresh_search = re.search(r"\d+(\.\d+)?", i_thresh)
    i_thresh_val = i_thresh_search.group(0)
    print(i_thresh_val)
    

    #calculating thd from client input
    thd_thresh_client = np.sqrt(int(i_thresh_val) ** 2)/(i_fund**2)
    print("This is the calculated thd from client in", thd_thresh_client)
    return thd_thresh_client


def compare_thd(thd_thresh):
    #calling function for calculating thd w fft input
    thd_fft = thd_fft_calc()
   
    if thd_fft > thd_thresh:
        print("Incoming current greater than threshold")
        GPIO.output(7,True)
        time.sleep(1)
        GPIO.output(7,False)
        time.sleep(1)
        
    else:
        print("Current below threshold")
        GPIO.output(7,False)
#alarm      
'''
## I2C variables
i2c = machine.I2C(id=1, scl=machine.Pin(15), sda=machine.Pin(14))

# Screen Variables
width = 128
height = 64
line = 1 
highlight = 1
shift = 0
list_length = 0
total_lines = 6

oled = SSD1306_I2C(width, height, i2c)

#rotart setup
button_pin = Pin(22, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(21, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(20, Pin.IN, Pin.PULL_UP)

#using 4N33 for Alarm block
#pin = machine.Pin(16, machine.Pin.OUT)

# for tracking the direction and button state
previous_value = True
button_down = False






def show_menu(menu):
    """ Shows the menu on the screen"""
      
    # bring in the global variables
    global line, highlight, shift, list_length #no longer local variables but global

    # menu variables
    item = 1
    line = 1
    line_height = 10
    

    # clear the display
    oled.fill_rect(0,0,width,height,0) #highligting the display

    #oled.text("Set threshold:", 0, 5)

    # Shift the list of files so that it shows on the display
    list_length = len(menu)
    short_list = menu[shift:shift+total_lines]

    for item in short_list:
        if highlight == line:
            oled.fill_rect(0,(line-1)*line_height, width,line_height,1)
            oled.text(">",0, (line-1)*line_height,0)
            oled.text(item, 10, (line-1)*line_height,0)
            oled.show()
        else:
            oled.text(item, 10, (line-1)*line_height,1)
            oled.show()
        line += 1 
    oled.show()


    
    
    show_menu(options)
'''
        
'''   
#try and accept 



#generates current threshold for client to choose from 
options =[]
i=0

while i<100:
    options.append(f"{i}A")
    i+=1
        
print(options)
show_menu(options) #showing list generated on display
get_file()

       





# Repeat forever
while True:
    if previous_value != step_pin.value():
        if step_pin.value() == False:

            # Turned Left 
            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1  
                else:
                    if shift > 0:
                        shift -= 1  

            # Turned Right
            else:
                if highlight < total_lines:
                    highlight += 1
                else: 
                    if shift+total_lines < list_length:
                        shift += 1

        
        show_menu(options)
        previous_value = step_pin.value()   
        
    # Check for button pressed
    if button_pin.value() == False and not button_down:
        button_down = True
        
        print("Threshold set")
        
        set_val(options[(highlight-1) + shift]) #highlight and shift is a global variable
        client_thresh= options[(highlight-1) + shift]
        print("chosen val...", options[(highlight-1) + shift])
        
        #calling function for calculating the thd w client input
        thd_thresh = thd_thresh_calc(client_thresh)
        
        #calling compare function to pass the thd calculated from client
        compare_thd(thd_thresh)

        
      

    # Decbounce button
    if button_pin.value() == True and button_down:
        button_down = False
      
'''

