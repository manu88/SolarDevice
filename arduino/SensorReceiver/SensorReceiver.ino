#include <SoftwareSerial.h>


// software serial #2: RX = digital pin 7, TX = digital pin 8
SoftwareSerial portTwo(7,8);

void setup()
{
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  portTwo.begin(9600);
}

void loop()
{
  // Now listen on the second port
  portTwo.listen();
  // while there is data coming in, read it
  // and send to the hardware serial port:
  //Serial.println("Data from port two:");
  while (portTwo.available() > 0) {
    char inByte = portTwo.read();
    Serial.write(inByte);
  }

  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);

}






