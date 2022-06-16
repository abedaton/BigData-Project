import numpy as np
import matplotlib.pyplot as plt
import random
from generate_data import test_uniform, generate_circle, generate_cluster, test_uniform3, generate_data
import threading
import sys
import logging
from logger import handler

logging.basicConfig(handlers=[handler()], level=logging.INFO)

from DLC import *


def plot_grid(num_grid, axs, _min=0, _max=1):
    step = (_max-_min) / num_grid
    li = [step*i for i in range(num_grid+1)]
    for ax in axs:
        ax.vlines(x = li, ymin=_min, ymax=_max, colors="black", linestyles=":")
        ax.hlines(y = li, xmin=_min, xmax=_max, colors="black", linestyles=":")


def plot_lib(data, ax):
    import pandas as pd
    from sklearn.neighbors import LocalOutlierFactor

    df = pd.DataFrame(np.array(data), columns=["x", "y"])
    model = LocalOutlierFactor(n_neighbors=2, contamination=0.02)
    y_pred = model.fit_predict(df)
    outlier_index = np.where(y_pred == -1)
    outlier_values = df.iloc[outlier_index]

    ax.scatter(df["x"], df["y"])
    ax.scatter(outlier_values["x"], outlier_values["y"], color="r")


def calc_lof(tuples, grid, k, scatter_fun, plot=False, ax=None, ):
    for p in tuples:
        lof = LOF(k, p, grid)
        if plot:
            if lof > 1.3:
                scatter_fun(p, ax, color="r", alpha=0.7)
            elif lof > 1:
                scatter_fun(p, ax, color="purple", alpha=0.7)
            else:
                scatter_fun(p, ax, color="b", alpha=0.7)

def threaded_lof(sub_grid, grid_dict, k, ax, thread_name, scatter_fun, plot=True):
    logging.info("Starting thread: " + str(thread_name))
    for g in sub_grid:
        tuples = g.list_tuples
        new_grid = grid_dict[g]
        calc_lof(tuples, new_grid, k, scatter_fun, plot, ax)
            
def get_data(file_name = "../datasets/shuttle/shuttle.trn"):
    f = open(file_name, "r")
    data = []
    for ligne in f:
        data.append([])
        for elem in ligne.split():
            data[-1].append(int(elem))
    f.close()
    return data

if __name__ == "__main__":
    seed = random.randint(0, 2**32-1) #2651051345
    num_split = 4
    k = 3
    num_thread = 10
    num_plot = 1
    plot = True
    info_plot = False
    time = False
    for i, arg in enumerate(sys.argv):
        if arg == '-s' or arg == '-seed':
            seed = int(sys.argv[i+1])
        if arg == '-ns' or arg == '-number_split':
            num_split = int(sys.argv[i+1])
        if arg == '-k':
            k = int(sys.argv[i+1])
        if arg == '-nt' or arg == '-number_thread':
            num_thread = int(sys.argv[i+1])
        if arg == '-np' or arg == '-no_plot':
            plot = False
            num_plot -= 1
        if arg == '-i' or arg == '-info':
            info_plot = True
            num_plot += 1

    if num_plot == 0:
        exit()

    random.seed(seed)
    np.random.seed(seed)
    logging.info("Seed for this run: " + str(seed))


    #data = get_data()
    # -----
    # data = test_uniform(size=100, err=2, num_outlier=3)
    # -----
    # data = test_uniform(size=100, err=2, num_outlier=3)
    dim = 2
    data = generate_data(size=100, err=2, num_outlier=5, dim=dim)
    #data = generate_circle(size=100, radius=2, num_outlier=5)
    #data = generate_cluster()

    # #------------ To Del
    # fig, ax = plt.subplots(num_plot, 1)
    # axs = fig.axes
    # plot_grid(num_split, list(axs))
    # gridSet = GridSet(data, num_split)
    # step = 1/num_split
    # ax.set_title("Number of points per grid")
    # for grid in gridSet.grid_set:
    #     i,j = grid.pos
    #     ax.text((i+0.4)*step, (j+0.4)*step, str(grid.number_tuples), fontsize=16)
    # plt.show()
    # exit()
    #------------

    fig, ax, fun = None, None, None
    if dim == 2:
        fig, axs = plt.subplots(num_plot, 1)
        fun = lambda p, ayx, color, alpha: ayx.scatter(p[0], p[1], color=color, alpha=alpha)
    elif dim == 3:
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax = fig.add_subplot(projection="3d")
        fun = lambda p, ayx, color, alpha: ayx.scatter(p[0], p[1], p[2], color=color, alpha=alpha)
        info_plot = False
    else:
        print("Cannot print in", len(data[0]), "dimensions")
        plot = False
        info_plot = False

    ax_plot, ax_info = None, None

    if 1 < dim < 4:
        axs = fig.axes
        if plot:
            ax_plot = list(axs)[0]
            ax_plot.set_title("DLC")
        if info_plot:
            ax_info = list(axs)[-1]
            ax_info.set_title("Info")

        fig.tight_layout()
        if dim == 2:
            # pass
            plot_grid(num_split, list(axs), 0, 1)

    gridSet = GridSet(data, num_split)

    grid_dict = {}
    for grid in gridSet.grid_set:
        new_grid = dlc(k, grid, gridSet.find_neighbours(grid), plot_info=info_plot, ax=ax_info)
        grid_dict[grid] = new_grid

    N = gbp(gridSet, [[]]*num_thread)
    verify_theorem1(N)

    threads = [threading.Thread(target=threaded_lof, args=(sub_grid, grid_dict, k, ax_plot, name + 1, fun, plot)) for name, sub_grid in enumerate(N)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    plt.show()