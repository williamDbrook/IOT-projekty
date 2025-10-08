from machine import UART, SPI, Pin
import time
import urandom  # vestavěný modul MicroPythonu pro náhodná čísla
from max7219 import Matrix8x8  # pokud je knihovna v lib/

# UART inicializace
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# SPI pro MAX7219 displej
spi = SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

# Inicializace displeje
display = Matrix8x8(spi, cs, 1)  # jeden 8x8 modul
display.brightness(5)
display.fill(0)
display.show()

# Předdefinované vzory (obrazce)
patterns = [
    [0x18, 0x3C, 0x7E, 0xDB, 0xFF, 0x7E, 0x3C, 0x18],  # srdce
    [0x00, 0x66, 0xFF, 0xFF, 0x7E, 0x3C, 0x18, 0x00],  # šipka dolů
    [0x81, 0x42, 0x24, 0x18, 0x18, 0x24, 0x42, 0x81],  # X
    [0xFF, 0x81, 0xBD, 0xA5, 0xA5, 0xBD, 0x81, 0xFF],  # obličej
    [0x3C, 0x66, 0x42, 0xA5, 0x99, 0x42, 0x66, 0x3C],  # jiný obrazec
]

def show_random_pattern():
    pattern = urandom.choice(patterns)
    display.fill(0)
    for y, row in enumerate(pattern):
        for x in range(8):
            bit = (row >> (7 - x)) & 1
            display.pixel(x, y, bit)
    display.show()

# Hlavní smyčka – čeká na příkazy přes UART
while True:
    if uart.any():
        cmd = uart.readline()
        if cmd and b'SHOW' in cmd:
            print("Přijat příkaz:", cmd)
            show_random_pattern()
    time.sleep(0.05)
