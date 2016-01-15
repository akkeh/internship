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

def essPitchAnalysis(filename, window):
    pYin = esstd.PitchYinFFT()  # pitch estimation algorithm
    pSal = esstd.PitchSalience()    # pitch salience
    if window != 'none':
        win = esstd.Windowing(type=window)    # pitch salience
    # load audiofile:
    loader = esstd.MonoLoader(filename = filename)
    x = loader();
    N = len(x)
    if N / 2 != N / 2.:
        x = ess.array(np.append(x, np.zeros(1)))
    
    # get spectrum:
    spec = esstd.Spectrum()
    X = spec(x)

    if window != 'none':
        X = win(X)

    # calculate pitch:
    pitch, conf = pYin(X)
    sal = pSal(X)
    return pitch, conf, sal

