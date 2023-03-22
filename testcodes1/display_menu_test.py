from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

# Initialize I2C and OLED display
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))
display = SSD1306_I2C(width=128, height=64, i2c=i2c)

# Initialize rotary encoder and set up callback function
enc = Pin(17), Pin(16)




#button_pin = Pin(16, Pin.IN, Pin.PULL_UP)
#direction_pin = Pin(17, Pin.IN, Pin.PULL_UP)
#step_pin  = Pin(18, Pin.IN, Pin.PULL_UP)


# Set up menu options
options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
selected_option = 0


def encoder_callback(direction):
    global selected_option
    # Increment or decrement selected option based on direction of rotary encoder
    if direction == 1:
        selected_option = (selected_option + 1) % len(options)
    else:
        selected_option = (selected_option - 1 + len(options)) % len(options)
    display_menu()
    
#set up callback function
callback = encoder_callback


def display_menu():
    display.fill(0)
    for i, option in enumerate(options):
        if i == selected_option:
            display.text(" > " + option, 0, i*10)
        else:
            display.text("    " + option, 0, i*10)
    display.show()



# Main loop
while True:
    display_menu()
    sleep(0.01)