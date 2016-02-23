import os, sys
import numpy as np
import math
import matplotlib.pyplot as plt

import essentia as ess
import essentia.standard as esstd

import pEstAssess as pa

def testImprovement(pool, pFunc, M=1000, argv=''):
    names = np.append(pool['name'], '')
    N = len(names)
    
    for m in range(M):
        i = np.random.randint(N)
        filename = names[i]
        print "file: "+filename
        loader = esstd.MonoLoader(filename = './sounds/all/'+filename);
        x = loader();
        
        p, c, ip, ic = pFunc((x, argv))
        
        
        pTag = float(pool['annotated_pitch'][i])
        pEst = float(pool['lowLevel.pitch.median'][i])

        ipEst = np.median(ip)
        
        if np.median(p) != pEst:
            print "Different estimates:\t", np.median(p), '\t', pEst, '\n'
        # remove sound from possible next sounds: 
        names = np.delete(names, i)
        N = len(names)

def noSilence_pYinFFT(argv):
    x = argv[0]
    
    StrtStop = esstd.StartStopSilence();
    FC = esstd.FrameCutter(frameSize=2048, hopSize=1024);
    pYin = esstd.PitchYinFFT(frameSize=1024);
    
   
    frames = [];
    pitch = []; conf = [];

    fc = FC(x);
    while len(fc) > 0:
        frames.append(fc)
        fc = FC(x);
   
    for frame in frames:
        p, c = pYin(frame)
        pitch.append(p);
        conf.append(c);
        srtStp = StrtStop(frame)

    start, stop = srtStp;

    ns_pitch = pitch[start:stop];
    ns_conf = conf[start:stop]
    return pitch, conf, ns_pitch, ns_conf

def improvePitch(dirname):
    # list files:
    filenames = [];
    print "listing files"
    with open('./results/' + dirname.split('/')[-2] + '_ESS.txt') as f:
        f.readline()    # skip first line
        line = f.readline();
        while line != '':
            filenames.append(line.split('\t')[0].split('/')[-1])
            line = f.readline();
    pool = ess.Pool()

    for filename in filenames:
        print "file: " + filename
        loader = esstd.MonoLoader(filename = dirname+filename);
        x = loader();
        return x
        t_pool = ess.Pool()
        pitch, conf = noSilence_pYinFFT(x)
        t_pool.add('name', filename);
        t_pool.add('noSilence.pitch.mean', np.mean(pitch));
        t_pool.add('noSilence.pitch.median', np.median(pitch));
        t_pool.add('noSilence.conf.mean', np.mean(conf));
        t_pool.add('noSilence.conf.median', np.median(conf));
        
        for dName in t_pool.descriptorNames():
            pool.add(dName, t_pool[dName])
        
    return pool        

def essExtractor(dirname):
    Extr = esstd.Extractor(rhythm=False, midLevel=False);
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


def loadData():
    try:
        dataIn = esstd.YamlInput(filename='./results/descriptors.json')
        pool = dataIn();
    except:
        calcAll()
        pool = dataIn();
    return pool

