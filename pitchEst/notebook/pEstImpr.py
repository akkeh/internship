import os, sys
import numpy as np
import math
import matplotlib.pyplot as plt

import essentia as ess
import essentia.standard as esstd

import pEstAssess as pa

def testImprovement(pool, newFunc, oldFunc='', M=100, newArgv='', oldArgv=''):
    names = np.append(pool['name'], '')
    pEsts = np.append(pool['lowLevel.pitch.median'], 0)
    pTags = np.append(pool['annotated_pitch'], 0)
    confs = np.append(pool['lowLevel.pitch_instantaneous_confidence.median'], 0);
    N = len(names)-1
   
    tag = np.zeros(M); oEst = np.zeros(M); iEst = np.zeros(M); 
    oConf = np.zeros(M); iConf = np.zeros(M); filenames = [];
    for m in range(M):
        i = np.random.randint(N)
        filename = names[i]
        print "file: "+filename
        loader = esstd.MonoLoader(filename = './sounds/all/'+filename);
        x = loader();
      
         
        try: 
            ip, ic = newFunc((x, newArgv))
            pTag = pTags[i]
            if oldFunc == '':
                pEst = pEsts[i] 
                oconf = confs[i]
            else:
                pEst, oconf = oldFunc((x, oldArgv));
                

            ipEst = np.median(ip)
            iconf = np.median(ic)

            tag[m] = pTag;
            oEst[m] = np.median(pEst);
            iEst[m] = ipEst;
            oConf[m] = np.median(oconf);
            iConf[m] = iconf;
            
            filenames.append(names[i])
        except:
            print "\nError loading: " + filename + '\n' 
        # remove sound from possible next sounds: 
        names = np.delete(names, i)
        pEsts = np.delete(pEsts, i)
        pTags = np.delete(pTags, i)
        confs = np.delete(confs, i)
        N = len(names)-1

    oErr = abs(tag - oEst)
    iErr = abs(tag - iEst)
   
    ost = pa.semitoneDist(tag, oEst)
    ist = pa.semitoneDist(tag, iEst)
 
    print "Improvement:\n\told mu: " + str(np.mean(abs(ost))) + " st\tnew mu: " + str(np.mean(abs(ist))) + " st"
    print "\tOctave errors:\n\t\told: " + str(len(np.where(pa.isOctErr(tag, oEst) != 0)[0])) + "\t\t\tnew: " + str(len(np.where(pa.isOctErr(tag, iEst) != 0)[0]))

    impr = "No"
    if np.mean(abs(ost)) > np.mean(abs(ist)):
        impr = "Yes"
    print '\nImporoved: ' + impr;
    return filenames, tag, oEst, iEst, oConf, iConf


def incResolution_pYinFFT(argv):
    '''
        In some noisy signals a higher resulotion in the spectrogram can 
            increase the difference between the noisefloor and the harmonics.
            -   check for oct error between pass 0 and pass N (if is oct err, choose pass 0?)
    '''    
    x = argv[0]
    passes = argv[1]

    M = 2048
    H = 1024
    
    x = trimAttack(x, M, H) 
    pitchs = []; confs = [];
    
    for pas in range(passes):
        pYin = esstd.PitchYinFFT(frameSize=M*(2**pas))
        win = esstd.Windowing(size=M*2**pas, type='blackmanharris62')
        spec = esstd.Spectrum(size=M*2**pas)

        ps = np.array([]); cs = np.array([]);
        for fr in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
            fr_zp = np.array(np.append(fr, np.zeros(len(fr) * (2**pas))), dtype='single')
            p, c = pYin(spec(win(fr_zp)))
            ps = np.append(ps, p);
            cs = np.append(cs, c);

        pitchs.append(ps)
        confs.append(cs)

    
    # choose
    # calc confidences:
    c_meds = np.array([])
    for conf in confs:
        c_meds = np.append(c_meds, np.median(conf))

    i = np.where(c_meds == max(c_meds))[0]    
    print "resolution: ", i, '\n\t', c_meds
    return np.median(pitchs[i]), c_meds[i]

