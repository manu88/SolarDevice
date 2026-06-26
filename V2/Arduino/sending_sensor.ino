// Read 6 analog inputs and send them every second
// Format:
// HALL;value_0;value_1;value_2;value_3;value_4;value_5

const int NUMBER_OF_PINS_READ = 6;
const uint8_t hallPins[NUMBER_OF_PINS_READ] = { A0, A1, A2, A3, A4, A5 };
float values_rpm[NUMBER_OF_PINS_READ];

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    // Read all sensors
    for (int i = 0; i < 6; i++)
    {
        values_rpm[i] = analogRead(hallPins[i]);
    }
    send_all_data();
    delay(1000);
}

void send_all_data()
{
    // Send formatted packet
    Serial.print("RPM");
    for (int i = 0; i < 6; i++)
    {
        Serial.print(";");
        Serial.print(values_rpm[i], 2); // seulement deux digits de precision
    }
    Serial.println();

}