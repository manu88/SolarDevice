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
int nbLeds = 2;
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);



void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }

  strip.begin();
  strip.show(); 
}


int inPeak = 0;


int intensity = 100;


void loop() {

  if (Serial.available() > 0) {
    int inByte = Serial.read();
    intensity = inByte;
  }

  for (int i=0;i<nbLeds;i++){
    strip.setPixelColor(i, intensity,intensity ,intensity);
  }

  strip.show();

  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  int val = analogRead(inputPin);
  readings[readIndex] = val;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
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
      Serial.print("activity:");
      Serial.println(reading);
      if (revStartTime > 0){
        unsigned long ellapsed = now - revStartTime;
        float speed = 1000.f/ellapsed;
        Serial.print("speed:");
        Serial.println(speed);
        
      }
      revStartTime = now;
    }
    inPeak = 1;
  }else{
    inPeak = 0;
  }
  if (now - lastIdleCheckTime >IdleInterval){
    Serial.print("speed:");
    Serial.println(0);
    lastIdleCheckTime = now;
  }
  digitalWrite(LED_BUILTIN, ledState);
  delay(10);  // delay in between reads for stability
}