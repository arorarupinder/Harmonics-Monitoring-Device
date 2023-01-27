#import libraries
from ulab import numpy as np
import sys
import machine 
import time



#normalize array
z = np.zeros(len(x))

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
        
# initialize the SPI connection
#spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0)

# convert the string to bytes
#string_bytes = csv_str.encode()

# send the string over SPI
#spi.write(string_bytes)
