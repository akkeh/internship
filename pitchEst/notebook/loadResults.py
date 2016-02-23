import numpy as np

def readData(fn):
    '''
    Read data from the results directory. Formatted:
    fields: comma separated.
    Data:   '\t' separated.
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

csN = len(carlosJSON[0])-1
gsN = len(goodsoundsJSON[0])-1
msN = len(modularsamplesJSON[0])-1

# soundfile-data:
carlosESS = readData('./results/carlos_ESS.txt')
goodsoundsESS = readData('./results/good-sounds_ESS.txt')
modularsamplesESS = readData('./results/modularsamples_ESS.txt')
# non Freesound:
philharmoniaESS =  readData('./results/philharmonia_ESS.txt')
iowaESS =  readData('./results/IOWA_ESS.txt')
phN = len(philharmoniaESS[0])-1
iwN = len(iowaESS[0])-1

print "read "+str(csN+gsN+msN)+" lines of Freesound data"
print "read "+str(phN+iwN)+" lines of non-Freesound soundfile data"

print "Total amount of sounds assessed: "+str(csN+gsN+msN + phN+iwN)


# load all the fields into arrays:

# get all the estimated pitches:
field = 'pEst'
csJ_pEst =  np.array(getField(carlosJSON, field), dtype='float32')
gsJ_pEst =  np.array(getField(goodsoundsJSON, field), dtype='float32')
msJ_pEst =  np.array(getField(modularsamplesJSON, field), dtype='float32')

frsJSON_pEst = np.append(csJ_pEst, np.append(gsJ_pEst, msJ_pEst));

# get all the annotated MIDI notes:
field = 'midinote'
csJ_midi =  np.array(getField(carlosJSON, field), dtype='float32')
gsJ_midi =  np.array(getField(goodsoundsJSON, field), dtype='float32')
msJ_midi =  np.array(getField(modularsamplesJSON, field), dtype='float32')

csE_midi =  np.array(getField(carlosESS, field), dtype='float32')
gsE_midi =  np.array(getField(goodsoundsESS, field), dtype='float32')
msE_midi =  np.array(getField(modularsamplesESS, field), dtype='float32')

phE_midi =  np.array(getField(philharmoniaESS, field), dtype='float32')
iwE_midi =  np.array(getField(iowaESS, field), dtype='float32')

# append some midi-arrays:
frsJSON_midi = np.append(csJ_midi, np.append(gsJ_midi, msJ_midi));
frsESS_midi = np.append(csE_midi, np.append(gsE_midi, msE_midi));
ESS_midi = np.append(csE_midi, np.append(gsE_midi, np.append(msE_midi, np.append(phE_midi, iwE_midi))));

# get all the annotated pitches:
field = 'pTag'
csJ_pTag =  np.array(getField(carlosJSON, field), dtype='float32')
gsJ_pTag =  np.array(getField(goodsoundsJSON, field), dtype='float32')
msJ_pTag =  np.array(getField(modularsamplesJSON, field), dtype='float32')

frsJSON_pTag = np.append(csJ_pTag, np.append(gsJ_pTag, msJ_pTag));

# get all the confidences:
field = 'confidence'
csJ_conf =  np.array(getField(carlosJSON, field), dtype='float32')
gsJ_conf =  np.array(getField(goodsoundsJSON, field), dtype='float32')
msJ_conf =  np.array(getField(modularsamplesJSON, field), dtype='float32')

frsJSON_conf = np.append(csJ_conf, np.append(gsJ_conf, msJ_conf));

# get all the saliences:
field = 'salience'
csJ_sal =  np.array(getField(carlosJSON, field), dtype='float32')
gsJ_sal =  np.array(getField(goodsoundsJSON, field), dtype='float32')
msJ_sal =  np.array(getField(modularsamplesJSON, field), dtype='float32')

frsJSON_sal = np.append(csJ_sal, np.append(gsJ_sal, msJ_sal));

# get all data from the essentia Extractor:
from descriptors import *
pool = loadData()
