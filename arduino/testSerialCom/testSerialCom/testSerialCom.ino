#include "proto.hpp"
#include "Adafruit_WS2801.h"


uint8_t dataPin = 3;  // Yellow wire on Adafruit Pixels
uint8_t clockPin = 13; // Green wire on Adafruit Pixels
int nbLeds = 24;

Adafruit_WS2801 strip = Adafruit_WS2801(nbLeds, dataPin, clockPin, WS2801_RGB);

void setAll(uint8_t red, uint8_t green, uint8_t blue) {
  for(uint8_t b = 0; b <255; b++) {
     for(uint8_t i=0; i < nbLeds; i++) {
        strip.setPixelColor(i, red * b/255, green * b/255, blue * b/255);
     }
  }
   strip.show();
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  strip.begin();
  strip.show();

  //setAll(100,100,100);
}

static ParserState parserState = ParserState_Start;
static uint8_t expectedPayloadSize = 0;
static uint8_t currentPayloadSize = 0;


#define PAYLOAD_SIZE 72
static uint8_t payload[PAYLOAD_SIZE];

void resetParserState() {
  // Serial.println("reset parser state");
  parserState = ParserState_Start;
  expectedPayloadSize = 0;
  currentPayloadSize = 0;
  memset(payload, 0, PAYLOAD_SIZE);
}

int parseInput() {
  //Serial.print("Parser state:");
  //Serial.println(parserState);
  switch (parserState) {
  case ParserState_Start: {
    uint8_t input = 0;
    if (Serial.readBytes(&input, 1) != 1) {
      return 0;
    }
    if (input == BYTE_START) {
      parserState = ParserState_PayloadSize;
      //Serial.println("Got START");
    }
    break;
  }
  case ParserState_PayloadSize: {
    if (Serial.available() == 0) {
      return 0;
    }
    uint8_t size = 0;
    if (Serial.readBytes(&size, 1) != 1) {
      return 0;
    }

    //Serial.print("Got SIZE:");
    //Serial.println((uint8_t)size, HEX);
    expectedPayloadSize = size;
    parserState = ParserState_Payload;
    return 0;
  }
  case ParserState_Payload: {
    if (Serial.available() == 0) {
      return 0;
    }
    
    //Serial.print("Read payload, size:");
    //Serial.println((uint8_t)expectedPayloadSize, HEX);
    size_t read = Serial.readBytes(payload, expectedPayloadSize);
    if (read == 0) {
      return 0;
    }
    currentPayloadSize += read;
    if (currentPayloadSize == expectedPayloadSize) {
      //Serial.println("Got all payload");
      return 1;
    }
    return 0;
  }
  default:
    Serial.print("UNHANDLED Parser state:");
    Serial.println(parserState, HEX);
  } // end switch
  return 0;
}

void loop() {
  while (Serial.available() > 0) {
    if (parseInput()) {
      for(int i=0;i<24;i++){
        if(i >= nbLeds){
          continue;
        }
        int r = payload[i*3];
        int g = payload[(i*3)+1];
        int b = payload[(i*3)+2];
        strip.setPixelColor(i, r, g, b);
      }
      strip.show();
      resetParserState();
    }
  }

  //delay(10);
}
