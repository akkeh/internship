#! /usr/bin/python2
ARGCOUNT = 2    # file containing values; bins

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < ARGCOUNT+1:
    print "usage: [infile][binwidth]"
else:
    valFile = sys.argv[1]
    bins = int(sys.argv[2])
    ths = np.array([])
    for th in sys.argv[3:]:
        print "th: "+th
        ths = np.append(ths, float(th))
  
    with open(valFile) as values:
        line = values.readline()
        label = line
        vals = np.array([])
        while line != '':
            vals = np.append(vals, float(line))
            line = values.readline()


valmax = max(vals)
valmin = min(vals)
 
plt.hist(vals, bins=bins); 

N_lt_th = np.zeros(len(ths))
i = 0
for th in ths:
    N_lt_th[i] = len(np.where(abs(vals) < th)[0])
    print "vals < "+str(th)+" : "+str(N_lt_th[i] )
    i += 1



