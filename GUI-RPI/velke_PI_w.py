# app_wireless.py
from flask import Flask, render_template, request, jsonify
import requests
import serial
import threading
import time

app = Flask(__name__)

PICO_IP = "192.168.1.123"        # ← IP Pico W s LEDkou (změň podle potřeby)

# Nastavení sériového portu pro druhé Pico (s tlačítkem)
SERIAL_PORT = "/dev/ttyACM0"     # nebo /dev/ttyACM1 – zkus `ls /dev/ttyACM*` v terminálu
BAUD_RATE = 115200

button_state = "Uvolněno"

# Připojení na sériový port
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Připojeno k druhému Pico na {SERIAL_PORT}")
except Exception as e:
    print("Chyba připojení k sériovému portu:", e)
    ser = None

def control_led(state):
    try:
        if state == "on":
            requests.get(f"http://{PICO_IP}/led/on", timeout=1)
        else:
            requests.get(f"http://{PICO_IP}/led/off", timeout=1)
        print(f"LED posláno: {state}")
    except Exception as e:
        print("Pico W s LED nedostupné:", e)

def read_button_serial():
    global button_state
    while True:
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line == "PRESSED":
                    button_state = "Stisknuto"
                    control_led("on")
                    print("Tlačítko stisknuto")
                elif line == "RELEASED":
                    button_state = "Uvolněno"
                    control_led("off")
                    print("Tlačítko uvolněno")
            except:
                pass
        time.sleep(0.01)

# Spustíme vlákno pro čtení sériového portu
if ser:
    threading.Thread(target=read_button_serial, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html", button_state=button_state)

@app.route("/led", methods=["POST"])
def led_control():
    state = request.json.get("state")
    control_led(state)
    return jsonify(success=True)

@app.route("/button_state")
def get_button_state():
    return jsonify(state=button_state)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        if ser:
            ser.close()