from machine import UART, SPI, Pin
import time

# UART (TX GP0, RX GP1)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# SPI pro MAX7219 (CLK GP2, DIN GP3, CS GP5)
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
cs.value(1)

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
    send_command(SHUTDOWN, 0x01)      # Normal operation
    send_command(DISPLAY_TEST, 0x00)  # Disable test
    send_command(DECODE_MODE, 0x00)   # No decode
    send_command(SCAN_LIMIT, 0x07)    # Display all 8 digits
    send_command(INTENSITY, 0x08)     # Brightness
    clear_display()

def clear_display():
    for i in range(1, 9):
        send_command(i, 0)

def show_bar(level):
    clear_display()
    for i in range(1, level + 1):
        send_command(i, 0xFF)  # Full line lit

init_max7219()

while True:
    if uart.any():
        line = uart.readline()
        if line:
            try:
                level = int(line.strip())
                if 0 <= level <= 8:
                    show_bar(level)
            except:
                pass
    time.sleep(0.05)
