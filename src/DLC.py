from LOF import *
import matplotlib.pyplot as plt
import logging


# Given a tuple p and a grid g', the minimum distance between p and g' on the i-th dimension is
def disi(i, p, grid):
    if p[i] > grid.max[i]:
        return p[i]-grid.max[i]
    elif p[i] < grid.min[i]:
        return grid.min[i]-p[i]
    else:
        return 0


# the minimum distance between p and g' is
def dispPGrid(p, grid):
    res = 0
    for i in range(len(p)):
        res += disi(i, p, grid) ** 2
    return np.sqrt(res)


def is_cross_grid(p, grid, localDistK):
    for i in range(len(p)):
        if not (p[i]-localDistK >= grid.min[i] and p[i]+localDistK < grid.max[i]):
            return True
    return False


def NeiDis(i, p, g, localDistK):
    res = localDistK**2
    for j  in range(len(p)):
        if j != i:
            res -= disi(j, p, g)**2
    return np.sqrt(res)


def rectangle(i, p, g, localDistK):
    neiDis = NeiDis(i, p, g, localDistK)
    if p[i] > g.max[i]:
        rmin = p[i]-neiDis
        rmax = g.max[i]
    elif p[i] < g.min[i]:
        rmin = g.min[i]
        rmax = p[i]+neiDis
    else:
        rmin = max([p[i]-neiDis, g.min[i]])
        rmax = min([p[i]+neiDis, g.max[i]])
    return rmin, rmax


def integrated_rectangle(p, g, localDistK):
    rmin, rmax = [], []
    for i in range(len(p)):
        a, b = rectangle(i, p, g, localDistK)
        rmin.append(a)
        rmax.append(b)
    return rmin, rmax


# Distributed LOF Computation method
def dlc(k, grid, neighbours, plot_info=False, ax=None):
    cross_grid_list = []
    add = []
    for p in grid.list_tuples:
        localDistK = k_distance(k, p, grid)
        if is_cross_grid(p, grid, localDistK):
            cross_grid_list = cross_grid_list + [p]
            for adjacent in neighbours:
                if dispPGrid(p, adjacent) < localDistK:
                    # Compute the related minimum rectangle in g
                    rmin, rmax = integrated_rectangle(p, adjacent, localDistK)
                    if plot_info:
                        ax.scatter(p[0], p[1], color = 'g', alpha=0.9)
                        ax.hlines(y = rmin[1], xmin = rmin[0], xmax = rmax[0], colors = "grey", linestyles = ":")
                        ax.hlines(y = rmax[1], xmin = rmin[0], xmax = rmax[0], colors = "grey", linestyles = ":")
                        ax.vlines(x = rmin[0], ymin = rmin[1], ymax = rmax[1], colors = "grey", linestyles = ":")
                        ax.vlines(x = rmax[0], ymin = rmin[1], ymax = rmax[1], colors = "grey", linestyles = ":")

                    for elem in adjacent.getTupleBetween(rmin, rmax):
                        if elem not in add:
                            add.append(elem)
        elif plot_info:
            ax.scatter(p[0], p[1], color = 'purple', alpha=0.9)

    new_grid = grid.__copy__()
    new_grid.add_tuple( add )

    return new_grid

"""
def dlc(_k: int, grid: Grid, neighbours: list[Grid]):
    new_grid = grid.__copy__()
    for n in neighbours:
        new_grid.add_tuple( n.list_tuples )
    return new_grid
"""
