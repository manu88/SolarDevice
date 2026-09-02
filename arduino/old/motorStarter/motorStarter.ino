#include <PWMServo.h>
PWMServo myServo;
#define SERVO_PIN SERVO_PIN_B // PIN 10

void setup() {
  Serial.begin(9600);
  Serial.println("Started");
  setupServo();
}

void setupServo() {
  myServo.attach(SERVO_PIN); // Min 500µs, max 2500µs
  myServo.write(90);
}

// 70 1000
void loopServo() {
  static unsigned long nextTimeStop = 0;
  static int valueToSet = -1;

  if (Serial.available()) {
    int value = Serial.parseInt();
    int wait = Serial.parseInt();
    Serial.print("value: ");
    Serial.print(value);
    Serial.print(" wait:");
    Serial.println(wait);
    valueToSet = value;
    nextTimeStop = millis() + wait;
  }

  if (nextTimeStop != 0 && millis() >= nextTimeStop) {
    Serial.println("Stop");
    nextTimeStop = 0;
    valueToSet = -1;
    myServo.write(90);
  } else if (valueToSet != -1) {
    myServo.write(valueToSet);
  }
}

void loop() { loopServo(); }