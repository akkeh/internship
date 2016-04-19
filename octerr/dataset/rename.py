#! /usr/bins/python2
import sys, os

ARGCOUNT = 3

argv = sys.argv

def nn2midi(nn):
    Ab, A, Bb, B, C, Db, D, Eb, E, F, Gb, G = range(12)
    try:
        return eval(nn)
    except:
        return 'None'

def midi_IOWA(filename):
    if filename.find('.aif') == -1:
        print "error %s" % filename
    else:
        if filename.split('.')[-2] == 'stereo' or filename.split('.')[2] == 'mono':
            nn = filename.split('.')[-3]
        else:
            nn = filename.split('.')[-2]
        if len(nn) > 3:
            print "error: %s" % filename
        else:
            octave = nn[-1]
            midinote = nn2midi(nn[0])
            if nn[-2] == 'b':
                midinote -= 1
            try:
                return midinote + ((int(octave)-1) * 12)    # midi_IOWA
            except:
                return 'None'

def midi_ph(filename):
    if filename.find('.mp3') == -1:
        print "error %s" % filename
    else:
        nn = filename.split('_')[1]
        if len(nn) > 3:
            print "error %s" % filename
        else:
            octave = nn[-1]
            midinote = nn2midi(nn[0])
            if nn[-2] == 's':
                midinote += 1
            try:
                return midinote + ((int(octave)-1) * 12)
            except:
                return 'None'

if len(argv) < ARGCOUNT+1:
    print "usage: rename [][]"
else:
    dirname = argv[1]
    source = argv[2]
    outdir = argv[3]
    for filename in os.listdir(dirname):
        print filename
        if source == 'iowa' or source == 'IOWA':
            midi = midi_IOWA(filename)

        if source == 'philharmonia' or source == 'ph':
            midi = midi_ph(filename)

        if midi < 10 and midi > -1:
            os.system('mv ' + dirname+filename + ' ' + outdir+'M0'+str(midi)+'_'+filename)
        else:    
            os.system('mv ' + dirname+filename + ' ' + outdir+'M'+str(midi)+'_'+filename)




            
