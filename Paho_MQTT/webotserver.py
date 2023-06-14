import paho.mqtt.client as mqtt
import time as t
import json

broker = "localhost"
port = 1883


destinations = [["1","2"],["5","6"],["11","10"],["3","1"]]

queue = []


availableRobotIndex = [False, False, False, False];



rob1Pos = [None,None]
rob2Pos = [None,None]
rob3Pos = [None,None]
rob4Pos = [None,None]


obstacleMasterList = []
obstacleList1 = []
obstacleList2 = []
obstacleList3 = []
obstacleList4 = []


subscribe_topics =["$SYS/broker/clients","obstacles/1","obstacles/2","obstacles/3","obstacles/4","currentDestination","queuedDestination",
                   "robots/1/x","robots/2/x","robots/3/x","robots/4/x"
                   ,"robots/1/y","robots/2/y","robots/3/y","robots/4/y"]


def on_connect (client,userdata,flags,rc):
    if rc == 0:
        for topic in subscribe_topics:
            print("subscribing to topic " + topic)
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
    print(msg.topic[:5])

    if msg.topic[:6] == "robots":
        print('msg Pos received')
        updatePosition(msg)


    if msg.topic == "queuedDestination":
        print('queuedDestination received')
        queue.append(json.loads(msg.payload.decode()))
    
    if msg.topic [:9] == "obstacles":
        print('obstacles received')

        updateObstacles(msg)
        
        updateList()
        print("obstacleMasterList: " + str(obstacleMasterList))
        client.publish("obstacles/masterlist", str(obstacleMasterList))
        #json.dumps()


def updateObstacles(case):
    global obstacleList1
    global obstacleList2
    global obstacleList3
    global obstacleList4
    if case.topic == "obstacles/1":
        obstacleList1 = json.loads(str(case.payload.decode()))
    elif case.topic == "obstacles/2":
        obstacleList2 = json.loads(str(case.payload.decode()))
    elif case.topic == "obstacles/3":
        obstacleList3 = json.loads(str(case.payload.decode()))
    elif case.topic == "obstacles/4":
        obstacleList4 = json.loads(str(case.payload.decode()))
    

    print("obstacleList1: " + str(obstacleList1))
    print("obstacleList2: " + str(obstacleList2))
    print("obstacleList3: " + str(obstacleList3))
    print("obstacleList4: " + str(obstacleList4))


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
    elif case.topic == "robots/4/x":
        rob4Pos[0] = case.payload.decode()
    elif case.topic == "robots/4/y":
        rob4Pos[1] = case.payload.decode()

    print("rob1Pos: " + str(rob1Pos))
    print("rob2Pos: " + str(rob2Pos))
    print("rob3Pos: " + str(rob3Pos))
    print("rob4Pos: " + str(rob4Pos))

def on_publish(client, userdata, mid):
    print("Message published")
    print(userdata)


def matchRobot(robotID):
    if robotID == 1:
        return rob1Pos
    elif robotID == 2:
        return rob2Pos
    elif robotID == 3:
        return rob3Pos
    elif robotID == 4:
        return rob4Pos


def checkIfArrived(robotID):
    robotPosition = matchRobot(robotID)
    print(robotPosition)
    if robotPosition == destinations[robotID-1]:
        print("robot " + str(robotID) + " arrived at destination")
        return True
    


def updateAvailableIndex():
    for i in range(4):
        print(i)
        if checkIfArrived(i+1) == True:
            print('setting state in available index')
            availableRobotIndex[i] = True


def assignTasks():
    if len(queue) >= 0 & availableRobotIndex.count(True) > 0:
        for i in range(4):
            if availableRobotIndex[i] == True:
                client.publish("currentDestination/"+str(i)+"/x",queue[0]['x'])
                client.publish("currentDestination/"+str(i)+"/y",queue[0]['y'])
                availableRobotIndex[i] = False
                setDestination = queue.pop(0)
                destinations[i-1] = [setDestination['x'],setDestination['y']]
                break
            else:
                pass



def updateList():

    obstacle_lists = [
    obstacleList1,
    obstacleList2,
    obstacleList3,
    obstacleList4
    ]

    for obst_list in obstacle_lists:
        for obst in obst_list:
            if obst not in obstacleMasterList:
                obstacleMasterList.append(obst)


    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish



client.connect(broker, port)
client.loop_start()
client.publish("connecTest", "Hello, MQTT from Server!")

while True:
    # print('CheckUpdate')
    # print(availableRobotIndex)
    # updateAvailableIndex()
    # print(queue)
    t.sleep(1)
    # print('queue')
    # print(queue)
    # print('robdex')
    # print(availableRobotIndex)
    pass

