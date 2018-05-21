
import os
import numpy as np
import random
from linearEnc.cmp import *
from linearEnc.MinHeap import *
from linearEnc.predict import *

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
print("训练集初始化完成...")

#TODO testing 3223-5222
faceS = open("../faces/faceS")
Q = []
for v in faceS:
    w = [int(float(x)) for x in v.split()[1:]]
    w.append(1)
    Q.append(w)
Q = np.array(Q)
print("测试集初始化完成...")

if __name__ == "__main__":
    statisticDic = [0, 0, 0, 0]
    sumQ = 900
    for q in range(sumQ):
        #TODO server
        P = []
        for Bi in B:
            Bi = np.matrix(Bi)
            qq = np.matrix(np.array(Q[q])).T
            Pi = np.dot(Bi, qq)
            P.append(Pi)

        listP = [int(x.tolist()[0][0]) for x in P]
        #TODO 得到最小的K个距离编号 对应的Pi应该是最大的
        K = 10
        tempMinK = listP[:K]
        minK_index = list(range(10))
        begin(tempMinK)
        for i in range(K, 2000):
            temp = int(P[i].tolist()[0][0])
            if temp > tempMinK[0]:
                tempMinK[0] = temp
                sink(tempMinK, 0)
        ind = findWhere(tempMinK, listP)
        print([x+1223 for x in ind])#[1541, 1567, 2788, 1990, 2467, 3003, 2888, 1473, 1422, 3208]
        predictLabel = getLabel(ind)
        realLabel = showReal(q)
        print(q, predictLabel)
        # print(realLabel)
        for i in range(4):
            if predictLabel[i] == realLabel[i]:
                statisticDic[i] = statisticDic[i] + 1
    print(statisticDic)


#2000 [446, 685, 630, 381]
#1500 [446, 688, 630, 381]
#1200 [450, 674, 630, 368]
#1000 [450, 682, 630, 384]
#900  [439, 694, 626, 375]
#800  [426, 658, 593, 358]
#700  [416, 581, 584, 327]
#400  [241, 289, 361, 192]
#100  [68, 25, 92, 54]
#50   [pr31, 4, 42, 32]
#20   [15, 1, 18, 13]
