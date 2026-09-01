/*
Firmware de control des Servos et lecture des capteurs hall.
L'identifiant de la carte est faite
*/
#include <Servo.h>

int boardID = 1;
// Servos
Servo servos[3];

const int servo0Pin = 3;
const int servo1Pin = 5;
const int servo2Pin = 6;

// sensors

int readSensorsEveryMs = 10;
int sendSensorsEveryMs = 1000;

unsigned long lastTimeReadSensors = 0;
unsigned long lastTimeSentSensors = 0;

void setup() {
  Serial.begin(9600);
  servos[0].attach(servo0Pin);
  servos[1].attach(servo1Pin);
  servos[2].attach(servo2Pin);

  setupSensors();

  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  int v0 = !digitalRead(A3);
  int v1 = !digitalRead(A4);

  Serial.print(v0);
  Serial.print(" - ");
  Serial.print(v1);

  Serial.println();
  if (v0 == 1) {
    boardID = 2;
  } else if (v1 == 1) {
    boardID = 3;
  }
  Serial.print("BoardId=");
  Serial.println(boardID);
}

void handleLoopSensors() {
  unsigned long now = millis();
  if (now - lastTimeReadSensors >= readSensorsEveryMs) {
    loopSensors();
    lastTimeReadSensors = now;
  }

  now = millis();
  if (now - lastTimeSentSensors >= sendSensorsEveryMs) {
    sendSensors(boardID);
    lastTimeSentSensors = now;
  }
}

void loop() {
  handleLoopSensors();
  if (Serial.available()) {
    int value = Serial.parseInt();
    Serial.println(value);
    if (value >= 1 && value < 4) {
      int index = value - 1;
      Serial.print("Start motor ");
      Serial.println(index);
      servos[index].write(60);
      delay(1000);
      Serial.print("Stop motor ");
      Serial.println(index);
      servos[index].write(90);
    }
  }
}
