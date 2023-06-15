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
    # print("Received message: " + message + " from " + msg.topic)
    # print(msg.topic[:5])

    if msg.topic[:6] == "robots":
        # print('msg Pos received')
        updatePosition(msg)

    if msg.topic == "obstacles/masterlist":
        # print('obstacles received')

        # print(msg)
        pass

        # json.dumps()


def updatePosition(case):
    global location_unit1
    global location_unit2
    global location_unit3
    global location_unit4
    temp_location = ()
    locations_units = [
        location_unit1,
        location_unit2,
        location_unit3,
        location_unit4
    ]
    # topics
    unit_index = -1
    # print(f'unit_2 = {location_unit2} ')
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

    global graph
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
    # TODO remove from obstacles if moved
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

    return adjacency_list


def add_obstacle(adjacency_list, obstacle):
    '''
    Update the graph when an obstacle is added. And send obstacle_list to server
    '''
    obstacles_local.append(obstacle)
    # Remove the obstacle from the neighbors of its neighbors
    for neighbor in adjacency_list[obstacle]:
        if obstacle in adjacency_list[neighbor]:
            adjacency_list[neighbor].remove(obstacle)

    # Update the adjacency list with the new location
    adjacency_list[obstacle].clear()

    for i, name in enumerate(unit_names):
        if sv_name == name:
            # print(json_obstacles_server)
            # TODO: if not in other_units_locations
            obstacles_publish = []
            # for obst in obstacles_local:
            #     if obst not in other_units:
            # obstacles_publish.append(obst)
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
    elif next[0] < current[0]:
        led_neg_x.set(1)
    elif next[1] > current[1]:
        led_pos_y.set(1)
    elif next[1] < current[1]:
        led_neg_y.set(1)


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
mqtt_obstacles_master = "obstacles/masterlist"

# subscribe_topics = ["$SYS/broker/clients",
#                     "obstakels",
#                     "currentDestination",
#                     "queuedDestination",
#                     "robots/1/x",
#                     "robots/2/x",
#                     "robots/3/x",
#                     "robots/4/x",
#                     "robots/1/y",
#                     "robots/2/y",
#                     "robots/3/y",
#                     "robots/4/y"]

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

# TODO get locations from all the units from the server
for i, name in enumerate(unit_names):
    if sv_name != name:
        client.subscribe(mqtt_robot_x_location_topics[i])
        client.subscribe(mqtt_robot_y_location_topics[i])
client.subscribe("obstacles/masterlist")


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

    # Update graph if another unit has moved
    for unit in other_units:
        # TODO update all unit's locations from server (except current unit)
        pass
        # TODO copmare local units with server if moved
        # if unit_local != unit_server:   # unit has moved
        #   graph = update_graph(graph, obstacles+other_units, unit_local_location, unit_server_location)

    cur_pos = (round(10 * position_field[0]),   # round example: 0.1 -> 1
               round(10 * position_field[1]))
    target = (round(sv_target_field[0]),    # round example: 1.0 -> 1
              round(sv_target_field[1]))

    # Publish MQTT messages
    # message = "Hello, ESP32. This is WeBots!"
    for i, name in enumerate(unit_names):
        if sv_name == name:
            # print(f'cur_pos[{i}] = {cur_pos[i]} ')
            client.publish(mqtt_robot_x_location_topics[i], cur_pos[0])
            client.publish(mqtt_robot_y_location_topics[i], cur_pos[1])
    # print(message)

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

    # obstacles_server = [tuple(x)
    #                          for x in json.loads(json_obstacles_local)]
    if sv_name == "box_unit1":
        print(f'{sv_name} Unit 2: {location_unit2} ')

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
