#! /usr/bin/python2
ARGCOUNT = 4
'''
    todo:
    -   reference pitch from description in modularsamples or good-sounds?
'''

import os, sys
import json
import numpy as np
th = -999
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
    
    return eval(note)   # noteName_to_noteNr()

# JSON  -----------------------------------------------
def getJsonData(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)
    return data

def getNoteFromJSON(d, pack):
    '''
        
    '''
    nn = -1
    octave = -1
    if pack == 'carlos':
        note = d['name'].split(" ")[1]
        if len(note) == 1:
            note = note+d['name'].split(" ")[2]
        if len(note) > 4 or len(note) < 2:   # notename not in filename!
            return -1
        elif note.find("-") != -1:
            nn = note.split("-")[0]
        else:
            nn = note[0] 
        if note.find("#") == -1:
            nn = noteName_to_noteNr(nn)
        else:
            nn = noteName_to_noteNr(nn[0]) + 1
        octave = int(note[-1])
        midi = nn + (12 * octave)
    # fi pack == 'carlos'  
    
    elif pack == 'modularsamples':
        tags = d['tags']
        i = 0
        note = tags[i]
        while note.find('midi') == -1 and i < len(tags):
            note = tags[i]
            i += 1
        if note == '':
            return -1   # notename not in tags!
        else:
            midi = int(note.split('-')[-1])
    # fi pack == 'modularsamples'
    
    elif pack == 'good-sounds':
        note = d['name'].split(" ")[-1]
        if len(note) > 4:
            return -1
        nn = noteName_to_noteNr(note[0])
        if note.find('#') != -1:
            nn += 1
        octave = int(note[-1])
        midi = nn + (12 * octave)
    # fi pack== 'good-sounds'
   
    else:
        return -1 
    return midi # getNoteFromJSON()

def getFrefFromJSON(d, pack=''):
    desc = d['description']
    # search for reference pitch in description:
    opt = ['Hz', 'hz', 'HZ'];
    i = -1; j = 0;
    while i == -1 and j < len(opt):
        i = desc.find(opt[j])
        j += 1
    if i != -1:
        if desc[i-1] == " ":
            i = i - 1
        fref = (int(desc[i-3]) * 10 + int(desc[i-2])) * 10 + int(desc[i-1]);   # assume fref is 3 digits
        return fref
    return -1
    
         
#def getNoteFromFilename(filename):


def getPitchFromJSON(d):
    '''
    '''
    pitch = d['analysis']['lowlevel']['pitch']
    salience = d['analysis']['lowlevel']['pitch_salience']
    
    return pitch['mean'], pitch['var'], salience['mean'], salience['var']


def tag_vs_freesoundAnalysis(jsonFile, pack=""):
    '''
    
    '''
    d = getJsonData(jsonFile)
    
    midinote = getNoteFromJSON(d, pack)
    if midinote == -1:
        with open('./unpitched.txt', 'a') as upsl:
            upsl.write(str(d['name'])+"\n")
        return 0
    fref = getFrefFromJSON(d, pack)
    if fref == -1:
        fref = 440.0
    pTag = MIDInote_to_freq(midinote, fref=fref)
    pEst, pEstVar, salience, salienceVar = getPitchFromJSON(d)
   
    err = pEst - pTag 
    absErr = abs(err)
    if th > 0:
        if abs(err) > th:
            with open('./bigErr.txt', 'a') as bE:
                bE.write(str(d['name'])+"\terr: "+str(err)+"\ttag: "+str(pTag)+"\tfound: "+str(pEst)+"\n")
    return d['name'], err, absErr, midinote, pTag, pEst, pEstVar, salience, salienceVar


def str_to_out(outp):
    name, err, absErr, midinote, pTag, pEst, pEstVar, salience = np.arange(8)
    return eval(outp)

if len(sys.argv) < ARGCOUNT + 1:
    print "usage: test_freesoundPitchAnalysis [.json file][pack][printfile][out1,out2,out3]"
else:
    jsonFile = sys.argv[1]
    pack = sys.argv[2]
    printFile = sys.argv[3]
    if printFile.find('JSON') > -1:
        outp = sys.argv[4] 

        res = tag_vs_freesoundAnalysis(jsonFile, pack)
        if res == 'unpitched':
            print "Unpitched sound!"
        else:
             
            outp = outp.split(",")
            
            with open(printFile, "a") as outfile:
                
                for out in outp:
                    outfile.write(str(res[str_to_out(out)])+"\t")
                outfile.write("\n")



