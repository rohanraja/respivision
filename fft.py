import cv2
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

def searchFreq(freqs, signals):

    curMax = 0
    freMax = 0
    Mi = 0
    Mj = 0
    for i in range(10, signals.shape[1]):
        for j in range(signals.shape[2]):

            idxMax = signals[:,i,j].argmax()
            freqMax = freqs[idxMax]
            ampMax = signals[idxMax,i,j]

            if abs(curMax) < abs(ampMax):
                curMax = ampMax
                freMax = freqMax
                Mi = i
                Mj = j
                print "(%d,%d) -> Freq:%f Amp:%f"%(i,j,freqMax*60, abs(ampMax))

    rate = freqMax*60
    return rate
