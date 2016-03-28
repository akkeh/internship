import numpy as np
import essentia as ess

def readJSONS(dirname):
    pool = ess.Pool()

    for fn in os.listdir(dirname):
        yamlin = esstd.YamlInput(filename = dirname + fn)
        jsonPool = yamlin()
        
        for dname in jsonPool.descriptorNames():
            pool.add(dname, jsonPool[dname])

    return pool

def sortPool(static, sort):
        
    pool = ess.Pool()
    for name in static['name']:
        i = 0;
        while sort['name'][i] != name[0].split('.ogg')[0]:
            i+=1
        for dname in sort.descriptorNames():
            pool.add(dname, sort[dname][i])

    return pool


csN = 470
gsN = 113

phN = 2973
iwN = 639

#print "read "+str(csN+gsN)+" lines of Freesound data"
#print "read "+str(phN+iwN)+" lines of non-Freesound soundfile data"

#print "Total amount of sounds assessed: "+str(csN+gsN + phN+iwN)

# get all data from the essentia Extractor:
print "importing functions"
from descriptors import *
print "loading data"
pool = loadData()

locPool = ess.Pool()
for dname in pool.descriptorNames():
    for val in pool[dname][:csN+gsN]:
        locPool.add(dname, val)

print "loading Freesound data"
try:
    frsDataIn = esstd.YamlInput(filename='./results/freesoundData.json')
    frsPool = frsDataIn();
except:
    carlosFrs = readJSONS('./sounds/carlosJson/')
    goodsoundsFrs = readJSONS('./sounds/good-soundsJson/')

    frsPool = ess.Pool()

    for dname in carlosFrs.descriptorNames():
        for val in carlosFrs[dname]:
            frsPool.add(dname, val)

    for dname in goodsoundsFrs.descriptorNames():
        for val in goodsoundsFrs[dname]:
            frsPool.add(dname, val)

frsPool = sortPool(locPool, frsPool)

loadImpr = esstd.YamlInput(filename='./results/improvements.json')
imprPool = loadImpr();
print "done"
