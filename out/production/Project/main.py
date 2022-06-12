import numpy as np

from GridAllocation import GridSet, verify_theorem1, gbp
from LOF import dis

if __name__ == "__main__":
    # gridSet = GridSet(np.array([[10, 11, 7, 10],
    #                             [6, 6, 4, 6],
    #                             [4, 10, 9, 9],
    #                             [8, 5, 8, 7]]))
    gridSet = GridSet(np.array([[10, 6, 4, 8],
                                [11, 6, 10, 5],
                                [7, 4, 9, 8],
                                [10, 6, 9, 7]]))

    datanode = [[]] * 10
    new_N = gbp(gridSet, datanode)
    verify_theorem1(new_N)
    print("plop =", dis([4, 0], [6, 6]))
