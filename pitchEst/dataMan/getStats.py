import os, sys
import numpy as np
ARGCOUNT = 1



def getStat(fn, stat):
    with open(fn) as f:
        line = f.readline().split(',')
        i = 0
        for i in range(len(line)):
            if line[i] == stat:
                break;
        names = np.array([])
        vals = np.array([])
        line = f.readline() # read name
        while line != '':
            names = np.append(names, line.split('//')[1].split('\n')[0])
            line = f.readline().split('\t') # read val
            vals = np.append(vals, float(line[i]))
            line = f.readline() # read name
    return names, vals    

def getStats(fn):
    names = np.array([])
    stats = np.array([])
    with open(fn, 'rw') as f:
        line = f.readline()
        for name in line.split(','):
            names = np.append(names, name)
            stats = np.append(stats, 0)
        names[-1] = names[-1].split('\n')[0]
        line = f.readline()
        while line != '':
            line = f.readline()
            i = 0
            for val in line.split('\t')[:-1]: 
                stats[i] += float(val)
                i += 1
    output = np.ndarray(shape=(len(names), 2), dtype='|S32')
    i = 0
    for name in names:
        output[i] = (name, stats[i])
        i += 1
    return output


if len(sys.argv) < ARGCOUNT + 1:
    print "usage: getStats.py [file]"
else:
    fn = sys.argv[1]
    stats = getStats(fn)
    
    with open(fn, 'a') as f:
        f.write('\n total:\n')
        for val in stats:
            f.write(val[0]+":\t\t"+val[1]+"\n")
