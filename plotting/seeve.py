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
        print "labels: ", labels
        # find row:
        row = 0 
        while str(labels[row]) != str(dat) and row < len(labels):
            row += 1
        print row
        if row == len(labels):
            print "data not found!"
        else:
            line = d.readline()
            while line != '':
                print line
                datapoint = line.split('\n')[0].split('\t')[row]
                y = np.append(y, datapoint)
                line = d.readline()
    return y 



