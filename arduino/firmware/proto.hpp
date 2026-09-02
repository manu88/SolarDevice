#pragma once

#define BYTE_START (uint8_t)0XAF

extern "C" {

typedef struct {
  uint8_t start;
  uint8_t cmd;
  uint8_t payloadSize;
  // uint8_t payload[payloadSize];
  uint8_t crc;
} ComHeader;

typedef enum {
  ParserState_Start = 0,
  ParserState_Cmd = 1,
  ParserState_PayloadSize = 2,
  ParserState_Payload = 3,
  ParserState_CRC = 4,
} ParserState;

typedef struct {
  uint8_t start;
  uint8_t size;
  uint8_t com_size;
} ComResponse;

typedef enum {
  CmdId_Invalid = 0,
  CmdId_Leds = 0XBC,
  CmdId_Dump = 0XBD,
  CmdId_StartMotor = 0XAF,
} CmdId;

} // extern "C"
