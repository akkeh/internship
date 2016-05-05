import os
import numpy as np
import json

import essentia as ess
import essentia.standard as esstd

import util as ut 

# read token:
with open('auth_token') as tf:
    token = tf.readline()[:-1]

def frsExtractor(filename):
    loader = esstd.MonoLoader(filename=filename);
    Extr = esstd.Extractor(rhythm=False)    # rythm=False else an error is thrown?
    
    x = loader()
    desc = Extr(x)
    defStats = ['mean', 'var'];
    aggrPool = esstd.PoolAggregator(defaultStats = defStats)(desc)
    
    desc = ess.Pool()
    for d in descrs:
            desc.set(d, aggrPool[d])
 
    return desc

def changeLevel(dname):
    if dname.split('.')[0] == 'lowLevel':
        return dname[:3]+'l'+dname[4:]
    else:
        return dname

def findSimil(sndname, desc, pitch):
    fn = 'tmp/' + sndname + '_' + str(ut.freq2midi(pitch)) + '.json'
    url = 'http://www.freesound.org/apiv2/search/content/?'
    target=''
    for dname in desc.descriptorNames():
        if type(desc[dname]) == type(1.):
            if str(desc[dname]).find('e') == -1:
                target = target+ changeLevel(dname) +':' +str(desc[dname]) +' AND '

    target = target + 'lowlevel.pitch.mean:' + str(pitch)
    fields = '&fields=id,previews,analysis&descriptors=lowlevel.pitch.mean'
    #filters = '&filter=lowlevel.pitch.mean:
    url = url + "token=" + token + "&target=" + target + fields
    
    downloading =True
    while downloading:
        os.system('wget -O ' + fn + ' "' + url + '"');
        try:
            with open(fn) as jf:
                data = json.load(jf)
            downloading = False
        except:
            downlaoding = True

    return data 

def chooseSound(iName, desc, pTar):
    sSounds = findSimil(iName, desc, pTar)
    
    for i in range(20):
        sounds = sSounds.items()[2][1]
        for snd in sounds:
            nr = snd['id']
            pEst = snd['analysis']['lowlevel']['pitch']['mean']
            
            if abs(ut.freq2midi(pTar) - ut.freq2midi(pEst)) < 1:
                # download sound
                url = snd['previews']['preview-hq-ogg'] 
                os.system('wget -O ./tmp/snd' + str(nr) + '.ogg "' + url + '"');
                return 'snd'+str(nr)+'.ogg'

        nexturl = sSounds['next'] + '&token=' + token
        os.system('wget -O ./tmp/next.json "' + nexturl + '"');
        with open('./tmp/next.json') as jf:
            sSnounds = json.load(jf)
    print "ERROR DOWNLOADING SOUNDS"

'''
def chooseSound(iName, desc, pTar):
    # desc = frsExtractor(last_sound)
    # name = os.path.basename(last_sound)
    data = findSimil(iName, desc, pTar)
    
    for i in range(10):
        sounds = data.items()[2][1]
        for snd in sounds:
            nr = snd['id']
            url = 'http://www.freesound.org/apiv2/sounds/' + str(nr) + '/'
            url += '?token=' + token + '&descriptors=lowlevel.pitch.mean&fields=previews,analysis'
            os.system('wget -O ./tmp/' + str(nr) + '.json "' + url + '"');
           
            with open('./tmp/' + str(nr) + '.json') as jf:
                sndDat = json.load(jf)
           
            pEst = sndDat['analysis']['lowlevel']['pitch']['mean']
            
            if abs(freq2midi(pTar) - freq2midi(pEst)) < 1:
                # download sound
                url = sndDat['previews']['preview-hq-ogg'] 
                os.system('wget -O ./tmp/snd' + str(nr) + '.ogg "' + url + '"');
                return 'snd'+str(nr)+'.ogg'

        nexturl = data['next'] + '&token=' + token
        os.system('wget -O ./tmp/next.json "' + nexturl + '"');
        with open('./tmp/next.json') as jf:
            data = json.load(jf)
'''


# descriptors used: --------------------------------------------------------------------|
descrs = ['lowLevel.spectral_complexity', 'lowLevel.silence_rate_20dB', 'lowLevel.spectral_rms', 'lowLevel.spectral_kurtosis', 'lowLevel.barkbands_kurtosis', 'lowLevel.scvalleys', 'lowLevel.spectral_spread', 'lowLevel.pitch', 'lowLevel.dissonance', 'lowLevel.spectral_energyband_high', 'lowLevel.mfcc', 'lowLevel.spectral_flux', 'lowLevel.silence_rate_30dB', 'lowLevel.spectral_energyband_middle_high', 'lowLevel.barkbands_spread', 'lowLevel.spectral_centroid', 'lowLevel.pitch_salience', 'lowLevel.silence_rate_60dB', 'lowLevel.spectral_rolloff', 'lowLevel.barkbands', 'lowLevel.spectral_energyband_low', 'lowLevel.barkbands_skewness', 'lowLevel.pitch_instantaneous_confidence', 'lowLevel.spectral_energyband_middle_low', 'lowLevel.spectral_strongpeak', 'lowLevel.spectral_decrease', 'lowLevel.mfcc', 'lowLevel.spectral_energy', 'lowLevel.spectral_flatness_db', 'lowLevel.zerocrossingrate', 'lowLevel.spectral_skewness', 'lowLevel.hfc', 'lowLevel.spectral_crest' ]
#descrs = [ 'lowLevel.spectral_complexity', 'lowLevel.spectral_rms', 'lowLevel.spectral_kurtosis']

t_descrs = descrs
descrs = []
for d in t_descrs:
    if d != 'lowlevel.pitch':
        descrs.append(d+'.mean');
    descrs.append(d+'.var');

#descrs.append('lowLevel.average_loudness')
