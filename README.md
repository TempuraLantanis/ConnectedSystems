# ConnectedSystems

### Protocol: MQTT

This system uses the MQTT protocol for communication.

#### Topics

The following MQTT topics are used in the system:

- `/robots/<id>/locatie/x`: Represents the x-coordinate of a robot's location.
- `/robots/<id>/locatie/y`: Represents the y-coordinate of a robot's location.
- `/robots/<id>/richting/x`: Represents the x-component of a robot's direction.
- `/robots/<id>/richting/y`: Represents the y-component of a robot's direction.
- `/obstakels/<type>/<id>/locatie/x`: Represents the x-coordinate of an obstacle's location.
- `/obstakels/<type>/<id>/locatie/y`: Represents the y-coordinate of an obstacle's location.

#### Robots Topic

The Robots topic contains information about the robots in the system. The sub-topics under this topic provide the following data:

- `id`: A string identifier with two digits that uniquely identifies a robot.
- `locatie/x` and `locatie/y`: Floating-point values representing the x and y coordinates of a robot's location, respectively.
- `richting/x` and `richting/y`: Floating-point values representing the x and y components of a robot's direction vector, respectively.

#### Obstakels Topic

The Obstakels topic contains information about obstacles in the system. The sub-topics under this topic provide the following data:

- `type`: A string indicating the type of obstacle, which can be "wand" or "obstakel".
- `id`: A string identifier with two digits that uniquely identifies an obstacle.
- `locatie/x` and `locatie/y`: Floating-point values representing the x and y coordinates of an obstacle's location, respectively.

#### Raw

All messages published to these topics should be retained, meaning they will be saved and delivered to new subscribers when they join the system. This ensures that the latest information is available to all subscribers.
