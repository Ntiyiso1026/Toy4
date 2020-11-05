import sys
from world import obstacles
mode = ""

def get_game_commands():
    """
    Get valid commands from file for the program to use
    """ 
    valid_commands = ['OFF', 'HELP', 'REPLAY', 'FORWARD', 'BACK', 'RIGHT', 'LEFT', 'SPRINT', 'SILENT', 'REVERSED']
    return valid_commands, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays all movement commands from history [FORWARD, BACK, RIGHT, LEFT, SPRINT]
"""


def get_robot_name():
    """
    Get a name the user wants to give to the robot
    """

    name = input("What do you want to name your robot? ")
    print(f"{name}: Hello kiddo!")
    return(name)


def validate_command(in_command, command_list):
    """
    Vaidate command, Returns true if command is vallid
    """
    valid = False
    for command in in_command:
        valid = False
        if (command.upper() in command_list):
                    valid = True
        else:
            try:
                name = int(command)
                valid = True
            except:
                pass
            command = command.split('-')
            try:
                name = int(command[0]) + int(command[1])
                valid = True
            except:
                pass
        if valid == False:
            return False
    return True


def create_list_of_commands(name, command_list):
    """
    Take command as string, validate it, returns it as a list if valid or ask for
    valid command if not valid
    """

    while True:
        valid = False
        command_in = input(f"{name}: What must I do next? ")
        in_command = command_in
        if len(command_in) > 0:
            command_in = command_in.split()
            valid = validate_command(command_in, command_list)
        if valid:
            command_in = [command.lower() for command in command_in]
            try:
                command_in[-1] = int(command_in[-1])
            except:
                command_in.append(0)
            break
        if valid == False:
            print(f"{name}: Sorry, I did not understand '{in_command}'.")
    return command_in


def do_move(name, command, steps, position):
    """ 
    Display the valid move the robot carried out
    """
    if command == "back":
        print(f" > {name} moved {command} by {steps} steps.")
        world.print_position(name)
    else:
        print(f" > {name} moved {command} by {steps} steps.")
        world.print_position(name)


def turn_left(name, position):
    """
    Display left or right turn th robot made
    """
    print(f" > {name} turned left.")
    world.print_position(name)


def turn_right(name, position):
    print(f" > {name} turned right.")
    world.print_position(name)


def valid_move(name, direction, steps, check, command, position):
    """
    Check if requested move is within the boundry and there is no obstacle on the way
    return False if there is no obstacle.
    """

    move = False 
    if command == "back":
        steps = int(steps) * -1
    if direction[0] == "y":
        check[1] = int(check[1]) + (int(direction[1]) * int(steps))
        if (check[1] <= 200)&(check[1]>= -200):
            if obstacles.is_position_blocked(check[0], check[1]):
                return False
            else:
                if obstacles.is_path_blocked(position[0], position[1],check[0], check[1]):
                    print("Sorry, there is an obstacle in the way.")
                    return False
                return True
        else:
            print(f"HAL: Sorry, I cannot go outside my safe zone.")
            print(f" > {name} now at position ({position[0]},{position[1]}).")
    else:
        check[0] = (int(check[0]) + (int(direction[1]) * int(steps)))
        if (check[0] <= 100)&(check[0]>= -100):
            if obstacles.is_position_blocked(check[0], check[1]):
                print("Sorry, there is an obstacle in the way.")
                return False
            else:
                if obstacles.is_path_blocked(position[0], position[1],check[0], check[1]):
                    print("Sorry, there is an obstacle in the way.")
                    return False
                return True
        else:
            print(f"HAL: Sorry, I cannot go outside my safe zone.")
            print(f" > {name} now at position ({position[0]},{position[1]}).")


def sprint(name, command, steps, position,direction, display):
    """
    Sprint allows to the robot carry out all valid forward moves given
    number of steps, reccursively.
    display moves when sprint command is executed
    """
    check = []
    for L in position:
        check.append(L)
    move = valid_move(name, direction, steps, check, command, position)
    if steps > 0:
        if move:
            position = world.track_position(direction, steps, position, command)
            if display:
                print(f" > {name} moved forward by {steps} steps.")
        sprint(name, command, (steps -1), position, direction, display)
    return position


def run_command_list(name, infor ,History, display):
    """
    execute commands from the list of commands given
    """
    position = world.position
    direction = world.direction
    game = True
    run_list = []
    run_list.append(History[-1])
    for i in run_list:
        if i[0] == "off":
                game = False
                print(f"{name}: Shutting down..")
        elif i[0] == "help":
            print(infor)
        elif i[0] == "left":
            world.direction = world.get_direction(direction, i[0])
            if display:
                turn_left(name, tuple(position))
        elif i[0] == "right":
            direction = world.get_direction(direction, i[0])
            if display:
                turn_right(name, tuple(position))
        elif i[0] == "forward" or i[0] == "back":
            check = []
            for L in position:
                check.append(L)
            move = valid_move(name,direction, i[-1], check, i[0], position)
            if move == True:
                position = world.track_position(direction, i[-1], position, i[0])
                if display:
                    do_move(name, i[0], i[-1], position)
        elif i[0] == "sprint":
            position = sprint(name, i[0],i[-1], position,direction, display)
            world.print_position(name)
    return game


def get_range(list_of_commands):
    """
    Chech from the list of commands if there is a given option for range
    if true returns True and the selected range as list on integers.
    """
    int_range= [0,0]
    status = False
    try:
        list_of_commands[-3] = int(list_of_commands[-3])
        return [True, [-list_of_commands[-3], -1]]
    except:
        pass
    if list_of_commands[-1] > 0:
        return [True, [-list_of_commands[-1], -1]]
    elif list_of_commands[-1] == 0:
        try:
            split = list_of_commands[-2].split('-')
            int_range[0] = int(split[0]) *-1
            int_range[1] = (int(split[1]) * -1) - 1
            status = True
        except :
            pass
        try:
            split = list_of_commands[-3].split('-')
            int_range[0] = int(split[0]) *-1
            int_range[1] = (int(split[1]) * -1) - 1
            status = True 
        except:
            pass
        return [status , int_range]


def replay(name, infor , history, display,list_of_commands):
    """
    replay commands of a selected range from command history, 
    replay all if no range is given
    """

    direction = world.direction
    position =  world.position
    display = True
    reverse_text = ""
    replay_range = get_range(list_of_commands)
    if  "silent" in list_of_commands:
        display = False 
    if  "reversed" in list_of_commands:
        reverse_text = " in reverse"
        history.reverse()
    if replay_range[0] == True:
        lens = 0
        rev = -1
        start = replay_range[1][0]
        end = replay_range[1][1]
        lens = str(((start*-1) - (end*-1)) + 1)
        rev = 1
        while start != end:
            
            game = run_command_list(name, infor , [history[start]],  display)
            start += (1 * rev) 
        game = run_command_list(name, infor , [history[start]], display)
        if display == False:
            print(f" > {name} replayed {lens} commands{reverse_text} silently.")
        else:
            print(f" > {name} replayed {lens} commands{reverse_text}.")
    else:
        for com in history:
            i = [com]
            game = run_command_list(name, infor , i, display)
        if display == False:
            print(f" > {name} replayed {len(history)} commands{reverse_text} silently.")
        else:
            print(f" > {name} replayed {len(history)} commands{reverse_text}.")
    display = True
    world.print_position(name)
    return position, direction


def robot_start():
    #get obsticles and names
    obstacles.obsticles_list = obstacles.get_obstacles()
    if mode.lower() == "turtle":
        world.add_absticles(obstacles.obsticles_list)

    name = get_robot_name()
    command_list , infor = get_game_commands()
    
    #Print obsticle list if game played in text Mode
    if mode != "turtle" and len(obstacles.obsticles_list) > 1:
        print("There are some obstacles:")
        for i in obstacles.obsticles_list :
            print(f"- At position {i[0]},{i[1]} (to {i[0] + 4},{i[1] + 4})")
    elif (len(obstacles.obsticles_list) == 1):
        if ((obstacles.obsticles_list[0][0] != 0)and (obstacles.obsticles_list[0][1] != 0)):
            print("There are some obstacles:")
            for i in obstacles.obsticles_list :
                print(f"- At position {i[0]},{i[1]} (to {i[0] + 4},{i[1] + 4})")

    #initiate game variables
    game = True
    history = []
    display = True
    world.position =[0,0]
    world.direction = ["y", 1]

    while game:
        list_of_commands = create_list_of_commands(name, command_list)
        if list_of_commands[0] == "replay":
            world.position , world.direction = replay(name, infor , history, display, list_of_commands)
        elif list_of_commands[0] == "help":
            game = run_command_list(name, infor , [list_of_commands], display)
        else:
            history.append(list_of_commands)
            game = run_command_list(name, infor , history, display)

if __name__ == "__main__":
    mode = ""
    try:
        mode = sys.argv[1]
    except :
        pass
    if mode.lower() == "turtle":
        from world.turtle import world
    else:
        from world.text import world
        
    robot_start()
else:
    try:
        mode = sys.argv[1]
    except :
        pass
    if mode.lower() == "turtle":
        from world.turtle import world
    else:
        from world.text import world