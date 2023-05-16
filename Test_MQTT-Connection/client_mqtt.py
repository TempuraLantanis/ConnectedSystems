# import socket
# import threading
# import json
# import paho.mqtt.client as mqtt

# # Define the host and port of the server
# HOST = 'localhost'
# PORT = 5555

# # Define the MQTT broker details
# MQTT_BROKER = 'broker.mqtt-dashboard.com'
# MQTT_PORT = 1883
# MQTT_TOPIC = 'robot/messages'

# # Create a TCP socket connection to the server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

# # Define the thread function to continuously receive data from the server


# def receive_data():
#     while True:
#         try:
#             # Receive data from the server
#             data = client_socket.recv(1024)
#             if data:
#                 # Decode the received data
#                 message = data.decode('utf-8')
#                 print(f'[

import paho.mqtt.client as mqtt
import threading

# set MQTT broker address and port
# broker_address = "localhost"
broker_address = "mqtt.eclipseprojects.io"  # Broker moet veranderd worden
broker_port = 1883

# define a function to handle incoming MQTT messages


def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")


# create an MQTT client instance
client = mqtt.Client()

# set the function to handle incoming messages
client.on_message = on_message

# connect to the MQTT broker
client.connect(broker_address, broker_port)

# subscribe to the "robots" topic
client.subscribe("robots")

# define a function to handle sending messages to the server


def send_message():
    while True:
        message = input("Enter a message to send to the server: ")
        client.publish("robots", message)


# start a new thread for sending messages to the server
threading.Thread(target=send_message).start()

# loop forever to receive incoming messages
client.loop_forever()
