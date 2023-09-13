import pythonGraph as pg
from bezier import line_parametric
from time import time

SCREEN_SIZE = 990
SHIP_X = 500
SHIP_Y = 500
SHIP_SIZE = 50

# For the rotation of the whole starfield
pg.open_window(SCREEN_SIZE, SCREEN_SIZE)

def draw_ship(x, y, h = 0):
    pg.draw_image("images/ship.png", x, y, SHIP_SIZE, SHIP_SIZE, h)

def mouse(x, y, move, now):
    if(pg.mouse_button_pressed("left")):
        print("Belp")
        return pg.get_mouse_x(), pg.get_mouse_y(), True, time()
    else:
        return x, y, move, now

move = False
heading = 0
xc = SHIP_X
yc = SHIP_Y
now = 0
x = 0
y = 0

while(pg.window_not_closed()):
    x, y, move, now = mouse(x, y, move, now)

    draw_ship(SHIP_X, SHIP_Y, heading)
    

    if(move):
        t = (time() - now) / 3
        SHIP_X, SHIP_Y, heading = line_parametric(t, xc, yc, x, y)
        print(t, SHIP_X, SHIP_Y)
        if(t > 1):
            move = False
            xc = SHIP_X
            yc = SHIP_Y
    pg.update_window()
    pg.clear_window("black")
