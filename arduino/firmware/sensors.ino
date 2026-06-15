const int numReadings = 50;
int readings[numReadings]; // the readings from the analog input
int readIndex = 0;         // the index of the current reading
int total = 0;             // the running total
int average = 0;           // the average

const int minPeakDiff = 20;

unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;
int inPeak = 0;

void loopSensor() {
  int sensorId = 1;
  total = total - readings[readIndex];

  int val = analogRead(inputPin);
  readings[readIndex] = val;

  total = total + readings[readIndex];
  readIndex = readIndex + 1;

  if (readIndex >= numReadings) {
    readIndex = 0;
  }

  // calculate the average:
  average = total / numReadings;

  unsigned long now = millis();
  int reading = val > average + minPeakDiff;

  if (reading) {
    lastIdleCheckTime = now;
    if (inPeak == 0) {
      float speed = -1;
      if (revStartTime > 0) {
        unsigned long elapsed = now - revStartTime;
        speed = 1000.f / elapsed;
      }
      sendStatus(sensorId, speed, reading);
      revStartTime = now;
    }
    inPeak = 1;
  } else {
    inPeak = 0;
  }
  if (now - lastIdleCheckTime > IdleInterval) {
    resetReadings();
    sendStatus(sensorId, 0, 0);
    lastIdleCheckTime = now;
  }
  delay(2);
}

void resetReadings() {
  for (int i = 0; i < i; i++) {
    readings[i] = 0;
  }
}

void sendStatus(int sensorId, float speed, int activity) {
  Serial.print("S");
  Serial.print(sensorId);
  Serial.print(" ");
  Serial.print(speed);
  Serial.print(" ");
  Serial.print(activity);
  Serial.print(";\n");
}