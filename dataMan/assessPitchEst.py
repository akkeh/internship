import numpy as np
import matplotlib.pyplot as plt
import dataMan as dm
 

def predictEstErr(fn, evaluate='absErr', predict='conf', inverse_eval=False, inverse_predict=False, plot=0):
    data = dm.getData(fn)
    
    evalVals = dm.getField(data, evaluate)
    if inverse_eval:
        evalVals = -evalVals
    predictVals = dm.getField(data, predict)
    if inverse_predict:
        predictVals = -predictVals

    evalMean = dm.mean(evalVals)
    predictMean = dm.mean(predictVals)

    i_e_gt_eMean = np.where(evalVals > evalMean)
    i_e_lt_eMean = np.where(evalVals < evalMean)

    truePos = i_e_lt_eMean[0][np.where(predictVals[i_e_lt_eMean] > predictMean)]
    trueNeg = i_e_gt_eMean[0][np.where(predictVals[i_e_gt_eMean] < predictMean)]
    falsePos = i_e_gt_eMean[0][np.where(predictVals[i_e_gt_eMean] > predictMean)]
    falseNeg = i_e_lt_eMean[0][np.where(predictVals[i_e_lt_eMean] < predictMean)]

    if plot == 1:
        plt.plot(predictVals[truePos], evalVals[truePos], '.', label='truePos')
        plt.plot(predictVals[falseNeg], evalVals[falseNeg], '.', label='falseNeg')
        plt.plot(predictVals[falsePos], evalVals[falsePos], '.', label='falsePos')
        plt.plot(predictVals[trueNeg], evalVals[trueNeg], '.', label='trueNeg')

        plt.plot([min(predictVals), max(predictVals)], [evalMean, evalMean], label='mean '+str(evaluate))
        plt.plot([predictMean * 0.99999999, predictMean, predictMean * 1.0000000001], [0, max(abs(evalVals)), 0], label='mean '+str(predict))
        plt.legend( loc='upper left', numpoints = 1 ) 
       

    print "True positives:\t\t"+str(len(truePos))
    print "True negatives:\t\t"+str(len(trueNeg))
    print "False positives:\t"+str(len(falsePos))
    print "False negatives:\t"+str(len(falseNeg))
    return ('evaluate', evalVals), ('predict', predictVals), ('truePos', truePos), ('trueNeg', trueNeg), ('falsePos', falsePos), ('falseNeg', falseNeg)


def get_array_overlap(a, b):
    Na = len(a)
    Nb = len(b)
    y = 0
    for i in range(Na):
        for j in range(Nb):
            if a[i] == b[j]:
                y += 1
                np.delete(a, i)
                np.delete(b, j)
                i -= 1
                j -= 1
                break
    return y   

