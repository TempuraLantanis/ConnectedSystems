const broker = 'mqtt://localhost:1883';
const clientId = 'dashboard_' + Math.random().toString(16).substr(2, 8);
const topicPrefix = 'dashboard/';

const client = new Paho.MQTT.Client(broker, Number(1883), clientId);

const mapElement = document.getElementById('map');
const queueElement = document.getElementById('queue');
const unitSelectElement = document.getElementById('unit-select');
const goalInputElement = document.getElementById('goal-input');
const setGoalBtnElement = document.getElementById('set-goal-btn');
const opdrachtInputElement = document.getElementById('opdracht-input');
const addOpdrachtBtnElement = document.getElementById('add-opdracht-btn');
const removeOpdrachtBtnElement = document.getElementById('remove-opdracht-btn');
const noodstopBtnElement = document.getElementById('noodstop-btn');

// Connect to the MQTT broker
client.connect({
  onSuccess: onConnect,
  onFailure: onFailure
});

function onConnect() {
  console.log('Connected to MQTT broker');
  client.subscribe(topicPrefix + '#');
}

function onFailure(err) {
  console.error('Failed to connect to MQTT broker:', err);
}

// Handle received MQTT messages
client.onMessageArrived = function (message) {
  const topic = message.destinationName;
  const payload = JSON.parse(message.payloadString);

  // Handle different topics and update the dashboard accordingly
  if (topic === topicPrefix + 'map') {
    updateMap(payload);
  } else if (topic === topicPrefix + 'queue') {
    updateQueue(payload);
  } else if (topic === topicPrefix + 'units') {
    updateUnits(payload);
  }
};

// Update the map with unit and obstacle positions
function updateMap(mapData) {
  // Clear the map
  mapElement.innerHTML = '';

  // Add units and obstacles to the map
  mapData.units.forEach(unit => {
    const unitElement = document.createElement('div');
    unitElement.className = 'unit';
    unitElement.style.left = unit.x + 'px';
    unitElement.style.top = unit.y + 'px';
    mapElement.appendChild(unitElement);
  });

  mapData.obstacles.forEach(obstacle => {
    const obstacleElement = document.createElement('div');
    obstacleElement.className = 'obstacle';
    obstacleElement.style.left = obstacle.x + 'px';
    obstacleElement.style.top = obstacle.y + 'px';
    mapElement.appendChild(obstacleElement);
  });
}

// Update the opdrachtenqueue
function updateQueue(queueData) {
  // Clear the queue
  queueElement.innerHTML = '';

  // Add opdrachten to the queue
  queueData.forEach(opdracht => {
    const opdrachtElement = document.createElement('li');
    opdrachtElement.innerText = opdracht;
    queueElement.appendChild(opdrachtElement);
  });
}

// Update the unit dropdown for goal setting
function updateUnits(unitsData) {
  // Clear the unit dropdown
  unitSelectElement.innerHTML = '';

  // Add units to the dropdown
  unitsData.forEach(unit => {
    const unitOption = document.createElement('option');
    unitOption.value = unit.id;
    unitOption.innerText = unit.name;
    unitSelectElement.appendChild(unitOption);
  });
}

// Set goal for a unit
setGoalBtnElement.addEventListener('click', function () {
  const unitId = unitSelectElement.value;
  const goal = goalInputElement.value;

  const message = new Paho.MQTT.Message(JSON.stringify({ unitId, goal }));
  message.destinationName = topicPrefix + 'set-goal';
  client.send(message);
});

// Add an opdracht to the queue
addOpdrachtBtnElement.addEventListener('click', function () {
  const opdracht = opdrachtInputElement.value;

  const message = new Paho.MQTT.Message(JSON.stringify({ opdracht }));
  message.destinationName = topicPrefix + 'add-opdracht';
  client.send(message);
});

// Remove an opdracht from the queue
removeOpdrachtBtnElement.addEventListener('click', function () {
  const opdracht = opdrachtInputElement.value;

  const message = new Paho.MQTT.Message(JSON.stringify({ opdracht }));
  message.destinationName = topicPrefix + 'remove-opdracht';
  client.send(message);
});

// Send a noodstop command
noodstopBtnElement.addEventListener('click', function () {
  const message = new Paho.MQTT.Message('');
  message.destinationName = topicPrefix + 'noodstop';
  client.send(message);
});
