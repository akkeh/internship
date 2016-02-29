import os, sys
import numpy as np
import math
import matplotlib.pyplot as plt

import essentia as ess
import essentia.standard as esstd

import pEstAssess as pa

def descriptorTest(pool, dFunc, M=100, argv=''):
    names = np.append(pool['name'], '')
    pEsts = np.append(pool['lowLevel.pitch.median'], 0)
    pTags = np.append(pool['annotated_pitch'], 0)
    N = len(names)-1
   
    tag = np.zeros(M); oEst = np.zeros(M); dVals = np.zeros(M);
    for m in range(M):
        i = np.random.randint(N)
        filename = names[i]
        print "file: "+filename
        loader = esstd.MonoLoader(filename = './sounds/all/'+filename);
        x = loader();
        x = trimSilence(x)        
        dVal = dFunc((x, argv))
        
        
        pTag = pTags[i]
        pEst = pEsts[i] 

        tag[m] = pTag;
        oEst[m] = pEst;
        dVals[m] = dVal;
        # remove sound from possible next sounds: 
        names = np.delete(names, i)
        pEsts = np.delete(pEsts, i)
        pTags = np.delete(pTags, i)
        N = len(names)-1
        with open('log.txt', 'w') as lg:
            lg.write(filename+'\n')
    return tag, oEst, dVals

def calcDescriptor(pool, dFunc, argv=''):
    names = np.append(pool['name'], '')
    N = len(names)-1
    names = np.delete(names, N)
   
    i = 0 
    descr = np.array([])
    for filename in names:
        print "file: " + str(i) + "\t/\t" + str(N) + ":\t" + filename
        x = ESS_load('./sounds/all/' + filename)
        x = trimSilence(x)
        if len(x) == 0:
            descr = np.append(descr, 0)
        else: 
            descr = np.append(descr, np.median(dFunc((x, argv))))
        
        i += 1
    return descr

def percentageOfSignal(argv):
    x = argv[0]
    x_eff = trimSilence(x)
    
    return len(x_eff) / float(len(x)) * 100

def trimSilence(x, M=2048, H=1024):
    StrtStop = esstd.StartStopSilence();
    start = 0; stop = len(x)
    for frame in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        start, stop = StrtStop(frame)

    return x[start*H:stop*H]

def ESS_load(fn):
    loader = esstd.MonoLoader(filename = fn)
    return loader()

def addToPool(pool, name, x):
    for val in x:
        pool.add(name, val)
    return pool

def inharmonicity(argv):
    x = argv[0]
    M = 2048
    H = 1024

    if len(x) / 2 != len(x) / 2.:   
        x = np.array(np.append(x, 0), dtype='single'); 
    spec = esstd.Spectrum(size=M)
    win = esstd.Windowing();
    specP = esstd.SpectralPeaks()
    pYin = esstd.PitchYinFFT()
    harmP = esstd.HarmonicPeaks()
    
    inharm = esstd.Inharmonicity();
    inh = np.array([])
    i = 0
    for frame in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        print '\t' + str(i) + '\t/\t' + str(len(x) / H)
        X = spec(win(x))
        pitch, conf = pYin(X)
        fSP, mSP = specP(X)
        fHP, mHP = harmP(fSP[1:], mSP[1:], pitch)
        inh = np.append(inh, inharm(fHP, mHP))
        i += 1
    
    return np.median(inh)
        
def essExtractor(dirname):
    Extr = esstd.Extractor(rhythm=False);
    # list files:
    filenames = [];
    pTag = [];
    print "listing files"
    with open('./results/' + dirname.split('/')[-2] + '_ESS.txt') as f:
        f.readline()    # skip first line
        line = f.readline();
        while line != '':
            filenames.append(line.split('\t')[0].split('/')[-1])
            pTag.append(float(line.split('\t')[4]));  
            line = f.readline();
    print "calculating descriptors"
    pool = ess.Pool()
    N = len(filenames);
    n = 0
    for filename in filenames:
        print "file: " + str(n+1) + " of " + str(N)
        # load the audio:
        loader = esstd.MonoLoader(filename = dirname+filename)
        x = loader();
        extr = Extr(x);
        extr.add('name', filename)
        extr.set('annotated_pitch', pTag[n])
        aExtr = esstd.PoolAggregator(defaultStats = ['mean', 'median' ])(extr)
        for dName in aExtr.descriptorNames():
            pool.add(dName, aExtr[dName])   
        n += 1
    return pool


def calcAll(test=0):
    pool = False
    dirs = [ 'carlos/', 'good-sounds/', 'modularsamples/', 'philharmonia/', 'iowa/' ] 
    if test != 0:
        dirs = ['carlos/']
    for dirname in dirs:
        if pool:
            pool.merge(essExtractor('./sounds/'+dirname), 'append')
        else:
            pool = essExtractor('./sounds/'+dirname);
        

    esstd.YamlOutput(filename = './results/descriptors.json', format='json')(pool)


def removeFromPool(old_pool, strt, end):
    pool = ess.Pool()
    
    names = old_pool.descriptorNames()
    for name in names:
        print "Name: "+name
        vals = old_pool[name]
        if type(vals) != type("test"):    
            for i in range(strt):
                pool.add(name, vals[i])
            for i in range(end, len(vals)):
                pool.add(name, vals[i])
        else:
            pool.add(name, vals);
    return pool

def loadData():
    try:
        dataIn = esstd.YamlInput(filename='./results/descriptors_nomods.json')
        pool = dataIn();
    except:
        calcAll()
        pool = dataIn();
    return pool



