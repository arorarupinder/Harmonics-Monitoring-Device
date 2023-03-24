
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
import re

#import RPi.GPIO as GPIO
# I2C variables
i2c = machine.I2C(id=0, scl=machine.Pin(21), sda=machine.Pin(20))

# Screen Variables
width = 128
height = 64
line = 1 
highlight = 1
shift = 0
list_length = 0
total_lines = 6

# create the display
#oled = SSD1306_I2C(width=width, height=height, i2c=i2c)

oled = SSD1306_I2C(width=128, height=64, i2c=i2c)
oled.init_display()
#rotary
button_pin = Pin(11, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(10, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(9, Pin.IN, Pin.PULL_UP)

#using 4N33 for Alarm block
#set up GPIO
led_pin = machine.Pin(16, machine.Pin.OUT)

# for tracking the direction and button state
previous_value = True
button_down = False
#UART read from peripherals
com1 = Easy_comms(0,9600)
com2 = Easy_comms(1,9600)
led = Pin(25, Pin.OUT)
counter = 0

def i_fund_val(i1):
    return i1

def thd_fft_calc(received_data):
    # find highest value in 0-18
    i_fund = max(received_data[0:19])
    # find highest value in 18-36
    i3 = max(received_data[19:37])
    # find highest value in 36-45
    i5 = max(received_data[37:46])
    # find highest value in 54-63
    i7 = max(received_data[54:64])

    # calculate THD from FFT input
    thd_fft = np.sqrt((i3**2) + (i5**2) + (i7**2)) / (i_fund**2)
    
    #function for storing i fund value
    #call function for storing i_fund
    i_fund_val(i_fund)
    print("this is the fundamental val getting passed1", i_fund)

    print("Phase A THD: ", thd_fft, "%")
    return thd_fft


# flags to keep track of whether data has been received
data4_received = False
data2_received = False

while True:
    '''
    # read from com1
    if not data4_received:
        slave_id, received_data = com1.read()
        if received_data is not None and slave_id == 1:
            print("adctimer3 data:", end=" ")
            for value in received_data:
                print(value, end=" ")
            print()  # print a newline character to separate the output for each received message
            # toggle led for 5sec      
            led.value(1)
            sleep(5)
            led.value(0)
            sleep(5)
            counter += 1
            data4_received = True  # Set the flag
'''            
    # read from com2
    if not data2_received:
        slave_id, received_data = com2.read()
        if received_data is not None and slave_id == 2:
            print("adctimer2 data:", end=" ")
            for value in received_data:
                print(value, end=" ")
            print()  # print a newline character to separate the output for each received message
            # toggle led for 5sec      
            led.value(1)
            sleep(5)
            led.value(0)
            sleep(5)
            counter += 1
            data2_received = True  # Set the flag
            
            # call thd_fft_calc() function here
            thd_fft = thd_fft_calc(received_data)
            
            #print("Phase A THD :", thd_fft, "%")
            

            
    if data2_received:       
    #if data4_received and data2_received:
        break  # Exit the loop if both messages have been received

'''
# flags to keep track of whether data has been received
#data5_received = False
data4_received = False
data2_received = False
received_data = []  # define received_data before the slave_id if blocks
while True:
    # read from com1
    if not data4_received:
        data4 = com1.read()
        #print("data4:", data4) 
        if data4 is not None:
            #print("data4:",data4)
            slave_id, received_data = data4
            #print("received_data1:",received_data)
            if slave_id == 1:
                data4_received = True             
               # print("received_data1:",received_data)
            
    if data4_received:
        
        print("adctimer3 data:", end=" ")
        for value in received_data:
            print(value, end=" ")
        print()  # print a newline character to separate the output for each received message
        # toggle led for 5sec      
        led.value(1)
        sleep(5)
        led.value(0)
        sleep(5)
        counter += 1
        data4_received = False  # Reset the flag
        
    # read from com2
    if not data2_received:
        data2 = com2.read()
        if data2 is not None:
            slave_id, received_data = data2
            if slave_id == 2:
                data2_received = True
                
    

    if data2_received: 
        print("adctimer2 data:", end=" ")
        for value in received_data:
            print(value, end=" ")
        print()  # print a newline character to separate the output for each received message
        # toggle led for 5sec      
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
   
'''


def get_file():
    """FUNCTION DEFINED BUT NOT BEING UTILIZE"""
    """ Get a specific Python file in the root folder of the Pico """
    
    files = listdir() #getting files in the directory
      
    test_file = [] #creating an empty array
    for file in files: #each element in array files
        if file.startswith("test1"): #checking if file ends w py
            test_file.append(file) #if yes add file to menu array
    
    file=open("test1.py", "r") #reading outputting contents of file 
    f=file.read() 
    print(f)
            
    return(test_file) #return menu containing values
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
    
    
    
def set_val(threshold):
    
    global options
    # clear the screen
    oled.fill_rect(0,0,width,height,0)
    oled.text("Threshold set to", 1, 10)
    oled.text(threshold,1, 20)
    oled.show()
    sleep(2)
    show_menu(options)
    
    
def thd_thresh_calc(i_thresh):
    #assuming
    i_fund1 = i_fund_val():
    
    print("this is the fundamental val getting passed2", i_fund1)
    

    #converting string to int
    i_thresh_search = re.search(r"\d+(\.\d+)?", i_thresh)
    i_thresh_val = i_thresh_search.group(0)
    print(i_thresh_val)
    

    #calculating thd from client input
    thd_thresh_client = np.sqrt(int(i_thresh_val) ** 2)/(i_fund1**2)
    print("This is the calculated thd from client in", thd_thresh_client)
    return thd_thresh_client


def compare_thd(thd_thresh): #this function compares the thd from fft v thd from client input
    #calling function for calculating thd w fft input
    thd_fft = thd_fft_calc(received_data)
   
    if thd_fft > thd_thresh: #print if startement is true
        print("Incoming thd greater than threshold")
        # Turn on LED
        led_pin.value(1)
        
    else: #print otherwise
        print("Current below threshold")
        # Turn off LED
        led_pin.value(0)
        
        


#generates current threshold for client to choose from 
options =[]
i=0

while i<100:
    options.append(f"{i}A")
    i+=1
        
print(options)
show_menu(options) #showing list generated on display



t_button = time.ticks_ms()

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
        
        #print("turn time", t_turn)
        
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
        
        
        # Reset t_button timer
        t_button = time.ticks_ms()
        print("Threshold set")

    # Debounce button
    if button_pin.value() == True and button_down:
        button_down = False

    
    

    
    # Check t_button timer
    t_incr = time.ticks_ms()
    t_diff = t_incr - t_button
    
    
    if t_diff >= 2000:
        
        # Reset t_button timer
        t_button = time.ticks_ms()
        #sleep(1)
        
        # clear the screen
        oled.fill_rect(0,0,width,height,0)
        oled.text("Phase A harmonics", 1, 10)
        #oled.text(threshold,1, 20)
        oled.show()
