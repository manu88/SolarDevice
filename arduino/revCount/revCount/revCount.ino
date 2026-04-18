

const int numReadings = 50;

int readings[numReadings];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average

const int minPeakDiff = 20;

int ledState = HIGH;

unsigned long revStartTime = 0;
int inputPin = A0;

void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  // initialize all the readings to 0:
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}


int inPeak = 0;
void loop() {
  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  int val = analogRead(inputPin);
  readings[readIndex] = val;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average = total / numReadings;

  unsigned long now = millis();
  int reading = val > average + minPeakDiff;
  if (reading ){
    if(inPeak == 0){
      ledState = !ledState;
      if (revStartTime > 0){
        unsigned long ellapsed = now - revStartTime;
        float speed = 1000.f/ellapsed;
        Serial.print("speed:");
        Serial.println(speed);
        
      }
      revStartTime = now;
    }
    inPeak = 1;
  }else{
    inPeak = 0;
  }

  digitalWrite(LED_BUILTIN, ledState);
  delay(10);  // delay in between reads for stability
}