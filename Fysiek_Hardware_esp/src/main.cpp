#include <WiFi.h>
#include <PubSubClient.h>

// Define Pins
#define NOODSTOP 15
#define LEDNEGY 2  // FORWARD
#define LEDPOSY 4  // BACK
#define LEDNEGX 16 // LEFT
#define LEDPOSX 17 // RIGHT

const char *ssid = "Tesla IoT";        //"YourWiFiSSID"
const char *password = "fsL6HgjN";     //"YourWiFiPassword"

// MQTT Broker IP address and port
const char *brokerIP = "68.183.3.184";
const int brokerPort = 1883;

// MQTT topics to subscribe and publish to
const char *mqttRobotXLocationTopics[] = {
    "robots/1/x"
    // "robots/2/x",
    // "robots/3/x",
    // "robots/4/x"
    };

const char *mqttRobotYLocationTopics[] = {
    "robots/1/y"
    // "robots/2/y",
    // "robots/3/y",
    // "robots/4/y"
    };

const char *mqttObstaclesTopics[] = {
    "obstacles/1",
    "obstacles/2",
    "obstacles/3",
    "obstacles/4"};

const char *mqttLedTopics[] = {
    "robots/1/positieve/x",
    "robots/1/positieve/y",
    "robots/1/negatieve/x",
    "robots/1/negatieve/y"};


const char *mqttEspTopic = "esp32";
const char *mqttButtonTopic = "noodstop";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Pin definitions for LEDs and push button
const int ledPins[] = {LEDNEGY, LEDPOSY, LEDNEGX, LEDPOSX};

// State variables for LEDs and push button
int ledStates[] = {LOW, LOW, HIGH, LOW};
int prevButtonState = HIGH;
int currButtonState;

// Callback function when MQTT message is received
void callback(char *topic, byte *payload, unsigned int length)
{
  // Convert the payload to a string
  payload[length] = '\0';
  String message = String((char *)payload);
  Serial.println(message);
  // Check the received topic
  for (int i = 0; i < sizeof(mqttLedTopics) / sizeof(mqttLedTopics[0]); i++)
  {
    // Check the received topic
    if (String(topic) == mqttLedTopics[i])
    {
      if (message == "LEDNEGYON")
      {
        // Turn on the LEDs
        digitalWrite(LEDNEGY, HIGH);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      else if (message == "LEDNEGYOFF")
      {
        // Turn off the LEDs
        digitalWrite(LEDNEGY, LOW);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      if (message == "LEDNEGXON")
      {
        // Turn on the LEDs
        digitalWrite(LEDNEGX, HIGH);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      else if (message == "LEDNEGXOFF")
      {
        // Turn off the LEDs
        (LEDNEGY, LOW);
        digitalWrite(LEDNEGX, LOW);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      if (message == "LEDPOSYON")
      {
        // Turn on the LEDs
        digitalWrite(LEDPOSY, HIGH);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      else if (message == "LEDPOSYOFF")
      {
        // Turn off the LEDs
        digitalWrite(LEDPOSY, LOW);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      if (message == "LEDPOSXON")
      {
        // Turn on the LEDs
        digitalWrite(LEDPOSX, HIGH);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
      else if (message == "LEDPOSXOFF")
      {
        // Turn off the LEDs
        digitalWrite(LEDPOSX, LOW);
        // Serial.println("LED-Recevied");
        Serial.println(message);
      }
    }
  }
}

void reconnect()
{
  while (!mqttClient.connected())
  {
    if (mqttClient.connect("ESP32Client"))
    {
      Serial.println("Connected to MQTT Broker");

      // Subscribe to LED topics
      for (int i = 0; i < sizeof(mqttLedTopics) / sizeof(mqttLedTopics[0]); i++)
      {
        mqttClient.subscribe(mqttLedTopics[i]);
      }

      mqttClient.subscribe(mqttEspTopic);
    }
    else
    {
      Serial.print("Failed to connect to MQTT Broker, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void IRAM_ATTR sendStop()
{
  if (mqttClient.connected())
  {
    // mqttClient.print(mqttButtonTopic,"STOP");
    // mqttClient.publish(mqttButtonTopic, "STOP");
    // mqttClient.publish("noodstop","Y");
    // mqttClient.publish(buttonTopic, "STOP_PRESSED");
    Serial.println("Noodstop");
  }
  // Serial.println("Stop button pressed!");
}


void setup()
{
  Serial.begin(115200);
  while (!Serial)
    ;
  delay(2000);

  Serial.print("Connecting to .... ");
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

  // Connect to MQTT Broker
  mqttClient.setServer(brokerIP, brokerPort);
  mqttClient.setCallback(callback);

  while (!mqttClient.connected())
  {
    if (mqttClient.connect("ESP32Client"))
    {
      Serial.println("Connected to MQTT Broker");

      // Subscribe to LED topics
      for (int i = 0; i < sizeof(mqttLedTopics) / sizeof(mqttLedTopics[0]); i++)
      {
        mqttClient.subscribe(mqttLedTopics[i]);
      }

      mqttClient.subscribe(mqttEspTopic);
    }
    else
    {
      Serial.print("Failed to connect to MQTT Broker, retrying...");
      Serial.print(mqttClient.state());            // -
      Serial.println(" Retrying in 5 seconds..."); // -
      delay(2000);
    }
  }

  // Hardware Interupt

  // Initialize LED pins as outputs
  for (int i = 0; i < sizeof(ledPins) / sizeof(ledPins[0]); i++)
  {
    pinMode(ledPins[i], OUTPUT);
  }

  // NoodStop -- Button
  pinMode(NOODSTOP, INPUT_PULLUP);
  attachInterrupt(NOODSTOP, sendStop, FALLING);
}

void loop()
{

  if (!mqttClient.connected())
  {
    reconnect();
  }

  mqttClient.loop();

  // Read the state of the push button
  currButtonState = digitalRead(NOODSTOP);

  // Check if the button state has changed
  if (currButtonState != prevButtonState)
  {
    delay(50); // debounce delay

    // Check if the button is pressed (LOW state)
    if (currButtonState == HIGH)
    {
      // Publish a message indicating button press
      // mqttClient.publish(buttonTopic, "BUTTON_PRESSED");
      mqttClient.publish(mqttButtonTopic, "Y");
      Serial.println("Noodstop");
    }

    prevButtonState = currButtonState;
  }

  // Publish a test message
  // mqttClient.publish(mqttEspTopic, "Hello, MQTT from ESP32!");

  // Delay before publishing the next message
  // delay(5000);
}
