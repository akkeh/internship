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
    if window != '' and window != 'none':
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

    if window != '' and window != 'none':
        X = win(X)

    # calculate pitch:
    pitch, conf = pYin(X)
    sal = pSal(X)
    return pitch, conf, sal

def essPitchAnalysis_rolling(filename, window, M):
    pYin = esstd.PitchYinFFT()  # pitch estimation algorithm
    pSal = esstd.PitchSalience()    # pitch salience
    if window != '' and window != 'none':
        win = esstd.Windowing(type=window)    # pitch salience
    # load audiofile:
    loader = esstd.MonoLoader(filename = filename)
    x = loader();
    N = len(x)
   
    spec = esstd.Spectrum();

    # frame sound:
    pitch = np.array([]);
    conf = np.array([]);
    sal = np.array([]);

    for m in range(int(N/M)):
        # get spectrum:
        X = spec(x[M*m: M*(m+1)])
                
        if window != '' and window != 'none':
            X = win(X)
        # calculate pitch:
        t_pitch, t_conf = pYin(X)
        pitch = np.append(pitch, t_pitch)
        conf = np.append(conf, t_conf)
        t_sal = pSal(X)
        sal = np.append(sal, t_sal);
        
    return np.mean(pitch), np.mean(conf), np.mean(sal)


