#! /usr/bin/python2
ARGCOUNT = 3
'''
    todo:
    -   reference pitch from description
    -   other packs
'''

import os, sys
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
    c, db, d, eb, e, f, gb, g, ab, a, bb, b = np.arange(12) - 8;
    
    C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = np.arange(12) - 8;
    C, Csharp, D, Dsharp, E, F, Fsharp, G, Gsharp, A, Asharp, B = np.arange(12) - 8;
    
    return eval(note)   # noteName_to_noteNr()

# JSON  -----------------------------------------------
def getJsonData(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)
    return data

def getNoteFromJSON(d, pack=''):
    '''
        
    '''
    nn = -1
    octave = -1
    if pack == 'carlos':
        note = d['name'].split(" ")[1]
        if len(note) == 1:
            note = note+d['name'].split(" ")[2]
        if len(note) > 4:   # notename not in filename!
            return -1, -1
        elif note.find("-") != -1:
            nn = note.split("-")[0]
        else:
            nn = note[0] 
        if note.find("#") == -1:
            nn = noteName_to_noteNr(nn)
        else:
            nn = noteName_to_noteNr(nn[0]) + 1
        octave = int(note[-1])
    # fi pack == 'carlos'  

    
    return (nn + (12 * octave))   # getNoteFromJSON()
         
#def getNoteFromFilename(filename):

def getPitchFromJSON(d):
    '''
    '''
    pitch = d['analysis']['lowlevel']['pitch']
    salience = d['analysis']['lowlevel']['pitch_salience']
    
    return pitch['mean'], pitch['var'], salience['mean'], salience['var']

def getFref(d):
    '''
    FINISH
    '''
    desc = d['description']
    # try to find a statement to a reference pitch:
    i = desc.find('Hz')
     
    return 0

def tag_vs_freesoundAnalysis(jsonFile, pack=""):
    '''
    
    '''
    d = getJsonData(jsonFile)
    
    midinote = getNoteFromJSON(d, pack)
    noteFreq = MIDInote_to_freq(midinote, f_ref=440.0)
    p_mean, p_var, s_mean, s_var = getPitchFromJSON(d)
   
    err = p_mean - noteFreq
    return err, midinote, noteFreq, p_mean, p_var, s_mean 


def str_to_out(outp):
    err, midinote, pTag, pEst, pVar, salience = np.arange(6)
    return eval(outp)
if len(sys.argv) < ARGCOUNT + 1:
    print "usage: test_freesoundPitchAnalysis [.json file][pack][printfile][out1,out2,out3]"
else:
    jsonFile = sys.argv[1]
    pack = sys.argv[2]
    printFile = sys.argv[3]
    outp = sys.argv[4]
    #err, midinote, pTag, pEst, pitch_var, salience_mean = tag_vs_freesoundAnalysis(jsonFile, pack)
    res = tag_vs_freesoundAnalysis(jsonFile, pack)
   
    outp = outp.split(",")
    
    with open(printFile, "a") as outfile:
        for out in outp:
            outfile.write(str(res[str_to_out(out)])+"\t")
        #outfile.write(str(pitch_var)+"\t"+str(err)+"\n")   # x: pitch var; y: pEst - pTag
        #outfile.write(str(pTag)+"\t"+str(pEst)+"\n")        # x: pTag;      y: pEst
        #outfile.write(str(salience_mean)+"\t"+str(err)+"\n")
        outfile.write("\n")

