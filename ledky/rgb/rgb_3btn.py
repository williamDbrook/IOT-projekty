from machine import Pin, PWM
import random
import time

# Define PWM output pins for RGB channels
RED_PIN = 15
GREEN_PIN = 14
BLUE_PIN = 13

# Define button input pins
RED_BTN = 12
GREEN_BTN = 11
BLUE_BTN = 10

# Setup PWM objects
red_pwm = PWM(Pin(RED_PIN))
green_pwm = PWM(Pin(GREEN_PIN))
blue_pwm = PWM(Pin(BLUE_PIN))

# Set PWM frequency
for pwm in (red_pwm, green_pwm, blue_pwm):
    pwm.freq(1000)

# Setup buttons with pull-down resistors
red_btn = Pin(RED_BTN, Pin.IN, Pin.PULL_DOWN)
green_btn = Pin(GREEN_BTN, Pin.IN, Pin.PULL_DOWN)
blue_btn = Pin(BLUE_BTN, Pin.IN, Pin.PULL_DOWN)

# Convert 0-255 value to 16-bit PWM value
def to_pwm(val):
    return int((val / 255) * 65535)

# Current RGB values
r = 0
g = 0
b = 0

# Update the LED color
def update_led():
    red_pwm.duty_u16(to_pwm(r))
    green_pwm.duty_u16(to_pwm(g))
    blue_pwm.duty_u16(to_pwm(b))

# Main loop
while True:
    if red_btn.value():
        r = random.randint(0, 255)
        print("New RED:", r)
        update_led()
        time.sleep(0.3)  # Debounce

    if green_btn.value():
        g = random.randint(0, 255)
        print("New GREEN:", g)
        update_led()
        time.sleep(0.3)

    if blue_btn.value():
        b = random.randint(0, 255)
        print("New BLUE:", b)
        update_led()
        time.sleep(0.3)

    time.sleep(0.01)
