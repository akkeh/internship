import numpy as np
import matplotlib.pyplot as plt

import bins
import ERBdist as ERB
import seeve as sv

def getData(d):

    # variables: -------------------------------------------- #
    # errHist:
    errHist_bw = 10
    # ERBdistHist:
    ERBdist_bw = 1

    # outputs:----------------------------------------------- #
    #   -   err Histogram
    #   -   pTag / pEst
    #   -   salience / absErr
    #   -   ERB distance Histogram
    plots = ['errHist', 'pTag_pEst', 'salience_absErr', 'ERBdistHist']
    
    # ------------------------------------------------------- #

    # err histogram:
    err = sv.seeveData(d, 'err')
    errHist_x, errHist_y = bins.binData(err, errHist_bw)
    
    # x: pTag; y: pEst:
    pTag = sv.seeveData(d, 'pTag')
    pEst = sv.seeveData(d, 'pEst')
        
    # x: confidence; y: absErr
    conf = sv.seeveData(d, 'confidence')
    absErr = sv.seeveData(d, 'absErr')
    # x: salience; y: absErr:
    sal = sv.seeveData(d, 'salience')
    if len(sal) == 0 and len(conf) > 0:
        plots[2] = 'confidence_absErr'
        
    name = sv.seeveData(d, 'name')
    # ERB dist histogram
    ERBdist = ERB.errERB(pTag, pEst)
    ERBdist_x, ERBdist_y = bins.binData(ERBdist, ERBdist_bw)

    midi = sv.seeveData(d, 'midinote')
    '''
    pltid = 0
    while pltid != -1:
        print "Calculated stuff: "
        i = 0
        for j in range(len(plots)):
            print str(i)+": "+plots[j]+" (plot)"
            i += 1
        print "-1: exit"

        
        pltid = input("plot: ")
        try:
            if pltid == 0:
                plt.plot(errHist_x, errHist_y)
            elif pltid == 1:
                plt.plot(pTag, pEst, '.')
            elif pltid == 2:   
                if plots[2] == 'salience_absErr': 
                    plt.plot(sal, absErr, '.')
                elif plots[2] == 'confidence_absErr':
                    plt.plot(conf, absErr, '.')
            elif pltid == 3:
                plt.plot(ERBdist_x, ERBdist_y)
        except:
            pltid = -1
        '''
    #print "outputs: err, pTag, pEst, absErr, sal, conf, ERBdist"
    return ('name', name), ('err', err), ('pTag', pTag), ('midinote', midi), ('pEst', pEst), ('absErr', absErr), ('sal', sal), ('conf', conf), ('ERBdist', ERBdist)

def getField(x, fieldname):
    i = 0
    for field in x:
        #print str(field[0])
        if str(field[0]) == fieldname:
            return field[1]
    return -1
   
def mean(x):
    return np.sum(x) / float(len(x))

def stddev(x):
    xdev = x - mean(x)
    var = np.sum(xdev*xdev) / len(x)
    return np.sqrt(var)

'''
#   Mangle analysis results:
import os
def getFiles(directory):
    t = 'NUL'
    files = np.array([])
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            files = np.append(files, file)
    return files

def meanErrs(directory):
    files = getFiles(directory)
    N = len(files)
    y = np.ndarray(shape=(N, 3), dtype='S32')
    
    for i in range(N):
        data = getData(str(directory)+str(files[i]))
        errs = get_field(data, 'err')
        y[i] = (files[i], mean(errs), stddev(errs))
    #print "name, mean, standard dev"
    return y 

def err_vs_pTag(directory):
    files = getFiles(directory)
    N = len(files)
    
    for i in range(N):
        data = getData(str(directory)+str(files[i]))
        pTag = get_field(data, 'pTag')
        err = get_field(data, 'err')
        plt.ylabel('pTag')
        plt.xlabel('err');
        plt.title(files[i])
        plt.plot(pTag, err, '.')
        plt.show()
    #print "name, pTag, err"

'''
