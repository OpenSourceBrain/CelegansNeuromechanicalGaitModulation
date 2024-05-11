from matplotlib import pyplot as plt
from numpy import genfromtxt
import numpy as np
import json
import math
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

# num_steps = time_arr.size
num_steps = t.size

# Nbar = x_arr.shape[0]
Nbar = x.shape[0]
NSEG = int(Nbar - 1)
D = 80e-6

R = np.array([
    D / 2.0 * abs(math.sin(math.acos(((i) - NSEG / 2.0) / (NSEG / 2.0 + 0.2))))
    for i in range(Nbar)
]).reshape(-1, 1)

print(x.shape)
diff_x = np.diff(x, axis=0)
print(diff_x.shape)
diff_y = np.diff(y, axis=0)
arctan = np.arctan2(diff_x, -diff_y)
# arctan = np.arctan2(np.abs(diff_x), diff_y)
# arctan = np.arctan2(diff_x, np.abs(diff_y))
# arctan = np.arctan2(np.abs(diff_x), np.abs(diff_y))

# arctan = np.arctan(-np.abs(diff_x) / np.abs(diff_y)) # closest yet
# arctan = np.arctan(np.abs(diff_x) / diff_y)
# arctan = np.arctan(diff_x / np.abs(diff_y))
# arctan = np.arctan(diff_x / diff_y)
print(arctan.shape) # 48, 500
print(arctan[:, 0])
# convolve = np.convolve(arctan, [0.5, 0.5], "valid")
# print(convolve.shape)
d_arr = np.zeros((Nbar, num_steps)) # 49, 500
print(d_arr.shape)
# d of worm endpoints is based off of two points, whereas d of non-endpoints is based off of 3 (x, y) points
d_arr[:-1, :] = arctan
d_arr[1:, :] = d_arr[1:, :] + arctan
d_arr[1:-1, :] = d_arr[1:-1, :] / 2

print(d_arr[:, 0])



dx = np.cos(d_arr)*R
dy = np.sin(d_arr)*R

# px = np.zeros((2*Nbar, x_arr.shape[1]))
px_computed = np.zeros((2*Nbar, x.shape[1]))
# py = np.zeros((2*Nbar, x_arr.shape[1]))
py_computed = np.zeros((2*Nbar, x.shape[1]))

# px[:Nbar, :] = x_arr - dx
px_computed[:Nbar, :] = x - dx
# px[Nbar:, :] = np.flipud(x_arr + dx) # Make perimeter counter-clockwise
px_computed[Nbar:, :] = np.flipud(x + dx) # Make perimeter counter-clockwise

# py[:Nbar, :] = y_arr - dy
py_computed[:Nbar, :] = y - dy
# py[Nbar:, :] = np.flipud(y_arr + dy) # Make perimeter counter-clockwise
py_computed[Nbar:, :] = np.flipud(y + dy) # Make perimeter counter-clockwise

# timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
# info = "Loaded: %s points from %s, saving %i frames" % (num_steps, original_file_name, num_steps)
# time_arr_list = time_arr.tolist()
# x_arr_list = x_arr.T.tolist()
# y_arr_list = y_arr.T.tolist()
# px_arr_list = px.T.tolist()
# py_arr_list = py.T.tolist()



timesteps = t.size

midline_plot = None
perimeter_plot = None
perimeter_plot_computed = None

from Player import Player


def update(ti):
    global midline_plot, perimeter_plot, perimeter_plot_computed
    f = ti / timesteps

    color = "#%02x%02x00" % (int(0xFF * (f)), int(0xFF * (1 - f) * 0.8))
    print("Time step: %s, fract: %f, color: %s" % (ti, f, color))

    if midline_plot is None:
        (midline_plot,) = ax.plot(x[:, ti], y[:, ti], color="g", label="t=%sms" % t[ti], linewidth=0.5, marker='x')
    else:
        midline_plot.set_data(x[:, ti], y[:, ti])
    
    if perimeter_plot is None:
        (perimeter_plot,) = ax.plot(px[:, ti], py[:, ti], color="grey", linewidth=1, marker='x')
    else:
        perimeter_plot.set_data(px[:, ti], py[:, ti])
    
    if perimeter_plot_computed is None:
        (perimeter_plot_computed,) = ax.plot(px_computed[:, ti], py_computed[:, ti], color="red", linewidth=1, marker='x')
    else:
        perimeter_plot_computed.set_data(px_computed[:, ti], py_computed[:, ti])

ax.plot()  # Causes an autoscale update.

ani = Player(fig, update, maxi=timesteps - 1)

plt.show()
