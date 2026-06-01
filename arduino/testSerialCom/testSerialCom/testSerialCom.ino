#include "proto.hpp"

void setup() {
  Serial.begin(19200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

static ParserState parserState = ParserState_Start;
static uint8_t expectedPayloadSize = 0;
static uint8_t currentPayloadSize = 0;

void resetParserState() {
  Serial.println("reset parser state");
  parserState = ParserState_Start;
  expectedPayloadSize = 0;
  currentPayloadSize = 0;
}

int parseInput() {
  Serial.print("Parser state:");
  Serial.println(parserState);
  switch (parserState) {
  case ParserState_Start: {
    uint8_t input = 0;
    if (Serial.readBytes(&input, 1) != 1) {
      return 0;
    }
    if (input == BYTE_START) {
      parserState = ParserState_PayloadSize;
      Serial.println("Got START");
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
    if (Serial.available() == 0) {
      return 0;
    }
    uint8_t data = 0;
    if (Serial.readBytes(&data, 1) != 1) {
      return 0;
    }
    currentPayloadSize += 1;
    if (currentPayloadSize == expectedPayloadSize) {
      Serial.println("Got all payload");
      return 1;
    }
  }
  default:
    Serial.print("UNHANDLED Parser state:");
    Serial.println(parserState, HEX);
  } // end switch
  return 0;
}

int i = 0;
void loop() {
#if 0
  if(Serial.available() >0){
    uint8_t d;
    Serial.readBytes(&d,1);
    Serial.print(d, HEX);
    i++;
    if(i==8){
      Serial.println("");
    }
  }
  delay(100);
  return;
#endif
  while (Serial.available() > 0) {
    if (parseInput()) {
      Serial.println("Got entire msg");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      resetParserState();
    }
  }

  delay(10);
}
