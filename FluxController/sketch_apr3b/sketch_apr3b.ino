#include "SPI.h"
#include "Adafruit_WS2801.h"

uint8_t dataPin  = 2;    // Yellow wire on Adafruit Pixels
uint8_t clockPin = 3;    // Green wire on Adafruit Pixels
int nbLeds = 2;


Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);

void setup() {
  strip.begin();
  strip.show();  
}

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
}

