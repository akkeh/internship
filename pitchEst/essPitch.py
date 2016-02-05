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

def essPitchAnalysis_rolling(filename, window, zp=0, M=2048, H=1024):
    # load audiofile:
    loader = esstd.MonoLoader(filename = filename)
    x = loader();
    N = len(x)
    
    # frame cutter
    fc = esstd.FrameCutter(frameSize=M, hopSize=H);
    
    # window:
    w = esstd.Windowing(type=window, zeroPadding=zp);

    # spectrum:
    spec = esstd.Spectrum();

    pYin = esstd.PitchYinFFT(frameSize=M);    

    pSal = esstd.PitchSalience()    # pitch salience

    # frame sound:
    pitch = np.array([]);
    conf = np.array([]);
    sal = np.array([]);

    for m in range(int((N-M)/H)):
        # get spectrum:
        frame = fc(x)
        mX = spec(w(frame))
        
        # calculate pitch:
        t_pitch, t_conf = pYin(mX)
        pitch = np.append(pitch, t_pitch)
        conf = np.append(conf, t_conf)
        t_sal = pSal(mX)
        sal = np.append(sal, t_sal);
        
    return np.mean(pitch), np.mean(conf), np.mean(sal)


