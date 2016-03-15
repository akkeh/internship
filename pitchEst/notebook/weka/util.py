import numpy as np

import essentia as ess
import essentia.standard as esstd

def normalise(x):
    if type(x) == list:
        x = np.array(x)
    if np.max(abs(x)) > 0:
        return x / float(np.max(abs(x)))
    else:
        return x

def freq2midi(freq, fref=440.):
    x = np.float64(freq)
    return np.log2(x / float(fref)) * 12 + 49

def midi2freq(midi, fref=440.):
    x = np.float64(midi)
    return 2**((x - 49) / 12.) * fref


