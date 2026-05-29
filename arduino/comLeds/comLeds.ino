#include "Adafruit_WS2801.h"

const int numReadings = 50;

int readings[numReadings]; // the readings from the analog input
int readIndex = 0;         // the index of the current reading
int total = 0;             // the running total
int average = 0;           // the average

const int minPeakDiff = 20;

int ledState = HIGH;

unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;

// Leds part

uint8_t dataPin = 2;  // Yellow wire on Adafruit Pixels
uint8_t clockPin = 3; // Green wire on Adafruit Pixels
int nbLeds = 4;
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);

int intensity = 255;
int intensity1 = 255;
int intensity2 = 255;
int intensity3 = 255;

void resetReadings() {
  for (int i = 0; i < i; i++) {
    readings[i] = 0;
  }
}

void setup() {
  resetReadings();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(19200);

  strip.begin();
  strip.show();

  strip.setPixelColor(0, intensity, intensity, intensity);
  strip.setPixelColor(1, intensity1, intensity1, intensity1);
  strip.setPixelColor(2, intensity2, intensity2, intensity2);
  strip.setPixelColor(3, intensity3, intensity3, intensity3);
}

int inPeak = 0;

void sendStatus(int id, int val) {
  Serial.print(id);
  Serial.print(" ");
  Serial.print(val);
  Serial.print(";\n");
}

void loop() {
  if (Serial.available() >= 3) {
    int start = Serial.read();
    if (start == 23) {
      int id = Serial.read();
      if (id >= 0 && id < nbLeds) {
        int intenR = Serial.read();
        //int intenG = Serial.read();
        //int intenB = Serial.read();
        if (intenR != -1){// && intenG != -1 && intenB != -1) {
          // sendStatus(id, inten);
          strip.setPixelColor(id, intenR, intenR, intenR);
        }
      }
    }else{
      Serial.read();// let's consume a byte
    }
  }

  strip.show();
  delay(10); // delay in between reads for stability
  // sendStatus(0,0);
  return;
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
      ledState = !ledState;
      float speed = -1;
      if (revStartTime > 0) {
        unsigned long ellapsed = now - revStartTime;
        speed = 1000.f / ellapsed;
      }
      sendStatus(speed, reading);
      revStartTime = now;
    }
    inPeak = 1;
  } else {
    inPeak = 0;
  }
  if (now - lastIdleCheckTime > IdleInterval) {
    resetReadings();
    sendStatus(0, 0);
    lastIdleCheckTime = now;
  }
  digitalWrite(LED_BUILTIN, ledState);
  delay(10); // delay in between reads for stability
}