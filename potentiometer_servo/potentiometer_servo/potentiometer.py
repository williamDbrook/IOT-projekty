from machine import ADC, Pin, PWM
from time import sleep

# Setup ADC for potentiometer on GPIO 26
pot = ADC(Pin(26))

# Setup PWM for servo on GPIO 1 (make sure this pin supports PWM on your board)
servo = PWM(Pin(0))
servo.freq(50)  # Standard servo frequency

# Duty cycle range for the servo (adjust if needed)
min_duty = 1802    # 0 degrees
max_duty = 7864    # 180 degrees

def map_range(x, in_min, in_max, out_min, out_max):
    # Maps x from [in_min, in_max] to [out_min, out_max]
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

try:
    while True:
        adc_value = pot.read_u16()  # Read ADC (0-65535)
        # Map ADC value to servo duty cycle
        duty = map_range(adc_value, 0, 65535, min_duty, max_duty)
        
        servo.duty_u16(duty)
        print(f"ADC: {adc_value}, Servo duty: {duty}")
        sleep(0.05)  # 50 ms delay for smooth movement

except KeyboardInterrupt:
    print("Program stopped")
    servo.deinit()
