import socket
import threading
import json
import time
import paho.mqtt.client as mqtt

# Define the host and port of the server
HOST = 'localhost'
PORT = 5555

# Define the MQTT broker details
# MQTT_BROKER = 'localhost'
MQTT_BROKER = 'broker.mqtt-dashboard.com'# Broker moet veranderd worden
MQTT_PORT = 1883
MQTT_TOPIC = 'robot/messages'

# Create a list to store client connections
clients = []

# Define the thread function to handle client connections


def handle_client(conn, addr):
    # Add the client connection to the list of clients
    clients.append(conn)
    print(f'[INFO] New connection from {addr}')

    # Continuously receive data from the client
    while True:
        try:
            # Receive data from the client
            data = conn.recv(1024)
            if data:
                # Decode the received data
                message = data.decode('utf-8')
                print(f'[INFO] Received message from {addr}: {message}')

                # Publish the message to the MQTT broker
                mqtt_client.publish(MQTT_TOPIC, message)

        except:
            # If there's an error, remove the client connection from the list of clients and close the connection
            print(f'[INFO] Connection closed by {addr}')
            clients.remove(conn)
            conn.close()
            return

# Define the function to handle MQTT messages


def on_message(client, userdata, message):
    # Decode the received message
    message_data = message.payload.decode('utf-8')
    print(f'[INFO] Received message from MQTT: {message_data}')

    # Broadcast the message to all connected clients
    for client in clients:
        try:
            client.sendall(message_data.encode('utf-8'))
        except:
            # If there's an error, remove the client connection from the list of clients and close the connection
            clients.remove(client)
            client.close()


# Create an instance of the MQTT client
mqtt_client = mqtt.Client()

# Set the MQTT client callbacks
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# Subscribe to the MQTT topic
mqtt_client.subscribe(MQTT_TOPIC)

# Start the MQTT loop thread
mqtt_client.loop_start()

# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f'[INFO] Server started on {HOST}:{PORT}')

# Continuously accept client connections
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
