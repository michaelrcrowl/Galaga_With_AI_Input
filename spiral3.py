import pythonGraph as pg
from time import time, sleep
import random
import math
from bezier import *
from enemyClass import enemy
import helper_functions as hf
from constants import *
from multiprocessing import Process, Pipe, Array

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2
import numpy as np
from PIL import Image, ImageOps  # Install pillow instead of PIL

my_model = load_model('ml_model/keras_model.h5', compile=False)
class_names = open("ml_model/labels.txt", "r").readlines()

# from cs110 import autograder

'''
Concepts demonstrated:
    Calculus for the heading (provided to students by default)
    Equation for a circle (during end_game())
    Trig for laser angles (in draw_laser() and some other spots)
    Rotation matrices (for the starfield during the opening)
    Sine wave
    Parametric equation for a circle with a dot product to calculate an orthogonal vector
'''

'''
Extra features:
    Multiple lives
    Multiple "levels"
    Score
    upgrades shop based on store (prss 's' while playing the game)
        Click-able buttons
    Different enemy types
    More curves for enemies to follow
    Moving stars in the "background"
    End game animation
    Player ship capture
    Extra states for the AI
    Explosion animations
    Start menu
    Can restart the game after losing
    Enemies sometimes shoot missiles at the player.

    Maybe some others I'm forgetting
'''

COMMANDS = [0,0,0]

# This will hold the list of all our enemies eventually
enemies = []

# Based on time, we'll move enemies from enemies into drawn_enemies
# to make a staggered entrance
drawn_enemies = []

ship_x = SCREEN_SIZE / 2 - (.5 * SHIP_SIZE)

# [x, y, speed, size, id]
missiles = []
missile_speed = 20

# Typical gameplay things
level = 1
lives = 3
high_score = 1000
score = 1000000

# Just an initialization. It'll change in the animation loop
enemy_last_spawn = time()

ship_collected = False

# Stars. For use in populate_starfield() and update_starfield()
# [x, y, size, color, speed]
starfield = []

# Draws the enemies
def draw_enemy(enemies: list[enemy]):
    for i in enemies:
        if(i.state != 12):
            pg.draw_image("images/enemy" + str(i.type) + ".png", i.x, i.y, i.size, i.size, i.heading)


# Draws the ship
def draw_ship(x: int, y: int, h: int = 0):
    pg.draw_image("images/ship.png", x, y, SHIP_SIZE, SHIP_SIZE, h)
    

def draw_explosion(index: int, ship_x: int):
    pg.draw_image("images/shipExplosion" + str(index) + ".png", ship_x, SHIP_Y, SHIP_SIZE, SHIP_SIZE)

