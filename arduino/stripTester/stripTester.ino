#include <FastLED.h>

#if (FASTLED_VERSION != 3001000)
#error ("Invalid Fastled version, expected 3001000")
#endif
// Fastled version 3.1.0
#define NUM_LEDS 12
#define DATA_PIN 11
#define CLOCK_PIN 13
#define BRIGHTNESS 255

CRGB leds[NUM_LEDS];

void set(int x, int r, int g, int b) { leds[x] = CRGB(r, g, b); }

void setAll(int r, int g, int b) {
  for (int x = 0; x < NUM_LEDS; x++) {
    leds[x] = CRGB(r, g, b);
  }
}

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {

  Serial.println("White");
  setAll(255, 255, 255);
  FastLED.show();
  delay(2000);

  Serial.println("Red");
  setAll(255, 0, 0);
  FastLED.show();
  delay(2000);

  Serial.println("GReen");
  setAll(0, 255, 0);
  FastLED.show();

  delay(2000);

  Serial.println("Blue");
  setAll(0, 0, 255);
  FastLED.show();
  delay(2000);
}
