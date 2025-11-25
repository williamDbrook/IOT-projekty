from machine import Pin
import time
import sys

button = Pin(14, Pin.IN, Pin.PULL_UP)
last_state = button.value()

while True:
    state = button.value()
    if state != last_state:
        if state == 0:
            sys.stdout.write("BTN_PRESSED\n")
        else:
            sys.stdout.write("BTN_RELEASED\n")
        last_state = state
    time.sleep(0.02)
