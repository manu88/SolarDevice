#include <AltSoftSerial.h>
#include <SoftwareSerial.h>

// software serial #2: RX = digital pin 9, TX = digital pin 10
SoftwareSerial inSerial(9,10);

extern "C"{
  #define START_VAL  0XAB
  #define END_VAL  0XEF
  typedef struct{
    uint8_t start;
    uint8_t boardId;
    float v[3];
    uint8_t end;
  }SensorMsg;
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  inSerial.begin(9600);
  Serial.println("SensorReceiver");
}

void sendASCIIMsgSensor(uint8_t boardId, const float *v){
  Serial.print("S");
  Serial.print(boardId);
  Serial.print(" ");
  Serial.print(v[0]);
  Serial.print(" ");
  Serial.print(v[1]);
  Serial.print(" ");
  Serial.print(v[2]);
  Serial.println();
}

void relayFinalData(){
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
          sendASCIIMsgSensor(boardId, v);
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

void loop()
{
  relayFinalData();

}






