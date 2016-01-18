import numpy as np
import matplotlib.pyplot as plt
import dataMan as dm

# percentages!
ARGCOUNT = 2

def thData(x, th=-999):
    
     
    if th < 0:
        th = dm.mean(x)
        print "using mean"
    i_hiErr = np.where(x >= th) 
    i_loErr = np.where(x < th) #delete(np.arange(len(x)), i_hiErr)
    return i_hiErr[0], i_loErr[0]


def calc_stats(fn, ofile):
    d = dm.getData(fn)
    
    # absErr:
    absErr = dm.getField(d, 'absErr')
    absErr_m = np.mean(absErr)
    absErr_sd = dm.stddev(absErr)
    i_hiErr, i_loErr = thData(absErr, absErr_m)
    print "mean absErr: "+str( absErr_m), "std dev: "+str(absErr_sd)
    perc_loErr = len(i_loErr) / float(len(i_hiErr) + len(i_loErr))
    print "% absErr < mean absErr: "+str(perc_loErr)
    loErr_m = np.mean(absErr[i_loErr])
    loErr_sd = np.mean(absErr[i_loErr])
    print "mean low err.: "+str(loErr_m), "std dev: "+str(loErr_sd)+"\n"

    # ERB-err:
    ERBerr = dm.getField(d, 'ERBdist')
    absERBerr = abs(ERBerr)
    absERBerr_m = np.mean(absERBerr)
    absERBerr_sd = dm.stddev(absERBerr)
    print "mean absERBerr: "+str(absERBerr_m), "std dev: "+str(absERBerr_m)
    i_hiERBerr, i_loERBerr = thData(absERBerr, absERBerr_m)
    perc_absERBerr_lt_mean = len(i_loERBerr) / float(len(i_hiERBerr) + len(i_loERBerr))
    print "% absERBerr < mean absERBerr: "+str(perc_absERBerr_lt_mean)

    i_ERBerr_gt_2, i_ERBerr_lt_2 = thData(absERBerr, 2)
    perc_ERBerr_lt_2 = len(i_ERBerr_lt_2) / float(len(i_ERBerr_gt_2) + len(i_ERBerr_lt_2))
    print "% absERBerr < 2: "+str(perc_ERBerr_lt_2)
    
    pTag = dm.getField(d, 'pTag')
    pTag_m = np.mean(pTag)
    pTag_sd = dm.stddev(pTag)
    pTag_m_w_absErr_lt_m = np.mean(pTag[i_loErr])
    pTag_m_w_absErr_gt_m = np.mean(pTag[i_hiErr])
    pTag_m_w_ERBerr_lt_2 = np.mean(pTag[i_ERBerr_lt_2])
    pTag_sd_w_ERBerr_lt_2 = dm.stddev(pTag[i_ERBerr_lt_2])
    pTag_m_w_ERBerr_gt_2 = np.mean(pTag[i_ERBerr_gt_2])
    pTag_sd_w_ERBerr_gt_2 = dm.stddev(pTag[i_ERBerr_gt_2])
    print "mean pTag: "+str(pTag_m), "std dev: "+str(pTag_sd)
    print "mean pTag | ERBerr < 2: "+str(pTag_m_w_ERBerr_lt_2), "std dev: "+str(pTag_sd_w_ERBerr_lt_2)
    print "mean pTag | ERBerr > 2: "+str(pTag_m_w_ERBerr_gt_2), "std dev: "+str(pTag_sd_w_ERBerr_gt_2)

    print len(i_ERBerr_lt_2)
    print len(absErr), len(i_hiERBerr) + len(i_loERBerr)
    # write statistics to file:
    stat = [len(absErr), absErr_m, absErr_sd, len(i_loErr), absERBerr_m, absERBerr_sd, len(i_loERBerr), len(i_ERBerr_lt_2), pTag_m, pTag_m_w_ERBerr_lt_2]
    with open(ofile, 'a') as of:
        of.write(ofile+"\n")
        for val in stat:
            of.write(str(val)+'\t')
        of.write("\n")
        
        
import sys, os

if len(sys.argv) < ARGCOUNT + 1:
    print "usage: assessPitchEst.py [results.txt][output.txt]"
else:
    infile = sys.argv[1]
    ofile = sys.argv[2]
    calc_stats(infile, ofile)
