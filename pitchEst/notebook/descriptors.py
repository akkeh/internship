import os, sys
import numpy as np

import essentia as ess
import essentia.standard as esstd

def essDescriptors(dirname, window='hann', M=2048, H=1024, zp=0):
    # pitch:
    pYin = esstd.PitchYinFFT(frameSize=M);
    
    # declare descriptors:
    pSal = esstd.PitchSalience()
    Centr = esstd.Centroid();
    HFC = esstd.HFC(); 
    Flux = esstd.Flux();
    eDur = esstd.EffectiveDuration();
    logatt = esstd.LogAttackTime();
    rollOff = esstd.RollOff();
    specContr = esstd.SpectralContrast(frameSize=M, sampleRate=44100);
    Inharm = esstd.Inharmonicity();
    specComp = esstd.SpectralComplexity();
    tctotot = esstd.TCToTotal();
    strongP = esstd.StrongPeak();
    triStim = esstd.Tristimulus();
    dynComp = esstd.DynamicComplexity();

    # framing and windowing stuff:
    spec = esstd.Spectrum();
    win = esstd.Windowing(type=window, zeroPadding=zp);
    Env = esstd.Envelope();
    SpecPeaks = esstd.SpectralPeaks();
    HarmPeaks = esstd.HarmonicPeaks();
    
    pool = ess.Pool()
    # list files:
    files = 0
    filenames = [];
    pTag = [];
    print "listing files"
    with open('./results/' + dirname.split('/')[-2] + '_ESS.txt') as f:
        f.readline()    # skip first line
        line = f.readline();
        while line != '':
            filenames.append(line.split('\t')[0].split('/')[-1])
            pTag.append(float(line.split('\t')[4]));  
    
            line = f.readline();
            files += 1 

    print "Found " + str(files) + " files in directory: " + dirname
    filecount = 0

    for filename in filenames:
        print "file: " + str(filecount+1) + " / " + str(files)
        pool.add('names', filename)
        # load, cut and window the audio:
        loader = esstd.MonoLoader(filename = dirname+filename)
        x = loader();
        env = Env(x);

        N = len(x)
        
        if N / 2 != N / 2.:
            x = ess.array(np.append(x, np.zeros(1)));
            N = N+1
        
        
        fc = esstd.FrameCutter(frameSize=M, hopSize=H);
        frames = int((N-M) / H);

        # initiate empty arrays:
        pitch = []; conf = [];
        psal = []; centroid = []; hfc = []; flux = []; 
        rolloff = []; speccontr = []; inharm = [];
        speccomp = []; strongp = []; 
        tristim0 = []; tristim1 = []; tristim2 = [];

        for m in range(frames):
            frame = fc(x)
            mX = spec(win(frame))
        
            # pitchYinFFT:
            pYinPitch, pYinConf = pYin(mX)
            pitch.append(pYinPitch);
            conf.append(pYinConf);
            
            psal.append(pSal(mX));                              # salience
            centroid.append(Centr(mX))                          # centroid
            hfc.append(HFC(mX));                                # dynamic complexity      
            flux.append(Flux(mX))                               # flux
            rolloff.append(rollOff(mX));                        # rolloff
            speccontr.append(specContr(mX));                    # spectral contrast
            # inharmonicity:
            specp = SpecPeaks(mX)
            harmp = HarmPeaks(specp[0][1:], specp[1][1:], pYinPitch);
            inharm.append(Inharm(harmp[0], harmp[1]));
            speccomp.append(specComp(mX));                      # spectral complexity
            strongp.append(strongP(mX));                        # StrongPeak
            # Tristimulus:
            tristim = triStim(harmp[0], harmp[1]);
            tristim0.append(tristim[0]); 
            tristim1.append(tristim[1]); 
            tristim2.append(tristim[2]); 
            

        # pitchYin:
        pool.add('pYinPitch.mean', np.mean(pitch))
        pool.add('pYinPitch.median', np.median(pitch));
        pool.add('pYinPitch.std', np.std(pitch));
        pool.add('pYinConf.mean', np.mean(conf));
        pool.add('pYinConf.median', np.median(conf));
        pool.add('pYinConf.std', np.std(conf));            
        # Salience:
        pool.add('salience.mean', np.mean(psal))
        pool.add('salience.median', np.median(psal))
        pool.add('salience.std', np.std(psal))
        # Centroid:
        pool.add('centroid.mean', np.mean(centroid))
        pool.add('centroid.median', np.median(centroid))
        pool.add('centroid.std', np.std(centroid))
        # HFC:
        pool.add('hfc.mean', np.mean(hfc))
        pool.add('hfc.median', np.median(hfc))
        pool.add('hfc.std', np.std(hfc))
        # Flux:
        pool.add('flux.mean', np.mean(flux))
        pool.add('flux.median', np.median(flux))
        pool.add('flux.std', np.std(flux))
        # EffectiveDuration: 
        pool.add('effectiveduration', eDur(x))
        # LogAttackTime:
        pool.add('logattacktime', logatt(env))
        # RollOff:
        pool.add('rolloff.mean', np.mean(rolloff))
        pool.add('rolloff.median', np.median(rolloff))
        pool.add('rolloff.std', np.std(rolloff))
        # SpectralContrast:
        pool.add('specralcontrast.mean', np.mean(speccontr))
        pool.add('spectralcontrast.median', np.median(speccontr))
        pool.add('spectralcontrast.std', np.std(speccontr))
        # Inharmonicity:
        pool.add('inharmonicity.mean', np.mean(inharm))
        pool.add('inharmonicity.median', np.median(inharm))
        pool.add('inharmonicity.std', np.std(inharm))
        # SpectralComplexity:
        pool.add('spectralcomplexity.mean', np.mean(speccomp));
        pool.add('spectralcomplexity.median', np.median(speccomp));
        pool.add('spectralcomplexity.std', np.std(speccomp));
        # TCToTotal:
        pool.add('tctototal', tctotot(env))
        # StrongPeak
        pool.add('strongpeak.mean', np.mean(strongp))            
        pool.add('strongpeak.median', np.median(strongp))            
        pool.add('strongpeak.std', np.std(strongp))            
        # Tristimulus
        pool.add('tristimulus.0.mean', np.mean(tristim0))        
        pool.add('tristimulus.0.median', np.median(tristim0))        
        pool.add('tristimulus.0.std', np.std(tristim0))        
        pool.add('tristimulus.1.mean', np.mean(tristim1))        
        pool.add('tristimulus.1.median', np.median(tristim1))        
        pool.add('tristimulus.1.std', np.std(tristim1))        
        pool.add('tristimulus.2.mean', np.mean(tristim2))        
        pool.add('tristimulus.2.median', np.median(tristim2))        
        pool.add('tristimulus.2.std', np.std(tristim2))        
        # DynamicComplexity:
        pool.add('dynamiccomplexity', dynComp(x))

        pool.add('ptag', pTag[filecount]);
        filecount += 1
    
    print pool.descriptorNames();
    return pool

