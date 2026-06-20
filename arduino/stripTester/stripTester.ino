#include <FastLED.h>

// Fastled version 3.1.0
#define NUM_LEDS 26
#define DATA_PIN 11// Change this to match your LED strip's data pin
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
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS, DATA_RATE_MHZ(25));
  FastLED.setBrightness(BRIGHTNESS);
}

void chenillard(int x){
  setAll(0,0,0);
  set(x,x %2==0?255:0 ,0,x %2==0?0:255);
}

static int index_ = 0;
void loop1(){
  chenillard(index_);
  index_++;
  if (index_>=NUM_LEDS){
    index_ = 0;
  }
  FastLED.show();
  delay(100);
}

void loop() {
  setAll(255,255,255);
  FastLED.show();
  delay(2000);

  setAll(255,0,0);
  FastLED.show();  
  delay(2000);

  setAll(0,255,0);
  FastLED.show();
  delay(2000);  

  setAll(0,0,255);
  FastLED.show();
  delay(2000);
}

int inten = 0;
int dir = 1;

void loop34() {
  setAll(inten,0,0);
  FastLED.show();
  FastLED.delay(40);

  inten += dir*10;
  if(inten >255){
    dir = -1;
    inten = 255;
  }else if(inten <=0){
    dir = 1;
    inten = 0;
  }
}
  
