import bezier
from enemyClass import enemy
import math
import numpy as np
import random
from time import time
from constants import GRID_SIZE

#Function to take a comma seperated value (csv) file and return a 2D list from it's contents
def load_enemy_info(filename, level):
    ENEMIES = []
    # Opens the File
    file = open(filename, "r")
    contents = file.read()
    lines = contents.split('\n')

    for line in lines[1:-1]:
        if(line[0] != str(level)):
            continue
        row = line.split(',')

        # Use the string to get the function pointer
        enter = getattr(bezier, row[8])
        exit = getattr(bezier, row[9])
        swoop = getattr(bezier, row[10])
        #                    type,        size,        speed,        start_x,     start_y,     final_x,     final_y,     entrance, exit, swoop
        ENEMIES.append(enemy(int(row[1]), int(row[2]) * GRID_SIZE, float(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), enter,    exit, swoop))
    return ENEMIES

# Given a point and an angle, rotate that point by that many degrees
# Input 1: x - vector component
# Input 2: y - vector component
# Input 3: angle - in degrees how far you want to rotate the provided components
def rotation_matrix(x, y, angle):
    # Turn into radians for the math functions
    angle = angle * math.pi / 180

    # Here's my rotation matrix
    mat = np.array([[math.cos(angle), -math.sin(angle)],
                    [math.sin(angle),  math.cos(angle)]]
    )
    
    # My original vector
    vec = np.array([x, y])

    # Matrix multiplication made easy with numpy.  Thanks Python!
    return mat@vec

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)