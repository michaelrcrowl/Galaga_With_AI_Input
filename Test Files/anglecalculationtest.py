import pythonGraph as pg
from pythonGraph import pygame
import math

S_W = S_H = 990
xc = S_W / 2
yc = S_H / 2
MISSILES = []

move = False

pg.open_window(S_W, S_H)
size = S_W, S_H
screen = pygame.display.set_mode(size)
while(pg.window_not_closed()):
    pg.clear_window("WHITE")
    x = pg.get_mouse_x()
    y = pg.get_mouse_y()

    if(pg.mouse_button_down("left")):
        theta = math.atan(((x - xc)) / (y - yc))
        MISSILES.append([theta, xc, yc, 'torpedo_north'])

    for m in MISSILES:
        m[2] -= 5 * (1 * math.cos(-m[0]))
        m[1] += 5 * (1 * math.sin(-m[0]))
        image = pygame.image.load(m[3] + '.png')
        image = pygame.transform.rotate(image, m[0] * 180 / math.pi)
        screen.blit(image, (m[1] - (.5 * image.get_width()), m[2] - (.5 * image.get_height())))
    # if(move):

    pg.draw_circle(xc, yc, 10, "RED", True)
    pg.draw_circle(x, y, 10, "RED", True)

    pg.draw_line(x, y, xc, y, "RED")
    pg.draw_line(x, y, x, yc, "RED")
    pg.draw_line(x, yc, xc, y, "RED")
    
    # pg.draw_line(S_W / 2, S_H / 2, x, y, "RED")
    # pg.draw_line(x, S_H / 2, x, y, "RED")
    # pg.draw_line(S_W / 2, S_H / 2, x, S_H / 2, "RED")

    try:
        pg.draw_text("atan:  " + str(math.atan((x - xc) / (y - yc)) * 180 / math.pi), 0, 0, "BLACK")
        pg.draw_text("atan2: " + str(math.atan2(x - xc, y - yc) * 180 / math.pi), 0, 40, "BLACK")
    except:
        pass
    pg.update_window()