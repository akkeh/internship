import numpy as np
import matplotlib.pyplot as plt

import essentia as ess
import essentia.standard as esstd

from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

import util as ut
import dataset as dat

# create network: -------------------------------------------------------|
def createNet(ds, hN=2048, wFile=''):
    net = buildNetwork(ds.indim, hN, ds.outdim, outclass=SoftmaxLayer)
    
    if wFile != '':
        with open(wFile) as f:
            ws = np.array([]);
            for w in f.readlines():
                ws = np.append(ws, w)
        net._setParameters(ws)
    return net

def saveNet(net, wFile):
    with open(wFile, 'w') as f:
        for w in net.params:
            f.write(str(w)+'\n')
#------------------------------------------------------------------------|
# create trainer: -------------------------------------------------------|
def createTrainer(net, ds):
    return BackpropTrainer(net, ds, verbose=True)

def train(net, trainSet, testSet, maxIter=10, epochs=5):
    trainer = createTrainer(net, trainSet)

    for i in range(maxIter):
        trainer.trainEpochs(5)
        trainErr = percentError(trainer.testOnClassData(), trainSet['class'])
        testErr = percentError(trainer.testOnClassData(dataset=testSet), testSet['class'])

        print "Epoch %d:" % trainer.totalepochs
        print "\ttrain error: %5.2f%%" % trainErr
        print "\ttest error: %5.2f%%" % testErr
#------------------------------------------------------------------------|


# Evaluation: -----------------------------------------------------------|
def octEstimator(pool, net, inputFunc=ut.spectrum):
    
    pTag = pool['annotated.pitch']
    pEst = pool['lowLevel.pitch.median']
    tagOct = int(np.round(ut.freq2midi(pTag)) / 12)
    essOct = int(np.round(ut.freq2midi(pEst)) / 12)
    names = pool['name']
    
    netOct = np.zeros(len(essOct))
    i = 0
    for name in names:
        loader = esstd.MonoLoader(filename='../../notebook/sounds/all/'+name[0])
        x = loader()
        inp = inputFunc(ut.trimAttack(x))        
        netOct[i] = net.activate(inp)
        i+=1
    return tagOct, essOct, netOct

#------------------------------------------------------------------------|
#------------------------------------------------------------------------|
import sys
print sys.argv
if len(sys.argv) > 1:
    if sys.argv[1] == 'init':
        print "loading pool"
        pool = dat.loadPool()
        print "creating datasets:"
        trainSet, testSet = dat.createDatasets(pool, 1000)
        print "creating net"
        net = createNet(trainSet, 1024)
        print "training net"

        I = 4
        for i in range(I):
            print "training..."
            train(net, trainSet, testSet)
            print "evaluating results (%d of %d):" % (i, I)
            tagOct, essOct, netOct = octEstimator(pool, net)
            
            octDiff = (tagOct - netOct)
            print "Pass %d mis estimated:\t%d\t(pYinFFT:\t%d)" % (i, (len(np.where(octDiff != 0)[0]) / float(len(tagOct))), (len(np.where(essDiff != 0)[0]) / float(len(tagOct))))
            print "resampling datasets" 
            trainSet, testSet = dat.createDatasets(pool, 1000)
#------------------------------------------------------------------------|
