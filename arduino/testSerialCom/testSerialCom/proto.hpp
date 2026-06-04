#pragma once

#define BYTE_START (uint8_t)0XAF

extern "C" {

typedef struct {
  uint8_t start;
  uint8_t payloadSize;
  //uint8_t payload[payloadSize];
  uint8_t crc;
} ComHeader;

typedef enum {
  ParserState_Start = 0,
  ParserState_PayloadSize = 1,
  ParserState_Payload = 2,
  ParserState_CRC = 3,
} ParserState;

typedef struct {
  uint8_t start;
  uint8_t size;
  uint8_t com_size;
} ComResponse;

} // extern "C"
