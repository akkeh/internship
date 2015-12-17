#! /usr/bin/python2
import sys, os

ARGCOUNT = 2    # .json file, output dir
hq = False

argv = sys.argv

# read token:
tokenfile=open('.FreesoundAuthToken.txt')
token = tokenfile.read()
print "Token: "+token
token = token[:len(token)-1]    # get rid of \n

# read fields:
fieldsfile = open('fields.txt')
fields=fieldsfile.read()
print "fields="+fields
fields = "fields="+fields[:len(fields)-1];

# read descriptors:
descfile = open('desc.txt')
desc=descfile.read()
print "descriptors="+desc
desc = "descriptors="+desc[:len(desc)-1]


if len(argv) < ARGCOUNT+1:
    print "usage: downloadPacks [*.json][output directory]"
else:
    inputFile = argv[1]
    outdir = argv[2]
    os.system('mkdir '+outdir)
    os.system('mkdir '+outdir+'tmp')
    import json

    with open(inputFile) as infile:
        data = json.load(infile)
    
    numberOfPacks = data['count']
    print "found: "+str(numberOfPacks)+" packs"
    print "now downloading..."

    packsDld = 0
    while packsDld < numberOfPacks:
        page = data.items()[2][1]
        for pack in page:
            packId = pack['id']
            # download .json file for pack:
            url = pack['sounds']+"?format=json&token="+token+"&"+fields+"&"+desc
           
            print "Getting sounds from pack: "+str(packId)#+" ("+url+")" 
            os.system('wget -qO"'+outdir+'tmp/'+'pack'+str(pack['id'])+'.json" '+'"'+url+'"');
            # download sounds here!
                        
            packsDld += 1
            print "Downloaded: "+str(packsDld)+" / "+str(numberOfPacks)
        
        # get next page
        if type(data['next']) == unicode:   # is there a next page?
            print "Next page: "+data['next']+'&token='+token
            os.system('rm '+outdir+'tmp/page.json')
            os.system('wget -qO'+'"'+outdir+'tmp/page.json" '+'"'+data['next']+'&token='+token+'"')
         
            with open(outdir+'tmp/page.json') as infile:
                data = json.load(infile)
        else:
            break
