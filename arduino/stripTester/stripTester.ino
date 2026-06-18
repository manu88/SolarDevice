#include <FastLED.h>


#define NUM_LEDS 27
#define DATA_PIN 3 // Change this to match your LED strip's data pin
#define CLOCK_PIN 13
#define BRIGHTNESS 255


CRGB leds[NUM_LEDS];

void set(int x, int r,int g,int b) {
  leds[x] = CRGB(r, g, b);
}

void setAll(int r,int g,int b) {
  for (int x = 0; x < NUM_LEDS; x++) {
    leds[x] = CRGB(r, g, b);
  }
  
}

void setup() {
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}

void chenillard(int x){
  setAll(0,0,0);
  set(x,x %2==0?255:0 ,0,x %2==0?0:255);
}

int index = 0;
void loop(){
  chenillard(index);
  index++;
  if (index>=NUM_LEDS){
    index = 0;
  }
  FastLED.show();
  delay(100);
}

void loop2() {
  setAll(255,255,255);
  FastLED.show();
  delay(2000);

  setAll(0,0,0);
  FastLED.show();  
  delay(2000);
  return;
  setAll(0,255,0);
  FastLED.show();
  delay(2000);  

  setAll(0,0,255);
  FastLED.show();
  delay(2000);
}
