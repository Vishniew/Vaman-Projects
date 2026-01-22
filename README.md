# Vaman Vision LED Control



This project uses **OpenCV** on a laptop to detect colored objects via webcam and sends proximity data to a **Vaman (RP2040)** board to control physical LEDs based on distance.



##  Features

* **Color Detection:** Recognizes Red (easily adjustable to other colors).

* **Distance Estimation:** Uses contour area to determine how close an object is.

* **Hardware Feedback:** Controls three LEDs (Onboard, GPIO 4, and GPIO 5) to indicate "Far", "Medium", or "Close" status.



---



##  Hardware Requirements

* **Vaman (RP2040) Board**

* **USB Data Cable**

* **2x External LEDs** (connected to GPIO 4 and 5 with resistors)



---



##  Project Structure

* `main.py`: MicroPython code to be uploaded to the RP2040.

* `vision_control.py`: Python script to be run on your laptop.



---



##  Setup



### 1. Laptop Side

Install the required dependencies using the terminal:

```bash

pip install opencv-python numpy pyserial

```

### 2. Pico Side

* Open **VS Code** and ensure the **MicroPico** extension is installed.

* Connect your **Vaman board** to your laptop via USB.

* Open your `main.py` file in the editor.

* Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac) to open the Command Palette.

* Type and select: **MicroPico: Upload current file to Pico**.



### 3. Execution

* Identify your board's **COM port** in **Device Manager** (e.g., COM3 or COM4).

* Update the **COM port** in `vision_control.py` to match your device.

* **Important:** Close the VS Code serial terminal/connection to free up the port.

* Run the laptop script:

```bash

python vision_control.py

```

##  Usage

* **Detection:** Place a **Red** object in front of the webcam.

* **Visual Feedback:** A bounding box will appear around the object on your screen.

* **Hardware Feedback:** * If the object is **Far**, the **Onboard LED** (GPIO 25) will glow.

    * If the object moves to **Medium** distance, **External LED 1** (GPIO 4) will glow.

    * If the object is **Very Close**, **External LED 2** (GPIO 5) will glow.

* **Exit:** Press the **'q'** key on your keyboard to stop the camera and close the application.