import dataMan as dm
import predictErr as pEE
import numpy as np

def ERBerrs(d):
    ERBerr = dm.getField(d, 'ERBdist')
    N = len(ERBerr)

    aERBerr = abs(ERBerr)
    
    m_aERBerr = np.mean(aERBerr)
    print "mean absolute ERB distance:\t\t\t", m_aERBerr
   
    i_lt_m = np.where(aERBerr < m_aERBerr)
    i_gt_m = np.where(aERBerr >= m_aERBerr)
    print "% ERB dist. less than mean ("+str(m_aERBerr)+"):\t", len(i_lt_m[0]) / float(N)
        
    i_lt_2 = np.where(aERBerr < 2)
    i_gt_2 = np.where(aERBerr >= 2)
    print "% estimation and annotation within 1 ERB:\t", len(i_lt_2[0]) / float(N)
     
   

def pTags_vs_err(d, errName, th=-999):
    pTag = dm.getField(d, 'pTag')
    err = abs(dm.getField(d, errName))
    
    if th == -999:
        th = np.mean(err)
    
    inc = np.where(err < th)
    exc = np.where(err >= th)
    
    print "mean pTag of err < th:\t", np.mean(pTag[inc])
    print "mean pTag of err >= th:\t", np.mean(pTag[exc])
    print "min, max pTag of err < th:\t", min(pTag[inc]), ",\t", max(pTag[inc])
    print "min, max pTag of err >= th:\t", min(pTag[exc]), ",\t", max(pTag[exc])
    
    return inc, exc



#   functions to read data from files:
def concatenateData(data, fn):
    d = dm.getData(fn)
    
    newData = data
    if len(d) != len(newData):
        print "\nerror: no enough fields in new data file"
        return data

    name = np.append(data[0][1], d[0][1]);
    err = np.append(data[1][1], d[1][1]);
    pTag = np.append(data[2][1], d[2][1]);
    midi = np.append(data[3][1], d[3][1]);
    pEst = np.append(data[4][1], d[4][1]);
    absErr = np.append(data[5][1], d[5][1]);
    sal = np.append(data[6][1], d[6][1]);
    conf = np.append(data[7][1], d[7][1]);
    ERBdist = np.append(data[8][1], d[8][1]);

    return ('name', name), ('err', err), ('pTag', pTag), ('midinote', midi), ('pEst', pEst), ('absErr', absErr), ('sal', sal), ('conf', conf), ('ERBdist', ERBdist)

def getAllData(datafiles):
    d = dm.getData(datafiles[0])
    for f in datafiles[1:]:
        d = concatenateData(d, f)
    return d

def writeData(d, fn):
    with open(fn, 'w') as f:
        for field in d:
            f.write(field[0]+',')
        f.write('\n')
        for line in range(len(d[0][1])):
            for field in d:
                f.write(field[1][line]+',')
            f.write('\n')


def writeArray(arr, fn):
    with open(fn, 'w') as  f:
        for val in arr:
            f.write(val+'\n')


           
files = ['../results/carlos_ESS.txt', '../results/good-sounds_ESS.txt', '../results/IOWA_ESS.txt', '../results/philharmonia_guitar_ESS.txt', '../results/philharmonia_violin_ESS.txt', '../results/philharmonia_cello_ESS.txt', '../results/philharmonia_clarinet_ESS.txt', '../results/modularsamples_ESS_mod.txt']

filelists = [ files, files[:-1] ]

def sumup(files):
    print ""
    print "---------------------------------------------------------------------------------------------------------------------------------------"
    print "Files", files
    print "---------------------------------------------------------------------------------------------------------------------------------------"
    d = getAllData(files)

    pTag = dm.getField(d, 'pTag')
    pEst = dm.getField(d, 'pEst')
    err = dm.getField(d, 'err')
    ERBd = dm.getField(d, 'ERBdist')

    print "pEst > pTag?: "+str( len(np.where(pEst > pTag)[0]) / float(len(pTag)))
    print "mean of error: "+str(np.mean(err))
    print "\t for ERB: "+str(np.mean(ERBd))
    print ''

     
    print "ERBdist < 2"
    e, i = pTags_vs_err(d, 'ERBdist', 2)
    print("stddev\n\t< 2: "+str(dm.stddev(pTag[i]))+"\t> 2: "+str(dm.stddev(pTag[e])))
    print ''
    print "ERBdist < m"
    e, i = pTags_vs_err(d, 'ERBdist')
    print("stddev\n\tinc: "+str(dm.stddev(pTag[i]))+"\texc: "+str(dm.stddev(pTag[e])))
    print ''
    print "err < m"
    e, i = pTags_vs_err(d, 'err')
    print("stddev\n\tinc: "+str(dm.stddev(pTag[i]))+"\texc: "+str(dm.stddev(pTag[e])))
    print ''


    print "confidence < mean:"
    e, i = pTags_vs_err(d, 'conf')
    print("stddev\n\tinc: "+str(dm.stddev(pTag[i]))+"\texc: "+str(dm.stddev(pTag[e])))
    print ''

    print "---------------------------------Confidence predicts:"
    print "ERBdist:"
    e, p, tP, tN, fP, fN = pEE.predictEstErr(data=d, evaluate='ERBdist', plot=0)
    print "confidence got: "+str((len(tP[1])+len(tN[1]))/float(len(tP[1])+len(tN[1])+len(fP[1])+len(fN[1])))+" correct"
    print ''

    print "err:"
    e, p, tP, tN, fP, fN = pEE.predictEstErr(data=d, evaluate='err', plot=0)
    print "confidence got: "+str((len(tP[1])+len(tN[1]))/float(len(tP[1])+len(tN[1])+len(fP[1])+len(fN[1])))+" correct"

    print "---------------------------------salience predicts:"
    print "ERBdist:"
    e, p, tP, tN, fP, fN = pEE.predictEstErr(data=d, predict='sal', evaluate='ERBdist', plot=0)
    print "salience got: "+str((len(tP[1])+len(tN[1]))/float(len(tP[1])+len(tN[1])+len(fP[1])+len(fN[1])))+" correct"
    print ''

    print "err:"
    e, p, tP, tN, fP, fN = pEE.predictEstErr(data=d, predict='sal', evaluate='err', plot=0)
    print "salience got: "+str((len(tP[1])+len(tN[1]))/float(len(tP[1])+len(tN[1])+len(fP[1])+len(fN[1])))+" correct"



for files in filelists:
    sumup(files)
