from flask import Flask, render_template, request, jsonify
import serial
import threading

app = Flask(__name__)

# Otevřeme dvě sériové linky
led_pico = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
button_pico = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

button_state = "Uvolněno"

def listen_button():
    global button_state
    while True:
        line = button_pico.readline().decode().strip()
        if line == "BTN_PRESSED":
            button_state = "Stisknuto"
            led_pico.write(b"LED_ON\n")     # ZAPNEME LED
        elif line == "BTN_RELEASED":
            button_state = "Uvolněno"
            led_pico.write(b"LED_OFF\n")    # VYPNEME LED

# Spustíme thread na čtení tlačítka
threading.Thread(target=listen_button, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html", button_state=button_state)


@app.route("/led", methods=["POST"])
def led_control():
    state = request.json.get("state")
    if state == "on":
        led_pico.write(b"LED_ON\n")
    else:
        led_pico.write(b"LED_OFF\n")
    return jsonify(success=True)


@app.route("/button_state")
def get_button_state():
    return jsonify(state=button_state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)