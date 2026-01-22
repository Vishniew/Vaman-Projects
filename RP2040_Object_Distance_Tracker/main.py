import machine
import sys
import select

# Setup the LED pins
onboard_led = machine.Pin(25, machine.Pin.OUT)
led1 = machine.Pin(4, machine.Pin.OUT)
led2 = machine.Pin(5, machine.Pin.OUT)

# Put all LEDs in a list for easy control
leds = [onboard_led, led1, led2]

def clear_leds():
    for led in leds:
        led.value(0)

print("RP2040 Ready. Waiting for laptop data...")

while True:
    # Check if there is data waiting in the USB serial buffer
    if select.select([sys.stdin], [], [], 0)[0]:
        # Read the character sent by the laptop
        data = sys.stdin.read(1)
        
        if data == '1':
            clear_leds()
            onboard_led.value(1)
        elif data == '2':
            clear_leds()
            led1.value(1)
        elif data == '3':
            clear_leds()
            led2.value(1)
        elif data == '0':
            clear_leds()