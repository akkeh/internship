import numpy as np

def readData(fn):
    '''
    Read data from the results directory. Formatted:
    fields: comma se ated.
    Data:   '\t' se eted.
    '''
    with open(fn) as f:
        N = 0;  # linecount
        fields = f.readline().split(',')
        M = len(fields)    # collum count
        while f.readline() != '':
            N += 1              
    
    data = np.ndarray(shape=(M, N+1), dtype='|S32')   # create data matrix
    
    col = 0
    for field in fields:
        d = np.array([], dtype='|S32')
        with open(fn) as f:
            f.readline();   # skip first line
            
            d = np.append(d, field.split('\n')[0])
            line = f.readline();
            while line != '':
                d = np.append(d, line.split('\t')[col])
                line = f.readline()
            data[col] = d
            col += 1           
    return data


def getField(data, field):
    M = len(data)
    out = np.array([])
    for col in range(M):
        if data[col][0] == field:
            for row in np.arange(len(data[col]) - 1)+1:
                out = np.append(out, data[col][row])
    return out

# First load all the data from the results directory:
# JSON-data:
carlosJSON =  readData('./results/carlos_JSON.txt')
goodsoundsJSON =  readData('./results/good-sounds_JSON.txt')
modularsamplesJSON =  readData('./results/modularsamples_JSON.txt')

csJ_N = len(carlosJSON[0])-1
gsJ_N = len(goodsoundsJSON[0])-1
msJ_N = len(modularsamplesJSON[0])-1

# soundfile-data:
# Freesound:
carlosESS =  readData('./results/carlos_ESS.txt')
goodsoundsESS =  readData('./results/good-sounds_ESS.txt')
modularsamplesESS =  readData('./results/modularsamples_ESS.txt')
csE_N = len(carlosESS[0])-1
gsE_N = len(goodsoundsESS[0])-1
msE_N = len(modularsamplesESS[0])-1

'''
carlosESSroll512 = readData('./results/carlos_ESS_roll512.txt')
goodsoundsESSroll512 = readData('./results/good-sounds_ESS_roll512.txt')
modularsamplesESSroll512 = readData('./results/modularsamples_ESS_roll512.txt')
csEr_N = len(carlosESSroll512[0])-1
gsEr_N = len(goodsoundsESSroll512[0])-1
msEr_N = len(modularsamplesESSroll512[0])-1
'''

# non Freesound:
philharmoniaESS =  readData('./results/philharmonia_ESS.txt')
iowaESS =  readData('./results/IOWA_ESS.txt')
phE_N = len(philharmoniaESS[0])-1
iwE_N = len(iowaESS[0])-1
'''
philharmoniaESSroll512 =  readData('./results/philharmonia_ESS_roll512.txt')
iowaESSroll512 =  readData('./results/IOWA_ESS_roll512.txt')
phEr_N = len(philharmoniaESSroll512[0])-1
iwEr_N = len(iowaESSroll512[0])-1
'''

print "read "+str(csJ_N+gsJ_N+msJ_N)+" lines of Freesound data"
print "read "+str(csE_N+gsE_N+msE_N)+" lines of Freesound soundfile data"
print "read "+str(phE_N+iwE_N)+" lines of non-Freesound soundfile data"

print "Total amount of sounds assessed: "+str(csJ_N+gsJ_N+msJ_N + phE_N+iwE_N)


# load all the fields into arrays:

# get all the errors:
field = 'err'
csJ_err =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_err =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_err =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_err =  np.array(getField(carlosESS, field), dtype='float')
gsE_err =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_err =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_err =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_err =  np.array(getField(iowaESS, field), dtype='float')

# sample the modularsamples results:


# append some error-arrays:
frsJSON_err = np.append(csJ_err, np.append(gsJ_err, msJ_err));
frsESS_err = np.append(csE_err, np.append(gsE_err, msE_err));
ESS_err = np.append(csE_err, np.append(gsE_err, np.append(msE_err, np.append(phE_err, iwE_err))));


# get all the annotated MIDI notes:
field = 'midinote'
csJ_midi =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_midi =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_midi =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_midi =  np.array(getField(carlosESS, field), dtype='float')
gsE_midi =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_midi =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_midi =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_midi =  np.array(getField(iowaESS, field), dtype='float')

# append some midi-arrays:
frsJSON_midi = np.append(csJ_midi, np.append(gsJ_midi, msJ_midi));
frsESS_midi = np.append(csE_midi, np.append(gsE_midi, msE_midi));
ESS_midi = np.append(csE_midi, np.append(gsE_midi, np.append(msE_midi, np.append(phE_midi, iwE_midi))));

# get all the annotated pitches:
field = 'pTag'
csJ_pTag =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_pTag =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_pTag =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_pTag =  np.array(getField(carlosESS, field), dtype='float')
gsE_pTag =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_pTag =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_pTag =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_pTag=  np.array(getField(iowaESS, field), dtype='float')

# append some pTag-arrays:
frsJSON_pTag = np.append(csJ_pTag, np.append(gsJ_pTag, msJ_pTag));
frsESS_pTag = np.append(csE_pTag, np.append(gsE_pTag, msE_pTag));
ESS_pTag = np.append(csE_pTag, np.append(gsE_pTag, np.append(msE_pTag, np.append(phE_pTag, iwE_pTag))));

# get all the estimated pitches:
field = 'pEst'
csJ_pEst =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_pEst =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_pEst =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_pEst =  np.array(getField(carlosESS, field), dtype='float')
gsE_pEst =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_pEst =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_pEst =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_pEst =  np.array(getField(iowaESS, field), dtype='float')

# append some pEst-arrays:
frsJSON_pEst = np.append(csJ_pEst, np.append(gsJ_pEst, msJ_pEst));
frsESS_pEst = np.append(csE_pEst, np.append(gsE_pEst, msE_pEst));
ESS_pEst = np.append(csE_pEst, np.append(gsE_pEst, np.append(msE_pEst, np.append(phE_pEst, iwE_pEst))));

# get all the confidences:
field = 'confidence'
csJ_conf =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_conf =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_conf =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_conf =  np.array(getField(carlosESS, field), dtype='float')
gsE_conf =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_conf =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_conf =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_conf =  np.array(getField(iowaESS, field), dtype='float')

# append some conf-arrays:
frsJSON_conf = np.append(csJ_conf, np.append(gsJ_conf, msJ_conf));
frsESS_conf = np.append(csE_conf, np.append(gsE_conf, msE_conf));
ESS_conf = np.append(csE_conf, np.append(gsE_conf, np.append(msE_conf, np.append(phE_conf, iwE_conf))));

# get all the saliences:
field = 'salience'
csJ_sal =  np.array(getField(carlosJSON, field), dtype='float')
gsJ_sal =  np.array(getField(goodsoundsJSON, field), dtype='float')
msJ_sal =  np.array(getField(modularsamplesJSON, field), dtype='float')

csE_sal =  np.array(getField(carlosESS, field), dtype='float')
gsE_sal =  np.array(getField(goodsoundsESS, field), dtype='float')
msE_sal =  np.array(getField(modularsamplesESS, field), dtype='float')

phE_sal =  np.array(getField(philharmoniaESS, field), dtype='float')
iwE_sal =  np.array(getField(iowaESS, field), dtype='float')

# append some salience-arrays:
frsJSON_sal = np.append(csJ_sal, np.append(gsJ_sal, msJ_sal));
frsESS_sal = np.append(csE_sal, np.append(gsE_sal, msE_sal));
ESS_sal = np.append(csE_sal, np.append(gsE_sal, np.append(msE_sal, np.append(phE_sal, iwE_sal))));




