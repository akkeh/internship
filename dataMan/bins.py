import sys
import numpy as np
import matplotlib.pyplot as plt
import math


def binData(data, bw):
    # assume symmetry around 0:
    xmin = min(data)
    xmax = max(data)
    if abs(xmin) > xmax:
        binCount =  math.ceil(abs(xmin / float(bw)))
    else:
        binCount = math.ceil(abs(xmax / float(bw)))

    y = np.zeros(binCount * 2 + 1)
    x = np.arange(-binCount, binCount + 1)
    for val in data:
        y[math.floor((val + (bw / 2.0)) / float(bw)) + binCount] += 1
    return x, y

    
