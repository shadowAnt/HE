import os
import numpy as np
import random
from linearEnc.cmp import *

#TODO training 1223-3222
faceR = open("../faces/faceR")
B = []
for v in faceR:
    w = [int(float(x)) for x in v.split()[1:]]
    w.append(int(-0.5 * sum([x*x for x in w])))
    B.append(w)
B = np.array(B)
maxNum = np.amax(B)
# maxNum = 100

#TODO testing 3223-5222
faceS = open("../faces/faceS")
Q = []
for v in faceS:
    w = [int(float(x)) for x in v.split()[1:]]
    w.append(1)
    Q.append(w)
Q = np.array(Q)

H = np.random.randint(1, maxNum, 100)
R = np.random.randint(1, maxNum, 100)
M1 = np.random.randint(0, maxNum, [100, 100])
M1 = np.matrix(M1)
M1_ = M1.I
M2 = np.random.randint(0, maxNum, [100, 100])
M2 = np.matrix(M2)
M2_ = M2.I
M3 = np.random.randint(0, maxNum, [100, 100])
M3 = np.matrix(M3)
M3_ = M3.I

CH = H * M1_
R.shape = (100, 1)
CR = M3_ * R

if __name__ == "__main__":
    rightNum = 0
    for k in range(100):
        #TODO generate Di i=1, 2
        D0 = []
        for i in range(100):
            Aik = np.random.randint(0, maxNum, 99)
            sumNum = sum([x*y for x, y in zip(H[:-1], Aik)])
            Aik = np.append(Aik, (1-sumNum) / H[-1])
            Dik = Aik * B[0][i]
            D0.append(Dik)
        D0 = np.matrix(np.array(D0).T)
        D1 = []
        for i in range(100):
            Aik = np.random.randint(0, maxNum, 99)
            sumNum = sum([x*y for x, y in zip(H[:-1], Aik)])
            Aik = np.append(Aik, (1-sumNum) / H[-1])
            Dik = Aik * B[1][i]
            D1.append(Dik)
        D1 = np.matrix(np.array(D1).T)

        #TODO encrypy H R Di
        C0 = M1 * D0 * M2
        C1 = M1 * D1 * M2

        #TODO Client Query
        Bc = Q[0]

        #TODO owner encrypts Bc
        Fc = []
        # R.shape = (1, 100)
        for i in range(100):
            Eik = np.random.randint(0, maxNum, 99)
            sumNum = sum([x * y for x, y in zip(R[:-1], Eik)])
            Eik = np.append(Eik, (1 - sumNum) / R[-1])
            Eik = Eik * Bc[i]
            Fc.append(Eik)
        Fc = np.matrix(np.array(Fc))
        CF = M2_ * Fc * M3

        #TODO server
        P0 = CH * C0 * CF * CR
        P1 = CH * C1 * CF * CR
        ans = P0 - P1
        # print(2*int(ans))

        realDis = compareDis(1224, 3223) - compareDis(1223, 3223)
        # print(realDis)
        if np.sign(ans)==np.sign(realDis):
            rightNum = rightNum + 1
            print(True)
        else:
            print(False)
    print(rightNum)