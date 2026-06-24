#include "proto.hpp"
#include <AltSoftSerial.h>
#include <FastLED.h>

// Fastled version 3.1.0
#if (FASTLED_VERSION != 3001000)
#error ("Invalid Fastled version, expected 3001000")
#endif

#define FIRMWARE_VERSION "0.0.7"

unsigned long numCRCErrors = 0;

/////////////////////////////////

int sendSensorsEveryMs = 2000;
unsigned long lastTimeSentSensors = 0;

int readSensorsEveryMs = 10;
unsigned long lastTimeReadSensors = 0;

#define NUM_LEDS 26
#define DATA_PIN 11 // Change this to match your LED strip's data pin
#define CLOCK_PIN 13
#define BRIGHTNESS 255

CRGB leds[NUM_LEDS];

void setAll(int r, int g, int b) {
  for (int x = 0; x < NUM_LEDS; x++) {
    leds[x] = CRGB(r, g, b);
  }
  FastLED.show();
}

/////////////////////////////////

// only using RX, no need to wire TX
// Arduino Uno  TX=9 RX=8
AltSoftSerial inSerial;

extern "C" {
#define START_VAL 0XAB
#define END_VAL 0XEF
typedef struct {
  uint8_t start;
  uint8_t boardId;
  float v[3];
  uint8_t isRotating[3];
  uint8_t end;
} SensorMsg;
}

/////////////////////////////////

void setup() {
  Serial.begin(115200);
  inSerial.begin(19200);
  FastLED.addLeds<WS2801, DATA_PIN, CLOCK_PIN, RGB>(
      leds, NUM_LEDS); //, DATA_RATE_MHZ(8));
  FastLED.setBrightness(BRIGHTNESS);

  setupSensors();

  setAll(0, 0, 0);

  Serial.println("Connected");
  Serial.print("Version: ");
  Serial.println(FIRMWARE_VERSION);
}

static ParserState parserState = ParserState_Start;
static CmdId currentCmd = CmdId_Invalid;
static uint8_t expectedPayloadSize = 0;
static uint8_t currentPayloadSize = 0;

#define PAYLOAD_SIZE 78
static uint8_t payload[PAYLOAD_SIZE];

void resetParserState() {
  // Serial.println("reset parser state");
  parserState = ParserState_Start;
  expectedPayloadSize = 0;
  currentPayloadSize = 0;
  currentCmd = CmdId_Invalid;
  memset(payload, 0, PAYLOAD_SIZE);
}

