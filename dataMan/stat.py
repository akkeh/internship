import numpy as np
import matplotlib.pyplot as plt


def n_lt_th(x, th):
    if str(type(x)).find('array') > -1:
        N = len(th)
        y = np.zeros(N)
        for n in range(N):
            y[n] = len(np.where(x < th[n])[0])
    else:
        y = len(np.where(x < th)[0])
    return y

def perc_lt_th(x, th):
    return n_lt_th(x, th) / float(len(x))



