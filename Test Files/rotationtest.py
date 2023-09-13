import pythonGraph as pg
import random
import math
import numpy as np
from time import time

SCREEN_SIZE = 990
STARFIELD = []
NUM_STARS = 50 # totally arbitary
STAR_SIZE = 2 # pixels
STAR_SLOW = 10 # pixels per update
STAR_FAST = 20 # pixels per update

SHIP_X = 500
SHIP_Y = 500
SHIP_SIZE = 50

# Randomly generate the background stars
def populate_starfield():
    global STARFIELD

    for x in range(NUM_STARS):
        STARFIELD.append([random.randint(50, SCREEN_SIZE - 50), random.randint(0, SCREEN_SIZE), random.choices(["white", "yellow", "red", "blue"])[0], random.choice([STAR_SLOW, STAR_FAST])])

# TODO: Make the stars rotate around my ship
def rotate_starfield(degrees):
    global STARFIELD

    ox = SHIP_X
    oy = SHIP_Y

    for star in STARFIELD:
        # Pretend the star is at these coordinates.  Result is my x and y coord of the vector
        x = star[0] - ox
        y = star[1] - oy

        # # Calculate and transform into degrees
        # try:
        #     angle = math.atan(x / y) * 180 / math.pi
        # except:
        #     angle = 0

        # # Rotate by specified number of degrees
        # angle += degrees

        # Turn back into radians for the math functions
        angle = degrees * math.pi / 180

        # Here's my rotation matrix
        mat = np.array([[math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)]]
        )
        
        # My original vector
        vec = np.array([x, y])

        res = mat@vec

        star[0] = ox + res[0]
        star[1] = oy + res[1]


def test(degrees):
    global STARFIELD

    ox = SHIP_X
    oy = SHIP_Y

    # Pretend the star is at these coordinates.  Result is my x and y coord of the vector
    x = 600 - ox
    y = 600 - oy

    # # Calculate and transform into degrees
    # try:
    #     angle = math.atan(x / y) * 180 / math.pi
    # except:
    #     angle = 0

    # # Rotate by specified number of degrees
    # angle += degrees

    # Turn back into radians for the math functions
    angle = degrees * math.pi / 180

    # Here's my rotation matrix
    mat = np.array([[math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]]
    )
    
    # My original vector
    vec = np.array([[x], [y]])

    res = mat@vec

    print(ox + res[0], oy + res[1])

# Move the stars down the screen to give the impression of FLYING...THROUGH...SPACE space space space....
def update_starfield():
    global STARFIELD

    for star in STARFIELD:
        pg.draw_rectangle(star[0], star[1], star[0] + STAR_SIZE, star[1] + STAR_SIZE, star[2], True)
        star[1] += star[3]

        # Star goes supernova off the screen, and another takes its place at the top of the screen.   These are violent times, hence the aliens.
        if(star[1] > SCREEN_SIZE):
            STARFIELD.remove(star)
            STARFIELD.append([random.randint(50, SCREEN_SIZE - 50), -1, random.choices(["white", "yellow", "red", "blue"])[0], random.choice([STAR_SLOW, STAR_FAST])])

# Move the stars down the screen to give the impression of FLYING...THROUGH...SPACE space space space....
def draw_starfield():
    global STARFIELD

    for star in STARFIELD:
        pg.draw_rectangle(star[0], star[1], star[0] + STAR_SIZE, star[1] + STAR_SIZE, star[2], True)


# This is just a test
test(45)

# For the rotation of the whole starfield
pg.open_window(SCREEN_SIZE, SCREEN_SIZE)
populate_starfield()
pg.clear_window("black")

while(not pg.mouse_button_down("left")):
    draw_starfield()
    pg.update_window()

d = 45
t = 0
lu = time()
while(t < d):
    if(time() > lu + .1):
        lu = time()
        rotate_starfield(1)
        t += 1
    draw_starfield()
    pg.update_window()    
pg.wait_for_close()