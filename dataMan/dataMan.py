import numpy as np
import matplotlib.pyplot as plt

import bins
import ERBdist as ERB
import seeve as sv

def manData(d):

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
        
    
    # ERB dist histogram
    ERBdist = ERB.calcERBdist(pTag, pEst)
    ERBdist_x, ERBdist_y = bins.binData(ERBdist, ERBdist_bw)

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

    print "outputs: err, pTag, pEst, absErr, sal, conf, ERBdist"
    return err, pTag, pEst, absErr, sal, conf, ERBdist
