#ADCtimer_best gain_FFT : Phase1
from easy_comms import Easy_comms
from ulab import numpy as np
import utime
from machine import Pin
from time import sleep
from machine import Timer
import sys
import math
import struct

# Initialize the ADC and timer
adc = machine.ADC(28)
#adc1 = machine.ADC(27)
#adc2 = machine.ADC(26)
tim = Timer(-1)

# Initialize the counter 
count = 0

# Set the size of the array to store the ADC values
ARRAY_SIZE = 128
adc_values = np.zeros(ARRAY_SIZE, dtype=np.uint16)
#adc1_values = np.zeros(ARRAY_SIZE, dtype=np.uint16)
#adc2_values = np.zeros(ARRAY_SIZE, dtype=np.uint16)

#function decorator
@micropython.native

# Define a function to read the ADC value
def read_adc(timer):
    # Check if we've read 1024 values
    global count
    if count >= ARRAY_SIZE:
        # Stop the timer and return
        tim.deinit()
        return
    
    # Increment the counter
    count += 1
    
    # Trigger the ADC conversion and read the value
    value = adc.read_u16()
    #value1 = adc1.read_u16()
    #value2 = adc2.read_u16()
    
    # Store the value in the array
    adc_values[count-1] = value
    #adc1_values[count-1] = value1
    #adc2_values[count-1] = value2
    
    
        
# Set the timer to trigger the read_adc function every 1 second
tim.init(freq=1280, mode=machine.Timer.PERIODIC, callback=read_adc)

# Wait for the timer to finish
while count < ARRAY_SIZE:
    pass


print(adc_values)
#print(adc1_values)
#print(adc2_values)

'''
# Define a function to find the highest samples and count their occurrences
def find_highest_samples(adc_values, adc1_values, adc2_values):
    # Find the five highest samples
    highest_samples = np.sort(adc_values)[-5:]
    highest_samples1 = np.sort(adc1_values)[-5:]
    highest_samples2 = np.sort(adc2_values)[-5:]
    
    # Count the number of occurrences of each highest sample
    occurrences = [np.sum(adc_values == sample) for sample in highest_samples]
    occurrences1 = [np.sum(adc1_values == sample) for sample in highest_samples1]
    occurrences2 = [np.sum(adc2_values == sample) for sample in highest_samples2]
    
     # Choose the highest sample out of the three arrays with the highest occurrence
    max_occurrences = max(max(occurrences), max(occurrences1), max(occurrences2))
    if max_occurrences in occurrences:
        highest_sample = highest_samples[np.argmax(occurrences)]
    elif max_occurrences in occurrences1:
        highest_sample = highest_samples1[np.argmax(occurrences1)]
    else:
        highest_sample = highest_samples2[np.argmax(occurrences2)]

    # Return the results
    return highest_sample, max_occurrences
       

# Wait for the timer to finish
while count < ARRAY_SIZE:
    pass

# Find the highest samples and count their occurrences
highest_sample, max_occurrences = find_highest_samples(adc_values, adc1_values, adc2_values)

#3v:lm4040 precision voltage
conversion_factor = 3/(65535)

# Print the results
print("Highest sample:", highest_sample)
print("Highest sample:", highest_sample*conversion_factor, "volts")
print("Occurrences:", max_occurrences)

'''
def hamming(n):
    """
    Define a hamming window function with n samples
    """
    return 0.54 - 0.46 *np.cos(2* np.pi *np.arange(n) / (n-1))

def process_signal(adc_values):
              
    #normalize array
    z = np.zeros(len(adc_values))
    #create a square wave
    y = np.where(np.sin(2 * np.pi * 0.1 * adc_values) < 0, -1, 1)
    #apply hamming window
    y_windowed = y*hamming(len(y))
    #perform fft
    a, b = np.fft.fft(y_windowed, z)
    #absolute value of the array
    f1 = abs(a) + abs(b)
    #take absolute value for only the first half of the array
    #f = abs(a[:len(a)//2]) + abs(b[:len(b)//2])     
    f1[f1<3.5] = 0
    non_zero_indices = f1 != 0
    return f1

def time():    
    start_time = utime.ticks_us()
    x = process_signal(adc_values)
    end_time = utime.ticks_us() - start_time
    print("FFT duration (us):", end_time)
    return end_time

def save_to_txt(f1, file_name):
    #print the array without truncating
    np.set_printoptions(threshold=sys.maxsize)
    print(f1)
    
    #create a file called "fft.text" and write elements of array to it, each on a new line
    with open(file_name, "w", encoding="utf-8") as f:
        for i in f1:        
           f.write(str(i) + '\n')
           
def read_txt(file_name):
    # Read the data from the text file
    with open(file_name, "r") as f:
        data1 = f.read()

    # Split the string into a list of strings
    data1 = data1.split()

    #Convert the strings to floats and print it 
    data1_list = []
    for i in data1:
        data1_list.append(float(i))
    #print(data1_list)

    return data1_list


def save_to_csv(data1_list, file_name):
    # Convert the float array to a list of strings
    data_str = [str(x) for x in data1_list]

    # Join the list of strings with commas
    csv_str = ",".join(data_str)

    # Print the CSV string
    #pzrint(csv_str)

    # Replace the last comma with a newline character
    csv_str = csv_str.rstrip(",") + "\n"

    # Open the CSV file in write mode
    with open(file_name, "w") as f:
        # Write the CSV string to the file
        f.write(csv_str)

    # Close the file
    f.close()


f1 = process_signal(adc_values)
end_time = time()
save_to_txt(f1, "fft.txt")
data1_list = read_txt("fft.txt")
save_to_csv(data1_list, "fft.csv")


#UART writes data to p2(adctimer3)
com2 = Easy_comms(1,9600)
led = Pin(25, Pin.OUT)

data2 = f1

while True:
    #com1.send(str(json.dumps(data)))
    com2.send(data2, slave_id = 2)
    
    led.toggle()
    sleep(1)


