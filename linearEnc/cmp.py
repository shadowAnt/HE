import os
import numpy as np

def compareDis(index1, index2):
    '''
      0000-1999
    R:1223-3222
    S:3223-5222
    :param index1:
    :param index2:
    :return:
    '''
    faceR = open("../faces/faceR")
    faceS = open("../faces/faceS")
    aTemp = []; bTemp = []
    R = []
    for v in faceR:
        w = [int(float(x)) for x in v.split()[1:]]
        R.append(w)
    S = []
    for v in faceS:
        w = [int(float(x)) for x in v.split()[1:]]
        S.append(w)
    if index1 in range(1223, 3223):
        aTemp = R[index1 - 1223]
    elif index1 in range(3223, 5223):
        aTemp = S[index1 - 3223]
    if index2 in range(1223, 3223):
        bTemp = R[index2 - 1223]
    elif index2 in range(3223, 5223):
        bTemp = S[index2 - 3223]
    d = sum([(x-y)*(x-y) for x, y in zip(aTemp, bTemp)])
    return d