# The fininte state machine for my enemies
def ai(enemies: list[enemy], ship_collected: bool, lives: int, ship_x: int, score: int) -> (int, bool, int):
    # For every enemy
    for i in enemies:
        # This t needs to be a ratio from 0 to 1 for the parametric curve to work
        # The speed variable set when creating the enemy determines how long it takes to get to 1
        t = (time() - i.last_update) / i.speed

        # Enter state when they fly onto the screen
        if(i.state == 1):
            if(t < 1):
                # use the function pointer to call the desired curve for this enemy
                i.x, i.y, i.heading = i.enter_function(t, i.start_x, i.start_y, i.final_x, i.final_y)
            # If the full time has elapsed, then set it's final heading and position to what it should be (since I can't make t equal exactly 1)
            elif(1 <= t < 1.2):
                i.set_end_position()
            else:
                # Transition to the next state
                i.state = 2

        # As long as the enemy is moving back and forth, there's a chance it'll enter the swoop state
        # Even with a 1/2000th chance, this still happens way more often time-wise than I'd like, but it's OK for now
        elif((i.state == 2 or i.state == 3) and random.randint(0, 3500) == 0):
            i.state = 5
            i.last_update = time()

        # Small chance it'll enter the exit state
        elif((i.state == 2 or i.state == 3) and random.randint(0, 2000) == 0):
            i.set_exit_coordinates(random.randint(0, SCREEN_SIZE), SCREEN_SIZE)
            i.state = 4
            i.last_update = time()

        # Small chance enemy type 1 will pincer the player's ship
        # elif(((i.state == 2 or i.state == 3) and i.type == 1 and random.randint(0,1500) == 0 and not ship_collected) or enemy.pincer):
        #     i.set_exit_coordinates(i.x, SCREEN_HEIGHT)

        #     # This will make the next enemy type 1 in the enemy list also perform this action
        #     enemy.pincer = not enemy.pincer

        #     i.state = 18
        #     missiles.append([i.x, i.y, -missile_speed, MISSILE_SIZE, 1])
        #     i.speed = 2
        #     i.last_update = time()

        # Enter a circle pattern for 20 seconds (5 times 4 cycles)
        # TODO: Make the entrance and exit from this smoother.  I'll need at least one more state for it, I think
        # I have this state transition commented out for now, because at some point it just becomes too much.  Perhaps it's only enabled for later levels or a harder difficulty?
        # elif((i.state == 2 or i.state == 3) and random.randint(0, 5000) == 0):
        #     i.state = 19
        #     i.set_exit_coordinates(random.randint(i.size + RADIUS, SCREEN_SIZE - i.size), SHIP_Y - 2 * RADIUS)
        #     i.last_update = time()
        #     i.speed = 5

        # While in this state, we'll update every second
        elif(i.state == 2 and time() > i.last_update + 1):
            i.x += 10
            i.state = 3 # Move left
            i.last_update = time()
        
        # While in this state, we'll update every second
        elif(i.state == 3 and time() > i.last_update + 1):
            i.x -= 10
            i.state = 2
            i.last_update = time()
                
        # Transition from moving left and right to flying off the screen
        elif(i.state == 4):
            if(t < 1):
                i.x, i.y, i.heading = i.exit_function(t, i.start_x, i.start_y, i.final_x, i.final_y)
            else:
                i.state = 1

                # Set the coordinates for the upcoming entrance
                i.reset_coordinates()

                # Reset the time to calculate the parametric curve for the entrance
                i.last_update = time()

        # Swoop at the player
        elif(i.state == 5):
            if(t < 1):
                i.x, i.y, i.heading = i.swoop_function(t, i.final_x, i.final_y, i.final_x, i.final_y)
            elif(1 <= t < 1.2):
                i.set_end_position()
            else:
                i.state = 3
                i.last_update = time()

        # Destroyed
        if(i.state == 12):
            if(i.destroy_index == 5):
                enemies.remove(i)
                score += i.type * 100
            else:
                pg.draw_image('images/enemyExplosion' + str(i.destroy_index) + '.png', i.x, i.y, i.size, i.size)
                i.destroy_index += 1

        # Pincer
        # elif(i.state == 18):
        #     if(t < 1):
        #         i.x, i.y, i.heading = exitSin(t, i.start_x, i.start_y, i.final_x, i.final_y)
        #     else:
        #         i.state = 1
        #         i.last_update = time()
        #         i.reset_coordinates()

    return lives, ship_collected, score


# Move missiles up and enemies do their things
def update():
    global missiles

    for m in missiles:
        m[1] -= m[2]
        if(m[1] < 0 or m[1] > SCREEN_HEIGHT):
            missiles.remove(m)
        

# Determines if the missile and an enemy are in the same spot
####### Haven't updated this since Space Invaders #######
def check_collision(score: int, missiles: list) -> (bool, bool, int, list):
    ship_destroyed = False
    collision_distance = 2 * GRID_WIDTH

    for i in drawn_enemies:
        for missile in missiles:
            # Basically, is the missile x between the left and right of the enemy
            # And is the missile y between the top and bottom of the enemy
            # And does the missile belong to the player
            if(i.x < missile[0] < i.x + i.size and i.y < missile[1] < i.y + i.size and missile[4] == 0):
                # Type 3 takes two hits
                # TODO: This isn't working
                if(i.type == 3):
                    i.type = 4
                else:
                    # Otherwise, destroy both
                    i.state = 12
                    missiles.remove(missile)
                    score += (100 * i.type) # This will give me 400 points for enemy type 3 (4), but that's OK, whatever

                # TODO: Make the captured player ship linear_parametric toward the player ship
                if(i.state == 10 or i.state == 11):
                    pass

            # If the missiles belongs to an enemy
            # Put the missile ID logic first since this is unlikely and will save CPU cycles.  #CompooterScyunce
            if(missile[4] == 1 and ship_x < missile[0] < ship_x + SHIP_SIZE and SHIP_Y < missile[1] < SHIP_Y + SHIP_SIZE):
                ship_destroyed = True

        # Added "not ship_collected", because it was annoying going through the capture animation 
        # and having other enemies destroying my non-existent ship (and costing me lives)
        if(not ship_collected and ship_x <= i.x <= ship_x + SHIP_SIZE and SHIP_Y <= i.y + (i.size) <= SHIP_Y + SHIP_SIZE and i.state != 12):
            i.state = 12
            ship_destroyed = True
    return ship_destroyed, len(drawn_enemies) == 0 and len(enemies) == 0, score, missiles


