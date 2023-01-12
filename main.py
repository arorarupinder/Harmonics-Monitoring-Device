from ulab import numpy as np
import sys

x = np.linspace(0, 10, num=1024)
y = np.sin(x)
z = np.zeros(len(x))

a, b = np.fft.fft(x)

np.set_printoptions(threshold=sys.maxsize)
print('real part:\t', a)
print('\nimaginary part:\t', b)

file = open("fft.txt", "w")
file.write(str(a) + "\n")
file.close()








