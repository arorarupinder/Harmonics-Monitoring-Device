
from machine import Pin, I2C, ADC, Timer
from os import listdir
from ssd1306 import SSD1306_I2C
from time import sleep
from ulab import numpy as np
import re
import RPi.GPIO as GPIO
import time


###Self notes:####
#try and accept 
#10 arrays (colums)
#do average and plot



#from test1 import show_threshold

# I2C variables
i2c = machine.I2C(id=1, scl=machine.Pin(15), sda=machine.Pin(14))

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

# Setup the Rotary Encoder
'''
button_pin = Pin(19, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(18, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(22, Pin.IN, Pin.PULL_UP)
'''

#using 4N33 for Alarm block
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)

button_pin = Pin(22, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(21, Pin.IN, Pin.PULL_UP)
step_pin  = Pin(20, Pin.IN, Pin.PULL_UP)

#using 4N33 for Alarm block
#pin = machine.Pin(16, machine.Pin.OUT)

# for tracking the direction and button state
previous_value = True
button_down = False



def get_file():
    """FUNCTION DEFINED BUT NOT BEING UTILIZE"""
    """ Get a specific Python file in the root folder of the Pico """
    
    files = listdir() #getting files in the directory
      
    test_file = [] #creating an empty array
    for file in files: #each element in array files
        if file.endswith("txt"): #checking if file ends w py
            test_file.append(file) #if yes add file to menu array
    
    #file=open("fft.txt", "r") #reading outputting contents of file 
    #f=file.read() 
    #print(f)
            
    #file.seek(5)
    #val=file.read(20 - 5)
    #print("This is the value in txt file", val)
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
    sleep(3)
    
    ##retrieved_file = get_file() #calling another function for getting test file in the directory
    ##print(retrieved_file)
    
    #converting list to string
    ##str_retrieved_file = "{}".format(retrieved_file[0])
    ##print(str_retrieved_file)
    
    
    #call function from test1 file and give it a value
    #show_threshold(threshold)
    ##exec(open(str_retrieved_file).read()) #have to get the file
    
    
    show_menu(options)

    
   
def thd_fft_calc():
    #hardcoded value from tge fft function
    i_fund=60.99953
    i2=40.21981
    i3=35.98355
    i4=25.9734
    i5=34.9257
    i6=52.90605
    i7=73.43269
    
    #calculating thd from fft input
    thd_fft=np.sqrt((i2**2)+(i3**2)+(i4**2)+(i5**2)+(i6**2)+(i7**2))/(i_fund**2)
    print("This is the calculated threshold from fft in", thd_fft)
    #This is the calculated threshold from client in 0.03064008
    return thd_fft
  

def thd_thresh_calc(i_thresh):
    #assuming
    i_fund=60.99953

    #converting string to int
    i_thresh_search = re.search(r"\d+(\.\d+)?", i_thresh)
    i_thresh_val = i_thresh_search.group(0)
    print(i_thresh_val)
    

    #calculating thd from client input
    thd_thresh_client = np.sqrt(int(i_thresh_val) ** 2)/(i_fund**2)
    print("This is the calculated thd from client in", thd_thresh_client)
    return thd_thresh_client


def compare_thd(thd_thresh): #this function compares the thd from fft v thd from client input
    #calling function for calculating thd w fft input
    thd_fft = thd_fft_calc()
   
    if thd_fft > thd_thresh: #print if startement is true
        print("Incoming current greater than threshold")
        GPIO.output(7,True)
        time.sleep(1)
        GPIO.output(7,False)
        time.sleep(1)
        
    else: #print otherwise
        print("Current below threshold")
        GPIO.output(7,False)
        
        


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
