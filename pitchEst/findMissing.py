
def find_JSON_ESS(jsonFn, essFn, essNew):
    with open(essNew, 'w') as eN:
        with open(jsonFn) as jF:
            eN.write(jF.readline())   # skip first line

            jLineNr = 0
            jLine = jF.readline()
            while jLine !='':
                j = jLine.split('\t')[0]

                with open(essFn) as eF:
                    eF.readline()   #   skip first line
                    eLine = eF.readline()

                    while eLine != '':
                        e =  eLine.split('\t')[0].split('/')[-1].split('.ogg')[0]
                        if e == j:
                            eN.write(jLine);
                            break
                        eLine = eF.readline();
                    if eLine == '':
                        print "no match for line: "+str(jLineNr+2)+"\n\t"+j
                jLine = jF.readline();
                jLineNr += 1

def find_ESS_JSON(essFn, jsonFn, essNew):
    with open(essNew, 'w') as eN:
        with open(essFn) as eF:
            eN.write(eF.readline())   # skip first line
            
            eLineNr = 0
            eLine = eF.readline();
            while eLine != '':
                e = eLine.split('\t')[0].split('/')[-1].split('.ogg')[0]
                
                with open(jsonFn) as jF:
                    jF.readline()   # skip first line
                    jLine = jF.readline()

                    while jLine != '':
                        j = jLine.split('\t')[0]
                        if j == e:
                            eN.write(eLine);
                            break;
                        jLine = jF.readline()
                    if jLine == '':
                        print "no match for line: "+str(eLineNr+2)+"\n\t"+e
                eLine = eF.readline()
                eLineNr += 1


def compareLines(essFn, jsonFn):
    with open(essFn) as eF:
        eF.readline() 
        with open(jsonFn) as jF:
            jF.readline()
            eL = eF.readline()
            jL = jF.readline()
            while eL != '' and jL != '':
                if eL.split('\t')[0].split('/')[-1].split('.ogg')[0] != jL.split('\t')[0]:
                    print "no match!"
                eL = eF.readline();
                jL = jF.readline()
            if eL != '' or jL != '':
                print "more error!"
