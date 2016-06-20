import cv2
from parameters import getParam
import numpy as np

def applyFFT(frames, fps):
    n = frames.shape[0]
    t = np.linspace(0,float(n)/fps, n)
    disp = frames.mean(axis = 0)
    y = frames - disp

    k = np.arange(n)
    T = n/fps
    frq = k/T # two sides frequency range
    freqs = frq[range(n/2)] # one side frequency range

    Y = np.fft.fft(y, axis=0)/n # fft computing and normalization
    signals = Y[range(n/2), :,:]

    return freqs, signals

def bandPass(freqs, signals, freqRange):

    signals[freqs < freqRange[0]]  *=0
    signals[freqs > freqRange[1]] *= 0

    return signals

from numpy import argmax, sqrt, mean, diff, log
from matplotlib.mlab import find

def freq_from_crossings(sig, fs):
    """Estimate frequency by counting zero crossings
    
    """
    # Find all indices right before a rising-edge zero crossing
    indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
    
    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    #crossings = indices
    
    # More accurate, using linear interpolation to find intersample 
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
    
    # Some other interpolation based on neighboring points might be better. Spline, cubic, whatever
    
    return fs / mean(diff(crossings))

def searchFreq(freqs, signals, frames, fs):

    curMax = 0
    freMax = 0
    Mi = 0
    Mj = 0
    for i in range(10, signals.shape[1]):
        for j in range(signals.shape[2]):

            idxMax = abs(signals[:,i,j]).argmax()
            freqMax = freqs[idxMax]
            ampMax = signals[idxMax,i,j]

            if abs(curMax) < abs(ampMax):
                curMax = ampMax
                freMax = freqMax
                Mi = i
                Mj = j
                # print "(%d,%d) -> Freq:%f Amp:%f"%(i,j,freqMax*60, abs(ampMax))


    y = frames[:,Mi, Mj]
    y = y - y.mean()
    fq = freq_from_crossings(y, fs)
    rate_fft = freMax*60
    rate_count = fq*60
    if np.isnan(rate_count):
        rate = rate_fft
    elif abs(rate_fft - rate_count) > getParam["fft_count_diff"]:
        rate = rate_fft
    else:
        rate = rate_count

    return rate
