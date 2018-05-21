import os
import numpy as np
import random
import time
from pg2.paillier_gmpy2 import *
from pr31.compare import *
from numpy import *
import numpy as np
from functools import reduce

from src.mean_face import mean_face
M = np.load("../src/eigenfaces.npy")

if __name__ == "__main__":
    #TODO Step 1 数据拥有者对数据进行PCA处理
    time1 = time.time()
    # training 1223-3222
    faceR = open("../faces/faceR")
    D = []
    for v in faceR:
        w = [int(float(x)) for x in v.split()[1:]]
        D.append(w)
        i = M.transpose().dot(w) + mean_face.transpose()
    time2 = time.time()
    print("训练集初始化完成...", (time2 - time1)*1000.0, " ms")

    #TODO Step 2 用户生成密钥对 初始化测试集合
    # testing 3223-5222
    faceS = open("../faces/faceS")
    Q = []
    for v in faceS:
        w = [int(float(x)) for x in v.split()[1:]]
        Q.append(w)

    T = []
    priv, pub = generate_keypair(512)
    time3 = time.time()
    print("测试集初始化完成...", (time3 - time2) * 1000.0, " ms")
    for q in range(1):
        print(q)
        omgpie = [encrypt(pub, x) for x in Q[q]]
        #TODO 计算所有距离表征加密形式
        V = []
        for i in range(2000):
            di = D[i]
            e_wi2 = reduce(lambda x, y: e_add(pub, x, y), [encrypt(pub, x*x) for x in di])
            e_wiwipie = reduce(lambda x, y: e_add(pub, x, y), [e_mul_const(pub, x, -2 * y) for x, y in zip(omgpie, di)])
            vi = e_add(pub, e_wi2, e_wiwipie)
            V.append(vi)
        time4 = time.time()
        print("距离计算完成...", (time4 - time3) * 1000.0, " ms")
        #TODO 建立最大堆得到最小的1个数
        temp = reduce(lambda x, y: mycmp(x, y, pub, priv), V)
        T.append(temp)

    #TODO 得到结果
    realDis = [decrypt(priv, pub, t) for t in T]
    # print(realDis)
    time5 = time.time()
    print("距离计算完成...", (time5 - time4) * 1000.0, " ms")
