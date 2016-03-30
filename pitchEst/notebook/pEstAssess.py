import numpy as np
import matplotlib.pyplot as plt

import essentia as ess
import essentia.standard as esstd

import util as ut

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
   

def predictContainer(pr, ev, ev_th=1, res=100.):
    pr = abs(pr)
    ev = abs(ev)
    
    best_score = 0
    best_th = 0
    best_mode = 'normal'
    for pr_th in np.arange(min(pr), max(pr), (max(pr)-min(pr)) / float(res)):
        tP, tN, fP, fN = predict(pr, ev, pr_th=pr_th, ev_th=ev_th, invPred=False)
        score = len(tP) + len(tN)
        if score > best_score:
            best_score = score
            best_th = pr_th
            best_mode = 'normal'
        tP, tN, fP, fN = predict(pr, ev, pr_th=-pr_th, ev_th=ev_th, invPred=True)
        score = len(tP) + len(tN)
        if score > best_score:
            best_score = score
            best_th = pr_th
            best_mode = 'inverse'
    
    return best_score, best_mode, best_th

def predict(pr, ev, pr_th=-999, ev_th = -999, plot=0, invEval=False, invPred=False):
    pr = abs(pr)    # predictor
    ev = abs(ev)    # evaluator

    if invEval == True:
        ev = -ev

    if invPred == True:
        pr = -pr

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
        plt.plot([pr_mu * 0.9999999, pr_mu, pr_mu * 1.000000001], [0, max(ev), 0], label='pr. bnd')
        plt.plot([min(pr), max(pr)], [np.mean(ev), np.mean(ev)], label='ev. bnd')
        plt.plot(pr[tP], ev[tP], '.', label='tP')
        plt.plot(pr[tN], ev[tN], '.', label='tN')
        plt.plot(pr[fP], ev[fP], '.', label='fP')
        plt.plot(pr[fN], ev[fN], '.', label='fN')
        
        plt.legend( loc='upper left', numpoints = 1 )
    return tP, tN, fP, fN


def isOctErr(pTag, pEst):
    stDist = semitoneDist(pTag, pEst)
   
    ind = np.where(np.round(abs(stDist)) % 12 == 0)
    
    y = np.zeros(len(stDist))
    for i in ind[0]:
        if int(stDist[i]) != 0:
            y[i] = np.round(stDist[i])
    return y
    

def searchPredictor(pool, pestimation):
    
    pTag = pool['annotated_pitch']
    pEst = pool[pestimation]
    st = semitoneDist(pTag, pEst)
    N = len(st)
    scores = [];
    for descrname in pool.descriptorNames():
        print descrname
        descr = pool[descrname]
        if type(descr[0]) != list:
            if len(descr.shape) == 1:
                succes = np.zeros(4);
                tP, tN, fP, fN = predict(descr, st)
                succes[0] = (len(tP) + len(tN)) / float(N);
         
                tP, tN, fP, fN = predict(descr, st, invPred=True); 
                succes[1] = (len(tP) + len(tN)) / float(N);

                tP, tN, fP, fN = predict(descr, st, invEval=True); 
                succes[2] = (len(tP) + len(tN)) / float(N);

                tP, tN, fP, fN = predict(descr, st, invPred=True, invEval=True); 
                succes[3] = (len(tP) + len(tN)) / float(N);

                scores.append(succes[np.where(succes == max(succes))[0][0]]);

    return scores;

# regression:
def linreg(pool, pestimation='lowLevel.pitch.median'):
    pTag = pool['annotated_pitch']
    pEst = pool[pestimation]
    
    st = abs(semitoneDist(pTag, pEst))
    
    names = pool.descriptorNames()
    errors = np.array([])
    coeffa = np.array([])
    coeffb = np.array([])

    for dname in names:
        descr = pool[dname]
        if type(descr[0]) != list:
            if len(descr.shape) == 1:   # $TODO: barkbands
                x = np.array([descr, np.ones(len(descr))])
                w = np.linalg.lstsq(x.T, st)
                a = w[0][0]
                b = w[0][1]
                
                errors = np.append(errors, np.sum(((a*x + b)-st)**2))
                coeffa = np.append(coeffa, a)
                coeffb = np.append(coeffb, b)
    return errors, coeffa, coeffb 



def getOctErrIndexes(pTag, pEst):
    midiTag = ut.freq2midi(pTag); midiEst = ut.freq2midi(pEst);
    st = midiTag - midiEst
    i_err = np.where(abs(st) > 1)[0];
    x = np.log2(pEst[i_err] / pTag[i_err]);

    frqs, lbounds = np.histogram(x, range=(-max(-x), max(-x)), bins=16*np.round(max(-x)) + 1); bw = lbounds[3]-lbounds[2];

    # octave errors:
    i_octErrEdges = list();
    t_octErrBins = list();
    for i in range(1, 9): 
        val = np.log2(i);
        i_sup = 0; i_sub = 0 
        for lbound in lbounds:
            if lbound < -val:
                i_sub += 1
            if lbound < val:
                i_sup += 1
        i_octErrEdges.append((lbounds[i_sub-1], lbounds[i_sub]))
        i_octErrEdges.append((lbounds[i_sup-1], lbounds[i_sup]))
        t_octErrBins.append(val)
        t_octErrBins.append(val)
        
    i_octErr = list();
    t_octErr = list();
    k = 0 
    for binEdges in i_octErrEdges:
        i = 0;
        for val in x:
            if val > binEdges[0] and val < binEdges[1]:
                i_octErr.append(i)
                mul = 1 
                if pEst[i] < pTag[i]:
                    mul = -1
                t_octErr.append((mul*t_octErrBins[k]))
            i+=1
        k += 1
    i_octErr = i_err[i_octErr];


    st_err = st[i_err];
    return i_octErr, t_octErr


def correctFrames_container(pool):
    pTag = pool['annotated.pitch']
    names = pool['name']

    pool2 = ess.Pool()
    i=0
    for name in names:
        loader = esstd.MonoLoader(filename='./sounds/all/'+name[0])
        results = correctFrames(loader(), pTag[i])
        for res in results:
            pool2.add(res[0], res[1])
        i+=1
    return pool2

def correctFrames(x, pTag, M=2048, H=1024):
    win = esstd.Windowing(type='blackmanharris62', zeroPadding=0);
    spec = esstd.Spectrum(); 
    pYin = esstd.PitchYinFFT(frameSize=M);

    mTag = ut.freq2midi(pTag)
    c_corr = np.array([]); c_wrong = np.array([])
    for frame in esstd.FrameGenerator(ut.normalise(x), frameSize=M, hopSize=H):
        p, c = pYin(spec(win(frame)))
        
        m = ut.freq2midi(p)
        if abs(m - mTag) >= 1:
            c_wrong = np.append(c_wrong, c)
        else:
            c_corr = np.append(c_corr, c)
    return ('confidence.correct', np.median(c_corr)), ('confidence.wrong', np.median(c_wrong))
        
