const host = 'ws://68.183.3.184:1884';

// Simulate a location message for robot1
const message1 = '2';
const message2 = '2';
const topic1 = 'robots/1/x';
const topic2 = 'robots/1/y';
const packet1 = {};

const options = {
    keepalive: 50,
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 2000,
    connectTimeout: 50000,
};
const client = mqtt.connect(host, options);

const robot_subscriptions = ["robots/1/x",
                      "robots/1/y",   
                      "robots/2/x",
                      "robots/2/y", 
                      "robots/3/x",
                      "robots/3/y", 
                      "robots/4/x",
                      "robots/4/y"]

const obstacles_master_topic = "obstacles/masterlist";

// Connection successful
client.on('connect', () => {
    console.log('Connected to the broker');
    // Subscribe to robot and obstacle topics
    robot_subscriptions.forEach(topic => client.subscribe(topic));
    // obstacle_subscriptions.forEach(topic => client.subscribe(topic));
    client.subscribe(obstacles_master_topic);
});


let obstacleList = []; // Declare obstacleList 

let robotData = {
  "robots": {
    "1": {
      "x": 0,
      "y": 0
    },
    "2": {
      "x": 0,
      "y": 0
    },
    "3": {
      "x": 0,
      "y": 0
    },
    "4": {
      "x": 0,
      "y": 0
    }
  },
  "obstacles": {
    "1": {},
    "2": {},
    "3": {},
    "4": {}
  }
};

client.on('message', (topic, message, packet) => {
    console.log("Message received " + message + " on topic " + topic);

    const messageType = topic.split('/')[0];
    const robotName = topic.split('/')[1];
    const attribute = topic.split('/')[2];

    console.log("robotName");
    console.log(robotName);
    console.log("messageType");
    console.log(messageType);
    console.log("attribute");
    console.log(attribute);

    const payload = JSON.parse(message.toString());

    if (messageType === 'robots') {
        robotData.robots[robotName][attribute] = payload;

        // clearRobot(robotName);

        switch (robotName) {
            case '1':
                robot1.clearRect(20 * previousX1, 20 * previousY1, 20, 20);
                drawRobot1(robotData.robots[robotName].x + 1, robotData.robots[robotName].y + 1);
                updateBotCoordinates('robot1', robotData.robots[robotName].x, robotData.robots[robotName].y);
                document.getElementById('robot1Coordinates').textContent = '(' + robotData.robots[robotName].x + ', ' + robotData.robots[robotName].y + ')';
                break;
            case '2':
                robot2.clearRect(20 * previousX2, 20 * previousY2, 20, 20);
                drawRobot2(robotData.robots[robotName].x + 1, robotData.robots[robotName].y + 1);
                updateBotCoordinates('robot2', robotData.robots[robotName].x, robotData.robots[robotName].y);
                document.getElementById('robot2Coordinates').textContent = '(' + robotData.robots[robotName].x + ', ' + robotData.robots[robotName].y + ')';
                break;
            case '3':
                robot3.clearRect(20 * previousX3, 20 * previousY3, 20, 20);
                drawRobot3(robotData.robots[robotName].x + 1, robotData.robots[robotName].y + 1);
                updateBotCoordinates('robot3', robotData.robots[robotName].x, robotData.robots[robotName].y);
                document.getElementById('robot3Coordinates').textContent = '(' + robotData.robots[robotName].x + ', ' + robotData.robots[robotName].y + ')';
                break;
            case '4':
                robot4.clearRect(20 * previousX4, 20 * previousY4, 20, 20);
                drawRobot4(robotData.robots[robotName].x + 1, robotData.robots[robotName].y + 1);
                updateBotCoordinates('robot4', robotData.robots[robotName].x, robotData.robots[robotName].y);
                document.getElementById('robot4Coordinates').textContent = '(' + robotData.robots[robotName].x + ', ' + robotData.robots[robotName].y + ')';
                break;
            default:
                break;
        }
    } else if (messageType === 'obstacles') {
        console.log("obstacles received:");
        obstacleList = JSON.parse(message.toString())
        console.log(obstacleList);
        obstacleList.forEach(obst => drawObstacle(obst[0] + 1, obst[1] + 1))
        updateObstaclesOnWebpage(obstacleList);
    }
    console.log(obstacleList);
});


//Connection Failed
client.on('error', (err) => {
    console.log('Connection failed error: ', err);
    client.end();
});

function noodstop() {
    client.publish("noodstop", "Y");
    console.log("Emergency stop button clicked");
}

