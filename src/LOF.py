import numpy as np
import bisect
from GridAllocation import *

"""The distance between tuples p and q"""
def dis(p, q):
    d = len(p)
    res = 0
    for i in range(d):
        res += (p[i] - q[i]) ** 2
    return np.sqrt(res)

"""For a given parameter k, the reachability distance of a tuple p w.r.t. o is"""
def k_distance(k, p, grid):
    list_distance = []
    for q in grid.list_tuples:
        if p != q:
            bisect.insort(list_distance, dis(p, q))
    if len(list_distance) > k:
        return list_distance[k-1]
    else:
        return (grid.max[0]-grid.min[0])/2


def realDistanceK(k, o, grid):
    for i, p in enumerate(grid):
        if  p != o:
            dpo = dis(p, o)
            countA = 0
            countB = 0
            for j, q in enumerate(grid):
                if q != p and q != o:
                    if dis(q, o) <= dpo:   #  (a)
                        countA += 1
                        for l, q_prime in enumerate(grid):
                            if q != q_prime and q_prime != o and q_prime != p:
                                if dis(q_prime, o) < dpo:   #  (b)
                                    countB += 1
            countB = (countB/countA) if countA != 0 else 0
            if float(countA) >= float(k) and float(countB) <= float(k-1):
                return p
    return None


"""
Given a positive integer k, the k-distance neighborhood of a tuple o is the set of tuples whose distances from o
are smaller than or equal to the k-distance of o
"""
def neighK(k, o, grid):
    distance = k_distance(k, o, grid)
    neighbours = []
    for q in grid.list_tuples:
        if o != q and dis(o, q) <= distance:
            neighbours.append(q)
    return neighbours


def reachability_distance(k, p, o, grid):
    return max([k_distance(k, p, grid), dis(p, o)])


# For a given parameter k, the local reachability density of a tuple o is
def LRD(k, o, grid, neighbours):
    sub = 0
    for p in neighbours:
        sub += reachability_distance(k, p, o, grid)
    return len(neighbours)/sub


#Given an integer k, the local outlier factor of a tuple o is
def LOF(k, o, grid):
    neighbours = neighK(k, o, grid)
    if len(neighbours) == 0:
        return 2
    num = 0
    for p in neighbours:
        num += LRD(k, p, grid, neighbours)
    sub = len(neighbours) * LRD(k, o, grid, neighbours)
    return num / sub
