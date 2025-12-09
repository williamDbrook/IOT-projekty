from machine import Pin
import time
import sys

# Nastav pin tlačítka (změň podle svého zapojení)
BUTTON_PIN = 14                  # např. GP14
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)  # pull-up, stisk = 0

last_state = None

print("Tlačítko Pico připraveno – odesílám stav přes USB serial")

while True:
    current_state = button.value()
   
    if current_state != last_state:
        # Pošleme jednoduchý text přes USB serial (viditelné v Pythonu jako sériový port)
        if current_state == 0:
            print("PRESSED")      # stisknuto
        else:
            print("RELEASED")     # uvolněno
       
        sys.stdout.flush()  # důležité – zajistí okamžité odeslání
       
        last_state = current_state
   
    time.sleep(0.02)  # debounce + nízká zátěž