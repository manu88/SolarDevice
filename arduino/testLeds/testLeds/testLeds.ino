#include "Adafruit_WS2801.h"


unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;


//Leds part

int nbLeds = 2;
uint8_t dataPin  = 2;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 3;    // Green wire on Adafruit Pixels
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);



int intensity = 255;



void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  

  strip.begin();
  strip.show();

  strip.setPixelColor(0, intensity, intensity, intensity);
  strip.setPixelColor(1, intensity, intensity, intensity);
}


int inPeak = 0;



void sendStatus(int id, int val){
  Serial.print(id);
  Serial.print(" ");
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
  delay(10);  // delay in between reads for stability
  //sendStatus(0,0);
  
}