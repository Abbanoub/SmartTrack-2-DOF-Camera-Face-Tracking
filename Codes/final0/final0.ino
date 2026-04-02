#include <Servo.h>

// Create servo objects to control the pan and tilt motors
Servo panServo;
Servo tiltServo;

// Initial positions (Center/Neutral)
int pan = 90;
int tilt = 120;

void setup() {
  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);
  
  // Attach the servos to the corresponding digital pins
  panServo.attach(9);   // Connect Pan Servo to Pin 9
  tiltServo.attach(10); // Connect Tilt Servo to Pin 10
  
  // Move servos to initial starting positions
  panServo.write(pan);
  tiltServo.write(tilt);
}

void loop() {
  // Check if data is available to read from the serial port
  if (Serial.available()) {
    // Read the incoming string until a newline character is received
    String input = Serial.readStringUntil('\n');
    input.trim(); // Remove any leading/trailing whitespace

    // Data format expected: "PanValue,TiltValue" (e.g., "90,120")
    int commaIndex = input.indexOf(',');
    
    // Ensure the data contains a comma and is valid
    if (commaIndex > 0) {
      // Split the string into two parts and convert to integers
      int panVal = input.substring(0, commaIndex).toInt();
      int tiltVal = input.substring(commaIndex + 1).toInt();

      // Safety Constraint: Ensure angles stay within the 0-180 degree range
      panVal = constrain(panVal, 0, 180);
      tiltVal = constrain(tiltVal, 0, 180);

      // Write the received angles to the servos
      panServo.write(panVal);
      tiltServo.write(tiltVal);
    }
  }
}