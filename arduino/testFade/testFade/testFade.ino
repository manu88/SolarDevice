#include "Adafruit_WS2801.h"

uint8_t dataPin = 3;  // Yellow wire on Adafruit Pixels
uint8_t clockPin = 13; // Green wire on Adafruit Pixels
int nbLeds = 6;

int ledFadeTime = 20;
Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);

void setup() {
  strip.begin();
  strip.show();
  //setAll(255,255,255);
}

/*
Midi 255 255 255

Matin 224 36 0

Nuit 0 36 69

Soir 88 11 30
*/

void loop() {
  rgbFadeInAndOut2(255,255, 255, ledFadeTime);
}

void setAll(uint8_t red, uint8_t green, uint8_t blue) {
  for(uint8_t b = 0; b <255; b++) {
     for(uint8_t i=0; i < nbLeds; i++) {
        strip.setPixelColor(i, red * b/255, green * b/255, blue * b/255);
     }
  }
   strip.show();
}

void rgbFadeInAndOut(uint8_t red, uint8_t green, uint8_t blue, uint8_t wait) {
  for(uint8_t b = 0; b <255; b++) {
     for(uint8_t i=0; i < nbLeds; i++) {
        strip.setPixelColor(i, red * b/255, green * b/255, blue * b/255);
     }

     strip.show();
     delay(wait);
  }

  for(uint8_t b=255; b > 0; b--) {
     for(uint8_t i = 0; i < nbLeds; i++) {
        strip.setPixelColor(i, red * b/255, green * b/255, blue * b/255);
     }
     strip.show();
     delay(wait);
  }
}

void rgbFadeInAndOut2(uint8_t red, uint8_t green, uint8_t blue, uint8_t wait) {
  for(uint8_t b = 0; b <200; b++) {
     for(uint8_t i=0; i < nbLeds; i++) {
        strip.setPixelColor(i, b, b,b);
     }

     strip.show();
     delay(wait);
  }

  for(uint8_t b=200; b > 0; b--) {
     for(uint8_t i = 0; i < nbLeds; i++) {
        strip.setPixelColor(i, b, b,b);
     }
     strip.show();
     delay(wait);
  }
}
