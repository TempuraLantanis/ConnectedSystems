"""box_supervisor controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from collections import deque
from controller import Supervisor


import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker (WeBots)")


def on_message(client, userdata, msg):
    message = msg.payload.decode()

    if msg.topic[:6] == "robots":
        updatePosition(msg)

    if msg.topic == "obstacles/masterlist":
        global obstacles_local
        global obstacles_server
        global graph
        obstacles_server = [tuple(x)
                            for x in json.loads(msg.payload.decode())]
        for obst_s in obstacles_server:
            if obst_s not in obstacles_local:
                # obstacles_local.append(obst_s)
                add_obstacle(graph, obst_s)

    if msg.topic == "target":  # TODO change topic and test
        global target
        target = tuple(json.loads(msg.payload.decode()))
        print(f'{sv_name} target: {target} ')


def updatePosition(case):
    global location_unit1
    global location_unit2
    global location_unit3
    global location_unit4
    global mqtt_robot_x_location_topics
    global mqtt_robot_y_location_topics
    global graph
    temp_location = ()
    locations_units = [
        location_unit1,
        location_unit2,
        location_unit3,
        location_unit4
    ]
    # topics
    unit_index = -1
    if case.topic == "robots/1/x":
        temp_location = location_unit1
        location_unit1 = (int(case.payload.decode()), location_unit1[1])
        unit_index = 0
    elif case.topic == "robots/1/y":
        temp_location = location_unit1
        location_unit1 = (location_unit1[0], int(case.payload.decode()))
        unit_index = 0
    elif case.topic == "robots/2/x":
        temp_location = location_unit2
        location_unit2 = (int(case.payload.decode()), location_unit2[1])
        unit_index = 1
    elif case.topic == "robots/2/y":
        temp_location = location_unit2
        location_unit2 = (location_unit2[0], int(case.payload.decode()))
        unit_index = 1
    elif case.topic == "robots/3/x":
        temp_location = location_unit3
        location_unit3 = (int(case.payload.decode()), location_unit3[1])
        unit_index = 2
    elif case.topic == "robots/3/y":
        temp_location = location_unit3
        location_unit3 = (location_unit3[0], int(case.payload.decode()))
        unit_index = 2
    elif case.topic == "robots/4/x":
        temp_location = location_unit4
        location_unit4 = (int(case.payload.decode()), location_unit4[1])
        unit_index = 3
    elif case.topic == "robots/4/y":
        temp_location = location_unit4
        location_unit4 = (location_unit4[0], int(case.payload.decode()))
        unit_index = 3

    # check what topic came in
    # for i, topic in enumerate(mqtt_robot_x_location_topics):
    #     # Check if x or y
    #     if case.topic == topic or case.topic == mqtt_robot_y_location_topics[i]:
    #         temp_location = locations_units[i]
    #         locations_units[i] = (
    #             int(case.payload.decode()),
    #             locations_units[i][1]) if case.topic == topic else (
    #             locations_units[i][0],
    #             int(case.payload.decode()))
    #         unit_index = i

    graph = update_graph(graph, obstacles_local,
                         temp_location, locations_units[unit_index])


def add_neighbor(adjacency_list, location, neighbor):
    '''
    Helper function to add a neighbor to a given location in the adjacency list.
    '''
    adjacency_list[location].add(neighbor)
    adjacency_list[neighbor].add(location)


def update_graph(adjacency_list, obstacles, old_location, new_location):
    '''
    Update graph when another unit has moved from old_location to new_location.

    First add old's neighbor's back to its adj. list
        Checks for each neighbor in if statement:
        - Don't add new_location as neighbor to old
        - Is neighbor within bounds
        - Don't add an obstacle as neighbor

    Parameters:
    - adjacency_list: The dictionary representing the adjacency list of the graph
    - obstacles: A list of obstacle locations
    - old_location: The old location of the moved unit
    - new_location: The new location of the moved unit
    '''
    # Remove other unit's old location from obstacles
    if old_location in obstacles_local:
        obstacles_local.remove(old_location)
    # Add unit's old location back to its neighbors
    if (old_location[0] + 1 != new_location[0] and
        old_location[0] + 1 <= 9 and
            (old_location[0] + 1, old_location[1]) not in obstacles):
        add_neighbor(adjacency_list, old_location,
                     (old_location[0] + 1, old_location[1]))

    if (old_location[0] - 1 != new_location[0] and
        old_location[0] - 1 >= 0 and
            (old_location[0] - 1, old_location[1]) not in obstacles):
        add_neighbor(adjacency_list, old_location,
                     (old_location[0] - 1, old_location[1]))

    if (old_location[1] + 1 != new_location[1] and
        old_location[1] + 1 <= 9 and
            (old_location[0], old_location[1] + 1) not in obstacles):
        add_neighbor(adjacency_list, old_location,
                     (old_location[0], old_location[1] + 1))

    if (old_location[1] - 1 != new_location[1] and
        old_location[1] - 1 >= 0 and
            (old_location[0], old_location[1] - 1) not in obstacles):
        add_neighbor(adjacency_list, old_location,
                     (old_location[0], old_location[1] - 1))

    # Remove the new location from the neighbors of new's neighbors
    for neighbor in adjacency_list[new_location]:
        if new_location in adjacency_list[neighbor]:
            adjacency_list[neighbor].remove(new_location)
    # clear new_location's adj. list
    adjacency_list[new_location].clear()

    # Add new location to obstacles
    # obstacles_local.append(new_location)

    return adjacency_list


def add_obstacle(adjacency_list, obstacle):
    '''
    Update the graph when an obstacle is added. And send obstacle_list to server
    '''
    global obstacles_local
    obstacles_local.append(obstacle)
    # Remove the obstacle from the neighbors of its neighbors
    for neighbor in adjacency_list[obstacle]:
        if obstacle in adjacency_list[neighbor]:
            adjacency_list[neighbor].remove(obstacle)

    # Update the adjacency list with the new location
    adjacency_list[obstacle].clear()

    for i, name in enumerate(unit_names):
        if sv_name == name:
            client.publish(
                mqtt_obstacles_topics[i], json.dumps(obstacles_local))


def create_graph(adjacency_list, obstacles_units):
    '''
    Creates a graph represented by an adjacency list based on a 10x10 grid,
    considering the specified obstacle units.

    Parameters:
    - adjacency_list: The dictionary representing the adjacency list of the graph
    - obstacles_units: A set containing the coordinates of the obstacle units in the grid

    Returns:
    - adjacency_list: The updated adjacency list representing the graph
    '''
    for i in range(10):
        for j in range(10):
            neighbors = set()

            if (i, j) not in obstacles_units:
                if i > 0 and (i - 1, j) not in obstacles_units:
                    neighbors.add((i - 1, j))  # Add the neighbor to the left
                if i < 9 and (i + 1, j) not in obstacles_units:
                    neighbors.add((i + 1, j))  # Add the neighbor to the right
                if j > 0 and (i, j - 1) not in obstacles_units:
                    neighbors.add((i, j - 1))  # Add the neighbor above
                if j < 9 and (i, j + 1) not in obstacles_units:
                    neighbors.add((i, j + 1))  # Add the neighbor below

            adjacency_list[(i, j)] = neighbors

    return adjacency_list


def solve(s):
    '''
    Performs a breadth-first search traversal on a graph, starting node s.

    Returns:
    - prev: A dictionary mapping each node to its previous node in the traversal path
    '''
    q = deque()
    q.append(s)

    visited = {node: False for node in graph}
    visited[s] = True

    prev = {node: None for node in graph}

    while q:
        node = q.popleft()
        neighbors = graph[node]

        for next in neighbors:
            if not visited[next]:
                q.append(next)
                visited[next] = True
                prev[next] = node
    return prev


def reconstructPath(s, e, prev):
    '''
    Reconstructs the path from the start node (s) to the end node (e) using the prev dictionary.

    Returns:
    - path: The reconstructed path from s to e (excluding s if it exists)
    '''
    path = []
    p = e
    while p:
        path.append(p)
        p = prev[p]

    path.reverse()

    # Return path except s if path exists
    return path[1:] if path[0] == s else []


def bfs(s, e):
    # Do a BFS starting at node s
    prev = solve(s)

    # Return reconstructed path from s -> e
    return reconstructPath(s, e, prev)


def update_leds(current, next):
    '''
    Turn on a led based on the current and next locations
    '''
    if next[0] > current[0]:
        led_pos_x.set(1)
        # Send "ON" string when subscribing
        client.publish(mqtt_led_topic[0], "LEDPOSXON")
    else:
        led_pos_x.set(0)
        # Send "OFF" string when subscribing
        client.publish(mqtt_led_topic[0], "LEDPOSXOFF")

    if next[0] < current[0]:
        led_neg_x.set(1)
        # Send "ON" string when subscribing
        client.publish(mqtt_led_topic[2], "LEDNEGXON")
    else:
        led_neg_x.set(0)
        # Send "OFF" string when subscribing
        client.publish(mqtt_led_topic[2], "LEDNEGXOFF")

    if next[1] > current[1]:
        led_pos_y.set(1)
        # Send "ON" string when subscribing
        client.publish(mqtt_led_topic[1], "LEDPOSYON")
    else:
        led_pos_y.set(0)
        # Send "OFF" string when subscribing
        client.publish(mqtt_led_topic[1], "LEDPOSYOFF")

    if next[1] < current[1]:
        led_neg_y.set(1)
        # Send "ON" string when subscribing
        client.publish(mqtt_led_topic[3], "LEDNEGYON")
    else:
        led_neg_y.set(0)
        # Send "OFF" string when subscribing
        client.publish(mqtt_led_topic[3], "LEDNEGYOFF")


# create the Robot instance
robot = Supervisor()
supervisorNode = robot.getSelf()

sv_translation_field = supervisorNode.getField("translation")
sv_target_field = supervisorNode.getField("target").value
sv_name = supervisorNode.getField("name").value

# get the time step of the current world
timestep = int(robot.getBasicTimeStep())

# calculate a multiple of timestep close to one second
duration = (1000 // timestep) * timestep

# Get leds
led_pos_y = robot.getDevice("led_pos_y")
led_neg_y = robot.getDevice("led_neg_y")
led_pos_x = robot.getDevice("led_pos_x")
led_neg_x = robot.getDevice("led_neg_x")
leds = [led_pos_y, led_neg_y, led_pos_x, led_neg_x]

# Init distance sensors
ds_n = robot.getDevice("sensor_north")
ds_e = robot.getDevice("sensor_east")
ds_s = robot.getDevice("sensor_south")
ds_w = robot.getDevice("sensor_west")
dist_sensors = [ds_n, ds_e, ds_s, ds_w]
for ds in dist_sensors:
    ds.enable(1)

global location_unit1
global location_unit2
global location_unit3
global location_unit4
location_unit1 = (0, 0)
location_unit2 = (9, 0)
location_unit3 = (9, 9)
location_unit4 = (0, 9)

other_units = [
    location_unit1,
    location_unit2,
    location_unit3,
    location_unit4,


]
this_unit_pos = supervisorNode.getPosition()
# Remove unit itself from other_units
other_units.remove(
    (round(10 * this_unit_pos[0]), round(10 * this_unit_pos[1])))

# Names of units
unit_names = [
    'box_unit1',
    'box_unit2',
    'box_unit3',
    'box_unit4'
]

# MQTT configuration
mqtt_broker = "68.183.3.184"  # 'broker_address'
mqtt_port = 1883

mqtt_robot_x_location_topics = [
    "robots/1/x",
    "robots/2/x",
    "robots/3/x",
    "robots/4/x",
]
mqtt_robot_y_location_topics = [
    "robots/1/y",
    "robots/2/y",
    "robots/3/y",
    "robots/4/y",
]
mqtt_obstacles_topics = [
    "obstacles/1",
    "obstacles/2",
    "obstacles/3",
    "obstacles/4"
]
mqtt_led_topic = [
    "led/positieve/x",
    "led/positieve/y",
    "led/negatieve/x",
    "led/negatieve/y"
]
mqtt_obstacles_master = "obstacles/masterlist"


# Create MQTT client
client = mqtt.Client()

# Set MQTT event callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
# client.connect(mqtt_broker, mqtt_port, 60)
client.connect(mqtt_broker, mqtt_port)
client.loop_start()

# Subscribe to other units' locations

for i, name in enumerate(unit_names):
    if sv_name != name:
        client.subscribe(mqtt_robot_x_location_topics[i])
        client.subscribe(mqtt_robot_y_location_topics[i])
client.subscribe("obstacles/masterlist")

global obstacles_local
global obstacles_server
obstacles_local = []
obstacles_server = []

# Create graph/adjacency list
graph = create_graph({}, other_units)


for obstacle_s in obstacles_server:
    if obstacle_s not in obstacles_local:  # check if a new obstacle came in from server
        add_obstacle(graph, obstacle_s)
        obstacles_local.append(obstacle_s)


# execute every second
while robot.step(duration) != -1:
    for led in leds:
        led.set(0)  # Turn of all leds

    position_field = supervisorNode.getPosition()

    # Get sensor values
    distance_north = ds_n.getValue()
    distance_east = ds_e.getValue()
    distance_south = ds_s.getValue()
    distance_west = ds_w.getValue()

    cur_pos = (round(10 * position_field[0]),   # round example: 0.1 -> 1
               round(10 * position_field[1]))
    target = (round(sv_target_field[0]),    # round example: 1.0 -> 1
              round(sv_target_field[1]))

    # Publish unit's location
    for i, name in enumerate(unit_names):
        if sv_name == name:
            client.publish(mqtt_robot_x_location_topics[i], cur_pos[0])
            client.publish(mqtt_robot_y_location_topics[i], cur_pos[1])

    # Check for obstacles with sensor data
    obstacle = ()
    if distance_north < 1000 and cur_pos[1] != 9:
        obstacle = (cur_pos[0], cur_pos[1] + 1)
        if obstacle not in obstacles_local:
            add_obstacle(graph, obstacle)
    if distance_east < 1000 and cur_pos[0] != 9:
        obstacle = (cur_pos[0] + 1, cur_pos[1])
        if obstacle not in obstacles_local:
            add_obstacle(graph, obstacle)
    if distance_south < 1000 and cur_pos[1] != 0:
        obstacle = (cur_pos[0], cur_pos[1] - 1)
        if obstacle not in obstacles_local:
            add_obstacle(graph, obstacle)
    if distance_west < 1000 and cur_pos[0] != 0:
        obstacle = (cur_pos[0] - 1, cur_pos[1])
        if obstacle not in obstacles_local:
            add_obstacle(graph, obstacle)

    # print(f'{sv_name} obst_local: {obstacles_local} ')

    # Calculate path if needed
    if target != cur_pos:
        path = bfs(cur_pos, target)
        if path:
            # path exists
            update_leds(cur_pos, path[0])
            sv_translation_field.setSFVec3f(
                [path[0][0]/10, path[0][1]/10, 0.05])
        else:
            # no path exists (path = [])
            pass    # TODO display on dashboard that target is unreachable
