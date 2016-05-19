import numpy as np
import sys, os

path = os.path.dirname(__file__)

def readMIDIcsv(mfile):
    os.system(path+'/midi-csv/midicsv-1.1/midicsv ' + mfile + ' ./tmp/MIDICVS.cvs')
    with open('./tmp/MIDICVS.cvs') as mf:
        lines = mf.readlines();
    os.system('rm -f ./tmp/MIDICVS.cvs');
    csv = [];
    for line in lines:
        csv.append(line.split(', '))
    return csv 

def getMetaData(csv):
    ppq = int(csv[0][5])
    tempo = 500000
    for e in csv:
        if e[2] == 'Tempo':
            tempo = int(e[3])
            break;
    return ppq, tempo

def createTrack(csv):
    track_count = int(csv[0][4])
    track_data = [];
    for i in range(track_count):
        track_data.append([])
    
    for event in csv:
        if event[0] != '0':
            track_data[int(event[0])-1].append(event)

    event_count = 0
    for track in track_data:
        event_count += len(track)

    events = [];
    while event_count > 0:
        ind = 0; least = 999999;
        for i in range(len(track_data)):
            if len(track_data[i]) > 0:
                if int(track_data[i][0][1]) < least:
                    ind = i
                    least = int(track_data[i][0][1])
        events.append(track_data[ind][0])
        track_data[ind] = track_data[ind][1:]
        event_count -= 1  
    return track_count, events

def createNoteList(csv):
    track_count, events = createTrack(csv)
    notes = np.zeros(shape=(track_count, 127), dtype=int)
    notes[:] = -1

    i = 0
    noteList = [];
    for event in events:
        if event[2] == 'Note_on_c':
            track = int(event[0]) - 1
            note = int(event[4])
            if int(event[-1]) > 0:
                # note on
                # start time, stop time, track nr, note nr, vel
                noteList.append([int(event[1]), 0, track, note, int(event[-1])])
                notes[track][note] = i
                
                i+=1
            else:
                # note off
                if notes[track][note] != -1:
                    noteList[notes[track][note]][1] = int(event[1])
                    notes[track][note] = -1

    return noteList 
        

def procEvent(event):
    if event[2].find('Note') > -1:
        dtime = int(event[1])
        note = int(event[4])
        vel = int(event[5])
        chn = int(event[3])
        print "%d:\tnote: %d\tvel: %d\tchn: %d" %(dtime, note, vel, chn)

 
