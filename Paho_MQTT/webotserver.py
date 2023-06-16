import paho.mqtt.client as mqtt
import time as t
import json
import random as r

broker = "68.183.3.184"
port = 1883


destinations = [[],[],[],[]]

queue = []
rob1Queue = []
rob2Queue = []
rob3Queue = []
rob4Queue = []


availableRobotIndex = [False, False, False, False];

locationhistory = set()

rob1Pos = [None,None]
rob2Pos = [None,None]
rob3Pos = [None,None]
rob4Pos = [None,None]


obstacleMasterList = []
obstacleList1 = []
obstacleList2 = []
obstacleList3 = []
obstacleList4 = []

global current_target
current_target = []


subscribe_topics =["$SYS/broker/clients","obstacles/1","obstacles/2","obstacles/3","obstacles/4",
                    "target-destination/1","target-destination/2","target-destination/3","target-destination/4",
                    "queued-destination/queue","queued-destination/target",
                    "robots/1/x","robots/2/x","robots/3/x","robots/4/x",
                    "robots/1/y","robots/2/y","robots/3/y","robots/4/y"]


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
    # print("Received message: " + message + " from "+ msg.topic)
    # print(msg.topic[:5])

    if msg.topic[:6] == "robots":
        # print('msg Pos received')
        updatePosition(msg)
        positions_x = [rob1Pos[0],rob2Pos[0],rob3Pos[0],rob4Pos[0]]
        positions_y = [rob1Pos[1],rob2Pos[1],rob3Pos[1],rob4Pos[1]]
        
        for i, pos_x in enumerate(positions_x):
            if pos_x and positions_y[i]:
                if current_target and current_target[0] == i+1:
                    # print(f'i:{i} - current_target = {current_target} ')
                    client.publish("target-destination/"+str(i+1), json.dumps(current_target[1]))
                locationhistory.add((int(pos_x),int(positions_y[i])))
        


    if msg.topic == "queued-destination/queue":
        print('queued destination received')
        queue.append(json.loads(msg.payload.decode()))

    if msg.topic == "queued-destination/target":
        payload = json.loads(msg.payload.decode())
        # if payload.
        print(f'payload received: {payload} ')
        robotID = int(payload['robotunit']['id'])
        target = [payload['target']['x'],payload['target']['y']]
        matchQueue(robotID).append(target)
        
    
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
    

    # print("obstacleList1: " + str(obstacleList1))
    # print("obstacleList2: " + str(obstacleList2))
    # print("obstacleList3: " + str(obstacleList3))
    # print("obstacleList4: " + str(obstacleList4))


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

    # print("rob1Pos: " + str(rob1Pos))
    # print("rob2Pos: " + str(rob2Pos))
    # print("rob3Pos: " + str(rob3Pos))
    # print("rob4Pos: " + str(rob4Pos))

def on_publish(client, userdata, mid):
    # print("Message published:")
    # print(userdata)
    pass
    # log.debug("on_publish, mid {}".format(mid))



def matchRobot(robotID):
    if robotID == 1:
        return rob1Pos
    elif robotID == 2:
        return rob2Pos
    elif robotID == 3:
        return rob3Pos
    elif robotID == 4:
        return rob4Pos
    


def matchQueue(robotID) -> list:
    if robotID == 1:
        return rob1Queue
    elif robotID == 2:
        return rob2Queue
    elif robotID == 3:
        return rob3Queue
    elif robotID == 4:
        return rob4Queue
    

def checkIfArrived(robotID):
    robotPosition = matchRobot(robotID)
    print(robotPosition)
    if not destinations[robotID-1] or robotPosition == destinations[robotID-1]:
        print("robot " + str(robotID) + " arrived at destination")
        client.publish("target-destination/"+str(robotID))    #TODO publish empty
        return True
    else:
        return False
    


def updateAvailableIndex():
    for i in range(4):
        # print(i)
        if checkIfArrived(i+1) == True:
            print("robot " + str(i+1) + " arrived at destination")
            availableRobotIndex[i] = True


def assignTasks():
    if len(queue) > 0:
        for i in range(len(queue)):
            command = queue.pop(0)
            commandOrigin = [command['origin']['x'],command['origin']['y']]
            commandTarget = [command['target']['x'],command['target']['y']]
            queueItem = [commandOrigin,commandTarget]
            matchQueue(r.randint(1,4)).extend(queueItem)
    else:
        print("no tasks in queue")

def executeTasks():
    # print(f'Excute tasks function')
    for i in range(4):
        if len(matchQueue(i+1)) > 0:
            print(f'robot{i+1} has Queue')
            if checkIfArrived(i+1):
                print(f'robot{i+1} has arrived')
                newdestination =  matchQueue(i+1).pop(0)
                # if destinations[i]:
                destinations[i] = newdestination
                print(f'destinations[{i}] = {destinations[i]} ')
                global current_target
                print(f'current_target = {current_target} ')
                current_target = [i+1, [int(json.dumps(newdestination)[2]), int(json.dumps(newdestination)[7])]]
                client.publish("target-destination/"+str(i+1), json.dumps(current_target[1]))
                    
        
            




def updateList():

    obstacle_lists = [
    obstacleList1,
    obstacleList2,
    obstacleList3,
    obstacleList4
    ]

    for obst_list in obstacle_lists:
        for obst in obst_list:
            if obst not in obstacleMasterList and tuple(obst) not in locationhistory:
                obstacleMasterList.append(obst)


    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish



client.connect(broker, port)
client.loop_start()
client.publish("connecTest", "Hello, MQTT from Server!")

while True:
    assignTasks()
    executeTasks()
    # print('CheckUpdate')
    # print(availableRobotIndex)
    # updateAvailableIndex()
    # print(queue)
    # print(locationhistory)
    t.sleep(1)
    # print('queue')
    # print(queue)
    # print('robdex')
    # print(availableRobotIndex)
    pass

