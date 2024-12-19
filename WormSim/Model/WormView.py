from matplotlib import pyplot as plt
import numpy as np
import json
import math
import os
import argparse
import sys
from Player import Player

# Global variables
midline_plot = None
perimeter_plot = None

def validate_file(file_path):
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist.")
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
    return file_path

def get_perimeter(x, y, r):
    n_bar = x.shape[0]
    num_steps = x.shape[1]

    n_seg = int(n_bar - 1)

    # radii along the body of the worm
    r_i = np.array([
        r * abs(math.sin(math.acos(((i) - n_seg / 2.0) / (n_seg / 2.0 + 0.2))))
        for i in range(n_bar)
    ]).reshape(-1, 1)

    diff_x = np.diff(x, axis=0)
    diff_y = np.diff(y, axis=0)

    arctan = np.arctan2(diff_x, -diff_y)
    d_arr = np.zeros((n_bar, num_steps))

    # d of worm endpoints is based off of two points, whereas d of non-endpoints is based off of 3 (x, y) points
    d_arr[:-1, :] = arctan
    d_arr[1:, :] = d_arr[1:, :] + arctan
    d_arr[1:-1, :] = d_arr[1:-1, :] / 2

    dx = np.cos(d_arr)*r_i
    dy = np.sin(d_arr)*r_i

    px = np.zeros((2*n_bar, x.shape[1]))
    py = np.zeros((2*n_bar, x.shape[1]))

    px[:n_bar, :] = x - dx
    px[n_bar:, :] = np.flipud(x + dx) # Make perimeter counter-clockwise

    py[:n_bar, :] = y - dy
    py[n_bar:, :] = np.flipud(y + dy) # Make perimeter counter-clockwise

    return px, py


def main():

    # Default behavior is to use (px, py) if it exists, and if it doesn’t then automatically generate the perimeter from the midline. 
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('-f', '--wcon_file', type=validate_file, help='WCON file path')
    parser.add_argument('-s', '--suppress_automatic_generation', action='store_true', help='Suppress the automatic generation of a perimeter which would be computed from the midline of the worm. If (px, py) is not specified in the WCON, a perimeter will not be shown.')
    parser.add_argument('-i', '--ignore_wcon_perimeter', action='store_true', help='Ignore (px, py) values in the WCON. Instead, a perimeter is automatically generated based on the midline of the worm.')
    parser.add_argument('-r', '--minor_radius', type=float, default=40e-3, help='Minor radius of the worm in millimeters (default: 40e-3)', required=False)

    args = parser.parse_args()

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title("2D WormSim replay")
    ax.set_aspect("equal")

    with open(args.wcon_file, 'r') as f:
        wcon = json.load(f)
    
    if "@CelegansNeuromechanicalGaitModulation" in wcon:
        center_x_arr = wcon["@CelegansNeuromechanicalGaitModulation"]["objects"]["circles"]["x"]
        center_y_arr = wcon["@CelegansNeuromechanicalGaitModulation"]["objects"]["circles"]["y"]
        radius_arr = wcon["@CelegansNeuromechanicalGaitModulation"]["objects"]["circles"]["r"]

        for center_x, center_y, radius in zip(center_x_arr, center_y_arr, radius_arr):
            circle = plt.Circle((center_x, center_y), radius, color="b")
            ax.add_patch(circle)
    else:
        print("No objects found")

        # Set the limits of the plot since we don't have any objects to help with autoscaling
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])

    t = np.array(wcon["data"][0]["t"])
    x = np.array(wcon["data"][0]["x"]).T
    y = np.array(wcon["data"][0]["y"]).T

    num_steps = t.size

    if "px" in wcon["data"][0] and "py" in wcon["data"][0]:
        if args.ignore_wcon_perimeter:
            print("Ignoring (px, py) values in WCON file and computing perimeter from midline.")
            px, py = get_perimeter(x, y, args.minor_radius)
        else:
            print("Using (px, py) from WCON file")
            px = np.array(wcon["data"][0]["px"]).T
            py = np.array(wcon["data"][0]["py"]).T
    else:
        if not args.suppress_automatic_generation:
            print("Computing perimeter from midline")
            px, py = get_perimeter(x, y, args.minor_radius)
        else:
            print("Not computing perimeter from midline")
            px = None
            py = None

    def update(ti):
        global midline_plot, perimeter_plot
        f = ti / num_steps

        color = "#%02x%02x00" % (int(0xFF * (f)), int(0xFF * (1 - f) * 0.8))
        print("Time step: %s, fract: %f, color: %s" % (ti, f, color))

        if midline_plot is None:
            (midline_plot,) = ax.plot(x[:, ti], y[:, ti], color="g", label="t=%sms" % t[ti], linewidth=0.5)
        else:
            midline_plot.set_data(x[:, ti], y[:, ti])
        
        if px is not None and py is not None:
            if perimeter_plot is None:
                (perimeter_plot,) = ax.plot(px[:, ti], py[:, ti], color="grey", linewidth=1)
            else:
                perimeter_plot.set_data(px[:, ti], py[:, ti])

    ani = Player(fig, update, maxi=num_steps - 1)

    # TODO WormViewCSV and WormViewWCON - should WormViewCSV just be the original WormView? That's what it initially did. 
    # TODO Could take out Player and WormViewWCON into separate repo - Taking out Player could be ugly. It is quite coupled with WormView due to the update function. 

    plt.show()

if __name__ == "__main__":
    sys.exit(main())