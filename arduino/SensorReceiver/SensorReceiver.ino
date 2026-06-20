#include <SoftwareSerial.h>


SoftwareSerial inSerial(7,8);

void setup()
{
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

  inSerial.begin(9600);
}



void relayFinalData(){
  inSerial.listen();
  while (inSerial.available() > 0) {
    char inByte = inSerial.read();
    Serial.write(inByte);
  }
}

void loop()
{
  relayFinalData();

}






