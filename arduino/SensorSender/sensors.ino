#define NUM_SENSORS 3
#define NUM_SENSOR_READINGS 50

#define MIN_ROTATIONS 2
#define START_MIN_SPEED (float)0.3f
#define START_MAX_SPEED (float)3.f

const int minPeakDiff = 15;
#define IDLE_INTERVAL_MS 5000

struct SensorReading {
  int readings[NUM_SENSOR_READINGS]; // the readings from the analog input
  int readIndex = 0;                 // the index of the current reading
  int total = 0;                     // the running total
  int average = 0;                   // the average
  int inPeak = 0;
  unsigned long revStartTime = 0;
  unsigned long lastIdleCheckTime = 0;
  float speed = 0;
  int inputPin;
  uint8_t rotatingCount;
  uint8_t isRotating;
  uint8_t isRotatingChanged;
};

SensorReading sensors[NUM_SENSORS];

void setupSensors() {
  sensors[0].inputPin = A0;
  sensors[1].inputPin = A1;
  sensors[2].inputPin = A2;
  resetAllReadings();
}

void loopSensors() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    processSensor(i);
  }
}

void resetReadings(int sensorId) {
  sensors[sensorId].readIndex = 0;
  sensors[sensorId].average = 0;
  for (int i = 0; i < NUM_SENSOR_READINGS; i++) {
    sensors[sensorId].readings[i] = 0;
  }
}

void resetAllReadings(void) {
  for (int i = 0; i < NUM_SENSORS; i++) {
    resetReadings(i);
  }
}

void processSensor(int sensorId) {
  SensorReading *reading = sensors + sensorId;
  reading->total = reading->total - reading->readings[reading->readIndex];
  int val = analogRead(reading->inputPin);
  reading->readings[reading->readIndex] = val;
  reading->total = reading->total + reading->readings[reading->readIndex];
  reading->readIndex += 1;

  if (reading->readIndex >= NUM_SENSOR_READINGS) {
    reading->readIndex = 0;
  }

  // calculate the average:
  reading->average = reading->total / NUM_SENSOR_READINGS;

  unsigned long now = millis();
  int theReading = val > reading->average + minPeakDiff;

  if (theReading) {
    reading->lastIdleCheckTime = now;
    if (reading->inPeak == 0) {
      reading->inPeak = 1;
      if (reading->revStartTime > 0) {
        unsigned long elapsed = now - reading->revStartTime;
        float speed = 1000.f / elapsed;
        if (speed < START_MAX_SPEED) {
          reading->speed = speed;
          if (reading->rotatingCount < MIN_ROTATIONS) {
            if (reading->speed > START_MIN_SPEED &&
                reading->speed < START_MAX_SPEED) {
              reading->rotatingCount += 1;
              if (reading->rotatingCount >= MIN_ROTATIONS) {
                reading->isRotatingChanged = 1;
                reading->isRotating = 1;
              }
            } else if (reading->rotatingCount) {
              reading->rotatingCount -= 1;
            }
          }
        }
      }
      reading->revStartTime = now;
    }
  } else {
    reading->inPeak = 0;
  }
  if (now - reading->lastIdleCheckTime > IDLE_INTERVAL_MS) {
    reading->isRotating = 0;
    reading->isRotatingChanged = 0;
    reading->rotatingCount = 0;
    reading->speed = 0;
    reading->lastIdleCheckTime = now;
  }
}

void sendMsgSensor(uint8_t boardId, const float *v, const int isRotating[3]) {
  static SensorMsg msg;
  msg.start = START_VAL;
  msg.boardId = boardId;
  msg.end = END_VAL;
  msg.v[0] = v[0];
  msg.v[1] = v[1];
  msg.v[2] = v[2];
  msg.isRotating[0] = isRotating[0];
  msg.isRotating[1] = isRotating[1];
  msg.isRotating[2] = isRotating[2];
  outSerial.write((const uint8_t *)&msg, sizeof(SensorMsg));
}

void sendASCIIMsgSensor(uint8_t boardId, const float *v, const int isRotating[3]) {
  Serial.print("S");
  Serial.print(boardId);
  Serial.print(" ");
  Serial.print(v[0]);
  Serial.print(" ");
  Serial.print(isRotating[0]);
  Serial.print(" ");
  Serial.print(v[1]);
  Serial.print(" ");
  Serial.print(isRotating[1]);
  Serial.print(" ");
  Serial.print(v[2]);
  Serial.print(" ");
  Serial.print(isRotating[2]);
  Serial.println();
}


void sendSensors() {
  float v[3] = {sensors[0].speed, sensors[1].speed, sensors[2].speed};
  int r[3] = {sensors[0].isRotating, sensors[1].isRotating, sensors[2].isRotating};
  sendMsgSensor(BOARD_ID, v,r);
#ifdef SERIAL_DEBUG
  sendASCIIMsgSensor(BOARD_ID, v, r);
#endif
}
