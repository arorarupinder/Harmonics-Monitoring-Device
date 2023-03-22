'''
from machine import Pin, Timer
led = Pin(25, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=4, mode=Timer.PERIODIC, callback=blink)

from machine import Pin
led = Pin(25, Pin.OUT)
led.value(1)
'''

'''

#required libraries
#from ulab import numpy as np
import machine
import utime
 
#initialize peripherals
analog_value = machine.ADC(28) #defining ADC input at pin28
 
#main application loop
while True: #infinite loop
    reading = analog_value.read_u16()     #reading ADC val
    print(reading) #print value to shell monitor
#    utime.sleep(0.2) #reading inteval of 200 microseconds

'''


#@micropython.native
#takes script parses and runs in virtual machine
#substitute bite code w machine instructions, alot faster, getting the sample time we care about
#t=660Hz
import machine
import utime
 
analog_value = machine.ADC(27) #defining ADC input at pin28
conversion_factor = 3.3/ (65535) #conversion factor which is dividing the max input voltage with max sample rate

while True: #infinite loop
    reading = analog_value.read_u16()     #reading ADC val
    print(reading * conversion_factor) #print value to shell monitor
    #utime.sleep(0.2)




'''
from ulab import numpy as np
import sys
import utime
#from easy_comms import Easy_comms
from time import sleep
from machine import Pin
#import json

#@micropython.native
def read_adc28(): #30mVp signal conditioning input
    # initialize the ADC
    adc = machine.ADC(28)

    # set the number of samples to be taken
    adc_values = np.zeros(1024)
    
    # Calculate the time between samples
    sample_time = 1 / 1080

    #read ADC and store them in an array
    for i in range(1024):
        adc_values[i] = adc.read_u16()
        #1080 samples per second 
        utime.sleep(sample_time)
        
    return adc_values

def read_adc27(): #15mVp signal conditioning input
    # initialize the ADC
    adc = machine.ADC(27)

    # set the number of samples to be taken
    adc_values = np.zeros(1024)
    
    # Calculate the time between samples
    sample_time = 1 / 1080

    #read ADC and store them in an array
    for i in range(1024):
        adc_values[i] = adc.read_u16()
        #1080 samples per second 
        utime.sleep(sample_time)
        
    return adc_values

def read_adc26(): #5mVp signal conditioning input
    # initialize the ADC
    adc = machine.ADC(26)

    # set the number of samples to be taken
    adc_values = np.zeros(1024)
    
    # Calculate the time between samples
    sample_time = 1 / 1080

    #read ADC and store them in an array
    for i in range(1024):
        adc_values[i] = adc.read_u16()
        #1080 samples per second 
        utime.sleep(sample_time)
        
    return adc_values

adc_values = read_adc28()
print(adc_values)
'''