# Draws all the missiles you shoot
def draw_missile():
    for m in missiles:
        tlx =  m[0] - m[3] # top left x
        tly = m[1] - m[3] # top left y

        # If an enemy is shooting the missile down, flip it over
        if(m[2] < 0):
            h = 180
        else:
            h = 0

        pg.draw_image("images/missile.png", tlx, tly, GRID_SIZE, 2 * GRID_SIZE, h)
        

def gen_enemies(spawn: bool, last_spawn: float): 
    global drawn_enemies, enemies
    spacing = 60
    
    if(spawn and time() > last_spawn + 3):
        for i in range(5):
            drawn_enemies.append(enemies.pop(0))
            drawn_enemies[-1].last_update = time()
        
        if(len(enemies) == 0):
            spawn = False
        last_spawn = time()

    return spawn, last_spawn

# At some point I'll make this random.  If RANDOMIZE_ENEMIES = 1 at the top of this file
# Then this function will get called.  It'll be nuts if it's truly random.  
# TODO: Perhaps a hard difficulty?
def populate_enemy_list(enemies: list[enemy]):

    # Populate the list of enemies
    if(not RANDOMIZE_ENEMIES):
        enemies = hf.load_enemy_info("enemyFormationFile.csv", level)
    else:
        # Each entry should be of type `enemy` from enemyClass.py
        curves = [line_parametric, enterCurve1, enterCurve2, exitCurve1, exitCurve2, exitCurve3, genericCurve1, loopCurve1, swoopCurve1, swoopCurve2]

        enemies = []
        spacing = 60

        # Expected order of inputs for the enemy class:
        # type, size, start_x, start_y, final_x, final_y, entrance function, exit function, swoop function
        for i in range(5):
            enemies.append(enemy(1, ENEMY_DEFAULT_SIZE, random.randint(0,SCREEN_SIZE), 0, SCREEN_SIZE / 2 + spacing, SCREEN_SIZE / 2, random.choice(curves),line_parametric, swoopCurve1))
            spacing += 60
    return enemies

