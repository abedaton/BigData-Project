import logging
import random
import numpy as np
import math


def test_uniform(size=100, err=2, num_outlier=5):
    x = np.arange(size)
    delta = np.random.uniform(-err, err, size=(size,))
    y = np.abs(0.4 * x + 3 + delta)

    x, y = normalize_xy(x, y)

    for _ in range(num_outlier):
        x.append(random.random())
        y.append(random.random())

    data = merge_xy(x, y)
    return data


def generate_cluster(size=100, number_cluster=5, err=2, num_outlier=10):
    x = np.array([])
    y = np.array([])
    for _ in range(number_cluster):
        i = random.random()
        j = random.random()
        for _ in range(size//number_cluster):
            delta = random.random()/10
            x = np.append(x, np.abs(i + delta))
            delta = random.random()/10
            y = np.append(y, np.abs(j + delta))
    for _ in range(num_outlier):
        x = np.append(x, random.random())
        y = np.append(y, random.random())
    data = merge_xy(x, y)
    logging.debug(str(data))
    return data


def generate_circle(size=100, radius=1, num_outlier=5):
    x = []
    y = []
    centerX = 0
    centerY = 0+radius/2
    r = radius * math.sqrt(random.random())
    for n in range(size):
        theta = random.random()*2*math.pi
        x.append(centerX + r * math.cos(theta))
        y.append(centerY + r * math.sin(theta))

    x, y = normalize_xy(x, y)

    for _ in range(num_outlier):
        x.append(random.random())
        y.append(random.random())

    data = merge_xy(x, y)
    return data


def normalize_xy(x, y):
    xmax = max(x)
    ymax = max(y)
    x2 = [float(i)/xmax for i in x]
    y2 = [float(i)/ymax for i in y]

    return x2, y2


def merge_xy(x, y):
    return [(x[i],y[i]) for i in range(len(x))]


# -------------------------------------------------------------------

# def generate_rand(median=100, err=12, outlier_err=100, size=80, outlier_size=10):
#     errs = err * np.random.rand(size) * np.random.choice((-1, 1), size)
#     data = median + errs
#
#     lower_errs = outlier_err * np.random.rand(outlier_size)
#     lower_outliers = median - err - lower_errs
#
#     upper_errs = outlier_err * np.random.rand(outlier_size)
#     upper_outliers = median + err + upper_errs
#
#     data = np.concatenate((data, lower_outliers, upper_outliers))
#     np.random.shuffle(data)
#
#     return data

# def merge_coordinates(x, y):
#     if len(x) == len(y):
#         data = []
#         for i in range(len(x)):
#             data.append([x[i], y[i]])
#         return data
#     else:
#         print("X and Y must have the same length")
#         return None