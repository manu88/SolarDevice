#define NUM_READINGS 50
int readings[NUM_READINGS]; // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average

const int minPeakDiff = 20;

unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;
int inPeak = 0;

extern "C" {
typedef struct {
  float speed;
  int activity;
} SensorState;
} // extern "C"

#define NUM_SENSOR_STATES 2

static SensorState sensor_state[NUM_SENSOR_STATES];

void loopSensor() {
  int sensorId = 1;
  total = total - readings[readIndex];

  int val = analogRead(inputPin);
  readings[readIndex] = val;

  total = total + readings[readIndex];
  readIndex = readIndex + 1;

  if (readIndex >= NUM_READINGS) {
    readIndex = 0;
  }

  // calculate the average:
  average = total / NUM_READINGS;

  unsigned long now = millis();
  int reading = val > average + minPeakDiff;

  if (reading) {
    lastIdleCheckTime = now;
    if (inPeak == 0) {
      float speed = -1;
      if (revStartTime > 0) {
        unsigned long elapsed = now - revStartTime;
        if (elapsed != 0) {
          speed = 1000.f / elapsed;
        }
      }
      setStatus(sensorId, speed, reading);
      revStartTime = now;
    }
    inPeak = 1;
  } else {
    inPeak = 0;
  }
  if (now - lastIdleCheckTime > IdleInterval) {
    resetReadings();
    setStatus(sensorId, 0, 0);
    lastIdleCheckTime = now;
  }
  // delay(2);
}

void resetReadings() {
  for (int i = 0; i < NUM_SENSOR_STATES; i++) {
    sensor_state[i] = {0.f, 0};
  }
  for (int i = 0; i < NUM_READINGS; i++) {
    readings[i] = 0;
  }
}

void setStatus(int sensorId, float speed, int activity) {
  if (sensorId >= NUM_SENSOR_STATES) {
    Serial.print("setStatus: invalid sensorId: ");
    Serial.println(sensorId);
    return;
  }
  sensor_state[sensorId].speed = speed;
  sensor_state[sensorId].activity = activity;
}
void sendAllSensors() {
  for (int i = 0; i < NUM_SENSOR_STATES; i++) {
    sendStatus(i, sensor_state[i].speed, sensor_state[i].activity);
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