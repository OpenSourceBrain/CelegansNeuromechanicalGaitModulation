import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import json
import argparse
import sys
import os
import math


def validate_file(file_path):
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"The file {file_path} does not exist.")
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"{file_path} is not a valid file.")
    return file_path


def main():

    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('-f', '--wcon_file', type=validate_file, help='WCON file path')

    args = parser.parse_args()

    fig, axs = plt.subplots(1, 2, figsize=(14, 3))

    with open(args.wcon_file, 'r') as f:
        wcon = json.load(f)

    title_font_size = 10

    t_arr = np.array(wcon["data"][0]["t"])
    x_arr = np.array(wcon["data"][0]["x"])
    y_arr = np.array(wcon["data"][0]["y"])

    num_steps = t_arr.size
    tmax = num_steps
    num = 60.

    axs[0].set_title('2D worm motion', fontsize=title_font_size)

    for t in range(0, tmax, int(tmax/num)):
        f = float(t)/tmax

        color = "#%02x%02x00" % (int(0xFF*(f)),int(0xFF*(1-f)*0.8))

        for x, y in zip(x_arr[t], y_arr[t]):
            axs[0].plot(x, y, '.', color=color, markersize=3 if t==0 else 0.4)

    axs[0].set_aspect('equal')

    x_transposed = x_arr.T
    y_transposed = y_arr.T

    # TODO: Below is same utility function as in WormView.py. Move to a utility file.
    r = 40e-3
    n_bar = x_transposed.shape[0]
    num_steps = x_transposed.shape[1]

    n_seg = int(n_bar - 1)

    # radii along the body of the worm
    r_i = np.array([
        r * abs(math.sin(math.acos(((i) - n_seg / 2.0) / (n_seg / 2.0 + 0.2))))
        for i in range(n_bar)
    ]).reshape(-1, 1)

    diff_x = np.diff(x_transposed, axis=0)
    diff_y = np.diff(y_transposed, axis=0)

    arctan = np.arctan2(diff_x, -diff_y)
    d_arr = np.zeros((n_bar, num_steps))

    # d of worm endpoints is based off of two points, whereas d of non-endpoints is based off of 3 (x, y) points
    d_arr[:-1, :] = arctan
    d_arr[1:, :] = d_arr[1:, :] + arctan
    d_arr[1:-1, :] = d_arr[1:-1, :] / 2

    # TODO: Determine what "0" starting position should be. Currently, worm facing left while horizontal is "white" in curvature plot.
    d_arr = d_arr - np.pi/2

    # Blue corresponds to -pi, white corresponds to 0, and red corresponds to pi
    colors = [
        (0, 'blue'),
        (0.5, 'white'),
        (1, 'red')
    ]
    custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)
    norm = Normalize(vmin=-np.pi, vmax=np.pi)

    axs[1].set_title('Body curvature', fontsize=title_font_size)
    axs[1].imshow(d_arr, aspect='auto', cmap=custom_cmap, norm=norm)

    print(np.max(d_arr))
    print(np.min(d_arr))
    print(d_arr)

    plt.show()


if __name__ == "__main__":
    sys.exit(main())