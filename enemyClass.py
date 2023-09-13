from time import time
from bezier import *

# States
# 1: Enter
# 2: Move left
# 3: Move right
# 4: Exit
# 5: Swoop at player

# How many seconds should it take the enemy to get from start point to finish point?
ENEMY_DEFAULT_SPEED = 4

class enemy:
    pincer = False

    def __init__(self, type, size, speed, start_x, start_y, final_x, final_y, entrance, exit, swoop):
        self.size = size
        self.type = type
        self.enter_function = entrance # When enemies enter the screen
        self.exit_function = exit # When enemies exit the screen
        self.swoop_function = swoop # When enemies swoop at you

        # This only works if I also tell this file how big the screen is, but that's getting messy.
        # I'll leave it up to the programmer for now to specify starting coordinates
        # I also don't want the user to have to give the screensize to the class here, because that's annoying

        # if(entrance == enterCurve1):
        #     self.start_x = 0
        #     self.start_y = 0
        # elif(entrance == enterCurve2):
        #     self.start_x = 

        if(self.type == 3):
            self.beam_index = 0

        self.destroy_index = 0

        self.state = 1
        self.x = 0
        self.y = 0
        self.heading = 0 # In degrees clockwise from straight up
        self.start_x = start_x
        self.start_y = start_y
        self.final_x = final_x
        self.final_y = final_y
        self.speed = speed
        self.last_update = time()


        # Copies for swapping values later
        self.s_x = start_x
        self.s_y = start_y
        self.f_x = final_x
        self.f_y = final_y

    # Not sure I'll ever actually use this.  I did once in a much earlier version of the game
    def swap_coordinates(self):
        self.start_x, self.start_y, self.final_x, self.final_y = self.final_x, self.final_y, self.start_x, self.start_y
    
    def set_exit_coordinates(self, target_x, target_y):
        # Start where the enemy ended last
        self.start_x, self.start_y = self.final_x, self.final_y
        # Finish where the user specifies
        self.final_x, self.final_y = target_x, target_y

    def set_start_coordinates(self, t_x, t_y):
        self.start_x, self_start_y = t_x, t_y

    # This is necessary because when an enemy exits the screen, their start point needs to be where the previous final point was
    # Therefore, I need this copy to overwrite the start variable with what it was originally
    def set_enter_coordinates(self):
        self.final_x, self.final_y = self.start_x, self.start_y
        self.start_x, self.start_y = self.s_x, self.s_y


    def set_end_position(self):
        self.x = self.final_x
        self.y = self.final_y
        self.heading = 0

    # This is necessary because my new functionality to stop mid-way to the bottom of the screen goofs up my previously-working
    # coordinate functionality.  Now I need to get those coordinates back on track
    def reset_coordinates(self):
        self.start_x, self.start_y, self.final_x, self.final_y = self.s_x, self.s_y, self.f_x, self.f_y


    # Not sure I'll actually use this, because sometimes when I switch states I don't want to update my last_update
    # Besides, it'd only save me about 10 lines of code
    def update_state(self, s):
        state = s
        last_update = time()

    
    # This is because my end game state is goofy with enemies that are in their entrance state
    # so this makes super sure everything will work right
    def set_coordinates(self, x, y):
        self.start_x = self.x
        self.start_y = self.y
        self.final_x = x
        self.final_y = y