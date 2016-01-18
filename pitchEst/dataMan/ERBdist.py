import numpy as np
import matplotlib.pyplot as plt
import math

def ERB(fc):
    '''
    |   Calculate Equivalent Rectangular Bandwidth  |
    |       source:                                 |
    |   -   fc: center frequency                    |
    '''
    return 24.7 + (0.108 * fc)

def errERB(pTag_in, pEst_in):
    if str(type(pTag_in)).find('array') > -1:
        N = len(pTag_in)
        if N != len(pEst_in):
            return -1
    else:
        N = 1 
    y = np.zeros(N)
    for n in range(N):
        if N > 1:
            pTag = pTag_in[n]   
            pEst = pEst_in[n]   
        else:
            pTag = pTag_in
            pEst = pEst_in
        fc = pTag
        erb = ERB(fc)
        if pEst > pTag:
            while fc < pEst:
                fc = fc + ERB(fc) / 2.0
                y[n] += 1
        elif pEst < pTag:
            while fc > pEst:
                fc = fc - ERB(fc) / 2.0
                y[n] -= 1
    return y


