/*
 * M5Stack Atom Switch - Serial Relay Controller
 *
 * Protocol: RELAY;<state_relay_1>;<state_relay_2>
 *   state = 0 (open) or 1 (close)
 *
 * LED colors:
 *   RED    => both relays open  (0,0)
 *   BLUE   => relay 1 close, relay 2 open  (1,0)
 *   YELLOW => relay 1 open,  relay 2 close (0,1)
 *   GREEN  => both relays close (1,1)
 */

#include <M5Atom.h>

// Atom Switch relay pins (Grove port on the switch unit)
#define RELAY1_PIN 22
#define RELAY2_PIN 19

bool relay1State = false;
bool relay2State = false;

void setLED(uint8_t r, uint8_t g, uint8_t b) {
  M5.dis.drawpix(0, CRGB(r, g, b));
}

void updateLED() {
  if (!relay1State && !relay2State) {
    setLED(255, 0, 0);       // RED   - both open
  } else if (relay1State && !relay2State) {
    setLED(0, 0, 255);       // BLUE  - relay1 close, relay2 open
  } else if (!relay1State && relay2State) {
    setLED(255, 180, 0);     // YELLOW - relay1 open, relay2 close
  } else {
    setLED(0, 255, 0);       // GREEN - both close
  }
}

void applyRelays() {
  digitalWrite(RELAY1_PIN, relay1State ? HIGH : LOW);
  digitalWrite(RELAY2_PIN, relay2State ? HIGH : LOW);
  updateLED();
}

void processCommand(String cmd) {
  cmd.trim();

  // Expected format: RELAY;0;1
  int firstSep  = cmd.indexOf(';');
  int secondSep = cmd.indexOf(';', firstSep + 1);

  if (firstSep == -1 || secondSep == -1)
  {
    Serial.println("command not supported");
    return;
  } 

  String prefix = cmd.substring(0, firstSep);
  prefix.toUpperCase();
  if (prefix != "RELAY") return;

  int s1 = cmd.substring(firstSep  + 1, secondSep).toInt();
  int s2 = cmd.substring(secondSep + 1).toInt();

  relay1State = (s1 != 0);
  relay2State = (s2 != 0);

  applyRelays();

  // Echo the command back as acknowledgement
  Serial.println(cmd);
}

void setup() {
  M5.begin(true, false, true);  // enable Serial, disable I2C, enable display
  Serial.begin(9600);

  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);

  relay1State = false;
  relay2State = false;
  applyRelays();
}

void loop() {
  M5.update();

  if (Serial.available()) {
    String incoming = Serial.readStringUntil('\n');
    processCommand(incoming);
  }
}
