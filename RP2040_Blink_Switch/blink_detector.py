# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# import serial
# import time

# # --- Serial Setup ---
# try:
#     ser = serial.Serial('COM5', 115200, timeout=0.1)
#     time.sleep(2)
#     print("✅ Connected to Vaman")
# except:
#     print("❌ Serial Error: Close VS Code Serial Monitor/Terminal first!")
#     exit()

# # --- MediaPipe Face Landmarker Setup ---
# base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
# options = vision.FaceLandmarkerOptions(
#     base_options=base_options,
#     output_face_blendshapes=True, # This helps detect blinks easily
#     num_faces=1)
# detector = vision.FaceLandmarker.create_from_options(options)

# cap = cv2.VideoCapture(0)
# already_blinked = False

# print("🚀 Blink-Switch Active! Wink or Blink to toggle LED.")

# while cap.isOpened():
#     success, frame = cap.read()
#     if not success: break

#     frame = cv2.flip(frame, 1)
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
#     # Detect face landmarks
#     detection_result = detector.detect(mp_image)
    
#     if detection_result.face_blendshapes:
#         # Index 9 is 'eyeBlinkLeft' and Index 10 is 'eyeBlinkRight'
#         # These values go from 0 (open) to 1.0 (closed)
#         blink_scores = detection_result.face_blendshapes[0]
#         left_blink = blink_scores[9].score
#         right_blink = blink_scores[10].score

#         # If either eye is more than 60% closed
#         if left_blink > 0.6 or right_blink > 0.6:
#             if not already_blinked:
#                 ser.write(b"B\n")
#                 print("😉 Blink Detected! Toggling LED...")
#                 already_blinked = True
#         else:
#             already_blinked = False

#     cv2.imshow('Vaman Blink-Switch', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
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

# --- Serial Setup ---
try:
    ser = serial.Serial('COM5', 115200, timeout=0.1)
    time.sleep(2)
    print("✅ Connected to Vaman")
except:
    print("❌ Serial Error: Close VS Code Serial Monitor first!")
    exit()

# --- MediaPipe Setup ---
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
already_blinked = False

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    detection_result = detector.detect(mp_image)
    
    if detection_result.face_blendshapes:
        # Index 9: eyeBlinkLeft, Index 10: eyeBlinkRight
        scores = detection_result.face_blendshapes[0]
        # We take the average of both eyes for a solid blink
        blink_avg = (scores[9].score + scores[10].score) / 2

        # Sensitivity: 0.5 means 50% closed. Adjust if needed.
        if blink_avg > 0.5:
            if not already_blinked:
                ser.write(b"B\n")
                ser.flush()
                print(f"😉 Blink! Score: {blink_avg:.2f}")
                already_blinked = True
        else:
            already_blinked = False

        # Visual Feedback
        bar_w = int(blink_avg * 200)
        cv2.rectangle(frame, (50, 400), (50 + bar_w, 430), (0, 255, 0), -1)
        cv2.putText(frame, "Blink Strength", (50, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Vaman Blink-Switch', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()