/// SENDER Code

#include <AltSoftSerial.h>
#define BOARD_ID 1
// software serial #1: RX = digital pin 7, TX = digital pin 8
AltSoftSerial outSerial(7,8);

// software serial #2: RX = digital pin 9, TX = digital pin 10
AltSoftSerial inSerial(9,10);


int readSensorsEveryMs = 20;
int sendSensorsEveryMs = 2000;


unsigned long lastTimeReadSensors = 0;
unsigned long lastTimeSentSensors = 0;

#define SERIAL_DEBUG

void setup() {
  setupSensors();
  pinMode(LED_BUILTIN, OUTPUT);
  outSerial.begin(9600);
  inSerial.begin(9600);
  inSerial.listen();

#ifdef SERIAL_DEBUG
  Serial.begin(9600);
#endif

}



void relayData(){
  
  while (inSerial.available() > 0) {
    char inByte = inSerial.read();
    outSerial.write(inByte);
#ifdef SERIAL_DEBUG
    Serial.write(inByte);
#endif
  }
}


void loop() {
  relayData();
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
