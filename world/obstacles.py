import random
obsticles_list = []
number = 0

def random_number():
    """
    return random number of obstacles to be created
    """
    number = random.randint(1, 10)
    return number

def get_obstacles():
    """
    create obstacles of given number 
    """
    global number
    global obsticles_list
    number = random_number()
    list_ = []
    obsticles = [[x, random.randint(-200, 200)] for x in [random.randint(-100, 100) for i in range(number)]]
    obsticles2 = [x  for x in obsticles if (x[0] != 0 and x[1] != 0)]
    return obsticles2

def is_position_blocked(x,y):
    """
    return true is the there is an obstacle on the distination of the move
    """
    global obsticles_list
    for i in obsticles_list:
        if (x in range(i[0], (i[0] + 5)) ) and (y in range(i[1], (i[1] + 5))):
            return True
    return False

def is_path_blocked(x1,y1, x2, y2):
    """
    returns true if the is an obstacle on the path
    """
    global obsticles_list
    for obs in obsticles_list:
        if x1 == x2:
            if x1 in range(obs[0], (obs[0] + 5)):
                if (obs[1] in range(min(y2, y1), max((y2, y1)))):
                    return True
                else:
                    pass
        else:
            if y1 in range(obs[1], (obs[1] + 5)):
                if (obs[0] in range(min(x2, x1), max((x2, x1)))):
                    return True
                else:
                    pass
        
    return False

if __name__== "__main__":
    pass
