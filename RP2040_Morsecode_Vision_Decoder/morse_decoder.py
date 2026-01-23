import cv2
import numpy as np
import time

# --- SETUP ---
cap = cv2.VideoCapture(0) # 0 is usually the built-in webcam

# Morse Code Dictionary
MORSE_DICT = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F", 
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L", 
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R", 
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X", 
    "-.--": "Y", "--..": "Z", ".----": "1", "..---": "2", "...--": "3", 
    "....-": "4", ".....": "5", "-....": "6", "--...": "7", "---..": "8", 
    "----.": "9", "-----": "0"
}

# Timing (Matches your Pico C code: DOT=200ms)
THRESHOLD = 120       # How bright the LED must be (0-255)
DOT_MAX_TIME = 0.4    # Max duration for a dot (seconds)
GAP_LETTER = 0.4      # Silence duration to trigger end of letter

# Variables to track signal
signal_string = ""
decoded_message = ""
start_time = 0
is_light_on = False
last_off_time = time.time()

print("Decoder Started! Press 'q' on the camera window to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Focus on a small area in the center (Region of Interest)
    h, w, _ = frame.shape
    roi_size = 60
    x1, y1 = (w // 2) - (roi_size // 2), (h // 2) - (roi_size // 2)
    roi = frame[y1:y1+roi_size, x1:x1+roi_size]

    # 2. Convert to grayscale and check brightness
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_roi)
    #print(f"Current Brightness: {avg_brightness:.2f}")
    current_time = time.time()

    # 3. Detection Logic
    if avg_brightness > THRESHOLD:
        if not is_light_on:
            is_light_on = True
            start_time = current_time
    else:
        if is_light_on:
            duration = current_time - start_time
            # Determine if it was a dot or a dash
            signal_string += "-" if duration > DOT_MAX_TIME else "."
            is_light_on = False
            last_off_time = current_time

        # 4. If light has been off for long enough, decode the letter
        if signal_string and (current_time - last_off_time > GAP_LETTER):
            char = MORSE_DICT.get(signal_string, "?")
            decoded_message += char
            print(f"Decoded: {signal_string} -> {char}")
            signal_string = ""

    # Visual UI
    box_color = (0, 255, 0) if is_light_on else (0, 0, 255)
    cv2.rectangle(frame, (x1, y1), (x1+roi_size, y1+roi_size), box_color, 2)
    cv2.putText(frame, f"Msg: {decoded_message}", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (139, 0, 0), 2)
    
    cv2.imshow("Pico Morse Decoder", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()