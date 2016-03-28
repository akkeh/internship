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
    return (np.log2(np.float64(freq) / np.float64(fref)) * 12.) + 49

def midi2freq(midi, fref=440.):
    return 2**((np.float64(midi) - 49) / 12.) * fref

def remove_overlap(a, b):
    '''
        returns a without overlapping elements from b
    '''
    i = 0
    i_double = np.array([])
    for aval in a:
        for bval in b:
            if aval == bval:
                i_double = np.append(i_double, i);
        i+=1

    return np.delete(a, i_double)
    

def trimSilence(x, M=2048, H=1024):
    StrtStop = esstd.StartStopSilence();
    start = 0; stop = len(x)
    for frame in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        start, stop = StrtStop(frame)

    if start-stop == 0:
        return trimSilence(normalise(x))
    else:
        return x[start*H:stop*H]

def trimAttack(x, M=2048, H=1024):
    # instantiate algorithms:
    Env = esstd.Envelope();
    LogAttT = esstd.LogAttackTime();

    '''
    x_trimmed = trimSilence(x, M, H)
    if len(x_trimmed) / float(len(x)) * 100 < 1:
        x = trimSilence(normalise(x), M, H)
    else:
        x = x_trimmed
    '''
    env = Env(x)
    logattt = LogAttT(env)
    start_n = np.where(np.array(env * 1000, dtype=int) > 0)[0][0]
    afterAtt = start_n + (10**logattt * 44100)

    x = x[int(afterAtt):]
    return x
