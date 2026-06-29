#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9, 500, 2500);  // Min 500µs, max 2500µs
  myServo.write(90);
  Serial.begin(9600);
  Serial.println("Started");
}

// 70 1000
void loop() {
  if (Serial.available()) {
    int value = Serial.parseInt();
    int wait = Serial.parseInt();
    myServo.write(value);
    delay(wait);
    Serial.print("Moved to: ");
    Serial.print(value);
    Serial.print(" read:");
    Serial.println(myServo.read());
    myServo.write(90);
    
  }
}