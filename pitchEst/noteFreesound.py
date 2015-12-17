import json
import numpy as np

# MIDI <-> frequency conversion -----------------------
def freq_to_MIDInote(f, f_ref=440.):
    return int(np.log2(f / float(f_ref)) * 12 + 49)

def MIDInote_to_freq(nn, f_ref=440.0):
    return float(f_ref) * 2**((nn-49) / 12.)

def noteName_to_noteNr(note):
    '''
        Convert a string to a note number
    '''
    C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B = np.arange(12) - 8;
    C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = np.arange(12) - 8;
    C, Csharp, D, Dsharp, E, F, Fsharp, G, Gsharp, A, Asharp, B = np.arange(12) - 8;

    return eval(note)   # noteName_to_noteNr()

# JSON  -----------------------------------------------
def getJsonData(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)
    return data

def getNoteFromPack(data, i):
    '''
    Try to extract the midinote of the i-th sound in data
        input:
        -   data:   a json file
        -   i:      member to extract note of (int)       
        output:
    
        todo:
        -   pages? (next)
    '''
    data = data.items()[2][1]
    
def notename2midinr(filename):
    f = filename.split('.')
    if len(f) > 3:
        pitch = f[-2]
    else:
        f = filename.split('_')
        pitch = f[1]
    octave = pitch[-1]
    
    if len(pitch) == 2:
        note = pitch[0]
    else:
        note = pitch[0]+pitch[1]
    print "Found: ", note, octave
    return NoteNames(note) + (12 * int(octave))


