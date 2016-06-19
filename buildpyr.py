import cv2
import numpy as np,sys


def buildPyr(A, n = 6):

    # generate Gaussian pyramid for A
    G = A.copy()
    gpA = [G]
    for i in xrange(n):
        G = cv2.pyrDown(G)
        gpA.append(G)

    lpA = [gpA[n-1]]
    for i in xrange(n-1,0,-1):
        GE = cv2.pyrUp(gpA[i])
        L = cv2.subtract(gpA[i-1],GE)
        lpA.append(L)

    return lpA, gpA
