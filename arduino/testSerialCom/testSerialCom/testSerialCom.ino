#include "proto.hpp"

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
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

    Serial.print("Got SIZE:");
    Serial.println((uint8_t)size, HEX);
    expectedPayloadSize = size;
    parserState = ParserState_Payload;
    return 0;
  }
  case ParserState_Payload: {
    if (Serial.available() == 0) {
      return 0;
    }
    
    if (Serial.readBytes(payload, PAYLOAD_SIZE) != 1) {
      return 0;
    }
    currentPayloadSize += 1;
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
      Serial.print("MSG:");
      Serial.println(payload[0], HEX);
      resetParserState();
    }
  }

  delay(10);
}
