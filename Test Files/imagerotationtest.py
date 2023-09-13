import pythonGraph as pg

pg.open_window(990, 990)

pg.clear_window('black')
pg.draw_image('images/lasertest.png', 420, 445, 50, 50, 45)
pg.draw_line(445, 0, 445, 990, "white")
pg.draw_line(0, 445, 990, 445, "white")
pg.wait_for_close()