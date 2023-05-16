"""box_supervisor controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Supervisor


# create the Robot instance
robot = Supervisor()
supervisorNode = robot.getSelf()

sv_translation_field = supervisorNode.getField("translation")
sv_target_field = supervisorNode.getField("target").value

# get the time step of the current world
timestep = int(robot.getBasicTimeStep())

# calculate a multiple of timestep close to one second
duration = (1000 // timestep) * timestep


# execute every second
while robot.step(duration) != -1:
    cur_pos = supervisorNode.getPosition()

    posX = round(10 * cur_pos[0])  # times 10 because grid size is 0.1 x 0.1 m
    posY = round(10 * cur_pos[1])
    new_posX, new_posY = posX, posY

    targetX = round(sv_target_field[0])
    targetY = round(sv_target_field[1])

    if targetX != posX:
        new_posX = round(
            (posX + 1) / 10, 1) if posX < targetX else round((posX - 1) / 10, 1)
    if targetY != round(posY / 10, 1):
        new_posY = round(
            (posY + 1) / 10, 1) if posY < targetY else round((posY - 1) / 10, 1)

    if targetX != posX or targetY != posY:
        sv_translation_field.setSFVec3f([new_posX, new_posY, 0.05])
