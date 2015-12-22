#! /usr/bin/python2
'''

'''

import sys, os

ARGCOUNT = 5    # .json file, outdir, tokenfile, fieldsfile, descriptorsfile
hq = False

argv = sys.argv
if len(argv) < ARGCOUNT+1:
    print "usage: downloadFreesounds [*.json][output dir][tokenfile][fieldsfile][descriptorfile]"
else:

    # read token:
    tokenfile=open(argv[3])
    token = tokenfile.read()
    print "Token: "+token
    token = token[:len(token)-1]    # get rid of \n

    # read fields:
    fieldsfile = open(argv[4])
    fields=fieldsfile.read()
    print "fields="+fields
    fields = "fields="+fields[:len(fields)-1]

    # read descriptors:
    descfile = open(argv[5])
    desc=descfile.read()
    print "descriptors="+desc
    desc = "descriptors="+desc[:len(desc)-1]


    inputFile = argv[1]
    outdir = argv[2]+inputFile.split('/')[-1].split('.')[0]
    os.system('mkdir '+outdir)
    import json

    with open(inputFile) as infile:
        data = json.load(infile)
    
    N = data['count']
    print "found: "+str(N)+" sounds"
    print "now downloading..."

    soundsDld = 0
    pagenr = 0
    while soundsDld < N:
        page = data.items()[2][1]
        for snd in page:
            if hq:
                preview_type = 'preview-hq-ogg'
            else:
                preview_type = 'preview-lq-ogg'
            url = snd['previews'][preview_type];
            print url         
 
            # download sound: 
            os.system('wget -O'+'"'+outdir+'/'+snd['name']+'.ogg"'+' '+url);
            # write data to json file:
            os.system('touch "'+outdir+'/'+snd['name']+'.json"')            
            with open(str(outdir+'/'+snd['name']+'.json'), 'w') as outfile:
                json.dump(snd, outfile)
    
            '''
            inputFilename = inputFile.split('/')
            if pagenr < 10:
                inputFilename = inputFilename[-1].split('.')[-2]+"_page_0"+str(pagenr)+".json"
            else:
                inputFilename = inputFilename[-1].split('.')[-2]+"_page_"+str(pagenr)+".json"
            os.system('cp '+inputFile+' '+outdir+'/'+inputFilename);
            '''
        # get next page:
        if type(data['next']) == unicode:   # is there a next page?
            print "Next page: "+data['next']
            os.system('wget -qO'+'"'+inputFile+'" "'+data['next']+'&format=json&token='+token+'"')
            with open(inputFile) as infile:
                data = json.load(infile)
            pagenr += 1
        else:
            break
    
    os.system('cp '+inputFile+' '+outdir);
