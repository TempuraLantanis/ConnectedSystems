"""box_supervisor controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor


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


led_pos_y = robot.getDevice("led_pos_y")
led_neg_y = robot.getDevice("led_neg_y")
led_pos_x = robot.getDevice("led_pos_x")
led_neg_x = robot.getDevice("led_neg_x")
leds = [led_pos_y, led_neg_y, led_pos_x, led_neg_x]

ds_n = robot.getDevice("sensor_north")
ds_e = robot.getDevice("sensor_east")
ds_s = robot.getDevice("sensor_south")
ds_w = robot.getDevice("sensor_west")
dist_sensors = [ds_n, ds_e, ds_s, ds_w]
for ds in dist_sensors:
    ds.enable(1)


# execute every second
while robot.step(duration) != -1:
    distance_north = ds_n.getValue()
    distance_east = ds_e.getValue()
    distance_south = ds_s.getValue()
    distance_west = ds_w.getValue()
    # print(f'{sv_name} - NORTH: {distance_north}')
    # print(f'{sv_name} - EAST: {distance_east}')
    # print(f'{sv_name} - SOUTH: {distance_south}')
    # print(f'{sv_name} - WEST: {distance_west}')

    for led in leds:
        led.set(0)  # Turn of all leds
    cur_pos = supervisorNode.getPosition()

    new_posX, new_posY = cur_pos[0], cur_pos[1]  # new = current
    posX = round(10 * cur_pos[0])  # 0.1 -> 1
    posY = round(10 * cur_pos[1])

    targetX = round(sv_target_field[0])  # 0.1 -> 1
    targetY = round(sv_target_field[1])

    if targetX > posX:
        new_posX = round((posX) / 10, 1) + 0.1
        led_pos_x.set(1)
    elif targetX < posX:
        new_posX = round((posX) / 10, 1) - 0.1
        led_neg_x.set(1)
    elif targetY > posY:
        new_posY = round((posY) / 10, 1) + 0.1
        led_pos_y.set(1)
    elif targetY < posY:
        new_posY = round((posY) / 10, 1) - 0.1
        led_neg_y.set(1)

    if targetX != posX or targetY != posY:
        sv_translation_field.setSFVec3f([new_posX, new_posY, 0.05])
