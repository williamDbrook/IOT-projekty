from machine import Pin, PWM
import time
import urandom  # MicroPython's random module

# Setup button
button = Pin(14, Pin.IN, Pin.PULL_UP)

# Setup PWM for RGB LED pins
red = PWM(Pin(16))
green = PWM(Pin(17))
blue = PWM(Pin(18))

# Configure PWM frequency (typical 1000 Hz)
for pwm_pin in (red, green, blue):
    pwm_pin.freq(1000)

debounce_time = 200  # ms
last_press_time = 0

def set_color(r, g, b):
    # r, g, b expected in 0-255 range
    # Convert 0-255 to 0-65535 for PWM duty cycle (16-bit resolution)
    red.duty_u16(int(r * 65535 / 255))
    green.duty_u16(int(g * 65535 / 255))
    blue.duty_u16(int(b * 65535 / 255))

while True:
    current_time = time.ticks_ms()

    if button.value() == 0:
        if time.ticks_diff(current_time, last_press_time) > debounce_time:
            # Generate random RGB values 0-255
            r = urandom.getrandbits(8)
            g = urandom.getrandbits(8)
            b = urandom.getrandbits(8)

            # Set LED color
            set_color(r, g, b)

            # Print RGB values
            print(f"Random RGB: ({r}, {g}, {b})")

            last_press_time = current_time

            # Wait for button release to avoid multiple triggers
            while button.value() == 0:
                time.sleep(0.01)

    time.sleep(0.01)
