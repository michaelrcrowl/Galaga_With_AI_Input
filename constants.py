# Sometimes I want to just right into testing and not wait for the beginning animation
DO_INTRO = 0

# Change this to 1 to create random enemies (NOT IMPLEMENTED RIGHT NOW)
# Change this to 0 if you want to load the enemy schema from a file
RANDOMIZE_ENEMIES = 0

# Screen variables
SCREEN_HEIGHT = 990
SCREEN_WIDTH = 1180
SCREEN_SIZE = 990
GRID_DIM = 60
GRID_SIZE = SCREEN_SIZE / GRID_DIM
GRID_WIDTH = SCREEN_SIZE / GRID_DIM
GRID_HEIGHT = SCREEN_SIZE / GRID_DIM

# My ship's size and location
SHIP_SIZE = 3 * GRID_WIDTH
SHIP_Y = (SCREEN_SIZE - 2 * SHIP_SIZE)
MISSILE_SIZE = 3

HUDX = HUDY = 0

# How quickly they'll spawn apart from each other
ENEMY_SPAWN_RATE = .1

# In case we care about size later
# This matches what's default in the enemyFormationFile.csv
# We'll later multiply this by GRID_SIZE when drawing it
ENEMY_DEFAULT_SIZE = 2 * GRID_SIZE

# Stars. For use in populate_starfield() and update_starfield()
NUM_STARS = 50 # totally arbitary
STAR_SIZE = 2 # pixels
STAR_SLOW = 10 # pixels per update
STAR_FAST = 20 # pixels per update
START_ANIMATION = 1 # 1: rotation, 0: warp

LASER_POINTER_SIZE = 4

# Radius in pixels of the parameterized circle in bezier (state 20 in the ai function)
RADIUS = 100