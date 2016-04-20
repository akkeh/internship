#! /usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt
import os, sys

import essentia as ess
import essentia.standard as esstd

import util as ut

def get_pitch_track(pool, i, dirname='./sounds/data/'):
    filename = pool['file'][i]
    
    pYin = esstd.PitchYinFFT();
    win = esstd.Windowing()
    spec = esstd.Spectrum();
    loader = esstd.MonoLoader(filename=dirname+filename)        
    x = ut.trimSilence(loader())
    
    pitch = []; conf = [];
    for frame in esstd.FrameGenerator(x, frameSize=2048, hopSize=1024):
        X = spec(win(frame))
        p, c = pYin(X)
        pitch.append(p);
        conf.append(c);
    
    pTag = np.zeros(len(pitch))
    pTag[:] = pool['mTag'][i]
    return ut.freq2midi(np.array(pitch)), pTag


def ERBBand_estPitch(pool, i, bands=40, dirname='./sounds/data/'):
    ERB = esstd.ERBBands(inputSize=1025, numberBands=bands);
    win = esstd.Windowing()
    spec = esstd.Spectrum();
    filename = pool['file'][i]
    loader = esstd.MonoLoader(filename=dirname+filename)        
    x = ut.trimSilence(loader())
    
    y = np.zeros(bands)
    est = np.zeros(bands)
    for frame in esstd.FrameGenerator(x, frameSize=2048, hopSize=1024):
        X = spec(win(frame))
        y += ERB(X)
    est = ERB(spec(win(np.array(np.sin(2.0*np.pi * ut.midi2freq(pool['mTag'][i]) * np.arange(2048)/ 44100.), dtype='single'))))

    est = ut.normalise(est)
    y = ut.normalise(y)

    return est, y
#est, y = ERBBand_estPitch(pool2, i); plt.plot(est); plt.plot(y); print 'n', i, octErr[i], mTag[i]-mEst[i], np.sum(y*est)

def peak_index(x):
    for i in np.arange(len(x)-2) + 1:
        if x[i-1] < x[i] and x[i] > x[i+1]:
            return i
    return -99 

def ERBvalTest(pool, bands=40, dirname='./sounds/data/'):
    files = pool['file']
    N = len(files)
    i = 0
    for fn in files:
        print "%d / %d:\t %s" % (i, N, fn)
        est, y = ERBBand_estPitch(pool, i, bands, dirname)
        pool.add('subOctval', np.sum(est*y))
        
        pool.add('superOctval', np.mean(y[:peak_index(est)]))
        
        i+=1
        

    return pool

def ERBEST(pool, i, bands=40, dirname='./sounds/data/'):
    est, y = ERBBand_estPitch(pool, i, bands, dirname)
    
    
    if np.sum(est*y) > 1E-3:    # check for sub_octave_error
        print "no sub oct"
        # find peak in est
        ind = peak_index(est)
        # check mean of values of y with index < peak index
        if np.mean(ut.normalise(y)[:ind]) > 0.04:
            print "super octave error"        
    else:
        print "sub octave? (octerr < 0)"
        plt.plot(est); plt.plot(y)
        


def get_mTag(nn):
    if nn[0] != 'M':
        return -99
    midi = int(nn[2])
    if nn[1] == '-':
        return midi * -1
    else:
        return midi + (10 * int(nn[1]));
    

def estPitches(dirname):
    files = os.listdir(dirname)
    print "found %s files" % len(files)

    # init algorithms
    pYin = esstd.PitchYinFFT();
    win = esstd.Windowing()
    spec = esstd.Spectrum();
    
    mEst = np.zeros(len(files)); confs = np.zeros(len(files));
    mTag = np.zeros(len(files));

    i = 0
    for fn in files:
        print fn
        # estimate pitch:
        try:
            loader = esstd.MonoLoader(filename=dirname+fn)        
            x = ut.trimSilence(loader())
            
        
            pitch = []; conf = [];
            for frame in esstd.FrameGenerator(x, frameSize=2048, hopSize=1024):
                X = spec(win(frame))
                p, c = pYin(X)
                pitch.append(p);
                conf.append(c);
                
            mEst[i] = ut.freq2midi(np.median(pitch))
            confs[i] = np.median(conf)
        except:
            print "error processing file: %s" % fn
            mEst[i] = -99
            confs[i] = 0
        # get annotated pitch:
        mTag[i] = get_mTag(fn[:3])
        
        i+=1
    return files, mTag, mEst, confs

def read_from_file(fn):
    inputFile = esstd.YamlInput(filename=fn)
    return inputFile()

def write_to_pool(files, mTag, mEst, confs, octErr='', fn=''):
    pool = ess.Pool()
    for i in range(len(mTag)):
        pool.add('file', files[i])
        pool.add('mTag', mTag[i])
        pool.add('mEst', mEst[i])
        pool.add('conf', confs[i])
        if octErr != '':
            pool.add('octErr', octErr[i])
    if fn != '':
        esstd.YamlOutput(filename=fn, format='json')(pool)

    return pool
   

def findOctErr(pool):
    mTag = pool['mTag']
    mEst = pool['mEst']

    octErr = np.zeros(len(mEst))

    for tag, est, i in zip(mTag, mEst, np.arange(len(mEst))):
        err = (tag - np.round(est)) 
        if err != 0.0:
            if err % 12 == 0:
                octErr[i] = err

    return octErr
           
def writeOcts(pool):
    mTag = pool['mTag']
    mEst = pool['mEst']

    octTag = np.zeros(len(mTag)) 
    octEst = np.zeros(len(mEst))
    octTag = np.floor((mTag - 4) / 12)
    octEst = np.floor((mEst - 4) / 12)
    
    return octTag, octEst

def removeFailed(pool):
    indexes = [];
    i = 0;
    for c in pool['conf']:
        if c == 0:
            indexes.append(i)
        i+=1 
    
    pool2 = ess.Pool()
    for dname in pool.descriptorNames():
        arr = np.delete(pool[dname], indexes)
        for val in arr:
            pool2.add(dname, val)

    return pool2
        
