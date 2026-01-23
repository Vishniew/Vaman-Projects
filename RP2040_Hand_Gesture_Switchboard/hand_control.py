# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# import serial
# import time

# # --- 1. SERIAL SETUP ---
# # Important: Ensure VS Code Serial Monitor is CLOSED before running this.
# COM_PORT = 'COM5' 

# try:
#     ser = serial.Serial(COM_PORT, 115200, timeout=1)
#     time.sleep(2) # Wait for Vaman to wake up
#     print(f"--- Connected to Vaman on {COM_PORT} ---")
# except Exception as e:
#     print(f"--- ERROR: Could not open {COM_PORT}. Check Device Manager or close other apps. ---")
#     print(f"Details: {e}")
#     exit()

# # --- 2. MEDIAPIPE SETUP ---
# base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
# options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
# detector = vision.HandLandmarker.create_from_options(options)

# cap = cv2.VideoCapture(0)
# last_sent_count = -1 

# print("Camera started. Press 'q' to stop.")

# while cap.isOpened():
#     success, frame = cap.read()
#     if not success: break

#     # Flip and convert for MediaPipe
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
#     # Run Hand Detection
#     detection_result = detector.detect(mp_image)
    
#     fingers_count = 0

#     if detection_result.hand_landmarks:
#         # Get coordinates of the first hand detected
#         hand_lms = detection_result.hand_landmarks[0]
        
#         # --- FINGER COUNTING LOGIC ---
#         # We compare Tip vs Knuckle (MCP joint)
#         # Tips: Index(8), Middle(12), Ring(16), Pinky(20)
#         # MCPs: Index(5), Middle(9), Ring(13), Pinky(17)
#         tips = [8, 12, 16, 20]
#         mcps = [5, 9, 13, 17]

#         for i in range(4):
#             if hand_lms[tips[i]].y < hand_lms[mcps[i]].y:
#                 fingers_count += 1

#         # Thumb Logic: Compare Tip(4) with Index Knuckle(5)
#         # (Assuming Right Hand palm facing camera)
#         #if hand_lms[4].x < hand_lms[5].x:
#         #    fingers_count += 1
#         if hand_lms[4].x < hand_lms[2].x - 0.05: # Added a small offset (0.05) for safety
#             fingers_count += 1
#     # --- 3. SEND TO VAMAN (Only on Change) ---
#     if fingers_count != last_sent_count:
#         data_to_send = str(fingers_count)
#         ser.write(data_to_send.encode())
#         print(f"Action: Hand shows {fingers_count} | Sent to Vaman: '{data_to_send}'")
#         last_sent_count = fingers_count

#     # --- 4. VISUAL UI ---
#     # Dark Blue (139, 0, 0) and Arial-like font
#     cv2.putText(frame, f"Fingers: {fingers_count}", (20, 50), 
#                 cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0), 2)
    
#     cv2.imshow('Vaman Hand Control', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         ser.write(b'0') # Turn off LEDs before closing
#         break

# cap.release()
# cv2.destroyAllWindows()
# ser.close()

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time

# --- 1. SERIAL SETUP ---
COM_PORT = 'COM5' 

try:
    ser = serial.Serial(COM_PORT, 115200, timeout=1)
    time.sleep(2) 
    print(f"--- Connected to Vaman on {COM_PORT} ---")
except Exception as e:
    print(f"--- ERROR: {e} ---")
    exit()

# --- 2. MEDIAPIPE SETUP ---
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
last_sent_count = -1 

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)
    
    fingers_count = 0

    if detection_result.hand_landmarks:
        hand_lms = detection_result.hand_landmarks[0]
        
        # 4 Fingers logic
        tips = [8, 12, 16, 20]
        mcps = [5, 9, 13, 17]
        for i in range(4):
            if hand_lms[tips[i]].y < hand_lms[mcps[i]].y:
                fingers_count += 1

        # Improved Thumb logic (Strict check)
        # Compares thumb tip to the thumb base joint
        if hand_lms[4].x < hand_lms[2].x - 0.05:
            fingers_count += 1

    # Send to Vaman only on change
    if fingers_count != last_sent_count:
        data_to_send = str(fingers_count)
        ser.write(data_to_send.encode())
        print(f"Sent to Vaman: {data_to_send}")
        last_sent_count = fingers_count

    # UI
    cv2.putText(frame, f"Fingers: {fingers_count}", (20, 50), 
                cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0), 2)
    cv2.imshow('Vaman Hand Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.write(b'0')
        break

cap.release()
cv2.destroyAllWindows()
ser.close()