import logging
import random
import numpy as np
import math


def test_uniform(size=100, err=2, num_outlier=5, dimensions = 2):
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

def normalize_xyz(x, y, z):
    xmax = max(x)
    ymax = max(y)
    zmax = max(z)
    x2 = [float(i)/xmax for i in x]
    y2 = [float(i)/ymax for i in y]
    z2 = [float(i) / zmax for i in z]

    return x2, y2, z2

def merge_xy(x, y):
    return [(x[i],y[i]) for i in range(len(x))]


def test_uniform3(size=100, err=2, num_outlier=5):
    x = np.arange(size)
    delta = np.random.uniform(-err, err, size=(size,))
    y = np.abs(0.4 * x + 3 + delta)
    z = np.abs(0.2 * x + 4 + delta)

    x, y, z = normalize_xyz(x, y, z)

    for _ in range(num_outlier):
        x.append(random.random())
        y.append(random.random())
        z.append(random.random())

    data = merge_xyz(x, y, z)
    return data

def merge_xyz(x, y, z):
    return [(x[i],y[i], z[i]) for i in range(len(x))]

def generate_data_new(size=100, err=2, num_outlier=5, dim = 2):
    err = err*size/100
    data = []
    for n in range(size):
        data.append([])
        for _d in range(dim):
            delta = np.random.uniform(-err, err, size=(1,))[0]
            data[-1].append((n+delta))
    for _n in range(num_outlier):
        data.append([])
        for _d in range(dim):
            data[-1].append(random.randint(0, size))
    return data

def generate_data(size=100, err=2, num_outlier=5, dim = 2):
    dimensions = [None]*dim
    dimensions[0] = np.arange(size)
    delta = np.random.uniform(-err, err, size=(size,))
    for otherdim in range(len(dimensions)):
        if otherdim != 0:
            dimensions[otherdim] = np.abs(np.random.rand() * dimensions[0] + np.random.randint(0, 6) + delta)

    normalized = normalize(dimensions)

    for i in range(len(normalized)):
        for _ in range(num_outlier):
            normalized[i].append(random.random())

    return merge(normalized)


def normalize(dimensions):
    data = []
    for dim in dimensions:
        maxi = max(dim)
        data.append([float(i)/maxi for i in dim])
    return data

def merge(data):
    # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    sol = []
    for i in range(len(data[0])):
        sol.append([])
        for d in range(len(data)):
            sol[-1].append(data[d][i])

    return sol