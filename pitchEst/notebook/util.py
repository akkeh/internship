import numpy as np

def normalise(x):
    if np.max(abs(x)) > 0:
        return x / np.max(abs(x))
    else:
        return x

def freq2midi(freq, fref=440.):
    return np.trunc(np.log2(freq / float(fref)) * 12 + 49)
