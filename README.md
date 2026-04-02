# Face Tracking Pan-Tilt Camera System

An automated face-tracking camera system that uses Computer Vision to detect human faces and controls a 2-DOF (Degree of Freedom) Pan-Tilt mechanism via Arduino to keep the face centered in the frame.

## 📺 Demo
![Project Demo](./Demo/project_demo.mp4) 
*(Note: You can also replace this with a GIF for better preview on GitHub)*

## 🚀 Features
- **Real-time Tracking:** Uses MediaPipe for high-speed face detection.
- **Smooth Motion:** Implements a smoothing algorithm for servo transitions to avoid jitter.
- **Custom Hardware:** Features 3D models designed in SolidWorks for a robust Pan-Tilt mount.
- **Cross-Platform:** Python-based control logic communicating via Serial.

## 🛠️ Components
### Hardware:
- **Microcontroller:** Arduino Uno.
- **Actuators:** 2x MG996R High-Torque Servo Motors.
- **Camera:** Standard USB Webcam / Laptop Camera.
- **Mount:** Custom 3D Printed / Laser-cut Pan-Tilt bracket (SolidWorks files included).

### Software:
- **Python 3.x**
- **OpenCV:** For image processing.
- **MediaPipe:** For face detection.
- **PySerial:** For communication between Python and Arduino.
- **Arduino IDE:** To flash the servo control logic.

## 📂 Project Structure
- `Code/`: Contains the Python tracking script and Arduino firmware.
- `Hardware/`: Includes SolidWorks parts (.SLDPRT) and assemblies (.SLDASM).
- `Demo/`: Video demonstrations of the system in action.

## 🔧 Setup & Installation

1. **Hardware Setup:**
   - Connect Pan Servo to Arduino Pin 9.
   - Connect Tilt Servo to Arduino Pin 10.
   - Power the servos using an external power source (shared ground with Arduino).

2. **Arduino:**
   - Upload `servo_control.ino` to your Arduino Uno.

3. **Python Environment:**
   - Install dependencies:
     ```bash
     pip install opencv-python mediapipe pyserial
     ```
   - Update the `COM` port in `face_tracking.py` to match your Arduino port.

4. **Run:**
   ```bash
   python Code/face_tracking.py