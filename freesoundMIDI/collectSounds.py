import os
import numpy as np
import json

import essentia as ess
import essentia.standard as esstd

import util as ut

descriptors = [
 'lowLevel.barkbands_kurtosis.mean',
 'lowLevel.barkbands_kurtosis.var',
 'lowLevel.barkbands_skewness.mean',
 'lowLevel.barkbands_skewness.var',
 'lowLevel.barkbands_spread.mean',
 'lowLevel.barkbands_spread.var',
 'lowLevel.dissonance.mean',
 'lowLevel.dissonance.var',
 'lowLevel.hfc.mean',
 'lowLevel.hfc.var',
 'lowLevel.spectral_centroid.mean',
 'lowLevel.spectral_centroid.var',
 'lowLevel.spectral_complexity.mean',
 'lowLevel.spectral_complexity.var',
 'lowLevel.spectral_crest.mean',
 'lowLevel.spectral_crest.var',
 'lowLevel.spectral_decrease.mean',
 'lowLevel.spectral_decrease.var',
 'lowLevel.spectral_energy.mean',
 'lowLevel.spectral_energy.var',
 'lowLevel.spectral_energyband_high.mean',
 'lowLevel.spectral_energyband_high.var',
 'lowLevel.spectral_energyband_low.mean',
 'lowLevel.spectral_energyband_low.var',
 'lowLevel.spectral_energyband_middle_high.mean',
 'lowLevel.spectral_energyband_middle_high.var',
 'lowLevel.spectral_energyband_middle_low.mean',
 'lowLevel.spectral_energyband_middle_low.var',
 'lowLevel.spectral_flatness_db.mean',
 'lowLevel.spectral_flatness_db.var',
 'lowLevel.spectral_flux.mean',
 'lowLevel.spectral_flux.var',
 'lowLevel.spectral_kurtosis.mean',
 'lowLevel.spectral_kurtosis.var',
 'lowLevel.spectral_rms.mean',
 'lowLevel.spectral_rms.var',
 'lowLevel.spectral_rolloff.mean',
 'lowLevel.spectral_rolloff.var',
 'lowLevel.spectral_skewness.mean',
 'lowLevel.spectral_skewness.var',
 'lowLevel.spectral_spread.mean',
 'lowLevel.spectral_spread.var',
 'lowLevel.spectral_strongpeak.mean',
 'lowLevel.spectral_strongpeak.var',
 'sfx.inharmonicity.mean',
 'sfx.inharmonicity.var',
 'sfx.oddtoevenharmonicenergyratio.mean',
 'sfx.oddtoevenharmonicenergyratio.var'
];
tags = ['single-note']

# read token:
with open('auth_token') as tf:
    token = tf.readline()[:-1]

# analyse starting sound:
def analyseSound(filename):
    loader = esstd.MonoLoader(filename=filename);
    Extr = esstd.Extractor(rhythm=False);   # rhythm=False else an error is thrown?!
    
    x = loader();
    x = ut.trimSilence(x)
    desc = Extr(x)
    defStats = ['mean', 'var']
    aggrPool = esstd.PoolAggregator(defaultStats = defStats)(desc)

    return aggrPool

def changeL(name):
    if name.split('.')[0] == 'lowLevel':
        return name[:3] + 'l' + name[4:]
    else:
        return name

# find similar sounds:
def similSounds(iname, startingPool, targetPitch, descr=descriptors, tags=tags, max_tries=10):
    url = 'http://www.freesound.org/apiv2/search/combined/?'
    filters = '&filter='
    for tag in tags:
        filters = filters + 'tag:' + tag + ' '

    midinote = ut.freq2midi(targetPitch)
    pitchrange = '[' + str(ut.midi2freq(midinote-1)) + ' TO ' + str(ut.midi2freq(midinote+1)) + ']'
    dfilters = '&descriptors_filter=lowlevel.pitch.mean:' + pitchrange
    target = '&target='
    for dname in descr:
        if type(startingPool[dname]) == type(1.):
            if str(startingPool[dname]).find('e') == -1:
                target = target + changeL(dname) + ':' + str(startingPool[dname]) + ' AND '

    target = target 
    fields = '&fields=id,previews,analysis&descriptors=lowlevel.pitch.mean'
     
    url = url + 'token=' + token + target + fields + filters + dfilters

    # download:
    data = '';
    downloading = True; i=0
    while downloading and i < max_tries:
        os.system('wget -O ./tmp/' + iname + '.json "' + url + '"');
        try:
            with open('./tmp/' + iname + '.json') as jf:
                data = json.load(jf)
            downloading = False
        except:
            i += 1 
    
    if data == '':
        print 'error downloading after %d tries' % max_tries
    else:
        return data

def downloadAndLoad(url, name, max_tries=10):
    data = ''; i=0
    while data == '' and i < max_tries:
        os.system('wget -O ./tmp/' + name + ' "' + url + '"');
        try:
            with open('./tmp/' + name) as jf:
                data = jf.load()
        except:
            i+=1
    return data

def downloadSoundAndLoad(url, name, max_tries=10):
    # download sound:
    x = np.array([]); i = 0
    while len(x) == 0 and i < max_tries:
        os.system('wget -O ' + name + ' "' + url + '"');
        try:
            loader = esstd.MonoLoader(filename=name)
            x = loader()
        except:
            i += 1
    return x

def checkSound(x, pitch, M=2048, H=1024):
    pYin = esstd.PitchYinFFT(frameSize=M)
    win = esstd.Windowing(size=M)
    spec = esstd.Spectrum();

    x = ut.trimSilence(x)
    pitches = np.array([]); confs = np.array([])
    for frame in esstd.FrameGenerator(x, frameSize=M, hopSize=H):
        p, c = pYin(spec(win(frame)))
        pitches = np.append(pitches, p)
        confs = np.append(confs, c)
    mTar = ut.freq2midi(pitch)
    mSnd = ut.freq2midi(np.median(pitches))
    if abs(mTar - mSnd) < 1:
        return True
    else:
        return False

def selectSound(data, targetPitch, max_tries=10):
    N = data.items()[0][1]
    sounds = data.items()[0][1]
    n = 0; sndid = '';
    while n < N: 
        for snd in sounds:
            estPitch = snd['analysis']['lowlevel']['pitch']['mean']
            if abs(ut.freq2midi(targetPitch) - ut.freq2midi(estPitch)) < 1:
                sndid = str(snd['id'])
                sndurl = snd['previews']['preview-hq-ogg']
                x = downloadSoundAndLoad(sndurl, './tmp/'+sndid+'.ogg')
                if checkSound(x, targetPitch):
                    break;
                else:
                    sndid = ''
            n += 1
        if sndid == '':
            print "next Page"
            # get next page:
            nexturl = data.items()[3][1] + '&token=' + token;
            data = downloadAndLoad(nexturl, 'next.json')
        else:
            break;

    return './tmp/' + sndid + '.ogg'

# combine
def getSound(iname, startingFilename, targetPitch, max_tries=10):
    startPool = analyseSound(startingFilename)
    data = similSounds(iname, startPool, targetPitch, max_tries=max_tries)
    soundname = selectSound(data, targetPitch, max_tries=max_tries)
    
    return soundname


