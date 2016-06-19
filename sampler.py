from pipeline import PipeLine
import numpy as np
from parameters import getParam
import cv2

def sampleAndRunLoop(vidSource):

    fps = vidSource.get(cv2.cv.CV_CAP_PROP_FPS)

    sampleLen = getParam["SampleLength"]

    ret, frame = vidSource.read()
    sample = np.zeros(( sampleLen, frame.shape[0], frame.shape[1], 3 ))

    idx = 0

    pipeline = PipeLine(fps)

    while True:
        ret, frame = vidSource.read()
        
        if idx < sampleLen:
            sample[idx] = frame
        else:
            # Slide sampling window
            sample = np.insert( sample[1:], -1, frame, axis = 0)
        
        # Perform computation of frequency
        respiratoryRate = pipeline.run(sample)

        idx += 1

        print idx

        # Display result on the output image
        cv2.putText(frame, "%d bps"%respiratoryRate, (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,20,255))
        cv2.imshow('output', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 

