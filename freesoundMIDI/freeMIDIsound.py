import numpy as np
import os, sys

import essentia.standard as esstd

import util as ut
import readMIDI_csv as rMIDI
import similSounds as simSnd

ARGCOUNT = 2

FS = 44100
NORMALISE = 1

def ticks_to_samples(ticks, ppq, tempo, fs=44100):
    return int((float(ticks) / ppq * tempo) * 1E-6 * fs)


def envelope(x, n0, nN):
    N = nN - n0
    y = np.zeros(N)
    if len(x) <= N:
        y[:len(x)] = x
    else:
        y = x[:N]
    return y

if len(sys.argv) < ARGCOUNT + 1:
    print "usage: freeMIDIsound [midifile][starting-sound-id-file]"
else:
    # reading MIDI file
    midiFile = sys.argv[1]

    csv = rMIDI.readMIDIcsv(midiFile)
    ppq, tempo = rMIDI.getMetaData(csv)
    noteL = rMIDI.createNoteList(csv)
    track_count, events = rMIDI.createTrack(csv)
   
    # getting the sounds:
    sndFiles = []; iNames = []; descs = [];
    for i in range(track_count):
        print "Track %d:\t%s" % (i, os.path.basename(sys.argv[2+i]))
        sndFiles.append(sys.argv[2 + i])
        iNames.append(os.path.basename(sndFiles[-1]).split('.')[-2])
        descs.append(simSnd.frsExtractor(sndFiles[-1]))

    # read events and gather sounds:
    sndTrk = [];
    for note in noteL:
        t0 = note[0]
        dur = note[1]
        track = note[2]
        pitch = note[3]
        vel = note[4]
        sndTrk.append([t0, dur, simSnd.chooseSound(iNames[track], descs[track], ut.midi2freq(pitch))])

    # create piece:
    max_ticks = sndTrk[-1][1]
    # ppq (tick per quarter note)
    # tempo (ms per 1/4 note)
    length = ticks_to_samples(max_ticks, ppq, tempo, FS)

    music = np.zeros(length)   # ten seconds

    n = 0
    for snd in sndTrk:
        loader = esstd.MonoLoader(filename='./tmp/'+snd[2])
        x = ut.trimSilence(loader())
        if NORMALISE == 1:
            x = ut.normalise(x)
        
        t0 = snd[0]; tN = snd[1]
        x = envelope(x, ticks_to_samples(t0, ppq, tempo, FS), ticks_to_samples(tN, ppq, tempo, FS))
        music[ticks_to_samples(t0, ppq, tempo, FS):ticks_to_samples(tN, ppq, tempo, FS)] = x
       

wr = esstd.MonoWriter(filename='./output.wav');
wr(np.array(music, dtype='single'))
 
