import machine
import sys

# Using GPIO 4 as you requested
led = machine.Pin(4, machine.Pin.OUT)
led_state = False

print("Vaman Listening...")

while True:
    # Read the line and remove spaces/newlines
    line = sys.stdin.readline().strip()
    
    if line == "B":
        led_state = not led_state
        led.value(1 if led_state else 0)
        print("Toggled!")