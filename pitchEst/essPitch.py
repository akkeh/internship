import numpy as np
import matplotlib.pyplot as plt

import essentia
import essentia.standard as ess


def freq_to_MIDInote(f, f_ref=440.):
    return int(np.log2(f / float(f_ref)) * 12 + 49)

def MIDInote_to_freq(nn, f_ref=440.0):
    return float(f_ref) * 2**((nn-49) / 12.)

def NoteNames(note):
    '''
        Convert a string to a note number
    '''
    C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B = np.arange(12) - 8;
    C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = np.arange(12) - 8;
    C, Csharp, D, Dsharp, E, F, Fsharp, G, Gsharp, A, Asharp, B = np.arange(12) - 8;
    c, cs, d, ds, e, f, fs, g, gs, a, as, b = np.arange(12) - 8;

    C, D-b, D, E-b, E, F, G-b, G, A-b, A, B-b, B = np.arange(12) - 8;
    C, C-s, D, D-s, E, F, F-s, G, G-s, A, A-s, B = np.arange(12) - 8;
    return eval(note)

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
    
def computePitchYinFFT(x):
    # instanciate algorithms:
    yinFFT = ess.PitchYinFFT()
    
    # call functions:
    pitch, conf = yinFFT(x);
    
    return pitch, conf

def testPitch(filename):
    # get supposed frequency:
    midiNN = notename2midinr(filename)
    noteFreq = midinotes[midiNN];
    loader = ess.MonoLoader(filename=filename);
    audio = loader();

    # essentia PitchYinFFT:
    ess_PitchYinFFT = computePitchYinFFT(audio)  # [pitch, confidence]
    
    ess_PitchYinFFT = np.append(noteFreq, ess_PitchYinFFT)
    return ess_PitchYinFFT
    
    