'''
def calcPack(fn):
    data = dm.getData(fn)
   
    # pTag:
    pTag = dm.getField(data, 'pTag')
    pEst = dm.getField(data, 'pEst')

    # err:
    err = dm.getField(data, 'err')
    
    sqErr = err*err
    m_sqErr = dm.mean(sqErr)
    sd_sqErr = dm.stddev(sqErr)
    
    i_hiErr = np.where(sqErr > m_sqErr) # indexes of sounds with squared error > mean of squared errors:
    m_hiErr_pTag = dm.mean(pTag[i_hiErr])
    m_hiErr_pEst = dm.mean(pEst[i_hiErr])

    return m_hiErr_pTag, pTag, m_hiErr_pEst, pEst

def conf_vs_err(fn):
    data = dm.getData(fn)
    
    conf = dm.getField(data, 'conf')
    err = dm.getField(data, 'err')
    sqErr = err * err
   
    plt.title(fn) 
    plt.xlabel('confidence')
    plt.ylabel('abs err')
    #rmsErr_m = np.sqrt(dm.mean(sqErr))
    absErr_m = dm.mean(np.sqrt(sqErr))
    #rmsPlt = plt.plot([min(conf), max(conf)], [rmsErr_m, rmsErr_m])
    conf_m = dm.mean(conf)
  
    errPlt = plt.plot(conf, np.sqrt(err*err), '.', label='absolute errors')
    name = dm.getField(data, 'name')

    i_hiErr = np.where(abs(err) > absErr_m)
    i_falsePos = i_hiErr[0][np.where(conf[i_hiErr] > conf_m)]
   
    falsePos = plt.plot(conf[i_falsePos], abs(err)[i_falsePos], '.', label='false positives'); 

    i_loErr = np.where(abs(err) < absErr_m)
    i_falseNeg = i_loErr[0][np.where(conf[i_loErr] < conf_m)]
    falseNeg = plt.plot(conf[i_falseNeg], abs(err)[i_falseNeg], '.', label='false negatives')
  

    absPlt = plt.plot([min(conf), max(conf)], [absErr_m, absErr_m], label='mean absolute error')
    confPlt = plt.plot([conf_m * 0.99999999, conf_m, conf_m * 1.0000000001], [0, max(abs(err)), 0], label='mean confidence')

 
    plt.legend( loc='upper left', numpoints = 1 ) 
    i_trueNeg = i_hiErr[0][np.where(conf[i_hiErr] < conf_m)]
    i_truePos = i_loErr[0][np.where(conf[i_loErr] > conf_m)]
    
    print "true positives: "+str(len(i_truePos))
    print "true negatives: "+str(len(i_trueNeg))
    print "false positives: "+str(len(i_falsePos))
    print "false negatives:: "+str(len(i_falseNeg))
    
    return data, i_falsePos, i_falseNeg, i_truePos, i_trueNeg


def calc_errMeans(fn):
    data = dm.getData(fn)

    # err:
    err = dm.getField(data, 'err')
    sqErr = err * err
    sqErr_m = dm.mean(sqErr)
    sqErr_sd = dm.stddev(sqErr)

    i_sqErr_lt_mean = np.where(sqErr > sqErr_m)

    sqErr_ex = np.delete(sqErr, i_sqErr_lt_mean)
    sqErr_ex_m = dm.mean(sqErr_ex)
    print "------------------------------------------------"
    print "nr. of sqErr > mean / nr. of sounds: "+str(len(i_sqErr_lt_mean[0]) / float(len(err)))
    print "root mean squared error: "+str(np.sqrt(sqErr_m))+"Hz"
    print "\t(with stddev: "+str(np.sqrt(sqErr_sd))+")"
    print "root mean squared error exclusive: "+str(np.sqrt(sqErr_ex_m))+"Hz"    
    print ""
    
    # pTag
    pTag = dm.getField(data, 'pTag')
    pTag_hiErr = pTag[i_sqErr_lt_mean]
    
    pTag_hiErr_m = dm.mean(pTag_hiErr)
    pTag_m = dm.mean(pTag)
    pTag_sd = dm.stddev(pTag)

    pTag_ex = np.delete(pTag, i_sqErr_lt_mean)
    pTag_ex_m = dm.mean(pTag_ex)

    print "mean pTag of sounds with sqErr > mean: "+str(pTag_hiErr_m)+"Hz"
    print "\t(mean pTag: "+str(pTag_m)+"Hz\t stddev pTag: "+str(pTag_sd)+")"
    print "mean pTag exclusive: "+str(pTag_ex_m)+"Hz"
    print ""

    # pEst
    pEst = dm.getField(data, 'pEst')
    pEst_hiErr = pEst[i_sqErr_lt_mean]

    pEst_hiErr_m = dm.mean(pEst_hiErr)
    pEst_m = dm.mean(pEst)
    pEst_sd = dm.stddev(pEst)

    pEst_ex = np.delete(pEst, i_sqErr_lt_mean)
    pEst_ex_m = dm.mean(pEst_ex)
    print "mean pEst of sounds with sqErr > mean: "+str(pEst_hiErr_m)+"Hz"
    print "\t(mean pEst: "+str(pEst_m)+"Hz\t stddev pEst: "+str(pEst_sd)+")"
    print "mean pEst exclusive: "+str(pEst_ex_m)+"Hz"
    print ""

    # confidence
    has_conf = True
    conf = dm.getField(data, 'conf')
    if conf == -1:
        has_conf = False
    
    conf_hiErr = conf[i_sqErr_lt_mean]
    conf_hiErr_m = dm.mean(conf_hiErr)
    conf_m = dm.mean(conf)
    conf_sd = dm.stddev(conf)
    
    conf_ex = np.delete(conf, i_sqErr_lt_mean)
    conf_ex_m = dm.mean(conf_ex)
    print "mean conf of sounds with sqErr > mean: "+str(conf_hiErr_m)
    print "\t(mean conf: "+str(conf_m)+"\t stddev conf: "+str(conf_sd)+")"
    print "mean conf exclusive: "+str(conf_ex_m)+"\n"

    # salience 
    sal_hiErr = sal[i_sqErr_lt_mean]
    sal_hiErr_m = dm.mean(sal_hiErr)
    sal_m = dm.mean(sal)
    sal_sd = dm.stddev(sal)
    
    sal_ex = np.delete(sal, i_sqErr_lt_mean)
    sal_ex_m = dm.mean(sal_ex)
    print "mean sal of sounds with sqErr > mean: "+str(sal_hiErr_m)
    print "\t(mean sal: "+str(sal_m)+"\t stddev sal: "+str(sal_sd)+")"
    print "mean sal exclusive: "+str(sal_ex_m)+"\n"
   
    i_cs_gt_exmean = 0 
    if t == 'c':
        print "ommitting sounds with conf < mean conf/sal_ex:"
        i_cs_gt_exmean = np.where(confsal > confsal_ex_m)
    elif t == 's':
        print "ommitting sounds with sal > mean sal ex:"
        i_cs_gt_exmean = np.where(confsal < confsal_ex_m)
    sqErr_cs_gt_exmean = sqErr[i_cs_gt_exmean]
    sqErr_conf_m = dm.mean(sqErr_cs_gt_exmean)
    print "root mean squared err of sounds with conf > conf ex mean: "+str(np.sqrt(sqErr_conf_m))

''' 
