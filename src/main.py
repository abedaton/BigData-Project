from tabnanny import verbose
import numpy as np
import matplotlib.pyplot as plt
import random
from generate_data import test_uniform, generate_circle, generate_cluster
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


def plot_lof(sub_grid, grid_dict, ax, thread_name):
    logging.info("Starting thread: " + str(thread_name))
    for g in sub_grid:
        tuples: list[tuple] = g.list_tuples
        new_grid: Grid = grid_dict[g]
        for p in tuples:
            lof = LOF(k, p, new_grid)

            if lof > 1.8:
                ax.scatter(p[0], p[1], color = 'r', alpha=0.9)
            elif lof > 1.2:
                ax.scatter(p[0], p[1], color = "purple", alpha=0.8)
            else:
                ax.scatter(p[0], p[1], color = "b", alpha=0.5)

if __name__ == "__main__":
    seed = random.randint(0, 2**32-1) #844397963904029491
    num_split = 4
    k = 3
    num_plot = 1
    plot = True
    info_plot = False
    for i, arg in enumerate(sys.argv):
        if arg == '-s' or arg == '-seed':
            seed = int(sys.argv[i+1])
        if arg == '-ns' or arg == '-num_split':
            num_split = int(sys.argv[i+1])
        if arg == '-k':
            k = int(sys.argv[i+1])
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


    x, y, data = test_uniform(size=100, err=2, num_outlier=3)
    #x, y, data = generate_circle(size=100, radius=2, num_outlier=5)
    #x, y, data = generate_cluster()

    fig, axs = plt.subplots(num_plot, 1)
    axs = fig.axes
    ax_plot, ax_info = None, None
    if plot:
        ax_plot = list(axs)[0]
        ax_plot.set_title("GBP + DLC + LOF")
    if info_plot:
        ax_info = list(axs)[-1]
        ax_info.set_title("Info")

    fig.tight_layout()

    gridSet = GridSet(data, num_split)
    plot_grid(num_split, list(axs))

    grid_dict = {}
    for grid in gridSet.grid_set:
        new_grid = dlc(k, grid, gridSet.find_neighbours(grid), plot_info=info_plot, ax=ax_info)
        # new_grid = dlc(k, grid, gridSet.find_neighbours(grid))
        grid_dict[grid] = new_grid

    if not plot:
        plt.show()
        exit()

    N = gbp(gridSet, [[]]*10)
    verify_theorem1(N)

    threads = [threading.Thread(target=plot_lof, args=(sub_grid, grid_dict, ax_plot, name+1)) for name, sub_grid in enumerate(N)]
    for thread in threads:
        thread.start()

    #plot_lib(data, axs[3])

    for thread in threads:
        thread.join()

    plt.show()
