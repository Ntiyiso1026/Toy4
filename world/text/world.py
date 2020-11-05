position =[0,0]
direction = ["y", 1]

def print_position(name):
    """
    Display position of the robot in text on the console
    """
    print(f" > {name} now at position ({position[0]},{position[1]}).")


def track_position(direction, steps, position, command):
    """
    Track position of the robot
    """
    if command == "back":
        steps = int(steps) * -1
    if direction[0] == "y":
        position[1] = int(position[1]) + ((int(direction[1]) * int(steps)))
    else:
        position[0] = (int(position[0]) + ((int(direction[1]) * int(steps))))
    #print(f" > {name} now at position ({position[0]},{position[1]}).")
    return(position)


def get_direction(direction, change):
    """
    Get the new direction if instructed to turn
    """
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
