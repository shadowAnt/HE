import os
import numpy as np
from linearEnc.MinHeap import *
from linearEnc.predict import *

#TODO training 1223-3222
faceR = open("../faces/faceR")
B = []
for v in faceR:
    w = [int(float(x)) for x in v.split()[1:]]
    B.append(w)
#TODO testing 3223-5222
faceS = open("../faces/faceS")
Q = []
for v in faceS:
    w = [int(float(x)) for x in v.split()[1:]]
    Q.append(w)

if __name__ == "__main__":
    K = 12
    indexQi = []
    statisticDic = [0, 0, 0, 0]
    for flag in range(2000):
        print(flag)
        qi = Q[flag]
        distanceQi = []
        testQi = []
        for bi in B:
            distanceQi.append(sum([(x-y)*(x-y) for x, y in zip(bi, qi)]))
            bi2 = -0.5*sum([x*x for x in bi])
            xy = [x*y for x, y in zip(bi, qi)]
            testQi.append(sum(xy) + bi2)
        tempK = distanceQi[:K]
        beginMin(tempK)
        for i in range(K, 2000):
            if distanceQi[i] < tempK[0]:
                tempK[0] = distanceQi[i]
                mink(tempK, 0)
        ind = findWhere(tempK, distanceQi)
        indexQi.append(ind)
        # print(ind)

        # tempK2 = testQi[:K]
        # begin(tempK2)
        # for i in range(K, 2000):
        #     if testQi[i] > tempK2[0]:
        #         tempK2[0] = testQi[i]
        #         sink(tempK2, 0)
        # print(findWhere(tempK2, testQi))
        # print(predictLabel)
        predictLabel = getLabel(ind)
        realLabel = showReal(flag)
        for i in range(4):
            if predictLabel[i] == realLabel[i]:
                statisticDic[i] = statisticDic[i] + 1
    print(statisticDic)
    # print([x+1223 for x in indexQi[0]])#[1541, 1567, 2788, 1990, 2467, 3003, 2888, 1473, 1422, 3208]
    # predictLabel = getLabel(indexQi[0])
    # realLabel = showReal(0)
    # print("predict ", predictLabel)
    # print("real ", realLabel)