// Bionic Hand Control Firmware
// This code runs on the Arduino Uno and waits for commands from Python.

#include <Servo.h>

// --- Configuration ---
const int NUM_SERVOS = 5;
// Assign the Arduino pins to which the servo signal wires are connected.
// Make sure these are PWM pins (usually marked with a '~').
const int servoPins[NUM_SERVOS] = {9, 10, 11, 6, 5}; // Thumb, Index, Middle, Ring, Pinky

// Create an array of Servo objects
Servo servos[NUM_SERVOS];

void setup() {
  // Start the serial communication at a 9600 baud rate.
  // This must match the rate used in the Python script.
  Serial.begin(9600);
  Serial.println("Arduino Bionic Hand Controller Initialized.");
  Serial.println("Waiting for commands in the format 'finger_index:angle' (e.g., '1:90')");

  // Attach each servo object to its corresponding pin
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(servoPins[i]);
  }
}

void loop() {
  // Check if there is data available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming string until the newline character
    String command = Serial.readStringUntil('\n');

    // Find the position of the colon ':' separator
    int colonIndex = command.indexOf(':');

    // If a colon is found, parse the string
    if (colonIndex > 0) {
      // Extract the finger index part and convert it to an integer
      String indexStr = command.substring(0, colonIndex);
      int fingerIndex = indexStr.toInt();

      // Extract the angle part and convert it to an integer
      String angleStr = command.substring(colonIndex + 1);
      int angle = angleStr.toInt();

      // Validate the received data
      if (fingerIndex >= 0 && fingerIndex < NUM_SERVOS) {
        // Constrain the angle to a safe range for the servo (0-180)
        angle = constrain(angle, 0, 180);

        // Move the specified servo to the specified angle
        servos[fingerIndex].write(angle);
        
        // Optional: Send a confirmation back to the computer
        Serial.print("Moved Finger ");
        Serial.print(fingerIndex);
        Serial.print(" to ");
        Serial.print(angle);
        Serial.println(" degrees.");
      } else {
        Serial.println("Error: Invalid finger index.");
      }
    } else {
      Serial.println("Error: Invalid command format. Use 'index:angle'.");
    }
  }
}