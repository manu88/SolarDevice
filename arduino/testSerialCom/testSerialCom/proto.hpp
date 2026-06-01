#pragma once

#define BYTE_START (uint8_t)0XAF

extern "C" {

typedef struct {
  uint8_t start;
  uint8_t payloadSize;

} ComHeader;

typedef enum {
  ParserState_Start,
  ParserState_PayloadSize,
  ParserState_Payload,
} ParserState;

typedef struct {
  uint8_t start;
  uint8_t size;
  uint8_t com_size;
} ComResponse;

} // extern "C"
