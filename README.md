# ConnectedSystems


## Project Contributors

The project was developed by the following students:

1. Sam Yost (Student ID: 1030197)
2. Terrence Zhong (Student ID: 1028516)
3. Giovanny Marchena (Student ID: 1021941)


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
