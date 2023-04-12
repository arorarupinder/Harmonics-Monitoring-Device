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

i_fund_A = 0
def i_fund_val_A(i_A):
    global i_fund_A
    i_fund_A = i_A
    
i_fund_B = 0
def i_fund_val_B(i_B):
    global i_fund_B
    i_fund_B = i_B
    
    

def thd_fft_calc_A(received_data_A):
    # find highest value in 0-18
    i_fund_A = max(received_data_A[0:19])
    # find highest value in 18-36
    i3 = max(received_data_A[19:37])
    # find highest value in 36-45
    i5 = max(received_data_A[37:46])
    # find highest value in 54-63
    i7 = max(received_data_A[54:64])

    # calculate THD from FFT input
    thd_fft_A = np.sqrt((i3**2) + (i5**2) + (i7**2)) / (i_fund_A)
    
    #function for storing i fund value
    #call function for storing i_fund
    i_fund_val_A(i_fund_A)
    

    print("Phase A THD: ", thd_fft_A, "%")
    return thd_fft_A

def thd_fft_calc_B(received_data_B):
    # find highest value in 0-18
    i_fund_B = max(received_data_B[0:19])
    # find highest value in 18-36
    i3 = max(received_data_B[19:37])
    # find highest value in 36-45
    i5 = max(received_data_B[37:46])
    # find highest value in 54-63
    i7 = max(received_data_B[54:64])

    # calculate THD from FFT input
    thd_fft_B = np.sqrt((i3**2) + (i5**2) + (i7**2)) / (i_fund_B)
    
    #function for storing i fund value
    #call function for storing i_fund
    i_fund_val_B(i_fund_B)
    

    print("Phase B THD: ", thd_fft_B, "%")
    return thd_fft_B


# flags to keep track of whether data has been received
data4_received = False
data2_received = False

while True:
    
    #Phase B
    # read from com0
    if not data4_received:
        slave_id, received_data_B = com1.read()
        if received_data_B is not None and slave_id == 1:
            print("Phase B:", end=" ")
            for i in range(min(len(received_data_B), 128)):
                print(received_data_B[i], end=" ")
            print()  # print a newline character to separate the output for each received message
            # toggle led for 5sec
            led.value(1)
            sleep(5)
            led.value(0)
            sleep(5)
            data4_received = True  # Set the flag
            
            # call thd_fft_calc() function here
            thd_fft_B = thd_fft_calc_B(received_data_B)

        
    #Phase A     
    # read from com1
    if not data2_received:
        slave_id, received_data_A = com2.read()
        if received_data_A is not None and slave_id == 2:
            print("Phase A:", end=" ")
            for i in range(min(len(received_data_A), 128)):
                print(received_data_A[i], end=" ")
            print()  # print a newline character to separate the output for each received message
            # toggle led for 5sec      
            led.value(1)
            sleep(5)
            led.value(0)
            sleep(5)
            
            data2_received = True  # Set the flag
            
            # call thd_fft_calc() function here
            thd_fft_A = thd_fft_calc_A(received_data_A)
            
            #print("Phase A THD :", thd_fft, "%")
            

            
    #if data2_received:       
    if data4_received and data2_received:
        break  # Exit the loop if both messages have been received


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
    
    
    
def set_val(threshold): #show selected value on display
    
    global options
    # clear the screen
    oled.fill_rect(0,0,width,height,0)
    oled.text("Threshold set to", 1, 10)
    oled.text(threshold,1, 20)
    oled.show()
    sleep(2)
    show_menu(options)
    
    
def thd_thresh_calc(i_thresh): #this function calculates thd from client input

    # call thd_fft_calc() function here
    #thd_fft = thd_fft_calc(received_data)

    #print("Phase A THD :", thd_fft, "%")
    print("Fundamental value A:", i_fund_A)
    
    #print("Phase B THD :", thd_fft, "%")
    print("Fundamental value B:", i_fund_B)

    #converting string to int
    i_thresh_search = re.search(r"\d+(\.\d+)?", i_thresh)
    i_thresh_val = i_thresh_search.group(0)
    print(i_thresh_val)
    
    #average i_fund
    i_fund_avg = (i_fund_A + i_fund_B)/2
    

    #calculating thd from client input
    thd_thresh_client = np.sqrt(int(i_thresh_val) ** 2)/(i_fund_avg)
    print("This is the calculated thd from client in", thd_thresh_client)
    return thd_thresh_client


def compare_thd(thd_thresh): #this function compares the thd from fft v thd from client input for Phase A and Phase B
    #calling function for calculating thd w fft input
    thd_fft_A = thd_fft_calc_A(received_data_A)
    
    #calling function for calculating thd w fft input
    thd_fft_B = thd_fft_calc_B(received_data_B)
    
   
    if thd_fft_A > thd_thresh: #print if startement is true
        if thd_fft_B > thd_thresh:
            print("Incoming thd greater than threshold")
            # Turn on LED
            led_pin.value(1)
        
        else: #print otherwise
            print("Current below threshold")
            # Turn off LED
            led_pin.value(0)
        
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
    
    
    if t_diff >= 2000: #show calculated Phase A and Phase B THD when no rotary activity
        
        # Reset t_button timer
        t_button = time.ticks_ms()
        #sleep(1)
        
        show_thd_val_A = thd_fft_calc_A(received_data_A)
        show_thd_val_str_A = str(show_thd_val_A)
        
        show_thd_val_B = thd_fft_calc_B(received_data_B)
        show_thd_val_str_B = str(show_thd_val_B)
        
        
        
        # clear the screen
        oled.fill_rect(0,0,width,height,0)
        oled.text("Phase A THD:", 1, 10)
        oled.text(show_thd_val_str_A,1, 20)
        oled.show()
        
        oled.text("Phase B THD:", 1, 30)
        oled.text(show_thd_val_str_B,1, 40)
        oled.show()

