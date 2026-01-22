from machine import Pin
import time

# For Raspberry Pi Pico onboard LED, use Pin(25) or Pin("LED")
# For ESP32 or external LED, Pin(4) is fine.
led = Pin(4, Pin.OUT) 

MORSE_CODE = {
    'A': '.-',   'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.', 'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',  'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.', 'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',  'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',  '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----'
}

DOT_DURATION = 0.2
DASH_DURATION = DOT_DURATION * 3
GAP_BETWEEN_ELEMENTS = DOT_DURATION
GAP_BETWEEN_LETTERS = DOT_DURATION * 3
GAP_BETWEEN_WORDS = DOT_DURATION * 7

def play_pattern(pattern):
    for symbol in pattern:
        if symbol == '.':
            led.value(1)
            time.sleep(DOT_DURATION)
        elif symbol == '-':
            led.value(1)
            time.sleep(DASH_DURATION)
        
        led.value(0)
        time.sleep(GAP_BETWEEN_ELEMENTS)

print("--- Morse Code Converter ---")
while True:
    user_input = input("Enter text to blink (or 'exit' to quit): ").upper()
    
    if user_input == "EXIT":
        print("Stopping...")
        break
        
    for char in user_input:
        if char in MORSE_CODE:
            print(f"Blinking {char}: {MORSE_CODE[char]}")
            play_pattern(MORSE_CODE[char])
            time.sleep(GAP_BETWEEN_LETTERS) 
        elif char == ' ':
            print("Space...")
            time.sleep(GAP_BETWEEN_WORDS)