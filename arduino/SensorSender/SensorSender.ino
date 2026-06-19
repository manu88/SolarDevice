/// SENDER Part

#include <SoftwareSerial.h>

// software serial #1: RX = digital pin 7, TX = digital pin 8
SoftwareSerial portOne(7,8);

// software serial #2: RX = digital pin 9, TX = digital pin 10
SoftwareSerial portTwo(9,10);


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  portOne.begin(9600);
  portTwo.begin(9600);

}

void loop() {
  portTwo.listen();
  // while there is data coming in, read it
  // and send to the hardware serial port:
  //Serial.println("Data from port two:");
  while (portTwo.available() > 0) {
    char inByte = portTwo.read();
    portOne.write(inByte);
  }

  portOne.println("Hello-1");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
