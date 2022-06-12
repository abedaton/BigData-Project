import numpy as np
import random


class GridSet:
    grids = None
    sorted_grid = None

    def __init__(self, matrix):
        self.grids = np.empty(matrix.shape, dtype=Grid)
        self.sorted_grid = np.array([])
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.grids[i][j] = Grid(matrix[i][j], i, j)
                self.sorted_grid = np.append(self.sorted_grid, self.grids[i][j])

        self.sorted_grid = sorted(self.sorted_grid, key=lambda x: x.value, reverse=True)

    def find_neighbours(self, grid):
        neighbours = []
        i = grid.i
        j = grid.j
        x_poss = [i]
        y_poss = [j]
        if i > 0:
            x_poss.append(i - 1)
        if i < len(self.grids) - 1:
            x_poss.append(i + 1)
        if j > 0:
            y_poss.append(j - 1)
        if j < len(self.grids[0]) - 1:
            y_poss.append(j + 1)
        for x in x_poss:
            for y in y_poss:
                if x != i or y != j:
                    neighbours.append(self.grids[x][y])
        return neighbours

    def __str__(self):
        return "Sorted List: " + str([grid.value for grid in self.sorted_grid])


class Grid:
    value = None
    i = None
    j = None

    def __init__(self, _value, _i, _j):
        self.value = _value
        self.i = _i
        self.j = _j

    def __add__(self, other):
        if isinstance(other, int):
            return self.value + other

    def __radd__(self, other):
        if isinstance(other, int):
            return self.value + other

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


def gbp(G, N):
    print(G)

    for g in G.sorted_grid:
        print("-----------------\nDoing grid", g.value, "at index i =", g.i, "j =", g.j)
        print("N =", N)
        available = [i for i, x in enumerate(N) if len(x) == 0]
        if len(available) > 0:
            chosen = random.choice(available)
            N[chosen] = N[chosen] + [g]
        else:
            epsilon = sum([sum(grid.value for grid in alist) for alist in N])/len(N)
            print("Epsilon =", epsilon)
            neighbours_g = set(G.find_neighbours(g))
            N_prime = [[]]*10

            for index, node in enumerate(N):
                if sum(elem.value for elem in node) <= epsilon:
                    N_prime[index] = node
            best_adj = -1
            best_node_index = -1
            for index, node in enumerate(N_prime):
                if len(node) > 0:
                    num_adj = 0
                    for grid in node:
                        neighbours_grid = set(G.find_neighbours(grid))
                        num_adj += len(neighbours_grid.intersection(neighbours_g))
                    if num_adj > best_adj:
                        best_adj = num_adj
                        best_node_index = index

            N[best_node_index] = N[best_node_index] + [g]
    return N


def verify_theorem1(N):
    print("\nVerifying Theorem 1: each node is smaller than mg + |P|/|N|")
    P = sum([sum(n) for n in N])
    g = max(N, key=len)
    mg = sum(g)
    len_N = len(N)
    print("P =", P, "| g =", g, "| mg =", mg, " | len N =", len_N)
    for node in N:
        if sum(node) >= mg + (P/len_N):
            print("Error: The node", node, "does not respect the Theorem 1")