uint8_t checksum(const byte *data, unsigned int dataLength) {
  uint8_t value = 0;
  for (unsigned int i = 0; i < dataLength; i++) {
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
      parserState = ParserState_Cmd;
      // Serial.println("Got START");
    }
    break;
  }
  case ParserState_Cmd: {
    uint8_t input = 0;
    if (Serial.readBytes(&input, 1) != 1) {
      return 0;
    }
    currentCmd = (CmdId)input;
    parserState = ParserState_PayloadSize;
  }
  case ParserState_PayloadSize: {
    if (Serial.available() == 0) {
      return 0;
    }
    uint8_t size = 0;
    if (Serial.readBytes(&size, 1) != 1) {
      return 0;
    }

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
    size_t read =
        Serial.readBytes(payload, expectedPayloadSize + currentPayloadSize);
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
      Serial.print(crc);

      Serial.println("");
      for (int i = 0; i < expectedPayloadSize; i++) {
        if (i % 8 == 0) {
          Serial.println("");
        }
        Serial.print("0x");
        Serial.print(payload[i], HEX);
        Serial.print(", ");
      }
      Serial.println("");
      numCRCErrors += 1;
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

void processDump() {
  Serial.println("arduino DUMP\n");
  for (int i = 0; i < NUM_LEDS; i++) {
    Serial.print(i);
    Serial.print(" :");
    Serial.print(leds[i].raw[0], HEX);
    Serial.print(" ");
    Serial.print(leds[i].raw[1], HEX);
    Serial.print(" ");
    Serial.print(leds[i].raw[2], HEX);
    Serial.println("");
  }

  Serial.print("numCRCErrors: ");
  Serial.println(numCRCErrors);
}

void processCmd() {
  switch (currentCmd) {
  case CmdId_Invalid:
    Serial.println("Invalid cmdID: CmdId_Invalid");
    return;
  case CmdId_Leds:
    processCmdLed();
    return;
  case CmdId_Dump:
    processDump();
    return;
  default:
    Serial.print("Invalid cmdID: ");
    Serial.println(currentCmd, HEX);
  }
}

void processCmdLed() {
  if (expectedPayloadSize != PAYLOAD_SIZE) {
    Serial.print("unexpected expectedPayloadSize: ");
    Serial.println(expectedPayloadSize);
  } else {
    for (int i = 0; i < NUM_LEDS; i += 1) {
      int r = payload[i * 3];
      int g = payload[(i * 3) + 1];
      int b = payload[(i * 3) + 2];
      leds[i] = CRGB(r, g, b);
    }
    FastLED.show();
  }
}

void sendASCIIMsgSensor(uint8_t boardId, const float *v, const int isRotating[3]) {
  Serial.print("S");
  Serial.print(boardId);
  Serial.print(" ");
  Serial.print(v[0]);
  Serial.print(" ");
  Serial.print(isRotating[0]);
  Serial.print(" ");
  Serial.print(v[1]);
  Serial.print(" ");
  Serial.print(isRotating[1]);
  Serial.print(" ");
  Serial.print(v[2]);
  Serial.print(" ");
  Serial.print(isRotating[2]);
  Serial.println();
}

void relayFinalData() {
  static uint8_t readerState = 0;
  static uint8_t boardId = -1;
  static uint8_t currentFloatReadPos = 0;
  static float v[3] = {0};
  static int isRotating[3] = {0};
  static uint8_t rcvIsRotatingIndex = 0;
  inSerial.listen();
  while (inSerial.available() > 0) {
    switch (readerState) {
    case 0: // Waiting for start;
    {
      uint8_t inByte = inSerial.read();
      if (inByte == START_VAL) {
        readerState = 1;
        currentFloatReadPos = 0;
      }
      break;
    }
    case 1: // boardId
    {
      int v = inSerial.read();
      if(v == -1){
        return;
      }
      boardId = v;
      readerState = 2;
      break;
    }
    case 2: // float values
    {
      char *readPos = ((char *)v) + currentFloatReadPos;
      size_t ret = inSerial.readBytes(readPos, 3 * sizeof(float));
      currentFloatReadPos += ret;
      if (currentFloatReadPos < 3 * sizeof(float)) {
        currentFloatReadPos = ret;
      } else {
        readerState = 3;
      }
      break;
    }
    case 3: // uint8_t values
    {
      int v = inSerial.read();
      if (v == -1){
        return;
      }
      isRotating[rcvIsRotatingIndex] = v;
      rcvIsRotatingIndex++;
      if (rcvIsRotatingIndex==3){
        readerState = 4;
      }
      break;
    }
    case 4: // end val;
    {
      uint8_t inByte = inSerial.read();
      if (inByte == END_VAL) {
        sendASCIIMsgSensor(boardId, v, isRotating);
        readerState = 0;
        boardId = -1;
        currentFloatReadPos = 0;
        rcvIsRotatingIndex = 0;
        v[0] = 0;
        v[1] = 0;
        v[2] = 0;
        isRotating[0] = 0;
        isRotating[1] = 0;
        isRotating[2] = 0;
      }
    }
    }
  }
}

void loop() {
  while (Serial.available() > 0) {
    if (parseInput()) {
      processCmd();
      resetParserState();
    }
  }
  unsigned long now = millis();
  if (now - lastTimeReadSensors >= readSensorsEveryMs) {
    loopSensors();
    lastTimeReadSensors = now;
  }
  relayFinalData();

  now = millis();

  if (now - lastTimeSentSensors >= sendSensorsEveryMs) {
    lastTimeSentSensors = now;
    sendSensors();
  }
}
