# RP2040 Blink-Switch

**RP2040 Blink-Switch** is a Human-Computer Interaction (HCI) project that allows you to control hardware (LEDs) using nothing but your eyes. By utilizing the **MediaPipe Face Landmarker AI** and a **Vaman (RP2040)** development board, this system detects a physical blink and toggles a digital output in real-time.

---

###  Project Components

* **Vaman Board (RP2040):** The brain handling the hardware toggle.
* **Python (Laptop):** Handles the AI processing and eye-tracking.
* **MediaPipe:** High-performance AI model for face mesh tracking.
* **External LED:** Connected to GPIO 4.

---
### 📋 Prerequisites

Before starting, ensure you have the following installed on your laptop:
1. **Python 3.10 or higher**
2. **Required Libraries:** Install them via terminal/cmd:
   ```bash
   pip install opencv-python mediapipe pyserial
   ```

### 3. Download the AI Model
The project uses the MediaPipe "Face Landmarker" to track eye movements. This requires a specific model file named `face_landmarker.task`. Simply run the `download_model.py` script in your project folder to download it automatically.

---

### 4. Uploading the Logic

To get the project running, you need to set up both the hardware and the software logic.

#### **Step A: Vaman Side (Hardware Logic)**
Follow these steps to flash the MicroPython code onto your Vaman board using **VS Code**:

1.  **Open VS Code:** Ensure you have the **MicroPico** extension installed.
2.  **Connect Hardware:** Plug your **Vaman board** into your laptop via a USB-C cable.
3.  **Select Script:** Open your `main.py` file in the VS Code editor.
4.  **Upload Code:** * Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac) to open the **Command Palette**.
    * Search for and select: **MicroPico: Upload current file to Pico**.
5.  **Release COM Port:** * *Crucial:* After the upload is successful, look at the bottom status bar and ensure the serial connection is closed/disconnected. If VS Code is "listening" to the board, your Python script won't be able to talk to it.



#### **Step B: Laptop Side (Vision Logic)**
Once the Vaman is ready and the AI model (`face_landmarker.task`) is in your folder:

1.  **Run the Detector:** Open your terminal and run the main script:
    ```bash
    python blink_detector.py
    ```
2.  **Interact:** A window will appear showing your camera feed. Face the camera and blink your eyes firmly to see the LED toggle in real-time!

---
### 💡 Pro-Tip: Finding your COM Port
If your Python script says it cannot find the Vaman board, you need to check which **COM Port** it is plugged into:

* **Windows:** Right-click the Start button > **Device Manager** > **Ports (COM & LPT)**. Look for "USB Serial Device" and note the number (e.g., COM5).
* **Linux/Mac:** Open terminal and type `ls /dev/tty*`. Look for `/dev/ttyUSB0` or `/dev/tty.usbmodem...`.

**Update your code:** Make sure the `port` variable in your `blink_detector.py` matches this number!

---
###  How to Run

Follow these steps in order to get the **Vaman Blink-Switch** running:

1.  **Hardware Check:** Ensure your LED is connected to **GPIO 4** and **GND** on the Vaman board.
2.  **Download the AI Model:** Open your terminal in the project folder and run:
    ```bash
    python download_model.py
    ```
3.  **Prepare the Vaman:** Connect your Vaman board to the laptop. Ensure `main.py` is saved on the board. 
    * *Note: Close Thonny or any Serial Monitor before the next step.*
4.  **Start the Vision System:** Run the main detection script:
    ```bash
    python blink_detector.py
    ```
5.  **Control with your Eyes:** Once the camera window opens, blink firmly to toggle the LED!

---

###  Folder Structure
```text
Vaman-Blink-Switch/
├── face_landmarker.task   # AI Model (Downloaded via script)
├── download_model.py      # Script to fetch the model
├── blink_detector.py      # Main Laptop script
└── main.py                # Vaman MicroPython script
