import numpy as np

import essentia as ess
import essentia.standard as esstd

def zeropad(x, Ny):
    N = len(x)
    if N > Ny:
        return x[:Ny]
    elif N < Ny:
        return np.append(x, np.zeros(Ny-N))
    else:
        return x

pYin = esstd.PitchYinFFT()  # pitch extimation algorithm
def essPitchAnalysis(filename):
    # load audiofile:
    loader = esstd.MonoLoader(filename = filename)
    x = loader();
    N = len(x)
    if N / 2 != N / 2.:
        x = ess.array(np.append(x, np.zeros(1)))
    
    # get spectrum:
    spec = esstd.Spectrum()
    X = spec(x)

    # calculate pitch:
    pitch, conf = pYin(X)

    return pitch, conf
