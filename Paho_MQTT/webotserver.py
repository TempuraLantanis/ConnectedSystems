import paho.mqtt.client as mqtt
import time as t



broker = "localhost"
port = 1883


destinations = [[1,2],[5,6],[11,10],[3,1]]


rob1queue = []
rob2queue = []
rob3queue = []
rob4queue = []


rob1Pos = [None,None]
rob2Pos = [None,None]
rob3Pos = [None,None]
rob4Pos = [None,None]


obstacleList = []

subscribe_topics =["obstakels","destination",
                   "robots/1/x","robots/2/x","robots/3/x","robots/4/x"
                   ,"robots/1/y","robots/2/y","robots/3/y","robots/4/y"]


def on_connect (client,userdata,flags,rc):
    if rc == 0:
        for topic in subscribe_topics:
            print("subscribing to topic" + topic)
            client.subscribe(topic)

        try:
            client.publish("testopic","connection succesfull")    
        except:
            print("error")

    else:
        print("connection error with error code" + str(rc))

def on_message(client,userdata,msg):
    message = msg.payload.decode()
    print("Received message: " + message + " from "+ msg.topic)


    updatePosition(msg)
   

def updatePosition(case):
    if case.topic == "robots/1/x":
        rob1Pos[0] = case.payload.decode()
    elif case.topic == "robots/1/y":
        rob1Pos[1] = case.payload.decode()
    elif case.topic == "robots/2/x":
        rob2Pos[0] = case.payload.decode()
    elif case.topic == "robots/2/y":
        rob2Pos[1] = case.payload.decode()
    elif case.topic == "robots/3/x":
        rob3Pos[0] = case.payload.decode()
    elif case.topic == "robots/3/y":
        rob3Pos[1] = case.payload.decode()
        
         


def on_publish(client, userdata, mid):
    print("Message published")
    print(userdata)




client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish



client.connect(broker, port)

client.loop_start()

client.publish("connecTest", "Hello, MQTT from Server!")

while True:
    t.sleep(1)
    print(rob1Pos)

    pass

