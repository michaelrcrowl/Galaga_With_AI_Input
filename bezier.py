import numpy as np
import math
import helper_functions as hf
from constants import RADIUS


def beziercurve(t, P):
    n = len(P) - 1
    point = 0
    dt = 0

    # Iteratively calculate the Bezier curve
    # Chat GPT was fairly helpful here, though I had to fix its code, so I claim some credit for the awesomeness that follows
    for i in range(n + 1):
        point += P[n-i] * math.comb(n, i) * ( t**(n-i) ) * (1 - t)**i

    # Iteratively calculate the derivative of the curve.  Math is beautiful
    # Chat GPT helped with this too, because I was too lazy to work through the chain rule.  
    # After fixing the above equation, ChatGPT nailed this on its first try
    for i in range(n):
        dt += (P[i+1] - P[i]) * (1 - t)**(n - i - 1) * n * np.math.comb(n-1, i) * t**i

    # Calculate the heading based off the slope of the derivative.
    # Want the answer in degrees to work with pg.draw_image
    # This was all me!!!!
    heading = 90 + math.atan2(dt[1], dt[0]) * 180 / math.pi 

    return point[0], point[1], heading

# This is just a straight line
# This is probably overkill for a straight line, but I have a process, and it works really well
def line_parametric(t, startx, starty, endx, endy):
    # Define starting and ending points
    x = startx + (endx - startx) * t
    y = starty + (endy - starty) * t
    heading = math.atan2(x - startx, y - starty) * 180 / math.pi 
    if(heading < 0):
        heading = (heading + 180) * -1
    if(heading > 0):
        heading = 180 - heading

    return x, y, heading

# Enter from top left corner
def enterCurve1(t, startx, starty, endx, endy):
    # Define starting and ending points
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([990, 0])
    P2 = np.array([800, 1000])
    return beziercurve(t, [P0, P1, P2, P3])


# Enter from top right corner
def enterCurve2(t, startx, starty, endx, endy):
    # Define starting and ending points
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([0, 0])
    P2 = np.array([90, 1000])

    return beziercurve(t, [P0, P1, P2, P3])


# Exit towards the bottom of the screen
def exitCurve1(t, startx, starty, endx, endy):
    # Define starting and ending points
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([700, 0])
    P2 = np.array([1000, 600])

    return beziercurve(t, [P0, P1, P2, P3])

# Exit towards the bottom of the screen
def exitCurve2(t, startx, starty, endx, endy):
    # Define starting and ending points
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([1000, 150])
    P2 = np.array([80, 130])

    return beziercurve(t, [P0, P1, P2, P3])

def genericCurve1(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([100, 500])
    P2 = np.array([700, 600])

    return beziercurve(t, [P0, P1, P2, P3])

def loopCurve1(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([0, 275])
    P2 = np.array([1000, 20])

    return beziercurve(t, [P0, P1, P2, P3])

def swoopCurve1(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([0, 1050])
    P2 = np.array([1050, 1050])

    return beziercurve(t, [P0, P1, P2, P3])


def swoopCurve2(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P7 = np.array([endx, endy])

    # Define control points
    P1 = np.array([0, 1050])
    P2 = np.array([1100, 1200])
    P3 = np.array([650, 350])
    P4 = np.array([900, 800])
    P5 = np.array([550, 1100])
    P6 = np.array([100, 1100])

    return beziercurve(t, [P0, P1, P2, P3, P4, P5, P6, P7])

# Through pure reasoning, I made this the way I wanted it.
def exitCurve3(t, startx, starty, endx, endy):
    # Define starting and ending points
    P0 = np.array([startx, starty])
    P7 = np.array([endx, endy])

    # Define control points
    P1 = np.array([150, 50])
    P2 = np.array([1000, 250])
    P3 = np.array([700, 900])
    P4 = np.array([700, 800])
    P5 = np.array([50, 800])
    P6 = np.array([300, 800])

    return beziercurve(t, [P0, P1, P2, P3, P4, P5, P6, P7])

def rkocurve(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([781, 618])
    P2 = np.array([784, 388])

    return beziercurve(t, [P0, P1, P2, P3])

# Didn't work right
# def rkocurve2(t, startx, starty, endx, endy):
#     P0 = np.array([startx, starty])
#     P7 = np.array([endx, endy])

#     # Define control points
#     P1 = np.array([891, 982])
#     P2 = np.array([891, 924])
#     P3 = np.array([850, 909])
#     P4 = np.array([945, 940])
#     P5 = np.array([889, 542])
#     P6 = np.array([738, 451])

#     return beziercurve(t, [P0, P1, P2, P3])

def cenacurve(t, startx, starty, endx, endy):
    P0 = np.array([startx, starty])
    P3 = np.array([endx, endy])

    # Define control points
    P1 = np.array([210, 20])
    P2 = np.array([377, 158])

    return beziercurve(t, [P0, P1, P2, P3])

def circle(t, startx, starty):
    t = math.pi * 2 * t

    # Normalize it so that it's always between 0 and 2pi
    # I need this for my heading calculation
    if(t > 2 * math.pi):
        t -= 2 * math.pi

    x = RADIUS * math.cos(t) + startx - RADIUS
    y = RADIUS * math.sin(t) + starty

    # The vector from the center of the circle to the enemy's location on the circle
    vecx = x - startx + RADIUS
    vecy = y - starty

    # dot product to calcuate the tangent
    y2 = (vecx**2 / vecy)

    # Use the tangent to calculate the heading
    heading = -180 + math.atan2(vecx, y2) * 180 / math.pi 

    if(math.pi / 2 < t < math.pi or 3 * math.pi / 2 < t < 2 * math.pi):
        heading += 180

    return x, y, heading

# Sine wave going down the screen
def exitSin(t, startx, starty, endx, endy):
    # Going down the screen in a linear fashion
    y = starty + (endy - starty) * t

    # But for my x coord to follow a sin curve, t needs to be between 0 and 2pi
    t = math.pi * 2 * t 

    # Sine!  It'll move left and right by 100 pixels
    x = 100 * math.sin(t) + startx

    # Derivative of x's sine function, scaled to make the heading more natural-looking
    # And rotated by 180 degrees since my pictures point straight up
    heading = 180 - 45 * math.cos(t)

    return x, y, heading