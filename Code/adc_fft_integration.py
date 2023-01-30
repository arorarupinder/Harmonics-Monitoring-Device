#import libraries
from ulab import numpy as np
import sys
import machine 
import utime

@micropython.native
def read_adc():
    # initialize the ADC
    adc = machine.ADC(28)

    # set the number of samples to be taken
    adc_values = np.zeros(1024)

    #read ADC and store them in an array
    for i in range(1024):
        adc_values[i] = adc.read_u16()
        utime.sleep(0.1)
        
    return adc_values

#call the function now 
adc_values = read_adc()

#print the array
print(adc_values)

# create a square wave
y = np.where(np.sin(2 * np.pi * 0.1 * adc_values) < 0, -1, 1)

#normalize array
z = np.zeros(len(adc_values))

#perform fft
a, b= np.fft.fft(y, z)

#the the absolute value of the array        
f1 = abs(a) + abs(b)

#print the array without truncating
np.set_printoptions(threshold=sys.maxsize)
print(f1)

#create a file called "fft.text" and write elements of array to it, each on a new line
with open("fft.txt", "w", encoding="utf-8") as f:
    for i in f1:        
       f.write(str(i) + '\n')
       

# Read the data from the text file
with open("fft.txt", "r") as f:
    data = f.read()
    
# Split the string into a list of strings
data = data.split()

#Convert the strings to floats and print it 
data_list = []
for i in data:
    data_list.append(float(i))
print(data_list)

# Convert the float array to a list of strings
data_str = [str(x) for x in data_list]

# Join the list of strings with commas
csv_str = ",".join(data_str)

# Print the CSV string
print(csv_str)

# Replace the last comma with a newline character
csv_str = csv_str.rstrip(",") + "\n"

# Open the CSV file in write mode
with open("fft.csv", "w") as f:
    # Write the CSV string to the file
    f.write(csv_str)

# Close the file
f.close()
