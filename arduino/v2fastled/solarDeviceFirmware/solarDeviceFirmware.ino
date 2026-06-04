#include <FastLED.h>

/////////////////////////////////////////
// Sensor reading part
#define NUM_SENSORS 1

// sensor reading logic:
#define NUM_SENSOR_READINGS (int)40
const int minPeakDiff = 30;

struct SensorReading {
  int readings[NUM_SENSOR_READINGS]; // the readings from the analog input
  int readIndex = 0;                 // the index of the current reading
  int total = 0;                     // the running total
  int average = 0;                   // the average
  int inPeak = 0;
  unsigned long revStartTime = 0;
  float speed = 0;
  int inputPin;
};

SensorReading sensors[NUM_SENSORS];

int state = 0;

/////////////////////////////////////////
// Leds part
#define NUM_LEDS 2
#define DATA_PIN 3 // Change this to match your LED strip's data pin
#define CLOCK_PIN 13
#define BRIGHTNESS 255

CRGB leds[NUM_LEDS];
uint8_t pos = 0;
bool toggle = false;

void setup() {
  Serial.begin(19200);
  sensors[0].inputPin = A0;
  // sensors[1].inputPin = A0;
  for (int i = 0; i < NUM_SENSORS; i++) {
    resetReadings(sensors[i]);
  }
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  setLed(100);
}

const int maxInten = 200;
void fadeIn() {
  for (int colorStep = 0; colorStep <= maxInten; colorStep++) {
    int r = colorStep;
    int g = colorStep;
    int b = colorStep;
    for (int x = 0; x < NUM_LEDS; x++) {
      leds[x] = CRGB(r, g, b);
    }
    FastLED.show();
    delayAndTest(10);
  }
}

void fadeOut() {
  for (int colorStep = 0; colorStep <= maxInten; colorStep++) {
    int r = maxInten - colorStep;
    int g = maxInten - colorStep;
    int b = maxInten - colorStep;
    for (int x = 0; x < NUM_LEDS; x++) {
      leds[x] = CRGB(r, g, b);
    }
    FastLED.show();
    delayAndTest(10);
  }
}

void setLed(int val) {
  for (int x = 0; x < NUM_LEDS; x++) {
    leds[x] = CRGB(val, val, val);
  }
  FastLED.show();
}

void readSerial() {
  if (Serial.available() >= 5) {
    int start = Serial.read();
    if (start == 23) {
      int id = Serial.read();
      if (id >= 0 && id < NUM_LEDS) {
        int intenR = Serial.read();
        int intenG = Serial.read();
        int intenB = Serial.read();
        if (intenR != -1 && intenG != -1 && intenB != -1) {
          leds[id] = CRGB(intenR, intenG, intenB);
          /*
          Serial.print(id);
          Serial.print(" ");
          Serial.print(intenR);
          Serial.print(" ");
          Serial.print(intenG);
          Serial.print(" ");
          Serial.print(intenB);
          Serial.print(";\n");
          */
        }
      }
    }
  }
}

void loop() {
  // readSerial2();
  // showNewData();
  readSerial();
  FastLED.show();
  for (int i = 0; i < NUM_SENSORS; i++) {
    processSensor(sensors[i], i);
  }
  delay(10);
  return;
  if (state == 0) {
    fadeIn();
    delayAndTest(4000);
    fadeOut();
    delayAndTest(4000);
  } else if (state == 1) {
    setLed(200);
    delayAndTest(2000);
  }
}

/////////////////////////////////////////
void sendStatus(int val, const SensorReading &reading, int sensorId) {
  Serial.print(val);
  Serial.print(" ");
  Serial.print(sensorId);
  Serial.print(" ");
  Serial.print(reading.speed);
  Serial.print(";\n");
}

void delayAndTest(int ms) {
  while (ms > 0) {
    delay(10);
    for (int i = 0; i < NUM_SENSORS; i++) {
      processSensor(sensors[i], i);
    }
    ms -= 10;
  }
}

void resetReadings(SensorReading &reading) {
  reading.readIndex = 0;
  for (int i = 0; i < NUM_SENSOR_READINGS; i++) {
    reading.readings[i] = 0;
  }
}

void processSensor(SensorReading &reading, int sensorId) {
  reading.total = reading.total - reading.readings[reading.readIndex];
  int val = analogRead(reading.inputPin);
  reading.readings[reading.readIndex] = val;
  reading.total = reading.total + reading.readings[reading.readIndex];
  reading.readIndex += 1;

  if (reading.readIndex >= NUM_SENSOR_READINGS) {
    reading.readIndex = 0;
  }

  // calculate the average:
  reading.average = reading.total / NUM_SENSOR_READINGS;

  unsigned long now = millis();
  int theReading = val > reading.average + minPeakDiff;
  unsigned long elapsed = now - reading.revStartTime;
  if (theReading) {
    if (reading.inPeak == 0) {
      reading.inPeak = 1;
      Serial.print(sensorId);
      Serial.print(" ");
      Serial.print("1");
      Serial.print(";\n");
      if (reading.revStartTime > 0) {
        reading.speed = 1000.f / elapsed;
      }
      reading.revStartTime = now;
      // sendStatus(1, reading, sensorId);
      if (state == 0 && reading.speed >= 0.3) {
        // Serial.println("started");
        state = 1;
      }
    }
  } else if (elapsed >= 10000) {
    // Serial.println("timeout");
    reading.revStartTime = now;
    state = 0;
  } else {
    reading.inPeak = 0;
  }
}
