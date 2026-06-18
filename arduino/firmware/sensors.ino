#define NUM_SENSORS 1
#define NUM_SENSOR_READINGS 50

const int minPeakDiff = 15;
const unsigned long IdleInterval = 5000;

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
};

SensorReading sensors[NUM_SENSORS];

void setupSensors() {
  sensors[0].inputPin = A0;
  sensors[1].inputPin = A1;
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
        reading->speed = 1000.f / elapsed;
        //delay(1);
      }
      reading->revStartTime = now;
    }
  } else {
    reading->inPeak = 0;
  }
  if (now - reading->lastIdleCheckTime >IdleInterval){
    reading->speed = 0;
    reading->lastIdleCheckTime = now;
  }
}

void sendAllSensors() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    sendStatus(i);
  }
}

void sendStatus(int sensorId) {
  Serial.print("S");
  Serial.print(sensorId);
  Serial.print(" ");
  Serial.print(sensors[sensorId].speed);
  Serial.print("\n");
}
