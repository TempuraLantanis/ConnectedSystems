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

        if (messageType === 'location') {
            const [x, y] = message.toString().split(';');
            robotData[robotName].location.X = parseInt(x);
            robotData[robotName].location.Y = parseInt(y);
            switch (robotName) {
                case 'robot1':
                    robot1.clearRect(20 * previousX1, 20 * previousY1, 20, 20);
                    drawRobot1(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot1', robotData[robotName].location.X, robotData[robotName].location.Y);
                    break;
                case 'robot2':
                    robot2.clearRect(20 * previousX2, 20 * previousY2, 20, 20);
                    drawRobot2(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot2', robotData[robotName].location.X, robotData[robotName].location.Y);
                    break;
                case 'robot3':
                    robot3.clearRect(20 * previousX3, 20 * previousY3, 20, 20);
                    drawRobot3(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot3', robotData[robotName].location.X, robotData[robotName].location.Y);
                    break;
                case 'robot4':
                    robot4.clearRect(20 * previousX4, 20 * previousY4, 20, 20);
                    drawRobot4(robotData[robotName].location.X + 1, robotData[robotName].location.Y + 1);
                    updateBotCoordinates('robot4', robotData[robotName].location.X, robotData[botNarobotNameme].location.Y);
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
    let target = document.getElementById("target").value;
    if (unit == "robot1"){
        client.publish("robots/1/x", target);
        client.publish("robots/1/y", target);
    }
    if (unit == "robot2"){
        client.publish("robots/2/x", target);
        client.publish("robots/2/y", target);
    }
    if (unit == "robot3"){
        client.publish("robots/3/x", target);
        client.publish("robots/3y", target);
    }
    if (unit == "robot4"){
        client.publish("robots/4/x", target);
        client.publish("robots/4/y", target);
    }
}

function addToQueue() {
    let origin = document.getElementById("origin").value;
    const originX = origin.charAt(1);
    const originY = origin.charAt(4);
    let target2 = document.getElementById("target2").value;
    const targetX2 = target2.charAt(1);
    const targetY2 = target2.charAt(4);
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