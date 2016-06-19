import sys
import cv2
from sampler import *

if len(sys.argv) > 1:
    cap = cv2.VideoCapture(sys.argv[1])
else:
    cap = cv2.VideoCapture(0)

sampleAndRunLoop(cap)

cap.release()
cv2.destroyAllWindows()
