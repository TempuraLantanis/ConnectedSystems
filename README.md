# ConnectedSystems


## Project Contributors

The project was developed by the following students:

1. Sam Yost (Student ID: 1030197)
2. Terrence Zhong (Student ID: 1028516)
3. Giovanny Marchena (Student ID: 1021941)

## Description

ConnectedSystems is a collaborative project developed by Sam Yost, Terrence Zhong, and Giovanny Marchena. The project aims to create a connected system using the MQTT protocol for efficient and reliable communication between Webots.

## Features

- MQTT Protocol: The system leverages the MQTT (Message Queuing Telemetry Transport) protocol, a lightweight messaging protocol, to facilitate seamless communication between different devices and components. MQTT ensures efficient message exchange and supports reliable communication even in low-bandwidth or unreliable network environments.

- Robot Tracking: The system enables real-time tracking and monitoring of multiple robots. Using MQTT topics such as `/robots/<id>/locatie/x`, `/robots/<id>/locatie/y`, `/robots/<id>/richting/x`, and `/robots/<id>/richting/y`, the system retrieves and updates the location and direction of each robot. This information can be utilized for coordination, navigation, and control purposes.

- Obstacle Detection: The system incorporates obstacle detection and sharing functionality. MQTT topics such as `/obstacles/<type>/<id>/locatie/x` and `/obstacles/<type>/<id>/locatie/y` provide the coordinates of detected obstacles. Additionally, a masterlist topic (`obstacles/masterlist`) is used to consolidate and update the obstacle data from all connected robots. This masterlist information can be utilized for pathfinding algorithms and obstacle avoidance strategies.

- Queue Management: The system includes a queue management system for organizing and prioritizing tasks and destinations. The `queued-destination/queue` topic receives incoming target destinations that are assigned to the robots by the server. This queue-based approach ensures orderly execution of tasks and efficient allocation of resources.

- Pathfinding Algorithm: The system incorporates a pathfinding algorithm based on breadth-first search (BFS). The BFS algorithm is utilized to calculate the shortest path between two locations, considering the presence of obstacles. This algorithm ensures efficient navigation for the robots, optimizing their movement and minimizing travel time.


- Noodstop Functionality: The system incorporates a "noodstop" functionality, which allows for an emergency stop of all running processes. When a "Y" message is published to the "noodstop" topic, the system responds by stopping all program execution. The system continuously monitors the "noodstop" topic, ensuring prompt response to emergency stop requests.


### Protocol: MQTT

This system uses the MQTT protocol for communication.

#### Topics

The following MQTT topics are used in the system:

- `/robots/<id>/locatie/x`: Represents the x-coordinate of a robot's location.
- `/robots/<id>/locatie/y`: Represents the y-coordinate of a robot's location.
- `/robots/<id>/richting/x`: Represents the x-component of a robot's direction.
- `/robots/<id>/richting/y`: Represents the y-component of a robot's direction.
- `/obstacles/<type>/<id>/locatie/x`: Represents the x-coordinate of an obstacle's location.
- `/obstacles/<type>/<id>/locatie/y`: Represents the y-coordinate of an obstacle's location.
- `obstacles/masterlist`: contains all known detected obstacle coordinates from all robot's, this is used to update the pathfinding algorithm for all connected robot's
- `obstacles/<id>`: contains the coordinates of obstacles detected by that specific id
- `currentdestination/<id>`: this topic is the current destination which the robot will go to 
- `queued-destination/queue`: this topic will receive all incoming target destination that will be assigned to the robot by the server
- `queued-destination/target/`: This topic is used to publish the target destinations that are queued for the robots.
    - Publish Format; JSON object with the following propoties:
        - `id`: A string identifier specifying the robot ID.
        - `destination/x`: The x-coordinate of the target destination.
        - `destination/y`: The y-coordinate of the target destination.
- `target-destination`: This topic is used to publish the target destination for a specific robot.
    - Publish Format: JSON object with the following properties:
        - `id:` A string identifier specifying the robot ID.
        - `destination/x:` The x-coordinate of the target destination.
        - `destination/y:` The y-coordinate of the target destination.

#### Robots Topic

The Robots topic contains information about the robots in the system. The sub-topics under this topic provide the following data:

- `id`: A string identifier with two digits that uniquely identifies a robot.
- `robots/x` and `robots/y`: values representing the x and y coordinates of a robot's location, respectively.
- `richting/x` and `richting/y`:values representing the x and y components of a robot's direction vector, respectively.
- `led/positieve/x`: This topic represents the x-coordinate of the positieve LED location on a robot.
    - Publish Format: Integer value representing the x-coordinate.
- `led/positieve/y`: This topic represents the y-coordinate of the positive LED location on a robot.
    - Publish Format: Integer value representing the y-coordinate..
- `led/negatieve/x`: This topic represents the x-coordinate of the negative LED location on a robot.
    - Publish Format: Integer value representing the x-coordinate.
- `led/negatieve/y`: This topic represents the y-coordinate of the negative LED location on a robot.
    - Publish Format: Integer value representing the y-coordinate.




#### Obstakels Topic

The Obstacles topic contains information about obstacles in the system. The sub-topics under this topic provide the following data:

- `obstacles/id` these represent obstacles
#### Raw

All messages published to these topics should be retained, meaning they will be saved and delivered to new subscribers when they join the system. This ensures that the latest information is available to all subscribers.



### Server
The server should be ran preferably as close to the broker as possible to reduce latency, the server interfaces with the mqtt protocol to check incoming positions, adding commands to the queue , updating states of the robots,and handles obstacle updates that are communicated through a mqtt broker.
