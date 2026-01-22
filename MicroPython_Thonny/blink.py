import machine
import time

# Set up the onboard LED (GPIO 25) as an output
led = machine.Pin(25, machine.Pin.OUT)

while True:
    led.value(1)    # Turn LED on
    time.sleep(0.5) # Wait for 0.5 seconds
    led.value(0)    # Turn LED off
    time.sleep(0.5) # Wait for 0.5 seconds