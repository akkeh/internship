import numpy as np
import json

import essentia as ess

import util as ut

def copyPool(pool):
    cpool = ess.Pool()
    for dname in pool.descriptorNames():
        try:
            cpool.add(dname, pool[dname])
        except:
            for val in pool[dname]:
                cpool.add(dname, val)

    return cpool

def stErr(pTag, pEst):
    mTag = ut.freq2midi(pTag)
    mEst = ut.freq2midi(pEst)
    st = abs(mTag - mEst)
    if st > 1:
        return 'wrong'
    else:
        return 'correct'

def essentia_to_ARFF(pool, arffFile, classes=['correct', 'wrong']):
    '''
    -   Assumes 'name' to be 'relation' field
    '''
    
    sounds = pool['name']   # get relations

    # get attributes
    dnames = pool.descriptorNames();

    pTag = pool['annotated.pitch']; pEst = pool['lowLevel.pitch.median']
    with open(arffFile, 'w') as arff:
        arff.write('@RELATION sounds\n')

        descrs = list()        
        for d in dnames:
            if d != 'name' and d != 'class' and d.find('tonal.') == -1:
                if len(np.shape(pool[d])) == 1:
                    if len(pool[d]) == len(sounds):
                        arff.write('@ATTRIBUTE '+str(d)+'\tNUMERIC\n')
                        descrs.append(d)
                elif len(np.shape(pool[d][0])) > 1:
                    if len(pool[d][0]) == len(sounds):
                        arff.write('@ATTRIBUTE '+str(d)+'\tNUMERIC\n')
                        descrs.append(d)
    
        arff.write('@ATTRIBUTE class\t{correct, wrong}\n\n')  # 0: correct, 1: wrong
 
        arff.write('@DATA\n')
        # iterate over sounds:
        for snd in range(len(sounds)):
            print "Sound\t%d\tof %d" % (snd, len(sounds))
            line = ''
            for d in descrs:
                if d != 'name' and d != 'tonal.key_key' and d.find('tonal.') == -1 and d != 'class':
                    if len(np.shape(pool[d])) == 1:
                        if len(pool[d]) == len(sounds):
                            line = line + str(pool[d][snd]) + ','
                    elif len(np.shape(pool[d][0])) > 1:
                        if len(pool[d][0]) == len(sounds):
                            line = line + str(pool[d][0][snd]) + ','
            arff.write(line + classes[int(pool['class'][snd])] + '\n')
    # data contains the values of the attributes for each relation
    # write as ARFF:

  

'''
   @DATA
   5.1,3.5,1.4,0.2,Iris-setosa
   4.9,3.0,1.4,0.2,Iris-setosa
   4.7,3.2,1.3,0.2,Iris-setosa
   4.6,3.1,1.5,0.2,Iris-setosa
   5.0,3.6,1.4,0.2,Iris-setosa
   5.4,3.9,1.7,0.4,Iris-setosa
   4.6,3.4,1.4,0.3,Iris-setosa
   5.0,3.4,1.5,0.2,Iris-setosa
   4.4,2.9,1.4,0.2,Iris-setosa
   4.9,3.1,1.5,0.1,Iris-setosa
'''

import essentia as ess
import essentia.standard as esstd

def makeSmallPool():
    datain = esstd.YamlInput(filename='../results/descriptors_nomods.json')
    print "loading data"
    t_pool = datain()
    print "extracting fields"
    names = t_pool['name']
    pTag = t_pool['annotated.pitch']
    pEst = t_pool['lowLevel.pitch.median']
    conf = t_pool['lowLevel.pitch_instantaneous_confidence.median']
    var = t_pool['lowLevel.pitch.var']
    sal = t_pool['lowLevel.pitch_salience.median']

    pool = ess.Pool()
    for name in names:
        pool.add('name', name)
    pool.set('annotated.pitch', pTag);
    pool.set('lowLevel.pitch.median', pEst)
    pool.set('lowLevel.pitch_instantaneous_confidence.median', conf);
    pool.set('lowLevel.pitch.var', var)
    pool.set('lowLevel.pitch_salience.median', sal)

    return pool
  

def takeSampleFromPool(pool, N, indexes=[]):
    outPool = ess.Pool();

    names = pool['name']
    if indexes != []:
        if len(indexes) < N:
            print "\nerror: list of indexes shorter than requested amount of samples\n"
            return -1
        else:
            for n in range(N):
                i = np.random.randint(len(indexes))
                ind = indexes[i]
                for d in pool.descriptorNames():
                    if len(np.shape(pool[d])) == 1:
                        if len(pool[d]) == len(pool['name']):
                            outPool.add(d, pool[d][ind])
                    elif len(np.shape(pool[d])) > 1:
                        if len(pool[d][0]) == len(pool['name']):
                            outPool.add(d, pool[d][0][ind])
                        elif d == 'name':
                            outPool.add('name', pool['name'][ind])
                indexes = np.delete(indexes, i)

    testHomogeneity(outPool, pool)
    return outPool


def testHomogeneity(sample, pool):
    print "Testing homogeneity:"
    for d in pool.descriptorNames():
        print d
        try:
            mu = np.mean(pool[d]); med = np.median(pool[d]); std = np.std(pool[d])
            s_mu = np.mean(sample[d]); s_med = np.median(sample[d]); s_std = np.std(sample[d]);
            print "\tSample:\tmean: %2.5f\tmedian: %2.5f\tstd: %2.5f" % (s_mu, s_med, s_std);
            print "\tTotal:\tmean: %2.5f\tmedian: %2.5f\tstd: %2.5f" % (mu, med, std);
        except:
            print "Descriptor %s\t could not be calculated" % d

def randomMergePools(poolA, poolB):
    '''
        poolA: correct
        poolB: wrong
    '''
    a = np.arange(len(poolA['name']))
    b = np.arange(len(poolB['name']))
    
    indexes = [a, b]
    pools = [poolA, poolB]
    N = len(a) + len(b)
    pool = ess.Pool()
    for n in range(N):
        randPool = np.random.randint(2) # 0: a, 1: b
        if len(indexes[0]) == 0:
            randPool = 1
        elif len(indexes[1]) == 0:
            randPool = 0
        i = np.random.randint(len(indexes[randPool]))
        
        for d in pools[randPool].descriptorNames():
            pool.add(d, pools[randPool][d][i])
        pool.add('class', randPool)
   
        indexes[randPool] = np.delete(indexes[randPool], i)
        
    return pool

def normalisePool(pool):
    oPool = ess.Pool()
    for d in pool.descriptorNames():
        data = np.array(pool[d])
        if str(data.dtype).find('float') > -1:
            oPool.set(d, ut.normalise(data))
        else:
            print "Ommitting: " + d
            for val in pool[d]:
                oPool.add(d, val)
    return oPool
        

def deleteDescr(pool, dname):
    pool.remove(dname)
    return pool
