from machine import Pin
import sys

led = Pin(15, Pin.OUT)  # LED na GPIO 15

while True:
    line = sys.stdin.readline().strip()
    if line == "LED_ON":
        led.value(1)
    elif line == "LED_OFF":
        led.value(0)