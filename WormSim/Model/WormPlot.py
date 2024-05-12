import numpy as np
from matplotlib import pyplot as plt
import json
import argparse
import sys
import os


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

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title("2D worm motion")

    with open(args.wcon_file, 'r') as f:
        wcon = json.load(f)

    title_font_size = 10

    t_arr = np.array(wcon["data"][0]["t"])
    x_arr = np.array(wcon["data"][0]["x"])
    y_arr = np.array(wcon["data"][0]["y"])

    num_steps = t_arr.size
    tmax = num_steps
    num = 60.

    ax.set_title('2D worm motion', fontsize=title_font_size)

    for t in range(0, tmax, int(tmax/num)):
        f = float(t)/tmax

        color = "#%02x%02x00" % (int(0xFF*(f)),int(0xFF*(1-f)*0.8))

        for x, y in zip(x_arr[t], y_arr[t]):
            ax.plot(x, y, '.', color=color, markersize=3 if t==0 else 0.4)

    plt.show()


if __name__ == "__main__":
    sys.exit(main())