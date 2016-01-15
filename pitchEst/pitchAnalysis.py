import numpy as np
import sys, os

import essPitch as essP
import freesoundPitchAnalysis as frsndPA

ARGCOUNT = 3

# MIDI <-> frequency conversion -----------------------
def freq_to_MIDInote(f, fref=440.):
    return int(np.log2(f / float(fref)) * 12 + 49) 

def MIDInote_to_freq(nn, fref=440.0):
    return float(fref) * 2**((nn-49) / 12.)

def noteName_to_noteNr(note):
    ''' 
        Convert a string to a note number
    '''
    C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B = np.arange(12) - 8;
    c, db, d, eb, e, f, gb, g, ab, a, bb, b = np.arange(12) - 8;
    
    C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = np.arange(12) - 8;
    C, Csharp, D, Dsharp, E, F, Fsharp, G, Gsharp, A, Asharp, B = np.arange(12) - 8;
    
    FAILED = -999
    return eval(note)   # noteName_to_noteNr()

def zeropad(x, Ny):
    Nx = len(x)
    if nX > Ny:
        return x[:Ny]
    elif nX < Ny:
        return np.append(x, np.zeros(Ny - Nx))
    else:
        return x

def getMIDINoteFromFilename(fn, pack=''):
    nname = 'FAILED'
    if pack == 'IOWA':
        nname = fn.split('.')[-2]
        
    if pack == 'philharmonia':
        nname = fn.split('_')[1]
    octave = int(nname[-1])
    
    nn = noteName_to_noteNr(nname[:len(nname)-1])
    if nn == noteName_to_noteNr('FAILED'):
        return -999
    
    return nn + (octave * 12)
   

if len(sys.argv) < ARGCOUNT + 1:
    print "usage: pitchAnalysis.py [filename][pack][outfile]([WINDOWINGTYPE])"
else:
    fn = sys.argv[1]
    pack = sys.argv[2]
    outfile = sys.argv[3]
    if len(sys.argv) > ARGCOUNT + 1:
        win = sys.argv[4]
    else:
        win = 'none'

    print "File: "+fn
    # get notenumber and frequency from filename:
    
    if pack == 'carlos' or pack == 'good-sounds' or pack == 'modularsamples':
        nn = frsndPA.getNoteFromJSON(frsndPA.getJsonData(fn.split('.ogg')[0]+'.json'), pack)
    else:
        nn = getMIDINoteFromFilename(fn, pack)
    pTag = MIDInote_to_freq(nn)
    
    # calculate pitchYinFFT & pitchSalience:
    pEst, conf, sal = essP.essPitchAnalysis(fn, win)
    
    err = pEst - pTag
    absErr = abs(err)
    res = [ fn, err, absErr, nn, pTag, pEst, conf, sal ]

    # write to file:
    with open(outfile, "a") as of:
        for i in range(len(res)):
            of.write(str(res[i])+"\t")
        of.write("\n")

