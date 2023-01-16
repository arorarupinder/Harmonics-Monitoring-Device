#import libraries
from ulab import numpy as np
import sys

#create an array of 1024 evenly spaced values between 0 and 10
x = np.linspace(0, 10, num=1024)
# create a square wave
y = np.where(np.sin(2 * np.pi * 0.1 * x) < 0, -1, 1)

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
        
