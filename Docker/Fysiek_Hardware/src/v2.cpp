#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// Replace with your network credentials
const char *ssid = "Tesla IoT"; //"your_SSID"
const char *password = "fsL6HgjN"; // "your_PASSWORD"

// Replace with your MQTT broker IP address
const char *mqtt_server ="localhost" ; // "your_MQTT_broker_IP"

// Initialize the MQTT client
WiFiClient espClient;
PubSubClient client(espClient);

// Pin definitions for LEDs and push button
const int ledPins[] = {2, 4, 5, 15}; // Replace with the appropriate GPIO pins
const int buttonPin = 14;            // Replace with the appropriate GPIO pin

// State variables for LEDs and push button
int ledStates[] = {LOW, LOW, LOW, LOW};
int prevButtonState = HIGH;
int currButtonState;

// Interrupt service routine to handle the stop button press
void IRAM_ATTR sendStop()
{
    // Publish a message indicating the stop button press
    client.publish("button_topic", "STOP_PRESSED");
}

// Callback function to handle MQTT messages
void callback(char *topic, byte *payload, unsigned int length)
{
    // Convert the incoming payload to a string
    String message = "";
    for (int i = 0; i < length; i++)
    {
        message += (char)payload[i];
    }

    // Check the incoming message and update LED states accordingly
    if (message.equals("LED1_ON"))
    {
        ledStates[0] = HIGH;
    }
    else if (message.equals("LED1_OFF"))
    {
        ledStates[0] = LOW;
    }
    else if (message.equals("LED2_ON"))
    {
        ledStates[1] = HIGH;
    }
    else if (message.equals("LED2_OFF"))
    {
        ledStates[1] = LOW;
    }
    else if (message.equals("LED3_ON"))
    {
        ledStates[2] = HIGH;
    }
    else if (message.equals("LED3_OFF"))
    {
        ledStates[2] = LOW;
    }
    else if (message.equals("LED4_ON"))
    {
        ledStates[3] = HIGH;
    }
    else if (message.equals("LED4_OFF"))
    {
        ledStates[3] = LOW;
    }

    // Update the LED states
    for (int i = 0; i < sizeof(ledPins) / sizeof(ledPins[0]); i++)
    {
        digitalWrite(ledPins[i], ledStates[i]);
    }
}

// Connect to the MQTT broker
void reconnect()
{
    while (!client.connected())
    {
        Serial.println("Attempting MQTT connection...");
        if (client.connect("ESP32Client"))
        {
            Serial.println("Connected to MQTT broker");
            client.subscribe("led_control_topic");
        }
        else
        {
            Serial.print("MQTT connection failed, rc=");
            Serial.print(client.state());
            Serial.println(" Retrying in 5 seconds...");
            delay(5000);
        }
    }
}

// Setup function
void setup()
{
    // Initialize Serial communication
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Connect to MQTT broker
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    reconnect();

    // Initialize

    LED pins as outputs for (int i = 0; i < sizeof(ledPins) / sizeof(ledPins[0]); i++)
    {
        pinMode(ledPins[i], OUTPUT);
    }

    // Initialize push button pin as input with internal pull-up resistor
    pinMode(buttonPin, INPUT_PULLUP);
    attachInterrupt(buttonPin, sendStop, FALLING);
}

// Loop function
void loop()
{
    // Check for MQTT messages and handle them
    if (!client.connected())
    {
        reconnect();
    }
    client.loop();

    // Read the state of the push button
    currButtonState = digitalRead(buttonPin);

    // Check if the button state has changed
    if (currButtonState != prevButtonState)
    {
        delay(50); // debounce delay

        // Check if the button is pressed (LOW state)
        if (currButtonState == LOW)
        {
            // Publish a message indicating button press
            client.publish("button_topic", "BUTTON_PRESSED");
        }

        prevButtonState = currButtonState;
    }
}