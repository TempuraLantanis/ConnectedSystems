#include <WiFi.h>
#include <PubSubClient.h>

// Define Pins
#define NOODSTOP 15

const char *ssid = "YourWiFiSSID";         //"YourWiFiSSID"
const char *password = "YourWiFiPassword"; //"YourWiFiPassword"

// MQTT Broker IP address and port
const char *brokerIP = "test.mosquitto.org";
const int brokerPort = 1883;

// MQTT topics to subscribe and publish to
const char *subscribeTopic = "my_topic/subscribe";
const char *publishTopic = "my_topic/publish";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Callback function when MQTT message is received
void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Received message: ");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}


void simple_message(){
  // Example: Print a message every second
  Serial.println("Hello, ESP32!");
  delay(1000);
}

void reconnect()
{
  while (!mqttClient.connected())
  {
    if (mqttClient.connect("ESP32Client"))
    {
      Serial.println("Connected to MQTT Broker");
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

void IRAM_ATTR sendStop() {
  // ISR logic goes here
  // This function will be executed when the interrupt is triggered
  // Make sure to keep the ISR code short and efficient

  if (mqttClient.connected()){
    // send message. Do not use println (introduces an empty line)
    mqttClient.print("STOP");
    // mqttClient.flush();
  }
  Serial.println("Stop button pressed!");
}

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

  // Connect to MQTT Broker
  mqttClient.setServer(brokerIP, brokerPort);
  mqttClient.setCallback(callback);

  while (!mqttClient.connected())
  {
    if (mqttClient.connect("ESP32Client"))
    {
      Serial.println("Connected to MQTT Broker");
      mqttClient.subscribe(subscribeTopic);
    }
    else
    {
      Serial.print("Failed to connect to MQTT Broker, retrying...");
      Serial.print(mqttClient.state()); // -
      Serial.println(" Retrying in 5 seconds..."); // -
      delay(2000);
    }
  }

  // Hardware Interupt
  pinMode(NOODSTOP, INPUT_PULLUP);
  attachInterrupt(NOODSTOP, sendStop, FALLING);
}


void loop()
{
  // mqttClient.loop();
  if (!mqttClient.connected())
  {
    reconnect();
  }

  // Publish a test message
  // mqttClient.publish(publishTopic, "Hello, MQTT from ESP32!");
  mqttClient.publish(subscribeTopic, "Hello, MQTT from ESP32!");

  // Delay before publishing the next message
  delay(5000);
}

