const host = 'ws://68.183.3.184:1884';

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

const obstacle_subscriptions = ["obstacles/1",
                      "obstacles/2",   
                      "obstacles/3",
                      "obstacles/4"]

//Connection lukt
client.on('connect', () => {
    console.log('Connected to the broker');
    //Testing
    robot_subscriptions.forEach(topic => client.subscribe(topic));
    obstacle_subscriptions.forEach(topic => client.subscribe(topic));
});

let robotData = {
    robot1: {
        location: { X: -1, Y: -1 },
        obstacles: "0000"
    },
    robot2: {
        location: { X: -1, Y: -1 },
        obstacles: "0000"
    },
    robot3: {
        location: { X: -1, Y: -1 },
        obstacles: "0000"
    },
    robot4: {
        location: { X: -1, Y: -1 },
        obstacles: "0000"
    }
};

client.on('message', (topic, message, packet) => {
    console.log("Message received " + message + " on topic " + topic);

    const robotName = topic.split('/')[0];
    const messageType = topic.split('/')[1];

    testMessage();
    
    // Extract the target coordinates from the message payload
    const payload = JSON.parse(message.toString());
    const targetX = payload.targetX;
    const targetY = payload.targetY;

        if (messageType === 'location') {
            const [x, y] = message.toString().split(';');
            robotData[robotName].location.X = parseInt(x);
            robotData[robotName].location.Y = parseInt(y);
            switch (robotName) {
                case 'robot1':
                    robot1.clearRect(20 * previousX1, 20 * previousY1, 20, 20);
                    drawRobot1(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot1', robotData[robotName].location.X, robotData[robotName].location.Y);
                    document.getElementById('robot1Coordinates').textContent = '(' + targetX + ', ' + targetY + ')';
                    break;
                case 'robot2':
                    robot2.clearRect(20 * previousX2, 20 * previousY2, 20, 20);
                    drawRobot2(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot2', robotData[robotName].location.X, robotData[robotName].location.Y);
                    document.getElementById('robot2Coordinates').textContent = '(' + targetX + ', ' + targetY + ')';
                    break;
                case 'robot3':
                    robot3.clearRect(20 * previousX3, 20 * previousY3, 20, 20);
                    drawRobot3(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot3', robotData[robotName].location.X, robotData[robotName].location.Y);
                     document.getElementById('robot3Coordinates').textContent = '(' + targetX + ', ' + targetY + ')';
                    break;
                case 'robot4':
                    robot4.clearRect(20 * previousX4, 20 * previousY4, 20, 20);
                    drawRobot4(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot4', robotData[robotName].location.X, robotData[botNarobotNameme].location.Y);
                    document.getElementById('robot4Coordinates').textContent = '(' + targetX + ', ' + targetY + ')';
                    break;
                default:
                    break;
            }

        } else if (messageType === 'obstacle') {
            

            robotData[robotName].obstacles = message.toString();
            let obstacles = robotData[robotName].obstacles;
            let obsNorth = obstacles.charAt(0);
            let obsEast = obstacles.charAt(1);
            let obsSouth = obstacles.charAt(2);
            let obsWest = obstacles.charAt(3);

            // Clear the obstacleList array before updating with new obstacles
            obstacleList.length = 0;

            if (obsNorth == '1'){
                obstacleList.push({ X: robotData[robotName].location.X, Y: robotData[robotName].location.Y - 1 });
                drawObstacle(robotData[robotName].location.X + 1, robotData[robotName].location.Y - 1 + 1);
            }
            if (obsEast == '1'){
                obstacleList.push({ X: robotData[robotName].location.X + 1, Y: robotData[robotName].location.Y});
                drawObstacle(robotData[robotName].location.X + 1 + 1, robotData[robotName].location.Y + 1);

            }
            if (obsSouth == '1'){
                obstacleList.push({ X: robotData[robotName].location.X, Y: robotData[robotName].location.Y + 1});
                drawObstacle(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1 + 1);

            }
            if (obsWest == '1'){
                obstacleList.push({ X: robotData[robotName].location.X - 1, Y: robotData[robotName].location.Y});
                drawObstacle(robotData[robotName].location.X + 1 - 1, robotData[robotName].location.Y + 1);

            }
            // Call a function to update the webpage with the new obstacle data
            updateObstaclesOnWebpage(obstacleList);
        }
        console.log(obstacleList);
});

//Connection lukt niet
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
    botCoordinatesSpan.textContent = " (" + x + ", " + y + ")";
}

function sendTarget() {
    let unit = document.getElementById("unit").value;
    let targetX = document.getElementById("targetX").value;
    let targetY = document.getElementById("targetY").value;
    if (unit == "robot1"){
        client.publish("robots/1/x", targetX);
        client.publish("robots/1/y", targetY);
        // client.publish(targetX,targetY);
        console.log("Robot1-Target Set");
    }
    if (unit == "robot2"){
        client.publish("robots/2/x", targetX);
        client.publish("robots/2/y", targetY);
        // client.publish(targetX,targetY);
        console.log("Robot2-Target Set");
    }
    if (unit == "robot3"){
        client.publish("robots/3/x", targetX);
        client.publish("robots/3/y", targetY);
        // client.publish(targetX,targetY);
        console.log("Robot3-Target Set");
    }
    if (unit == "robot4"){
        client.publish("robots/4/x", targetX);
        client.publish("robots/4/y", targetY);
        // client.publish(targetX,targetY);
        console.log("Robot4-Target Set");
    }
}

function addToQueue() {
    // let origin = document.getElementById("origin").value;
    // const originX = origin.charAt(1);
    // const originY = origin.charAt(4);
    // let target2X = document.getElementById("target2X").value;
    // const targetX2 = target2X.charAt(1);
    // client.publish("queued-destination/queue");
    // let target2Y = document.getElementById("target2Y").value;
    // const targetY2 = target2Y.charAt(4);
    // client.publish("queued-destination/queue");

      // Get the input values
  // const originX = document.getElementById("originX").value;
  // const originY = document.getElementById("originY").value;
  const targetX = document.getElementById("target2X").value;
  const targetY = document.getElementById("target2Y").value;

  // Create the payload object
  const payload = {
    // origin: {
    //   x: originX,
    //   y: originY
    // },
    target: {
      x: targetX,
      y: targetY
    }
  };

  // Convert the payload object to a JSON string
  const message = JSON.stringify(payload);

  // Publish the message to the "queued-destination/queue" topic
  client.publish("queued-destination/queue", message);

  // Clear the input fields
  // document.getElementById("originX").value = "";
  // document.getElementById("originY").value = "";
  document.getElementById("target2X").value = "";
  document.getElementById("target2Y").value = "";
}

let obstacleList = [];



const canvas = document.getElementById("theCanvas");
const border = canvas.getContext("2d");
const obstacles = canvas.getContext("2d");
const robot1 = canvas.getContext("2d");
const robot2 = canvas.getContext("2d");
const robot3 = canvas.getContext("2d");
const robot4 = canvas.getContext("2d");

canvas.width = 240;
canvas.height = 240;

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

function drawRobot1(x, y) {
    console.log(x,y);
    robot1.fillStyle = "red";
    robot1.drawBlock(x, y);
    previousX1 = x;
    previousY1 = y;
}

function drawRobot2(x, y) {
    robot2.fillStyle = "green";
    robot2.drawBlock(x, y);
    previousX2 = x;
    previousY2 = y;
}

function drawRobot3(x, y) {
    robot3.fillStyle = "blue";
    robot3.drawBlock(x, y);
    previousX3 = x;
    previousY3 = y;
}

function drawRobot4(x, y) {
    console.log("AYO");
    robot4.fillStyle = "yellow";
    robot4.drawBlock(x, y);
    previousX4 = x;
    previousY4 = y;
}

function drawObstacle(x, y) {
    obstacles.fillStyle = "darkred";
    obstacles.drawBlock(x, y);
}

function updateObstaclesOnWebpage(obstacles) {
    // Here, you can manipulate the webpage's HTML or DOM elements
    // to display the obstacles in the desired format

    // Example: Display obstacles as a list
    const obstacleListContainer = document.getElementById('obstacleList');
    obstacleListContainer.innerHTML = ''; // Clear previous obstacles

    obstacles.forEach((obstacle) => {
        const obstacleItem = document.createElement('li');
        obstacleItem.textContent = `X: ${obstacle.X}, Y: ${obstacle.Y}`;
        obstacleListContainer.appendChild(obstacleItem);
    });
    // Append the updated obstacle list to the obstacles container
    obstaclesContainer.appendChild(obstacleListElement);
}

function testMessage(){
  // Example test messages for location
client.publish('robot/1/location', JSON.stringify({ targetX: 10, targetY: 20 }));
client.publish('robot/2/location', JSON.stringify({ targetX: 5, targetY: 15 }));
client.publish('robot/3/location', JSON.stringify({ targetX: 8, targetY: 12 }));
client.publish('robot/4/location', JSON.stringify({ targetX: 3, targetY: 7 }));

// Example test messages for obstacle
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