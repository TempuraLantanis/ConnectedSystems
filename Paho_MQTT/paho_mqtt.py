import paho.mqtt.client as mqtt

# MQTT Broker (replace with your broker's IP address or hostname)

# "mqtt.example.com" , "mqtt://localhost:1883", "test.mosquitto.org"
broker = "localhost"
port = 1883

# MQTT topics to subscribe and publish to
subscribe_topic = "my_topic/subscribe"
publish_topic = "my_topic/publish"


# Callback function when a connection is established with the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker with result code: " + str(rc))
        # Subscribe to the topic when connected
        client.subscribe(subscribe_topic)  # Topic to subscribe to



# Callback function when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Received message: " + message)
    # print("Received message: " + str(msg.payload.decode()))

    # Process the received message here

    # Process the received message
    if message == "Hello, MQTT from ESP32!":
        print("Processing ESP32 message...")

        # Perform specific actions based on the received message
        print("Perform specific actions based on the received message")

    elif message == "Another message":
        print("Processing another message...")

        # Perform specific actions for another message
        print("Perform specific actions based on the received message")

    else:
        print("Unknown message received.")

# Callback function when a message is published
def on_publish(client, userdata, mid):
    print("Message published")


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker, port)

# Start the MQTT network loop (non-blocking)
client.loop_start()

# Publish a test message
client.publish(publish_topic, "Hello, MQTT from Server!")

# Keep the program running
while True:
    pass

# Disconnect from the MQTT broker
client.loop_stop()
client.disconnect()
