from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)  # Button connected to GPIO14 with pull-up

count = 0
debounce_time = 200  # ms
last_press_time = 0

while True:
    current_time = time.ticks_ms()

    if button.value() == 0:  # Button pressed (active low)
        if time.ticks_diff(current_time, last_press_time) > debounce_time:
            count += 1
            print("Button pressed count:", count)
            last_press_time = current_time

            # Wait for button release to avoid counting continuous press
            while button.value() == 0:
                time.sleep(0.01)

    time.sleep(0.01)
