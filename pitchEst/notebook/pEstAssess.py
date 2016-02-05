import numpy as np
import matplotlib.pyplot as plt

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
   

def predict(pr, ev, pr_th=-999, ev_th = -999, plot=0):
    pr = abs(pr)    # predictor
    ev = abs(ev)    # evaluator
    pr_mu = np.mean(pr)
    ev_mu = np.mean(ev)

    if pr_th > 0:
        pr_mu = pr_th
    if ev_th > 0:
        ev_mu = ev_th    

    pos = np.where(ev < ev_mu)[0]  # get positives
    neg = np.where(ev >= ev_mu)[0] # get negatives

    tP = pos[np.where(pr[pos] > pr_mu)]
    tN = neg[np.where(pr[neg] <= pr_mu)]
    fP = pos[np.where(pr[pos] <= pr_mu)]
    fN = neg[np.where(pr[neg] > pr_mu)]
    

    if plot == 1:
        plt.plot(pr[tP], ev[tP], '.')
        plt.plot([pr_mu * 0.9999999, pr_mu, pr_mu * 1.000000001], [0, max(ev), 0])
        plt.plot([min(pr), max(pr)], [np.mean(ev), np.mean(ev)])
        plt.plot(pr[fN], ev[fN], '.')
        plt.plot(pr[tN], ev[tN], '.')
        plt.plot(pr[fP], ev[fP], '.')

    return tP, tN, fP, fN
def isOctErr(pTag, pEst):
    stDist = semitoneDist(pTag, pEst)
   
    ind = np.where(np.round(abs(stDist) % 12) == 0)
    
    y = np.zeros(len(stDist))
    for i in ind[0]:
        if int(stDist[i]) != 0:
            y[i] = int(stDist[i])
    return y
    

 
