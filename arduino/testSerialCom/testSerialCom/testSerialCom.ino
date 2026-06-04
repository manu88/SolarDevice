#include "proto.hpp"
#include <FastLED.h>



/////////////////////////////////
const int numReadings = 50;
int readings[numReadings];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average

const int minPeakDiff = 20;

unsigned long revStartTime = 0;
unsigned long lastIdleCheckTime = 0;
const unsigned long IdleInterval = 5000;

int inputPin = A0;
int inPeak = 0;
/////////////////////////////////

#define NUM_LEDS 24
#define DATA_PIN 3 // Change this to match your LED strip's data pin
#define CLOCK_PIN 13
#define BRIGHTNESS 255

CRGB leds[NUM_LEDS];

void setAll(int r, int g, int b) {
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

  resetReadings();

  setAll(255, 255, 255);

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

uint8_t checksum(const byte *data, size_t dataLength) {
  uint8_t value = 0;
  for (size_t i = 0; i < dataLength; i++) {
    value += data[i];
  }
  return value;
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
      parserState = ParserState_CRC;
    }
    return 0;
  }
  case ParserState_CRC: {
    if (Serial.available() == 0) {
      return 0;
    }
    uint8_t expectedCrc = 0;
    if (Serial.readBytes(&expectedCrc, 1) != 1) {
      return 0;
    }
    uint8_t crc = checksum(payload, expectedPayloadSize);
    if (crc != expectedCrc) {
      Serial.print("Mismatch : Expected crc: ");
      Serial.print(expectedCrc);
      Serial.print(" Calc crc: ");
      Serial.println(crc);
      resetParserState();
      return 0;
    }
    return 1;
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
  loopSensor();
  // delay(10);
}

void loopSensor() {
  total = total - readings[readIndex];

  int val = analogRead(inputPin);
  readings[readIndex] = val;

  total = total + readings[readIndex];
  readIndex = readIndex + 1;

  
  if (readIndex >= numReadings) {
    readIndex = 0;
  }

  // calculate the average:
  average = total / numReadings;

  unsigned long now = millis();
  int reading = val > average + minPeakDiff;
  
  if (reading ){
    lastIdleCheckTime = now;
    if(inPeak == 0){
      float speed = -1;
      if (revStartTime > 0){
        unsigned long ellapsed = now - revStartTime;
        speed = 1000.f/ellapsed;
      }
      sendStatus(speed, reading);
      revStartTime = now;
    }
    inPeak = 1;
  }else{
    inPeak = 0;
  }
  if (now - lastIdleCheckTime >IdleInterval){
    resetReadings();
    sendStatus(0, 0);
    lastIdleCheckTime = now;
  }
  delay(2);
}

void resetReadings(){
  for (int i = 0; i < i; i++) {
    readings[i] = 0;
  }
}

void sendStatus(float speed, int activity){
  Serial.print(speed);
  Serial.print(" ");
  Serial.print(activity);
  Serial.print(";\n");
}
