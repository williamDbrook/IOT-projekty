from machine import UART, Pin, PWM
import time
import urandom
 
# UART nastavení
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
 
# LED na GPIO25 (PWM)
led_pin = Pin(22)
led_pwm = PWM(led_pin)
led_pwm.freq(1000)  # 1 kHz pro LED
 
# Servo na GPIO15 (PWM, 50 Hz)
servo_pin = Pin(15)
servo_pwm = PWM(servo_pin)
servo_pwm.freq(50)
 
# Funkce pro LED jas
def set_led_brightness(value):
    led_pwm.duty_u16(value)
 
# Funkce pro nastavení úhlu serva
def set_servo_angle(angle):
    min_duty = 1638   # ~0.5ms pulz (0°)
    max_duty = 8192   # ~2.5ms pulz (180°)
    duty = min_duty + int((angle / 180) * (max_duty - min_duty))
    servo_pwm.duty_u16(duty)
 
# Hlavní smyčka
while True:
    if uart.any():
        data = uart.read()
        if data and b'1' in data:
            # Náhodný jas (LED)
            brightness = urandom.getrandbits(16)
            set_led_brightness(brightness)
            print("LED jas nastaven na:", brightness)
 
            # Náhodný úhel (Servo)
            angle = urandom.getrandbits(8) % 181  # 0–180°
            set_servo_angle(angle)
            print("Servo natočeno na:", angle, "stupňů")
 
    time.sleep(0.1)