function updateBotCoordinates(robotName, x, y) {
    const botCoordinatesSpan = document.getElementById(robotName + "Coordinates");
    botCoordinatesSpan.textContent = `(${x}, ${y})`;
    // botCoordinatesSpan.textContent = " (" + x + ", " + y + ")";
}

// Define a global array to store the command queue
let commandQueue = [];

function addToQueue() {
  const originX = document.getElementById("originX").value;
  const originY = document.getElementById("originY").value;
  const targetX = document.getElementById("target2X").value;
  const targetY = document.getElementById("target2Y").value;

  const payload = {
    origin: {
      x: originX,
      y: originY
    },
    target: {
      x: targetX,
      y: targetY
    }
  };

  const message = JSON.stringify(payload);

  // Publish the message to the "queued-destination/queue" topic
  client.publish("queued-destination/queue", message);

  // Clear the input fields
  document.getElementById("originX").value = "";
  document.getElementById("originY").value = "";
  document.getElementById("target2X").value = "";
  document.getElementById("target2Y").value = "";
}

function sendTarget() {
  let unit = document.getElementById("robotunit").value;
  let targetX = document.getElementById("targetX").value;
  let targetY = document.getElementById("targetY").value;

  let payload = {};

  if (unit == "1") {
    payload = {
      robotunit: { id: "1" },
      target: { x: targetX, y: targetY }
    };
    console.log("Robot1-Target Set");
  } else if (unit == "2") {
    payload = {
      robotunit: { id: "2" },
      target: { x: targetX, y: targetY }
    };
    console.log("Robot2-Target Set");
  } else if (unit == "3") {
    payload = {
      robotunit: { id: "3" },
      target: { x: targetX, y: targetY }
    };
    console.log("Robot3-Target Set");
  } else if (unit == "4") {
    payload = {
      robotunit: { id: "4" },
      target: { x: targetX, y: targetY }
    };
    console.log("Robot4-Target Set");
  }

  // Create a command object
  const command = {
    unit,
    targetX,
    targetY
  };

  // Add the command to the queue
//   commandQueue.push(command); //-

  console.log("Command added to the queue:", command);

  // Display the queued task on the webpage
  const queueList = document.getElementById("queueList");
  const queueItem = document.createElement("li");
  queueItem.textContent = `robotunit: ${unit}, Target: (${targetX}, ${targetY})`; //#
  queueList.appendChild(queueItem);

  // Push the command to the command queue
  commandQueue.push(payload); //-

  // Clear the input fields
  document.getElementById("robotunit").value = "";
  document.getElementById("targetX").value = "";
  document.getElementById("targetY").value = "";
}

function processCommandQueue() {
  // Process the commands in the queue
  while (commandQueue.length > 0) {
    const command = commandQueue.shift(); // Retrieve and remove the first command from the queue

    // Perform the desired actions based on the command
    console.log("Processing command:", command);
    // Convert the command object to a JSON string
    const message = JSON.stringify(command);

    // Publish the command to the "queued-destination/target" topic
    client.publish("queued-destination/target", message);

    // Example: Update the robot coordinates based on the command
    const robotName = command.unit;
    const robotCoordinatesElement = document.getElementById(robotName + "Queue");
    if (robotCoordinatesElement) {
      robotData.robots[robotName].x = command.targetX;
      robotData.robots[robotName].y = command.targetY;
      robotCoordinatesElement.textContent = '(' + robotData.robots[robotName].x + ', ' + robotData.robots[robotName].y + ')';
    }
  }
}

// Function to remove a task from the command queue
function removeTaskFromQueue(index) {
  if (index >= 0 && index < commandQueue.length) {
    // Remove the task at the specified index
    const removedTask = commandQueue.splice(index, 1)[0];
    console.log("Removed task:", removedTask);

    // Update the queue list on the webpage
    updateQueueList();
  }
  // Generate buttons for each task in the queue
commandQueue.forEach((command, index) => {
  const removeButton = document.createElement("button");
  removeButton.textContent = "Remove";
  removeButton.addEventListener("click", () => {
    removeTaskFromQueue(index); // Pass the index value to the removeTaskFromQueue function
  });

  // Append the remove button to the queue item
  queueItem.appendChild(removeButton);
});

}

