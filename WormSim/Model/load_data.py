
from matplotlib import pyplot as plt

from numpy import genfromtxt
my_data = genfromtxt('simdata.csv', delimiter=',').T

t = my_data[0]

x_offset = 1
y_offset = 2

'''
for i in [(j*3)+y_offset for j in range(49)]:
    plt.plot(t,my_data[i],label=i)

plt.legend()'''


fig, ax = plt.subplots()
ax.set_aspect('equal')

import os
usingObjects = os.path.isfile('objects.csv')
if usingObjects:
    Objects = genfromtxt('objects.csv', delimiter=',')
    for o in Objects:
        x = o[0]
        y= o[1]
        r = o[2]
        print("Circle at (%s, %s), radius %s"%(x,y,r))
        circle1 = plt.Circle((x, y), r, color='b')
        plt.gca().add_patch(circle1)
else:
    print("No objects found")
    
num_t = 20
timesteps = len(t)

for ti in [int(timesteps * i/num_t) for i in range(num_t)]:

    f = ti/timesteps

    color = "#%02x%02x00" % (int(0xFF*(f)),int(0xFF*(1-f)*0.8))
    print("Color at ti: %s, f %f: %s"%(ti,f,color))
    xs = []
    ys = []

    for i in [(j*3)+x_offset for j in range(49)]:
        xs.append(my_data[i][ti])

    for i in [(j*3)+y_offset for j in range(49)]:
        ys.append(my_data[i][ti])

    print('\n t=%sms'%t[ti])
    print("xs: %s"%xs)
    print("ys: %s"%ys)

    plt.plot(xs,ys,color=color,label='t=%sms'%t[ti],markersize=3 if ti==0 else 0.4)


ax.plot()   #Causes an autoscale update.
plt.show()
