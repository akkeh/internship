import numpy as np

import essentia as ess
import essentia.standard as esstd


from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

import util as ut

def createDatasets(pool, N, test_perc=0.25, inputFunc=ut.spectrum, inpArg=(2048, 1024), targetFunc=ut.getOct, targetArg=()):
    trainN = int(np.round(N * (1-test_perc)))
    testN = int(np.round(N * test_perc))
    print "Training samples:\t%d\nTest samples:\t%d" % (trainN, testN)
    
    names = np.append(pool['name'], [])
    pTag = pool['annotated.pitch']
    pEst = pool['lowLevel.pitch.median']
    mTag = ut.freq2midi(pTag)
    mEst = ut.freq2midi(pEst)

    trainSet = ClassificationDataSet(len(inputFunc(np.arange(44100))), 1, nb_classes=9)
    testSet = ClassificationDataSet(len(inputFunc(np.arange(44100))), 1, nb_classes=9)
    for n in range(trainN):
        i = np.random.randint(len(names))
        loader = esstd.MonoLoader(filename='../../notebook/sounds/all/'+names[i])
        x = loader()
        if len(x) > 0:
            inp = inputFunc(ut.trimAttack(x))
            
            target = targetFunc(mTag[i])
            trainSet.addSample(inp, target)
        
        names = np.delete(names, i)
        pTag = np.delete(pTag, i)
        pEst = np.delete(pEst, i)
    
    for n in range(testN):
        i = np.random.randint(len(names))
        loader = esstd.MonoLoader(filename='../../notebook/sounds/all/'+names[i])
        x = loader()
        if len(x) > 0:
            inp = inputFunc(ut.trimAttack(x))
        
            target = targetFunc(mTag[i])
            testSet.addSample(inp, target)
        
        names = np.delete(names, i)
        pTag = np.delete(pTag, i)
        pEst = np.delete(pEst, i)


    trainSet._convertToOneOfMany()   
    testSet._convertToOneOfMany()   
    return trainSet, testSet 


def loadPool(path='../../notebook/results/descriptors_nomods.json'):
    datain = esstd.YamlInput(filename=path)
    return datain()
