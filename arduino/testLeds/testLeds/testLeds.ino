#include "Adafruit_WS2801.h"


int inputPin = A0;

// sensor reading logic:
#define NUM_SENSOR_READINGS (int)50
int readings[NUM_SENSOR_READINGS];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average
const int minPeakDiff = 30;
int inPeak = 0;

//Leds part

int nbLeds = 2;
uint8_t dataPin  = 2;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 3;    // Green wire on Adafruit Pixels
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);


int ledState = HIGH;
int intensity = 255;


void resetReadings(){
  for (int i = 0; i < NUM_SENSOR_READINGS; i++) {
    readings[i] = 0;
  }
}


void setup() {
  resetReadings();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  

  strip.begin();
  strip.show();

  strip.setPixelColor(0, intensity, intensity, intensity);
  strip.setPixelColor(1, intensity, intensity, intensity);
}






void sendStatus(int val){
  Serial.print(val);
  Serial.print(";\n");
}


int state = 0;

void serialReadAll(void){
  int numBytes = Serial.available();
  for (int n = 0; n < numBytes; n++) {
    Serial.read();
  }

}


unsigned long startTime;
unsigned long period = 6000;
int blinkstate = 0;

void blinkMode(void){
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - startTime;

  if(elapsedTime < period){
    return;
  }
  
  startTime = currentTime;
  blinkstate = !blinkstate;
  strip.setPixelColor(0, blinkstate*intensity, blinkstate*intensity, blinkstate*intensity);
  strip.setPixelColor(1, blinkstate*intensity, blinkstate*intensity, blinkstate*intensity);
}

void loop() {
  if (Serial.available()) {
    serialReadAll();
    state++;
    Serial.print("Change state to : ");
    Serial.println(state);
    if(state >= 3){
      state = 0;
    }
    switch(state){
    case 0:
      Serial.println("Leds ON");
      break;
    case 1:
      Serial.println("Leds OFF");
      break;
    case 2:
      Serial.println("Leds Blink");
      startTime = millis();
      blinkstate = 0;
      strip.setPixelColor(0, 0, 0, 0);
      strip.setPixelColor(1, 0, 0, 0);
      break;
    }
  }

  switch(state){
    case 0:
    strip.setPixelColor(0, intensity, intensity, intensity);
    strip.setPixelColor(1, intensity, intensity, intensity);
    break;
    case 1:
    strip.setPixelColor(0, 0, 0, 0);
    strip.setPixelColor(1, 0, 0, 0);
    break;
    case 2:
    blinkMode();
    break;
  }

  strip.show();

// Sensor logic


  total = total - readings[readIndex];
  int val = analogRead(inputPin);
  readings[readIndex] = val;
  total = total + readings[readIndex];
  readIndex = readIndex + 1;

  
  if (readIndex >= NUM_SENSOR_READINGS) {
    readIndex = 0;
  }

  // calculate the average:
  average = total / NUM_SENSOR_READINGS;

  unsigned long now = millis();
  int theReading = val > average + minPeakDiff;
  
  if (theReading ){
    if(inPeak == 0){
      inPeak = 1;
      ledState = !ledState;
      sendStatus(1);
    }
    
  }else{
    inPeak = 0;
  }

  digitalWrite(LED_BUILTIN, ledState);
  delay(10);  // delay in between reads for stability
  
}