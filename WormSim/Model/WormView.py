from matplotlib import pyplot as plt
from numpy import genfromtxt
import numpy as np
import json
import os

fig, ax = plt.subplots()
plt.get_current_fig_manager().set_window_title("2D WormSim replay")
ax.set_aspect("equal")

usingObjects = os.path.isfile("objects.csv")
if usingObjects:
    Objects = genfromtxt("objects.csv", delimiter=",")
    for o in Objects:
        x = o[0]
        y = o[1]
        r = o[2]
        # print("Circle at (%s, %s), radius %s"%(x,y,r))
        circle1 = plt.Circle((x, y), r, color="b")
        plt.gca().add_patch(circle1)
else:
    print("No objects found")

num_t = 30

with open("simdata.wcon", 'r') as f:
    wcon = json.load(f)

t = np.array(wcon["data"][0]["t"])
x = np.array(wcon["data"][0]["x"]).T
y = np.array(wcon["data"][0]["y"]).T
px = np.array(wcon["data"][0]["px"]).T
py = np.array(wcon["data"][0]["py"]).T

timesteps = t.size

midline_plot = None
perimeter_plot = None

from Player import Player


def update(ti):
    global midline_plot, perimeter_plot
    f = ti / timesteps

    color = "#%02x%02x00" % (int(0xFF * (f)), int(0xFF * (1 - f) * 0.8))
    print("Time step: %s, fract: %f, color: %s" % (ti, f, color))

    if midline_plot is None:
        (midline_plot,) = ax.plot(x[:, ti], y[:, ti], color="g", label="t=%sms" % t[ti], linewidth=0.5)
    else:
        midline_plot.set_data(x[:, ti], y[:, ti])
    
    if perimeter_plot is None:
        (perimeter_plot,) = ax.plot(px[:, ti], py[:, ti], color="grey", linewidth=1)
    else:
        perimeter_plot.set_data(px[:, ti], py[:, ti])

ax.plot()  # Causes an autoscale update.

ani = Player(fig, update, maxi=timesteps - 1)

plt.show()
