from machine import UART, SPI, Pin
import time
import urandom

# UART
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# SPI pro MAX7219
spi = SPI(0, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
cs.value(1)  # CS neaktivní

# MAX7219 registry
DECODE_MODE = 0x09
INTENSITY = 0x0A
SCAN_LIMIT = 0x0B
SHUTDOWN = 0x0C
DISPLAY_TEST = 0x0F

def send_command(register, data):
    cs.value(0)
    spi.write(bytearray([register, data]))
    cs.value(1)

def init_max7219():
    send_command(SHUTDOWN, 0x01)      # zapnout
    send_command(DISPLAY_TEST, 0x00)  # vypnout testovací režim
    send_command(DECODE_MODE, 0x00)   # no decode
    send_command(SCAN_LIMIT, 0x07)    # všech 8 řádků
    send_command(INTENSITY, 0x08)     # jas (0x00 až 0x0F)
    clear_display()

def clear_display():
    for i in range(1, 9):  # řádky 1–8
        send_command(i, 0)

# Ukázkové obrazce (seznam 8 hodnot = 8 řádků)
patterns = [
    [0x18, 0x3C, 0x7E, 0xDB, 0xFF, 0x7E, 0x3C, 0x18],  # srdce
    [0x00, 0x66, 0xFF, 0xFF, 0x7E, 0x3C, 0x18, 0x00],  # šipka dolů
    [0x81, 0x42, 0x24, 0x18, 0x18, 0x24, 0x42, 0x81],  # X
    [0xFF, 0x81, 0xBD, 0xA5, 0xA5, 0xBD, 0x81, 0xFF],  # obličej
    [0x3C, 0x66, 0x42, 0xA5, 0x99, 0x42, 0x66, 0x3C],  # jiný obrazec
]

def show_pattern(pattern):
    for i in range(8):
        send_command(i + 1, pattern[i])  # MAX7219 řádky jsou 1–8

# Inicializace
init_max7219()

# Hlavní smyčka
while True:
    if uart.any():
        cmd = uart.readline()
        if cmd and b'SHOW' in cmd:
            print("Příkaz přijat:", cmd)
            pattern = urandom.choice(patterns)
            show_pattern(pattern)
    time.sleep(0.05)
