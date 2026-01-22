from machine import Pin, PWM
import time

# Create a PWM object on the LED pin
led_pwm = PWM(Pin(15))
led_pwm.freq(1000) # Set frequency to 1kHz

while True:
    # Duty cycle goes from 0 to 65535
    for brightness in range(0, 65535, 1000):
        led_pwm.duty_u16(brightness)
        time.sleep(0.01)
    for brightness in range(65535, 0, -1000):
        led_pwm.duty_u16(brightness)
        time.sleep(0.01)