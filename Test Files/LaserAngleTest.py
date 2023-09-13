import pythonGraph as pg
import math

SCREEN_WIDTH = 990
SCREEN_HEIGHT = 990

def draw_trajectory(x1, y1, x2, y2):
    theta = -math.atan2(x2 - x1, y2 - y1)
    x2 = x1 + (y1 * math.tan(theta))
    y2 = 0

    pg.draw_line(x1, y1, x2, y2, "red", width=4)

pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)

while(pg.window_not_closed()):
    x = pg.get_mouse_x()
    y = pg.get_mouse_y()
    draw_trajectory(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, x, y)
    pg.update_window()
    pg.clear_window("white")