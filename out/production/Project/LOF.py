import numpy as np


# In a grid P * d the distance between to line of P is:
def dis(p, q):  # were p and q are two line of the grid
    d = np.size(p)
    res = 0
    for i in range(d):
        res += (p[i] - q[i]) ** 2
    return np.sqrt(res)