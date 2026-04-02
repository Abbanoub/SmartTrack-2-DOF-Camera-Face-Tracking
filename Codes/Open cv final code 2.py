import cv2
import mediapipe as mp
import serial
import time
import logging

# Configure Logging to track system status and potential errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Arduino Connection Setup ---
try:
    # IMPORTANT: Change 'COM5' to match your actual Arduino port from Device Manager
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)  # Wait for connection to stabilize after Arduino auto-reset
    logging.info("Successfully connected to Arduino on COM5")
except serial.SerialException as e:
    logging.critical(f"Could not connect to Arduino: {e}")
    exit(1)

# --- MediaPipe Face Detection Setup ---
mp_face_detection = mp.solutions.face_detection
# model_selection=0: short-range (within 2m), min_detection_confidence=0.6: filters out weak detections
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)

# --- Camera Configuration ---
frame_width, frame_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Initial Servo Positions (Neutral/Center)
pan_angle, tilt_angle = 90, 120

def map_value(val, src_min, src_max, dst_min, dst_max):
    """
    Translates pixel coordinates from the image frame to servo degree angles (0-180).
    """
    return int((val - src_min) * (dst_max - dst_min) / (src_max - src_min) + dst_min)

def smooth_angle(current, target, step=2):
    """
    Increments the angle by a small step to ensure smooth physical movement 
    and prevent sudden mechanical jerks.
    """
    if abs(target - current) <= step:
        return target
    return current + step if target > current else current - step

# --- Main Tracking Loop ---
while True:
    success, frame = cap.read()
    if not success:
        logging.error("Failed to grab frame from camera")
        break

    # Flip the image horizontally for a natural mirror-like experience
    frame = cv2.flip(frame, 1)
    
    # Convert BGR (OpenCV default) to RGB (MediaPipe requirement)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    # Process detections if a face is found
    if results.detections:
        # Focus on the first detected face
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        
        # Calculate the center of the bounding box (Face Center)
        cx = int(bbox.xmin * frame_width + (bbox.width * frame_width) / 2)
        cy = int(bbox.ymin * frame_height + (bbox.height * frame_height) / 2)

        # Map center coordinates to target servo angles
        # Pan: Horizontal movement (X-axis)
        # Tilt: Vertical movement (Y-axis) - Inverted based on camera orientation
        target_pan = map_value(cx, 0, frame_width, 0, 180)
        target_tilt = map_value(cy, 0, frame_height, 180, 0)

        # Apply smoothing logic to the current angles
        pan_angle = smooth_angle(pan_angle, target_pan)
        tilt_angle = smooth_angle(tilt_angle, target_tilt)

        try:
            # Send data to Arduino in "Pan,Tilt\n" format
            command = f"{pan_angle},{tilt_angle}\n"
            arduino.write(command.encode())
            logging.info(f"Target Sent -> Pan: {pan_angle}, Tilt: {tilt_angle}")
        except serial.SerialException as e:
            logging.error(f"Error sending data to Serial: {e}")

    # Optional: Display the tracking window
    cv2.imshow("Face Tracking Active", frame)

    # Press 'q' to break the loop and exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        logging.info("Exiting application...")
        break

# --- Cleanup Resources ---
cap.release()
cv2.destroyAllWindows()
arduino.close()