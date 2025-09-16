from machine import Pin
import time

# Setup pins
button_on = Pin(14, Pin.IN, Pin.PULL_UP)
button_off = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)

led_state = 0  # Start with LED off
led.value(led_state)

# Debounce delay in ms
debounce_time = 200

# Track last button press time
last_on_press = 0
last_off_press = 0

while True:
    current_time = time.ticks_ms()

    # Check button ON press
    if button_on.value() == 0:
        # Check debounce
        if time.ticks_diff(current_time, last_on_press) > debounce_time:
            led_state = 1
            led.value(led_state)
            last_on_press = current_time

    # Check button OFF press
    if button_off.value() == 0:
        if time.ticks_diff(current_time, last_off_press) > debounce_time:
            led_state = 0
            led.value(led_state)
            last_off_press = current_time

    time.sleep(0.01)  # Small delay to reduce CPU load
