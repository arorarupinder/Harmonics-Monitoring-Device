#ADC_FFT
from ulab import numpy as np
import utime
from time import sleep
from machine import Timer
import sys

# Initialize the ADC and timer
adc = machine.ADC(28)
tim = Timer(-1)

# Initialize the counter as a global variable
count = 0

# Set the size of the array to store the ADC values
ARRAY_SIZE = 1024
adc_values = np.zeros(ARRAY_SIZE, dtype=np.uint16)

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
    
    # Store the value in the array
    adc_values[count-1] = value    
      

# Set the timer to trigger the read_adc function every 1 second
tim.init(freq=1200, mode=machine.Timer.PERIODIC, callback=read_adc)

# Wait for the timer to finish
while count < ARRAY_SIZE:
    pass

print(adc_values)

def process_signal(adc_values):
    # create a square wave
    y = np.where(np.sin(2 * np.pi * 0.1 * adc_values) < 0, -1, 1)

    #normalize array
    z = np.zeros(len(adc_values))

    #perform fft     
    a, b= np.fft.fft(y, z)    
    
    #the the absolute value of the array        
    f1 = abs(a) + abs(b)    
      
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
    print(csv_str)

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

