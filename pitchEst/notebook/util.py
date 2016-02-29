import numpy as np


def freq2midi(freq, fref=440.):
    return np.trunc(np.log2(freq / float(fref)) * 12 + 49)
