#include "Adafruit_WS2801.h"

const int numReadings = 50;

int readings[numReadings];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average

const int minPeakDiff = 20;

int ledState = HIGH;

unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;


//Leds part

uint8_t dataPin  = 2;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 3;    // Green wire on Adafruit Pixels
int nbLeds = 4;
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);

void resetReadings(){
  for (int i = 0; i < i; i++) {
    readings[i] = 0;
  }
}


void setup() {
  resetReadings();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  
}


int inPeak = 0;


int intensity = 0;
int intensity1 = 0;
int intensity2 = 0;
int intensity3 = 0;

void sendStatus(float speed, int activity){
  Serial.print(speed);
  Serial.print(" ");
  Serial.print(activity);
  Serial.print(" ");
  Serial.print(intensity);
  Serial.print(" ");
  Serial.print(intensity1);
  Serial.print(";\n");
}

void loop() {


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
  
  if (reading ){
    lastIdleCheckTime = now;
    if(inPeak == 0){
      ledState = !ledState;
      float speed = -1;
      if (revStartTime > 0){
        unsigned long ellapsed = now - revStartTime;
        speed = 1000.f/ellapsed;
      }
      sendStatus(speed, reading);
      revStartTime = now;
    }
    inPeak = 1;
  }else{
    inPeak = 0;
  }
  if (now - lastIdleCheckTime >IdleInterval){
    resetReadings();
    sendStatus(0, 0);
    lastIdleCheckTime = now;
  }
  digitalWrite(LED_BUILTIN, ledState);
  delay(10);  // delay in between reads for stability
}