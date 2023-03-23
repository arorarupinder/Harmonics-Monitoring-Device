#Easy comms is a simple class that allows you to send and receive messages over a serial port.

from machine import UART, Pin
from time import time_ns, sleep
import struct

class Easy_comms:
 
    #uart_id = 0
    baud_rate = 9600
    timeout = 1000 # milliseconds
    
    def __init__(self, uart_id:int, baud_rate:int=None):
        self.uart_id = uart_id
        if baud_rate: self.baud_rate = baud_rate

        # set the baud rate
        self.uart = UART(self.uart_id,self.baud_rate)

        # Initialise the UART serial port
        self.uart.init(baudrate=self.baud_rate, bits=8, parity=None, stop=1)
            
    def send(self, data: list[float], slave_id:int):
        # Convert the list of floats to bytes using the struct module
        data_bytes = struct.pack('f'*len(data), *data)
        
        # Construct the message as bytes and send it over the UART
        message = bytes([slave_id]) + data_bytes
        #print(message)
        self.uart.write(message)
        
        
    def read(self) -> tuple[int,list[float]]:
        start_time = time_ns()
        current_time = start_time
        new_data = False
        message = b""
        while (not new_data) or (current_time <= (start_time + self.timeout)):
            if (self.uart.any() > 0):
                message += self.uart.read()
                #print(message)
                #print(len(message))
                if len(message) >= 6:  # We need at least 6 bytes to read a message (1 byte for slave_id, 1 byte for num_floats, and 4 bytes for a float)
                    data = []
                    slave_id = message[0]
                    
                    message = message[1:]
                    while len(message) >= 4:
                        # Extract the data bytes from the message
                        data_bytes = message[:4]                        
                        #print(len(data_bytes))

                        # Convert the data bytes to a float using the struct module
                        data.append(struct.unpack('f', data_bytes)[0])
                        #print(data)
                        # Remove the processed bytes from the message
                        message = message[4:]
                        
                        
                    return (slave_id, data)
            current_time = time_ns()
        else:
            return None



