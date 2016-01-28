import numpy as np

def readData(fn):
    '''
    Read data from the results directory. Formatted:
    fields: comma separated.
    Data:   '\t' separeted.
    '''
    with open(fn) as f:
        N = 0;  # linecount
        fields = f.readline().split(',')
        M = len(fields)    # collum count
        while f.readline() != '':
            N += 1              
    
    data = np.ndarray(shape=(M, N+1), dtype='|S32')   # create data matrix
    
    col = 0
    for field in fields:
        d = np.array([], dtype='|S32')
        with open(fn) as f:
            f.readline();   # skip first line
            
            d = np.append(d, field)
            line = f.readline();
            while line != '':
                d = np.append(d, line.split('\t')[col])
                line = f.readline()
            data[col] = d
            col += 1           
    return data


def getField(data, field):
    M = len(data)
    out = np.array([])
    for col in range(M):
        if data[col][0] == field:
            for row in np.arange(len(data[col]) - 1)+1:
                out = np.append(out, data[col][row])
    return out
