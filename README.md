# Vaman Projects (IoT & Embedded Systems)

This repository contains my development work on the **Vaman** platform, featuring projects for both **ESP32** and **RP2040** microcontrollers using multiple frameworks.

##  Projects Included

### 1. ESP32 Gateway (ESP-IDF)
* **Location:** `/ESP32_IDF`
* **Description:** Firmware for the ESP32 side of Vaman using the professional ESP-IDF framework.
* **Features:** Wi-Fi connectivity and Morse Code status signaling.

### 2. RP2040 C-SDK Projects
* **Location:** `/RP2040_C_SDK`
* **Description:** Low-level applications developed using the official Raspberry Pi Pico C-SDK for high performance.

### 3. RP2040 & ESP32 Temperature Bridge
* **Location:** `/RP2040_ESP32_Temperature_Bridge`
* **Description:** An integrated project enabling communication between the two processors to bridge sensor data.

### 4. MicroPython Prototyping
* **Location:** `/MicroPython_Thonny`
* **Description:** Rapid prototyping scripts developed in Thonny IDE for the RP2040.

### 5. PC Python Scripts
* **Location:** `/PC_Python_Scripts`
* **Description:** Desktop-side Python scripts for data logging, visualization, and monitoring hardware output.

---

##  Development Environment & Toolchain
* **Hardware:** Vaman (ESP32 & RP2040 Dual-Processor)
* **Languages:** C, Python, MicroPython
* **Frameworks:** ESP-IDF v5.5.2, Raspberry Pi Pico C-SDK
* **Tools:** VS Code, Thonny, Git/SSH, Ninja Build

##  Setup Note
Ensure you have the **ESP-IDF** and **Pico C-SDK** environments configured on your machine before attempting to build. For the ESP32 project, update your Wi-Fi credentials in a `secrets.h` file (not included in this repo for security).
