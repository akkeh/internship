#! /usr/bin/python2

import numpy as np
import sys

def seeveData(dataFile, dat):
    '''
    name,err,absErr,midinote,pTag,pEst,pEstVar,salience
    '''
    y = np.array([])
    with open(dataFile) as d:
        labels = d.readline().split('\n')[0].split(',')
        #print "labels: ", labels
        # find row:
        row = 0 
        while  row < len(labels) and str(labels[row]) != str(dat):
            row += 1
        if row == len(labels):
            return y 
        else:
            line = d.readline()
            while line != '':
                datapoint = line.split('\n')[0].split('\t')[row]
                if str(dat) == 'name':
                    y = np.append(y, datapoint)
                else:
                    y = np.append(y, float(datapoint))
                line = d.readline()
    return y 


def plot2d(dataFile, desc_x, desc_y):
    x = seeveData(dataFile, desc_x)
    y = seeveData(dataFile, desc_y)
   
    plt.plot(x, y)
    return x, y 
