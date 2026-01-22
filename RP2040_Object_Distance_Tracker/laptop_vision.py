import cv2
import numpy as np
import serial
import time

# 1. Setup Serial (Change 'COM3' to your actual port)
try:
    ser = serial.Serial('COM5', 115200, timeout=1)
    time.sleep(2) 
    print("Connected to Vaman Board!")
except Exception as e:
    print(f"Error: {e}. Ensure VS Code Terminal is closed.")
    exit()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. Red Color Detection (Two ranges combined)
    # Range 1: Lower Red
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    # Range 2: Upper Red
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine both masks to get the full red spectrum
    mask = cv2.add(mask1, mask2)

    # 3. Clean the noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # 4. Find the object
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_cnt)

        if area > 1000: 
            x, y, w, h = cv2.boundingRect(largest_cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) # Red box

            if area > 15000: # Very Close
                ser.write(b'3')
                cv2.putText(frame, "RED: VERY CLOSE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            elif area > 5000: # Medium
                ser.write(b'2')
                cv2.putText(frame, "RED: MEDIUM", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
            else: # Far
                ser.write(b'1')
                cv2.putText(frame, "RED: FAR", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            ser.write(b'0')
    else:
        ser.write(b'0')

    cv2.imshow("Vaman Camera - Red Detection", frame)
    cv2.imshow("Mask (Should see White for Red objects)", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ser.write(b'0')
        break

cap.release()
cv2.destroyAllWindows()
ser.close()