def get_image(array, conn):

    cv2.namedWindow("Input")
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while(True):
        size = (224, 224)        
        ret, frame = cap.read()

        # Shape this array as necessary to work with the model.  This skips the time-intensive step of saving and reloading an image
        frame_resized = cv2.resize(frame, size)
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_rgb_batch = np.expand_dims(frame_rgb, axis=0)

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Normalize the image
        normalized_image_array = (frame_rgb_batch.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = my_model.predict(data, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        # print("Class:", class_name[2:], end="")
        # print("Confidence Score:", confidence_score)

        # dir = predictions.index(max(predictions))
        if(index == 0):
            array = [1,0,0]
            # print("LEFT")
        elif(index == 1):
            array = [0,1,0]
            # print("RIGHT")
        elif(index == 2):
            array = [0,0,1]
            # print("SHOOT")
        else:
            array = [0,0,0]
            # print("NOTHING")
        conn.send(array)

# Listens for user input from the keyboard
def keyboard(conn):
    global ship_x, missiles, enemy_last_spawn
    # start = time()
    array = conn.recv()

    if (array[0] and ship_x > 0):
        ship_x -= GRID_SIZE

        # Make sure I don't go off the screen a bit, which was happening before this code
        if(ship_x < 0):
            ship_x = 0
    elif(array[1] and ship_x + SHIP_SIZE < SCREEN_SIZE):
            ship_x += GRID_SIZE
            if(ship_x + SHIP_SIZE > SCREEN_SIZE):
                ship_x = SCREEN_SIZE - SHIP_SIZE
    elif(array[2]):
        missiles.append([(ship_x + (SHIP_SIZE / 2)), (SHIP_Y + (SHIP_SIZE / 2) - .5), missile_speed, MISSILE_SIZE, 0])
    # print("Time spent in keyboard(): ", time() - start)
        

def game_over(lives: int, ship_collected: bool, ship_x: int, drawn_enemies: list[enemy], score: int) -> bool:
    while(not pg.key_pressed('r')):
        draw_starfield()
        draw_enemy(drawn_enemies)
        pg.draw_text("GAME OVER", SCREEN_SIZE / 2, SCREEN_HEIGHT / 2, "red", centered = True)
        pg.draw_text("Press 'r' to restart", SCREEN_SIZE / 2, SCREEN_HEIGHT / 2 + 50, "red", centered = True)
        pg.update_window()

    return True
    

def reset_variables():
    global score, lives, high_score, enemies, missiles, drawn_enemies, level, ship_collected, upgrades

    if(score > high_score):
        high_score = score
    score = 0
    lives = 3
    enemies = []
    missiles = []
    drawn_enemies = []
    ship_collected = False
    level = 1


# Randomly generate the background stars
def populate_starfield():
    global starfield

    for x in range(NUM_STARS):
        starfield.append([random.randint(50, SCREEN_SIZE - 50), random.randint(0, SCREEN_SIZE), random.choices(["white", "yellow", "red", "blue"])[0], random.choice([STAR_SLOW, STAR_FAST])])


# Move the stars down the screen to give the impression of FLYING...THROUGH...SPACE space space space....
def update_starfield():
    global starfield

    for star in starfield:
        pg.draw_rectangle(star[0], star[1], star[0] + STAR_SIZE, star[1] + STAR_SIZE, star[2], True)
        star[1] += star[3]

        # Star goes supernova off the screen, and another takes its place at the top of the screen.   These are violent times, hence the aliens.
        if(star[1] > SCREEN_HEIGHT):
            starfield.remove(star)
            starfield.append([random.randint(50, SCREEN_SIZE - 50), -1, random.choices(["white", "yellow", "red", "blue"])[0], random.choice([STAR_SLOW, STAR_FAST])])


# Draw but don't move the stars.  Used for the end game
def draw_starfield():
    for star in starfield:
        pg.draw_rectangle(star[0], star[1], star[0] + STAR_SIZE, star[1] + STAR_SIZE, star[2], True)


def game(conn):
    global enemy_last_spawn, reset, spawn, lives, enemies, ship_x, score, drawn_enemies, starfield, ship_collected, missiles, missile_speed
    # Open window and start the animcation loop
    pg.open_window(SCREEN_WIDTH, SCREEN_SIZE)

    populate_starfield()

    while (pg.window_not_closed()):
        enemy_last_spawn = time()
        reset = False
        spacing = 60
        spawn = True
        last_spawn = time()
        ship_destroyed = False
        enemies_remaining = True
        destroyed_image_index = 0
        destroy_counter = 0
        enemy_spawn = 0
        capture_time = time() # placeholder
        sharktime = 0 # Placeholder

        # Player can press 'r' to reset the game
        while(not reset and lives > -1):

            # If all enemies are destroyed, then that means we advanced to the next level
            if(len(enemies) == 0 and len(drawn_enemies) == 0):
                spawn = True
                enemies = populate_enemy_list(enemies)

            # If the ship is destroyed, I want the enemies to keep doing their thing
            # but the ship needs to go through it's blowy-upy animation
            if(ship_destroyed):
                pg.clear_window("black")
                draw_enemy(drawn_enemies)
                update()
                lives, ship_collected, score = ai(drawn_enemies, ship_collected, lives, ship_x, score)
                draw_explosion(destroyed_image_index, ship_x)
                update_starfield()

                # Cycle through the explosion images after a certain number of game loops
                if(destroy_counter < 30):
                    if(destroy_counter % 10 == 0):
                        destroyed_image_index += 1
                    destroy_counter += 1
                # Reset all the variables so that the player can keep playing
                else:
                    ship_destroyed = False
                    # Commented this out so that the game will just keep running during the demo
                    # lives -= 1
                    destroyed_image_index = 0
                    destroy_counter = 0

            # Ship isn't destroyed, play like normal
            else:
                # Generate enemies, if applicable
                # This function will need to change at some point to make more variations
                spawn, last_spawn = gen_enemies(spawn, last_spawn)
                pg.clear_window("black")

                # This is makes drawing the ship in its normal spot and keyboard input mutually exclusive to the animation that takes place in ai()
                if(not ship_collected):
                    draw_ship(ship_x, SHIP_Y)
                    reset = keyboard(conn)
                update()

                # This function checks all enemies to see if they hit a missile or the player
                ship_destroyed, enemies_remaining, score, missiles = check_collision(score, missiles)

                if(enemies_remaining):
                    level += 1 
                    # break

                # Draw the things
                draw_missile()
                draw_enemy(drawn_enemies)
                update_starfield()
                lives, ship_collected, score = ai(drawn_enemies, ship_collected, lives, ship_x, score)
            pg.update_window()

        game_over(lives, ship_collected, ship_x, drawn_enemies, score)
        reset_variables()
        # Now we restart level 1

if __name__ == '__main__':    
    arr = Array('i', COMMANDS)
    conn1, conn2 = Pipe()

    aiProc = Process(target=get_image, args=(arr, conn2,))
    gameProc = Process(target=game, args=(conn1,))
    
    aiProc.start()
    gameProc.start()

    gameProc.join()
    aiProc.join()