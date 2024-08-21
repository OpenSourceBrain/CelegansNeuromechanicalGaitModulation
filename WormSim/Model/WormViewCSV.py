from matplotlib import pyplot as plt

from numpy import genfromtxt
import numpy as np
import math
import os

data = genfromtxt("simdata_test.csv", delimiter=",").T

print("Loaded data: %s" % (str(data.shape)))

t = data[0]

x_offset = 1
y_offset = 2
d_offset = 3

"""
for i in [(j*3)+y_offset for j in range(49)]:
    plt.plot(t,my_data[i],label=i)
plt.legend()"""

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
timesteps = len(t)

# Using same variable names as WormView.m
Sz = len(data)
Nt = len(data[0])
Nbar = int((Sz - 1) / 3)
NSEG = int(Nbar - 1)
D = 80e-6

R = [
    D / 2.0 * abs(math.sin(math.acos(((i) - NSEG / 2.0) / (NSEG / 2.0 + 0.2))))
    for i in range(Nbar)
]

CoM = np.zeros([Nt, Nbar, 3])
CoMplot = np.zeros([Nt, 2])
Dorsal = np.zeros([Nbar, 2])
Ventral = np.zeros([Nbar, 2])

print(f"Sz: {Sz}, Nt: {Nt}, Nbar: {Nbar}, NSEG: {NSEG}")
# Dt = data(2,1) - data(1,1);

ventral_plot = None
midline_plot = None
dorsal_plot = None

from Player import Player


def update(ti):
    global dorsal_plot, ventral_plot, midline_plot
    f = ti / timesteps

    color = "#%02x%02x00" % (int(0xFF * (f)), int(0xFF * (1 - f) * 0.8))
    print("Time step: %s, fract: %f, color: %s" % (ti, f, color))
    ds = []
    xs = []
    ys = []

    for i in [(j * 3) + d_offset for j in range(Nbar)]:
        ds.append(data[i][ti])

    for i in [(j * 3) + x_offset for j in range(Nbar)]:
        xs.append(data[i][ti])

    for i in [(j * 3) + y_offset for j in range(Nbar)]:
        ys.append(data[i][ti])

    for j in range(Nbar):
        dX = R[j] * math.cos(ds[j])
        dY = R[j] * math.sin(ds[j])

        Dorsal[j, 0] = xs[j] + dX
        Dorsal[j, 1] = ys[j] + dY
        Ventral[j, 0] = xs[j] - dX
        Ventral[j, 1] = ys[j] - dY

    if dorsal_plot == None:
        (dorsal_plot,) = ax.plot(Dorsal[:, 0], Dorsal[:, 1], color="grey", linewidth=1)
    else:
        dorsal_plot.set_data(Dorsal[:, 0], Dorsal[:, 1])

    if ventral_plot == None:
        (ventral_plot,) = ax.plot(
            Ventral[:, 0], Ventral[:, 1], color="grey", linewidth=1
        )
    else:
        ventral_plot.set_data(Ventral[:, 0], Ventral[:, 1])

    if midline_plot == None:
        (midline_plot,) = ax.plot(
            xs, ys, color="g", label="t=%sms" % t[ti], linewidth=0.5
        )
    else:
        midline_plot.set_data(xs, ys)


ax.plot()  # Causes an autoscale update.

ani = Player(fig, update, maxi=timesteps - 1)

plt.show()
