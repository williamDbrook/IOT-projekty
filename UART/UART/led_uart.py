from machine import UART, Pin
import time
 
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
led = Pin(25, Pin.OUT)
 
while True:
    if uart.any():
        data = uart.read()
        if data and b'1' in data:
            led.value(1)  # LED ON
            print("Přijato '1' - LED zapnuta")
        else:
            led.value(0)  # LED OFF pokud není '1'
    else:
        led.value(0)
    time.sleep(0.1)