#include <FastLED.h>
#include "proto.hpp"


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
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  setAll(255,255,255);

  Serial.println("Connected");
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

uint16_t checksum(const byte *data, size_t dataLength)
{
  uint16_t value = 0;
  for (size_t i = 0; i < dataLength; i++)
  {
    value += data[i];
    //value ^= data[2*i] + (data[2*i+1] << 8);
  }
  return value;
  //if(dataLength%2) value ^= data[dataLength - 1];
  //return ~value;
}


int parseInput() {
  // Serial.print("Parser state:");
  // Serial.println(parserState);
  switch (parserState) {
  case ParserState_Start: {
    uint8_t input = 0;
    if (Serial.readBytes(&input, 1) != 1) {
      return 0;
    }
    if (input == BYTE_START) {
      parserState = ParserState_PayloadSize;
      // Serial.println("Got START");
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

    // Serial.print("Got SIZE:");
    // Serial.println((uint8_t)size, HEX);
    expectedPayloadSize = size;
    parserState = ParserState_Payload;
    return 0;
  }
  case ParserState_Payload: {
    if (Serial.available() == 0) {
      return 0;
    }

    // Serial.print("Read payload, size:");
    // Serial.println((uint8_t)expectedPayloadSize, HEX);
    size_t read = Serial.readBytes(payload, expectedPayloadSize);
    if (read == 0) {
      return 0;
    }
    currentPayloadSize += read;
    if (currentPayloadSize == expectedPayloadSize) {
      // Serial.println("Got all payload");
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
      uint16_t checksum = checksum(payload,expectedPayloadSize);
      Serial.print("expectedPayloadSize:");
      Serial.println(expectedPayloadSize, HEX);
      Serial.print("Checksum:");
      Serial.println(checksum, HEX);
      for (int i = 0; i < expectedPayloadSize; i++) {
        if (i >= NUM_LEDS) {
          continue;
        }
        int r = payload[i * 3];
        int g = payload[(i * 3) + 1];
        int b = payload[(i * 3) + 2];
        leds[i] = CRGB(r, g, b);
      }
      FastLED.show();

      resetParserState();
    }
  }

  // delay(10);
}
