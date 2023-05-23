#include <Arduino.h>          // Include the Arduino library
#include <PubSubClient.h>     // Include the PubSubClient library for MQTT
#include <WiFiClientSecure.h> // Include the WiFiClientSecure library for secure WiFi connections
#include "Adafruit_Sensor.h"  // Include the Adafruit_Sensor library for DHT sensor
#include <DHT.h>              // Include the DHT library for DHT sensor

#include "time.h" // Include the time library for NTP time synchronization

#include <string>   // Include the string library
#include <stdlib.h> // Include the standard library for string conversion functions
#include <iostream> // Include the iostream library for standard input/output

#include "secret.h" // Include the secret.h file that contains sensitive information like WiFi credentials and MQTT server details

const String studentNumber = "1021941"; // Define a string variable to store the student number

WiFiClientSecure espClient;         // Create a WiFiClientSecure object for secure WiFi connections
PubSubClient client(espClient);     // Create a PubSubClient object for MQTT communication
unsigned long lastMsg = 0;          // Define a variable to store the last time a message was sent
#define MSG_BUFFER_SIZE (50)        // Define the size of the message buffer
char msg[MSG_BUFFER_SIZE];          // Define a character array to store the message
const char *topic = "chat/message"; // Define the MQTT topic for the chat application
int value = 0;                      // Define a variable to store a value

const char *ntpServer = "europe.pool.ntp.org"; // Define the NTP server to use for time synchronization
const long gmtOffset_sec = 18000;              // Define the GMT offset in seconds
const int daylightOffset_sec = 0;              // Define the daylight offset in seconds

#define BUILTIN_LED 2 // Define the pin for the built-in LED on the ESP32 board

#define DHTPIN 4          // Define the pin for the DHT sensor
#define DHTTYPE DHT22     // Define the type of the DHT sensor
DHT dht(DHTPIN, DHTTYPE); // Create a DHT object for the DHT sensor

void printLocalTime() // Function to print the local time
{
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo))
    {                                            // Try to get the local time from the system
        Serial.println("Failed to obtain time"); // Print an error message if the time could not be obtained
        return;
    }
    Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S"); // Print the local time in a human-readable format
}

void setup_wifi()
{
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, pass);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    randomSeed(micros());

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void checkMessage(String receivedMessage)
{
    if (receivedMessage.indexOf("BOT-1021941") >= 0)
    {
        Serial.println("Message for BOT-1021941");
        if (receivedMessage.indexOf("temperature") > 0)
        {
            Serial.println("Send temperature");
            int temperature = dht.readTemperature();
            snprintf(msg, MSG_BUFFER_SIZE, "temp %d˚C", temperature);
            client.publish(topic, msg);
        }
        if (receivedMessage.indexOf("humidity") > 0)
        {
            Serial.println("Send humidity");
            int humidity = dht.readHumidity();
            snprintf(msg, MSG_BUFFER_SIZE, "Humidity is %d%", humidity);
            client.publish(topic, msg);
        }
        if (receivedMessage.indexOf("led") > 0)
        {
            if (receivedMessage.indexOf("on") > 0)
            {
                Serial.println("Led on");
                digitalWrite(BUILTIN_LED, HIGH);
                snprintf(msg, MSG_BUFFER_SIZE, "LED is on");
                client.publish(topic, msg);
            }
            if (receivedMessage.indexOf("off") > 0)
            {
                Serial.println("Led off");
                digitalWrite(BUILTIN_LED, LOW);
                snprintf(msg, MSG_BUFFER_SIZE, "LED is off");
                client.publish(topic, msg);
            }
        }
    }
}

void callback(char *topic, byte *payload, unsigned int length)
{
    String receivedMessage;
    Serial.println("Message arrived");

    for (int i = 0; i < length; i++)
    {
        receivedMessage += (char)payload[i];
    }

    Serial.println(receivedMessage);

    checkMessage(receivedMessage);
}

void reconnect()
{
    // Loop until we're reconnected
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");

        String userID = "BOT-" + studentNumber;

        // Attempt to connect
        if (client.connect(userID.c_str(), MQTT_USER, MQTT_PASS))
        {
            Serial.println("connected");

            snprintf(msg, MSG_BUFFER_SIZE, "BOT-%s is connected", MQTT_CLIENT_ID);
            client.publish(topic, msg);
            client.subscribe("#");
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void setup()
{
    Serial.begin(115200);

    pinMode(BUILTIN_LED, OUTPUT);
    dht.begin();

    setup_wifi();

    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    printLocalTime();

    espClient.setCACert(local_root_ca);
    client.setServer(MQTT_HOST, MQTT_PORT);
    client.setCallback(callback);
}

void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();
}
