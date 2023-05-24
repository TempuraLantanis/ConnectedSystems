#include <WiFi.h>

const char *ssid = "YourWiFiSSID"; //"YourWiFiSSID"
const char *password = "YourWiFiPassword"; //"YourWiFiPassword"

void setup()
{
    Serial.begin(115200);
    delay(2000);

    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("Wi-Fi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop()
{
    // Your code here

    // Example: Print a message every second
    Serial.println("Hello, ESP32!");
    delay(1000);
}
