from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO

# Nastavení GPIO
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Flask app
app = Flask(__name__)

# Stav LED
led_on = False

@app.route("/")
def index():
    return render_template("index.html", led_on=led_on)

@app.route("/toggle")
def toggle():
    global led_on
    led_on = not led_on
    GPIO.output(LED_PIN, GPIO.HIGH if led_on else GPIO.LOW)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
