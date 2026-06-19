/// SENDER Code

#include <SoftwareSerial.h>
#define BOARD_ID 2
#define SEND_DELAY 400
// software serial #1: RX = digital pin 7, TX = digital pin 8
SoftwareSerial outSerial(7,8);

// software serial #2: RX = digital pin 9, TX = digital pin 10
SoftwareSerial inSerial(9,10);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  outSerial.begin(9600);
  inSerial.begin(9600);

}

void sendSensors(float v0, float v1, float v2){
  outSerial.print("S");
  outSerial.print(BOARD_ID);
  outSerial.print(" ");
  outSerial.print(v0);
  outSerial.print(" ");
  outSerial.print(v1);
  outSerial.print(" ");
  outSerial.print(v2);
  outSerial.println();
}

void relayData(){
  inSerial.listen();
  while (inSerial.available() > 0) {
    char inByte = inSerial.read();
    outSerial.write(inByte);
  }
}

int ledState = 0;
void loop() {
  relayData();

  sendSensors(BOARD_ID*2.2, BOARD_ID*3.3,BOARD_ID*4.4 );
  digitalWrite(LED_BUILTIN, HIGH);
  delay(SEND_DELAY);
  digitalWrite(LED_BUILTIN, ledState);
  ledState = !ledState;
}
