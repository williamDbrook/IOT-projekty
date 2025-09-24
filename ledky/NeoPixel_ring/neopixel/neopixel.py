import machine
import neopixel
import time

# === Configuration ===
NUM_LEDS = 8
NEOPIXEL_PIN = 0      # Data input from Pico to NeoPixel ring
BUTTON_RIGHT_PIN = 1
BUTTON_LEFT_PIN = 2

# === Setup ===
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_LEDS)

btn_right = machine.Pin(BUTTON_RIGHT_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn_left = machine.Pin(BUTTON_LEFT_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Starting position
current_pos = 0

# Color for the active LED
ACTIVE_COLOR = (0, 0, 255)  # Blue
OFF_COLOR = (0, 0, 0)

def update_leds(pos):
    for i in range(NUM_LEDS):
        if i == pos:
            np[i] = ACTIVE_COLOR
        else:
            np[i] = OFF_COLOR
    np.write()

# Initial LED update
update_leds(current_pos)

# === Main loop ===
while True:
    if btn_right.value():
        current_pos = (current_pos + 1) % NUM_LEDS
        update_leds(current_pos)
        print("Moved right to", current_pos)
        time.sleep(0.25)  # Debounce delay

    if btn_left.value():
        current_pos = (current_pos - 1) % NUM_LEDS
        update_leds(current_pos)
        print("Moved left to", current_pos)
        time.sleep(0.25)  # Debounce delay

    time.sleep(0.01)