def essExtractor(dirname):
    Extr = esstd.Extractor(rhythm=False, midLevel=False);
    # list files:
    filenames = [];
    pTag = [];
    print "listing files"
    with open('./results/' + dirname.split('/')[-2] + '_ESS.txt') as f:
        f.readline()    # skip first line
        line = f.readline();
        while line != '':
            filenames.append(line.split('\t')[0].split('/')[-1])
            pTag.append(float(line.split('\t')[4]));  
            line = f.readline();
    print "calculating descriptors"
    pool = ess.Pool()
    N = len(filenames);
    n = 0
    for filename in filenames:
        print "file: " + str(n+1) + " of " + str(N)
        # load the audio:
        loader = esstd.MonoLoader(filename = dirname+filename)
        x = loader();
        extr = Extr(x);
        extr.add('name', filename)
        extr.set('annotated_pitch', pTag[n])
        aExtr = esstd.PoolAggregator(defaultStats = ['mean', 'median' ])(extr)
        for dName in aExtr.descriptorNames():
            pool.add(dName, aExtr[dName])   
        n += 1
    return pool

def calcAll(test=0):
    pool = False
    dirs = [ 'carlos/', 'good-sounds/', 'modularsamples/', 'philharmonia/', 'iowa/' ] 
    if test != 0:
        dirs = ['carlos/']
    for dirname in dirs:
        if pool:
            pool.merge(essExtractor('./sounds/'+dirname), 'append')
        else:
            pool = essExtractor('./sounds/'+dirname);
        

    esstd.YamlOutput(filename = './results/descriptors.json', format='json')(pool)


if len(sys.argv) > 1:
    try:
        dataIn = esstd.YamlInput(filename='./results/descriptors.json')
        pool = dataIn();
    except:
        calcAll()
        pool = dataIn();
