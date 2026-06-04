#include <FastLED.h>


#define NUM_LEDS 24
#define DATA_PIN 3 // Change this to match your LED strip's data pin
#define CLOCK_PIN 13
#define BRIGHTNESS 255


CRGB leds[NUM_LEDS];

void setAll(int r,int g,int b) {
  for (int x = 0; x < NUM_LEDS; x++) {
    leds[x] = CRGB(r, g, b);
  }
  FastLED.show();
}

void setup() {
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}


void loop() {
  setAll(255,255,255);
  delay(2000);
  setAll(255,0,0);
  delay(2000);
  setAll(0,255,0);
  delay(2000);
  setAll(0,0,255);
  delay(2000);
}
