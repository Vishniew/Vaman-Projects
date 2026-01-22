# from machine import Pin
# import time
# 
# # Initialize Pin 25 as an Input with an internal Pull-Down resistor
# button = Pin(15, Pin.IN, Pin.PULL_DOWN)
# 
# print("Waiting for button press...")
# 
# while True:
#     if button.value() == 1:
#         print("Button Pressed! (Logic HIGH)")
#         time.sleep(0.2) # Debounce delay to prevent multiple prints
#     time.sleep(0.01)   # Small delay to save power

from machine import Pin
import time

# Onboard LED on Vaman
led = Pin(25, Pin.OUT)
# External button on GP14
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Variable to store the current state (False = OFF, True = ON)
led_state = False

print("Toggle System Ready...")

while True:
    # Check if button is pressed
    if button.value() == 1:
        # 1. Change the state variable
        led_state = not led_state
        
        # 2. Apply the new state to the physical pin
        led.value(led_state)
        
        # Technical term: Printing the status to the REPL
        print("LED is now:", "ON" if led_state else "OFF")
        
        # 3. CRITICAL: Wait until the user lets go of the button
        # This prevents the loop from toggling 100 times in one press
        while button.value() == 1:
            time.sleep(0.01)
            
        # 4. Small delay to handle 'Contact Bounce'
        time.sleep(0.05)