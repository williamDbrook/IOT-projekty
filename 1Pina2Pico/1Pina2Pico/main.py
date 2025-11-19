from machine import UART, Pin
import time

uart = UART(0, 115200)
btn = Pin(14, Pin.IN, Pin.PULL_UP)
last = 1

while True:
    s = btn.value()
    if last == 1 and s == 0:
        uart.write(b'PRESSED\n')
        time.sleep(0.2)
    last = s
