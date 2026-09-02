/*
Firmware de control des Servos et lecture des capteurs hall.
L'identifiant de la carte est faite
*/
#include <Servo.h>

#define DEBUG 0

#define NUM_SERVOS 3
int boardID = 1;
// Servos
Servo servos[NUM_SERVOS];

const int servo0Pin = 3;
const int servo1Pin = 5;
const int servo2Pin = 6;

unsigned long motorStartedTime[NUM_SERVOS] = {-1, -1, -1};
int motorCommandDuration[NUM_SERVOS] = {-1, -1, -1};

// sensors

int readSensorsEveryMs = 10;
int sendSensorsEveryMs = 1000;

unsigned long lastTimeReadSensors = 0;
unsigned long lastTimeSentSensors = 0;

void setup() {
  Serial.begin(115200);
  servos[0].attach(servo0Pin);
  servos[1].attach(servo1Pin);
  servos[2].attach(servo2Pin);

  setupSensors();

  pinMode(A3, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  int v0 = !digitalRead(A3);
  int v1 = !digitalRead(A4);
#if DEBUG
  Serial.print(v0);
  Serial.print(" - ");
  Serial.print(v1);
  Serial.println();
#endif

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

const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data
bool newData = false;

void startMotor(int index, int duration) {
#if DEBUG
  Serial.print("Start motor ");
  Serial.print(index);
  Serial.print(" for ");
  Serial.print(duration);
  Serial.println("ms");
#endif
  servos[index].write(60);
  motorStartedTime[index] = millis();
  motorCommandDuration[index] = duration;
}

void loop() {
  handleLoopSensors();
  recvWithEndMarker();
  if (newData) {
    int strtokIndx = strtok(receivedChars, ";");
    int value = atoi(strtokIndx);
    strtokIndx = strtok(NULL, ";");
    int duration = atoi(strtokIndx);
#if DEBUG
    Serial.println(receivedChars);
    Serial.print("value=");
    Serial.print(value);
    Serial.print(" duration=");
    Serial.println(duration);
#endif
    if (value && duration) {
      if (value >= 1 && value < 4) {
        startMotor(value - 1, duration);
      }
    } else {
      Serial.println("INVALID");
    }
    newData = false;
  }

  for (int i = 0; i < NUM_SERVOS; ++i) {
    if (motorCommandDuration[i] != -1 &&
        millis() - motorStartedTime[i] >= motorCommandDuration[i]) {
#if DEBUG
      Serial.print("Stop motor ");
      Serial.println(i);
#endif
      servos[i].write(90);
      motorCommandDuration[i] = -1;
    }
  }
}

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  // if (Serial.available() > 0) {
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}
