import machine
import sys

# Define LEDs - Using GPIO 25, 4, and 5
led_onboard = machine.Pin(25, machine.Pin.OUT)
led_ext1 = machine.Pin(4, machine.Pin.OUT)
led_ext2 = machine.Pin(5, machine.Pin.OUT)

def reset_leds():
    led_onboard.value(0)
    led_ext1.value(0)
    led_ext2.value(0)

# Initial state
reset_leds()
print("Vaman is listening for gestures...")

while True:
    # Read the full line sent by Python
    line = sys.stdin.readline().strip()
    
    if line:
        try:
            count = int(line)
            
            if count == 0:
                reset_leds()
            elif count == 1:
                reset_leds()
                led_onboard.value(1)
            elif count == 2:
                reset_leds()
                led_ext1.value(1)
            elif count == 3:
                reset_leds()
                led_ext2.value(1)
            elif count >= 4:
                # Turn everything on for 4 or 5 fingers
                led_onboard.value(1)
                led_ext1.value(1)
                led_ext2.value(1)
                
        except ValueError:
            # In case of any serial noise/junk data
            continue

# Timing (Matches your Pico C code: DOT=200ms)
THRESHOLD = 135       # How bright the LED must be (0-255)
DOT_MAX_TIME = 0.5    # Max duration for a dot (seconds)
GAP_LETTER = 0.5      # Silence duration to trigger end of letter

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
    cv2.putText(frame, f"Msg: {decoded_message}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    cv2.imshow("Pico Morse Decoder", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()