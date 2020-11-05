import turtle

#Set up enviroment
s=turtle.getscreen()
s.setup(240, 560)
turtle.hideturtle()
robot = turtle.Turtle()
robot.penup()
robot.pensize(3)
robot.pencolor("#FF0000")
robot.forward(100)
robot.right(90)
robot.pendown()
robot.forward(200)
robot.right(90)
robot.forward(200)
robot.right(90)
robot.forward(400)
robot.right(90)
robot.forward(200)
robot.right(90)
robot.forward(200)
robot.right(90)
robot.penup()
position =[0,0]
direction = ["y", 1]

def print_position(name):
    pass

def track_position(direction, steps, position, command):
    """
    Track position of the robot
    """
    if command == "back":
        robot.back(steps)
        steps = int(steps) * -1
    else:
        robot.forward(steps)
    if direction[0] == "y":
        position[1] = int(position[1]) + ((int(direction[1]) * int(steps)))
    else:
        position[0] = (int(position[0]) + ((int(direction[1]) * int(steps))))
    return(position)


def get_direction(direction, change):
    """
    Get the new direction if instructed to turn
    """

    #Graphic display
    if (change == "left"):
        robot.left(90)
    else:
        robot.right(90)

    #position tracking for Code
    if ((direction[0] == "y")&(change == "left"))|((direction[0] == "x")&(change == "right")):
        if direction[1] > 0:
            direction[1] =  -1
        else:
            direction[1] =  1
    else:
        if direction[1] > 0:
            direction[1] = direction[1] * 1 
        else:
            direction[1] = -1
    if direction[0] == "y":
        direction[0] = "x"
    else:
        direction[0] = "y"
    return direction


def add_absticles(obstacle_list):
    """
    Display obsticles on Turltle Window from a list give.
    """
    robot.right(90)
    for i in obstacle_list:
        robot.penup()
        robot.setx(i[0])
        robot.sety(i[1])
        robot.color("blue")
        robot.pensize(2)
        robot.pendown()
        robot.forward(4)
        robot.right(90)
        robot.forward(4)
        robot.right(90)
        robot.forward(4)
        robot.right(90)
        robot.forward(4)
        robot.right(90)

    robot.penup()
    robot.setx(0)
    robot.sety(0)
    robot.pendown()
    robot.pensize(2)
    robot.pencolor("#000080")

