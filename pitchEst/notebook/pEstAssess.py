import numpy as np

def ERB(fc):
    return 24.7 + (0.108 * fc)

def ERBdist(pTag, pEst):
    if str(type(pTag)).find('array') > -1:
        N = len(pTag)
        if N != len(pEst):
            return nan
    else:
        N = 1
    y = np.zeros(N)
    for n in range(N):
        if N > 1:
            tag = pTag[n];
            est = pEst[n];
        else:
            tag = pTag
            est = pEst;
        fc = tag
        erb = ERB(tag)  # get equivalent rectangluar bandwidth
    
        if est > tag:
            while fc < est:
                fc = fc + ERB(fc) / 2.
                y[n] +=1
        elif est < tag:
            while fc > est:
                fc = fc - ERB(fc) / 2.
                y[n] -= 1
    return y


def semitoneDist(pTag, pEst):
    if str(type(pTag)).find('array') > -1:
        N = len(pTag)
        if N != len(pEst):
            return nan
    else:
        N = 1
    y = np.zeros(N)
    for n in range(N):
        if N > 1:
            tag = pTag[n];
            est = pEst[n];
        else:
            tag = pTag;
            est = pEst;
        y[n] = np.log2(est / float(tag)) * 12.
    
    return y
   

def isOctErr(pTag, pEst):
    stDist = semitoneDist(pTag, pEst)
   
    ind = np.where(np.round(abs(stDist) % 12) == 0)
    
    y = np.zeros(len(stDist))
    for i in ind[0]:
        if int(stDist[i]) != 0:
            y[i] = int(stDist[i])
    return y
     
