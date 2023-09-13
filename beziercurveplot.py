'''
The whole purpose of this program is to take all the functions from bezier.py and draw their associated curves to a file for reference
As you add more functions to bezier.py, add the function name here to the `curves` list
Also add the associated start and stop coordinates to the `coords` list

This has the added benefit that you can tweak a curve and see how that changes it
'''

import matplotlib.pyplot as plt
import numpy as np
import math
from bezier import *

import numpy as np

curves = [line_parametric, enterCurve1, enterCurve2, exitCurve1, exitCurve2, exitCurve3, genericCurve1, loopCurve1, swoopCurve1, swoopCurve2, rkocurve]
coords = [[0, 0, 445, 445], [0, 0, 445, 445], [990, 0, 445, 445], [445, 445, 300, 990], [445, 445, 990, 990], [445, 445, 990, 990], [445, 445, 445, 990], [990, 445, 445, 445], [445, 445, 445, 445], [445, 445, 445, 445], [990, 990, 445, 445]]
index = 0
for c in curves:
    # Define the time steps for the Bezier curve
    t_values = np.linspace(0, 1, 1000)

    # Compute the Bezier curve for each time step
    x_values = []
    y_values = []

    for t in t_values:
        # Get the x, y, and heading, but I don't care about heading right now
        x, y, _ = c(t, coords[index][0], coords[index][1], coords[index][2], coords[index][3], )
        x_values.append(x)
        y_values.append(y)

    # Get the next coordinates for the next function
    index += 1

    # Plot the Bezier curve
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values)
    # ax.plot([P0[0], P1[0], P2[0], P3[0]], [P0[1], P1[1], P2[1], P3[1]], 'o')
    ax.set_xlim([0, 990])
    ax.set_ylim([990, 0])
    ax.set_aspect('equal')
    plt.savefig("curves/" + c.__name__ + ".png")
    # plt.show()