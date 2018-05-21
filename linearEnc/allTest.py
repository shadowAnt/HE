import os
import numpy as np
import random
from linearEnc.cmp import *
from linearEnc.MinHeap import *
from linearEnc.predict import *
import time

if __name__ == "__main__":

    time1 = time.time()
    # TODO training 1223-3222
    faceR = open("../faces/faceR")
    B = []
    for v in faceR:
        w = [int(float(x)) for x in v.split()[1:]]
        w.append(int(-0.5 * sum([x * x for x in w])))
        B.append(w)
    B = np.array(B)
    maxNum = np.amax(B)
    # maxNum = 100
    print("训练集初始化完成...")

    # TODO testing 3223-5222
    faceS = open("../faces/faceS")
    Q = []
    for v in faceS:
        w = [int(float(x)) for x in v.split()[1:]]
        w.append(1)
        Q.append(w)
    Q = np.array(Q)
    print("测试集初始化完成...")

    H = np.random.randint(1, 2, 100)
    R = np.random.randint(1, 2, 100)
    M1 = np.eye(100)
    # M1 = np.random.randint(0, maxNum, [100, 100])
    M1 = np.matrix(M1)
    M1_ = M1.I
    M2 = np.eye(100)
    # M2 = np.random.randint(0, maxNum, [100, 100])
    M2 = np.matrix(M2)
    M2_ = M2.I
    M3 = np.eye(100)
    # M3 = np.random.randint(0, maxNum, [100, 100])
    M3 = np.matrix(M3)
    M3_ = M3.I
    CH = H * M1_
    R.shape = (100, 1)
    CR = M3_ * R
    print("加密模块初始化完成...")

    # TODO generate Di i=1, 2
    C = []
    for j in range(len(B)):
        Di = []
        for i in range(100):
            Aik = np.random.randint(0, 1, 99)
            sumNum = sum([x * y for x, y in zip(H[:-1], Aik)])
            Aik = np.append(Aik, (1 - sumNum) / H[-1])
            Dik = Aik * B[j][i]
            Di.append(Dik)
        Di = np.matrix(np.array(Di).T)
        Ci = M1 * Di * M2
        C.append(Ci)
    print("加密训练集完成...")
    time2 = time.time()
    blockPre = (time2 - time1) * 1000.
    print("step 1", blockPre, " ms")

    statisticDic = [0, 0, 0, 0]

    blockq = 0.
    blockS = 0.
    for q in range(2000):
        #TODO Client Query and encrypt it
        time3 = time.time()
        Bc = Q[q]
        Fc = []
        for i in range(100):
            Eik = np.random.randint(0, 1, 99)
            sumNum = sum([x * y for x, y in zip(R[:-1], Eik)])
            Eik = np.append(Eik, (1 - sumNum) / R[-1])
            Eik = Eik * Bc[i]
            Fc.append(Eik)
        Fc = np.matrix(np.array(Fc))
        CF = M2_ * Fc * M3
        print("加密查询数据完成...")
        time4 = time.time()
        blockq = blockq + (time4 - time3) * 1000.

        #TODO server
        P = []
        for Ci in C:
            Pi = CH * Ci * CF * CR
            P.append(Pi)

        listP = [int(x.tolist()[0][0]) for x in P]
        #TODO 得到最小的K个距离编号 对应的Pi应该是最大的
        K = 20
        minK = listP[:K]
        minK_index = list(range(10))
        begin(minK)
        for i in range(K, 2000):
            temp = int(P[i].tolist()[0][0])
            if temp > minK[0]:
                minK[0] = temp
                sink(minK, 0)
        # print(minK)    #[384, 1985, 1244, 1780, 767, 1565, 318, 199, 250, 1665]
        ind = findWhere(minK, listP)
        predictLabel = getLabel(ind)
        realLabel = showReal(q)
        print(q, predictLabel)
        # print(realLabel)
        for i in range(4):
            if predictLabel[i] == realLabel[i]:
                statisticDic[i] = statisticDic[i] + 1

        time5 = time.time()
        blockS = blockS + (time5 - time4) * 1000.

    print(statisticDic)

    print('step1  ', blockPre, 'ms')
    print('step2  ', blockq, 'ms')
    print('step3  ', blockS, 'ms')

# 预处理阶段   686.7198944091797 ms
# 加密数据库阶段   20414.981603622437 ms
# 计算距离   882.4315071105957 ms

#[1243, 1641, 1703, 1021]


    # rightNum = 0
    # for k in range(10):
    #     m = random.randint(0, 2000)
    #     while(True):
    #         n = random.randint(0, 2000)
    #         if m!=n: break
    #     ans = P[m] - P[n]
    #     realDis = compareDis(n+1223, q+3223) - compareDis(m+1223, q+3223)
    #     if np.sign(ans) == np.sign(realDis):
    #         rightNum = rightNum + 1
    #         print(True)
    #     else:
    #         print(False)
    # print(rightNum)
