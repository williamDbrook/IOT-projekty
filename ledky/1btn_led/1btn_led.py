from machine import Pin
import time

# Set up pins
button = Pin(14, Pin.IN, Pin.PULL_UP)  # Button connected to GPIO14 with pull-up
led = Pin(15, Pin.OUT)                 # LED connected to GPIO15

while True:
    if button.value() == 0:  # Button pressed (active low)
        led.value(1)         # Turn LED on
    else:
        led.value(0)         # Turn LED off
    time.sleep(0.01)          # Small debounce delay
