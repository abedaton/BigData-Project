import timeit
import matplotlib.pyplot as plt
import threading

import generate_data
import main
import GridAllocation
import DLC


def plotruntime(f, r, trials=1, figsize=[3,3]):
    Times=[timeit.timeit(lambda:f(n),number=trials)/trials for n in r]
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(r,Times)
    ax.set_xlabel("Value of n")
    ax.set_ylabel("Runtime")
    
def plotruntimes(functions, labels, r, trials=1, figsize=[3,3]):
    fig, ax = plt.subplots(figsize=figsize)
    for f,l in zip(functions,labels):
        Times=[timeit.timeit(lambda:f(n),number=trials)/trials for n in r]
        ax.plot(r,Times,label=l)
    ax.set_xlabel("number of elements")
    ax.set_ylabel("Runtime in sec")
    ax.set_title("Runtime plot: "+str(trials)+" trial"+("s" if trials>1 else ""))
    ax.legend()

def f1(n):
    data = generate_data.test_uniform(size=n, err=2, num_outlier=3)
    k = 3
    grid = GridAllocation.Grid([0,0], data)
    main.calc_lof(data, grid, k, None, False, None)

def f2(n):
    num_thread = 20
    num_split = 4
    k = 3
    data = generate_data.test_uniform(size=n, err=2, num_outlier=3)

    gridSet = GridAllocation.GridSet(data, num_split)

    grid_dict = {}
    for grid in gridSet.grid_set:
        new_grid = DLC.dlc(k, grid, gridSet.find_neighbours(grid), plot_info=False, ax=None)
        grid_dict[grid] = new_grid

    N = GridAllocation.gbp(gridSet, [[]]*num_thread)

    threads = [threading.Thread(target=main.threaded_lof, args=(sub_grid, grid_dict, k, None, name + 1, None, False)) for name, sub_grid in enumerate(N)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    plotruntimes([f1, f2], ["LOF", "DLC"], range(1,200,20), 10)
    plt.show()