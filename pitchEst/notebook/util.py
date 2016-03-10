import numpy as np

def normalise(x):
    if type(x) == list:
        x = np.array(x)
    if np.max(abs(x)) > 0:
        return x / float(np.max(abs(x)))
    else:
        return x

def freq2midi(freq, fref=440.):
    return np.log2(freq / float(fref)) * 12 + 49

def midi2freq(midi, fref=440.):
    return 2**((midi - 49) / 12.) * fref
