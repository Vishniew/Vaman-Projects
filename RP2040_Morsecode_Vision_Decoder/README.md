# Vaman Morse Code Vision Decoder

This project implements an optical communication link where the **Vaman (RP2040)** board acts as a transmitter, converting serial input into Morse code light pulses, which are then decoded in real-time by a laptop webcam using **OpenCV**.

## Features
* **Serial-to-Morse Translation:** Converts text entered via VS Code Serial Monitor into LED pulses.
* **Computer Vision Decoding:** Uses a Region of Interest (ROI) to detect LED brightness levels.
* **Real-time Translation:** Decodes "Dots" and "Dashes" into alphanumeric characters using standard Morse timing.

---

## Hardware Requirements
* **Vaman (RP2040) Board**
* **USB Data Cable**
* **Integrated or External Webcam**

---

## Project Structure
* `main.c` (or project folder): C-SDK code to be built and flashed to the RP2040.
* `morse_decoder.py`: Python script to be run on your laptop.

---

## Setup

### 1. Laptop Side
Install the required dependencies using the terminal:
```bash
pip install opencv-python numpy
```
### 2. Pico Side (C-SDK)
* **Open** the Morse project folder in **VS Code**.
* Ensure the **Pico SDK environment** is correctly configured.
* **Build** the project to generate the `.uf2` binary.
* Connect your **Vaman board** in **BOOTSEL mode** and flash the firmware.
* Open the **Serial Monitor** in VS Code and set the **baud rate to 115200**.

---

### 3. Execution
* Ensure the Vaman board is positioned so the onboard LED is visible to the webcam.
* Run the laptop script:
```bash
python morse_decoder.py
```
## Usage

* **Input:** Type a word or character into the **VS Code Serial Monitor** and press Enter.
* **Optical Transmission:** The Vaman LED will start pulsing the message in Morse code.
* **Visual Feedback:** * Align the pulsing LED inside the **ROI box** (center of the camera feed).
    * The box turns **Green** when light is detected and **Red** when it is off.
* **Decoding:** The decoded message will be displayed as an overlay on the camera window and printed in the terminal.
* **Exit:** Press the **'q'** key on your keyboard to stop the camera and close the application.