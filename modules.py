"""
Contains all the bindings to the modules.
To change the backend of a module, alter the _modules dict accordingly
"""

import cv2
import numpy as np
from parameters import getParam
from buildpyr import buildPyr

def getRegion(frames):
    return None

def crop(frames, boundingRects):
    return frames

def preProcess(vid):
    vid2 = []
    idx = getParam["pyramidLevel"]
    depth = getParam["pyramidDepth"]

    for i in range(vid.shape[0]):
        img2 = cv2.cvtColor(vid[i],cv2.COLOR_BGR2GRAY)
        lpr, gpr = buildPyr(img2,depth)
        vid2.append(lpr[idx])

    vid = np.array(vid2)
    return vid

from fft import *

_modules = {

        "RegionOfInterest": getRegion,
        "Crop": crop,
        "PreProcessing": preProcess,
        "Fourier Transform": applyFFT,
        "Band Pass": bandPass,
        "Select Frequency": searchFreq,

}

def getModule(modName):
    return _modules[modName]
