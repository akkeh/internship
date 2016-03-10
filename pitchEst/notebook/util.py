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
