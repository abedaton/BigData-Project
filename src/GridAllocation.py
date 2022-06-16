import random
import logging
# from main import logger


class GridSet:
    grid_set = None
    dimension = None

    def __init__(self, *args):
        if len(args) > 1:
            self.init(*args)

    def init(self, data, number_split):
        self.dimension = len(data[0])
        step = 1 / number_split

        grid = [ Grid( [], [], [], data) ]
        new_l = [  [ grid[0] ] ]
        for i in range(self.dimension):
            l = new_l
            new_l = []
            for elem in l:
                tmp_grid = elem.pop()
                grid.remove(tmp_grid)
                pos = tmp_grid.pos
                _min = tmp_grid.min
                _max = tmp_grid.max
                list_tuples = tmp_grid.list_tuples
                for j in range(number_split):
                    elem.append([])
                    new_tuples = []
                    for p in list_tuples:
                        if (step*(j + 1) > p[i] >= step*j) or (j==number_split-1 and p[i]==1.0):
                            new_tuples.append(p)
                    elem[-1] = [Grid(pos+[j], _min+[step*j],  _max+[step*(j+1)] ,new_tuples)]
                    grid.append(elem[-1][0])
                    new_l.append(elem[-1])
        self.grid_set = sorted(grid, key=lambda g:g.number_tuples, reverse=True)

    def __str__(self):
        return "Sorted List: " + str([grid.number_tuples for grid in self.grid_set]) + "\n" + str(self.grid_set)

    def __copy__(self):
        copy = GridSet()
        copy.dimension = self.dimension
        copy.grid_set = [g.__copy__() for g in self.grid_set]
        return copy


    def find_neighbours(self, grid):
        neighbours = self.grid_set[:]
        neighbours.remove(grid)
        pos = grid.pos
        for i in range(self.dimension):
            j = 0
            end = len(neighbours)
            while j != end:
                other_pos = neighbours[j].pos
                if other_pos[i] > pos[i]+1 or other_pos[i] < pos[i]-1:
                    neighbours.remove(neighbours[j])
                    end -= 1
                else:
                    j += 1
        logging.debug("Neighbours of " + str(grid.pos) + " = " + str(neighbours))
        return neighbours


class Grid:
    pos = []
    min = []
    max = []
    number_tuples = None
    list_tuples = []

    def __init__(self, *args):
        if len(args) == 2:
            self.init1(*args)
        elif len(args) == 4:
            self.init2(*args)

    def init1 (self, _pos, tuples):
        _min = [0 for _ in range(len(tuples[0]))]
        _max = [1 for _ in range(len(tuples[0]))]
        self.init2(_pos, _min, _max, tuples)

    def init2(self, _pos, _min, _max, tuples):
        self.pos = _pos
        self.min = _min
        self.max = _max
        self.number_tuples = len(tuples)
        self.list_tuples = tuples

    def __add__(self, other):
        if isinstance(other, int):
            return self.number_tuples + other

    def __radd__(self, other):
        if isinstance(other, int):
            return self.number_tuples + other

    def __str__(self):
        return  str(self.pos) + ' '+ str(self.min) + ' '+ str(self.max) +' '+ str(self.number_tuples) + ' ' + str(self.list_tuples)

    def __repr__(self):
        return  "Grid:" + str(self.pos) + " " + str(self.number_tuples)

    def __copy__(self):
        copy = Grid()
        copy.pos = self.pos[:]
        copy.min = self.min[:]
        copy.max = self.max[:]
        copy.number_tuples = self.number_tuples
        copy.list_tuples = self.list_tuples[:]
        return copy

    def add_tuple(self, tuples):
        self.number_tuples += len(tuples)
        self.list_tuples += tuples

    def getTupleBetween(self, rmin, rmax):
        res = []
        for p in self.list_tuples:
            boolean = True
            for i, val in enumerate(p):
                if rmin[i] > val or val > rmax[i]:
                    boolean = False
                    break
            if boolean:
                res.append(p)
        return res


def gbp(G, N):
    for g in G.grid_set:
        if g.number_tuples > 0:
            logging.debug("Doing grid " + str(g.number_tuples) + " at index i = " +
                        str([i for i in g.pos]) + " j = " + str([j for j in g.pos]))
            logging.debug("N = " + str(N))
            available = [i for i, x in enumerate(N) if len(x) == 0]
            if len(available) > 0:
                chosen = random.choice(available)
                N[chosen] = N[chosen] + [g]
            else:
                epsilon = sum([sum(grid.number_tuples for grid in alist) for alist in N])/len(N)
                logging.debug("Epsilon = " + str(epsilon))
                neighbours_g = set(G.find_neighbours(g))
                N_prime = [[]]*10

                for index, node in enumerate(N):
                    if sum(elem.number_tuples for elem in node) <= epsilon:
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
    logging.debug("Grid Allocation Done: " + str(N))
    return N


# Workload balancing on data nodes
def verify_theorem1(N):
    logging.debug("Verifying Theorem 1: each node is smaller than mg + |P|/|N|")
    P = sum([sum(n) for n in N])
    g = max(N, key=sum)
    mg = sum(g)
    len_N = len(N)
    good = True
    logging.debug("P = " + str(P) + " | g = " + str(g) + " | mg = " + str(mg) + " | len N = " + str(len_N))
    for node in N:
        if sum(node) >= mg + (P/len_N):
            logging.critical("Error: The node " + str(node) + " does not respect the Theorem 1")
            good = False
    if good: logging.info("Theorem 1 respected.")
    return good