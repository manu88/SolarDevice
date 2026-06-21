/// SENDER Code

#include <AltSoftSerial.h>
#include <SoftwareSerial.h>
#define BOARD_ID 1
// software serial #1: RX = digital pin 7, TX = digital pin 8
SoftwareSerial outSerial(7,8);

// software serial #2: RX = digital pin 9, TX = digital pin 10
SoftwareSerial inSerial(9,10);


int readSensorsEveryMs = 20;
int sendSensorsEveryMs = 2000;


unsigned long lastTimeReadSensors = 0;
unsigned long lastTimeSentSensors = 0;

#define SERIAL_DEBUG


extern "C"{
  #define START_VAL 0XAB
  #define END_VAL 0XEF
  typedef struct{
    uint8_t start;
    uint8_t boardId;
    float v[3];
    uint8_t end;
  }SensorMsg;
}

void setup() {
  setupSensors();
  pinMode(LED_BUILTIN, OUTPUT);
  outSerial.begin(9600);
  inSerial.begin(9600);
  inSerial.listen();

#ifdef SERIAL_DEBUG
  Serial.begin(9600);
  Serial.println("SensorSender");
#endif

}




void relayData2(){
  static uint8_t readerState = 0;
  static uint8_t boardId = -1;
  static uint8_t currentFloatReadPos = 0;
  static float v[3] = {0};
  inSerial.listen();
  while (inSerial.available() > 0) {
    switch(readerState){
      case 0:// Waiting for start;
      {
        uint8_t inByte = inSerial.read();
        if (inByte == START_VAL){
          readerState = 1;
          currentFloatReadPos = 0;
        }
        break;
      }
      case 1:// boardId
      {
        boardId = inSerial.read();
        readerState = 2;
        break;
      }
      case 2:// float values
      {
        char *readPos = ((char*)v) + currentFloatReadPos;
        size_t ret = inSerial.readBytes(readPos, 3*sizeof(float));
        currentFloatReadPos += ret;
        if (currentFloatReadPos < 3*sizeof(float)){
          currentFloatReadPos = ret;
        }else{
          readerState = 3;
        }
        break;
      }
      case 3:// end val;
      {
        uint8_t inByte = inSerial.read();
        if (inByte == END_VAL){
          sendMsgSensor(boardId, v);
          #ifdef SERIAL_DEBUG
          sendASCIIMsgSensor(boardId, v);
          #endif
          readerState = 0;
          boardId = -1;
          currentFloatReadPos = 0;
          v[0] = 0;
          v[1] = 0;
          v[2] = 0;
        }
      }
    }
    
    //Serial.write(inByte);
  }

}



void loop() {
  relayData2();
  handleLoopSensors();
}

int ledState = 0;
void handleLoopSensors(){
  unsigned long now = millis();
  if (now - lastTimeReadSensors >= readSensorsEveryMs) {
    //loopSensors();
    lastTimeReadSensors = now;
  }
  now = millis();

  if (now - lastTimeSentSensors >= sendSensorsEveryMs) {
    digitalWrite(LED_BUILTIN, ledState);
    ledState = !ledState;
    lastTimeSentSensors = now;
    sendSensors();
  }

}
