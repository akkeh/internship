import binascii as bascii

def get_dtime(adata, rptr):
    '''
        source: https://groups.google.com/forum/#!msg/alt.sources/eRG2bL3Re-k/FvRLrRl0RiIJ
            Will Ware
    '''
    dtime = 0
    for i in range(4): 
        x = ord(bascii.a2b_hex(adata[rptr]))
        dtime = (dtime << 7) + (x & 0x7F)
        rptr += 1
        if not (x & 0x80):
            return dtime, rptr

def get_message(adata, rptr):
    eventT = bascii.a2b_hex(adata[rptr])
    if eventT == '\xff': # sys exclusive stuff
        rptr+=1
        msgType = adata[rptr]
        rptr+=1
        msgSize = ord(bascii.a2b_hex(adata[rptr]))
        return 'ff:'+msgType, rptr+msgSize+1
    elif ord('\xc0') <= ord(eventT) and ord(eventT) <= ord('\xcf'):
        rptr+=2
        return hex(ord(eventT)), rptr
    elif ord('\xa0') <= ord(eventT) and ord(eventT) < ord('\xff'):
        rptr+=3
        return hex(ord(eventT)), rptr
    elif ord('\x90') <= ord(eventT) and ord(eventT) <= ord('\x9f'): # note on
        rptr+=1
        note = int(adata[rptr], 16)
        rptr+=1
        vel = int(adata[rptr], 16)
        rptr+=1
        print "Note: " + str(note) + "(" + str(vel) + ")"
        return "note:" + str(note) +"(" + str(vel) + ")", rptr
    else:
        print "unknown"
        rptr+=2
        return 'unk'+hex(ord(eventT)), rptr

def readMIDI(filename):
    # obtain MIDI data:
    with open(filename) as f:
        line = f.readline()
        # check for MThd:
        al = bascii.hexlify(line)
        if al[:8] != bascii.hexlify('MThd'):
            print "File is not a MIDI file?"
            return -1
        adata = [];
        while line != '':
            for i in range(len(al) / 2):
                adata.append(al[i*2:i*2+2])
            al = bascii.hexlify(line)
            line = f.readline();
    
    rptr = 4
    # Header:
    hdrSize = int(adata[rptr] + adata[rptr+1] + adata[rptr+2] + adata[rptr+3], 16)
    rptr += 4

    if hdrSize != 6:
        print "Not a standard MIDI file?"
        return -1
   
    fmt = adata[rptr]+adata[rptr+1];
    rptr+=2
    
    nTracks = int(adata[rptr] + adata[rptr+1], 16)
    rptr+=2
    print "Found %d tracks" % nTracks

    ppq = int(adata[rptr]+adata[rptr+1], 16)
    rptr+=2
    print "PPQ: %d" % ppq

    # Track chunk:
    if adata[rptr]+adata[rptr+1]+adata[rptr+2]+adata[rptr+3] != bascii.hexlify('MTrk'):
        print "Did not find track?"
        return -1
    rptr+=4

    trkSize = int(adata[rptr] + adata[rptr+1] + adata[rptr+2] + adata[rptr+3], 16)
    rptr+=4
    print "Track size: %d" % trkSize 
      
    events = [];    # dtime, message
    itime = 0
    i = 0
    while rptr < len(adata):
        dtime, rptr = get_dtime(adata, rptr)
        itime += dtime
        dat = adata[rptr]
        msg, rptr = get_message(adata, rptr)
        events.append([dtime, msg, dat]);
        #print "time: %d\tmsg: %s" % (itime, msg)
    return events

