import machine
import sys
import select

# Setup LEDs
onboard_led = machine.Pin(25, machine.Pin.OUT)
led_pin4 = machine.Pin(4, machine.Pin.OUT)
led_pin5 = machine.Pin(5, machine.Pin.OUT)

def all_off():
    onboard_led.value(0)
    led_pin4.value(0)
    led_pin5.value(0)

print("Vaman is listening for finger counts...")

while True:
    # Check if a character has arrived via USB
    if select.select([sys.stdin], [], [], 0.01)[0]:
        data = sys.stdin.read(1)
        
        if data == '0':
            all_off()
        elif data == '1':
            all_off()
            onboard_led.value(1)
        elif data == '2':
            all_off()
            led_pin4.value(1)
        elif data == '3':
            all_off()
            led_pin5.value(1)
        elif data == '4' or data == '5':
            # Turn on everything for 4 or 5 fingers
            onboard_led.value(1)
            led_pin4.value(1)
            led_pin5.value(1)