def calcImprP(pool, pFunc, argv=''):
    names = np.append(pool['name'], '') 
    N = len(names)-1
    names = np.delete(names, N)
   
    i = 0 
    pitch_mu = np.array([], dtype='single'); conf_mu = np.array([], dtype='single'); 
    pitch_med = np.array([], dtype='single'); conf_med = np.array([], dtype='single'); 
    for filename in names:
        print "file: " + str(i) + "\t/\t" + str(N) + ":\t" + filename
        x = ESS_load('./sounds/all/' + filename)
        
        p, c = pFunc((x, argv))
        pitch_med = np.append(pitch_med, np.median(p));
        pitch_mu = np.append(pitch_mu, np.mean(p));
        conf_med = np.append(conf_med, np.median(c));
        conf_mu = np.append(conf_mu, np.mean(c));
    
        i += 1
    return pitch_med, conf_med, pitch_mu, conf_mu 

def ESS_load(fn):
    loader = esstd.MonoLoader(filename = fn)
    return loader() 

def trimSilence(x, M=2048, H=1024):
    StrtStop = esstd.StartStopSilence();
    start = 0; stop = len(x)
    for frame in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        start, stop = StrtStop(frame)
 
    if start-stop == 0:
        return trimSilence(normalise(x))
    else:
        return x[start*H:stop*H]
 
def noSilence_pYinFFT(argv):
    x = argv[0]
    M = 2048
    H = 1024
 
    StrtStop = esstd.StartStopSilence();
    pYin = esstd.PitchYinFFT(frameSize=M);
    win = esstd.Windowing(size=M, type='blackmanharris62');
    spec =  esstd.Spectrum();
   
    N = len(x)
    frameC = int(N/M)
    pitch = np.array([]); conf = np.array([]);

    for fc in esstd.FrameGenerator(x, frameSize = M, hopSize = H):
        p, c = pYin(spec(win(fc)))
        pitch = np.append(pitch, p);
        conf = np.append(conf, c);
        srtStp = StrtStop(fc)

    start, stop = srtStp;

    pitch = pitch[start:stop];
    conf = conf[start:stop]
    return pitch, conf

def trimAttack(x, M, H):
    # instantiate algorithms:
    Env = esstd.Envelope();
    LogAttT = esstd.LogAttackTime();

    x = trimSilence(x, M, H) 
    env = Env(x)
    logattt = LogAttT(env)
       
    start_n = np.where(np.array(env * 1000, dtype=int) > 0)[0][0] 
    
    afterAtt = start_n + (10**logattt * 44100)
    x = x[int(afterAtt):]
    
    return x

def noAttack_pYinFFT(argv):
    x = argv[0]
    M = 2048
    H = 1024
    
    # instantiate algorithms:
    pYin = esstd.PitchYinFFT(frameSize=M)
    win = esstd.Windowing(size=M, type='blackmanharris62')
    spec = esstd.Spectrum();

    
    xtr = trimAttack(x, M, H)
    if len(xtr) > 0:
        x = xtr
    else:
        x = trimAttack(normalise(x), M, H)

    pitch = np.array([]); conf = np.array([])
    for fr in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        p, c = pYin(spec(win(fr)))
    
        pitch = np.append(pitch, p);
        conf = np.append(conf, c);
    return pitch, conf

def normalise(x):
    return x / float(np.max(abs(x)))

def removeFromPool(old_pool, strt, end, term=''):
    pool = ess.Pool()
    filenames = old_pool['name']
    
    dnames = old_pool.descriptorNames()
    for dname in dnames:
        print "Name: "+dname
        vals = old_pool[dname]
        if type(vals[0]) != type("test"):    
            for i in range(strt):
                pool.add(dname, vals[i])
    
            if term != '':
                for i in range(strt, end):
                    if filenames[i][0].find(term) == -1:
                        pool.add(dname, vals[i])
                

            for i in range(end, len(vals)):
                pool.add(dname, vals[i])
        else:
            pool.add(dname, vals);
    return pool

def loadData():
    try:
        dataIn = esstd.YamlInput(filename='./results/descriptors_nomods.json')
        pool = dataIn();
    except:
        calcAll()
        pool = dataIn();
    return pool