// Update the queue list on the webpage
function updateQueueList() {
  const queueList = document.getElementById("queueList");
  queueList.innerHTML = ""; // Clear the existing list

  // Rebuild the queue list based on the updated commandQueue array
  commandQueue.forEach((command, index) => {
    const queueItem = document.createElement("li");
    queueItem.textContent = `robotunit: ${command.unit}, Target: (${command.targetX}, ${command.targetY})`;

    // Create a button to remove the task
    const removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.addEventListener("click", () => {
      removeTaskFromQueue(index);
    });

    // Append the remove button to the queue item
    queueItem.appendChild(removeButton);

    // Append the queue item to the queue list
    queueList.appendChild(queueItem);
  });
}




const canvas = document.getElementById("theCanvas");
const border = canvas.getContext("2d");
const obstacles = canvas.getContext("2d");
const robot1 = canvas.getContext("2d");
const robot2 = canvas.getContext("2d");
const robot3 = canvas.getContext("2d");
const robot4 = canvas.getContext("2d");

canvas.width = 200;
canvas.height = 200;

CanvasRenderingContext2D.prototype.drawBlock = function(x, y) {
  this.fillRect(20 * x, 20 * y, 20, 20)
};

let previousX1 = -1;
let previousY1 = -1;
let previousX2 = -1;
let previousY2 = -1;
let previousX3 = -1;
let previousY3 = -1;
let previousX4 = -1;
let previousY4 = -1;

function clearCanvas() {
  robot1.clearRect(20 * previousX1, 20 * previousY1, 20, 20);
  robot2.clearRect(20 * previousX2, 20 * previousY2, 20, 20);
  robot3.clearRect(20 * previousX3, 20 * previousY3, 20, 20);
  robot4.clearRect(20 * previousX4, 20 * previousY4, 20, 20);
}

// Function to clear the previous position of a robot on the canvas
function clearRobot(robotName) {
  const context = getCanvasContext(robotName);
  const { X, Y } = robotData[robotName].location;
  context.clearRect(20 * X, 20 * Y, 20, 20);
}

// Function to get the canvas context based on the robot's name
function getCanvasContext(robotName) {
  const canvas = document.getElementById('theCanvas');
  return canvas.getContext('2d');
}

function drawRobot1(x, y) {
    console.log("Robot-1");
    // console.log(x,y);
    robot1.fillStyle = "red";
    robot1.drawBlock(x - 1, 10 - y);
    previousX1 = x - 1;
    previousY1 = 10 - y;
}

function drawRobot2(x, y) {
    console.log("Robot-2");
    robot2.fillStyle = "yellow";
    robot2.drawBlock(x - 1, 10 - y);
    previousX2 = x - 1;
    previousY2 = 10 - y;
}

function drawRobot3(x, y) {
    console.log("Robot-3");
    robot3.fillStyle = "blue";
    robot3.drawBlock(x - 1, 10 - y);
    previousX3 = x - 1;
    previousY3 = 10 - y;
}

function drawRobot4(x, y) {
    robot4.fillStyle = "green";
    robot4.drawBlock(x - 1, 10 - y);
    previousX4 = x - 1;
    previousY4 = 10 - y;
}

function drawObstacle(x, y) {
    obstacles.fillStyle = "darkred";
    obstacles.drawBlock(x - 1, 10 - y);
}

function updateObstaclesOnWebpage(obstacles) {
    // Display obstacles as a list
    const obstacleListContainer = document.getElementById('obstacleList');
    obstacleListContainer.innerHTML = ''; // Clear previous obstacles

    obstacles.forEach((obstacle) => {
        const obstacleItem = document.createElement('li');
        obstacleItem.textContent = `X: ${obstacle.X}, Y: ${obstacle.Y}`;
        obstacleListContainer.appendChild(obstacleItem);
    });
}

function testMessage(){
  // test messages for location
client.publish('robot/1/location', JSON.stringify({ targetX: 10, targetY: 20 }));
client.publish('robot/2/location', JSON.stringify({ targetX: 5, targetY: 15 }));
client.publish('robot/3/location', JSON.stringify({ targetX: 8, targetY: 12 }));
client.publish('robot/4/location', JSON.stringify({ targetX: 3, targetY: 7 }));

// test messages for obstacle
client.publish('robot/1/obstacle', '1000');
client.publish('robot/2/obstacle', '0100');
client.publish('robot/3/obstacle', '0010');
client.publish('robot/4/obstacle', '0001');

}

// Call the drawObstacle function
// drawObstacle(3, 4);

// Call the drawRobot function
// drawRobot1(1, 2);

// Inside the 'message' event handler, after the line "console.log(obstacleList);",
// add the following code to update the obstacle list on the webpage:
// updateObstaclesOnWebpage();



// client.emit('message', topic1, message1, packet1);
// client.emit('message', topic2, message2, packet1);