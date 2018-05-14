from src.mean_face import mean_face
import numpy as np
import os
from pg2.paillier_gmpy2 import *
from functools import reduce
import time

orig = np.fromfile("../faces/rawdata/rawdata/" + "2500", dtype=np.uint8)
fai = orig - mean_face  # (16384,) 行向量
M = np.load("eigenfaces.npy")  # 99*16384

p = fai.dot(M.transpose())

# faceR = open("../faces/faceR")
# for v in faceR:
#     if v.split()[0] != "2500":
#         pass
#     else:
#         w = [float(x) for x in v.split()[1:]]
#         break
# w = np.array(w)

#TODO 密文下的投影
time1 = time.time()
priv, pub = generate_keypair(512)
e_orig = [encrypt(pub, int(i)) for i in orig]
e_mean = [encrypt(pub, int(i)) for i in mean_face]
e_fai = [e_add(pub, x, e_mul_const(pub, y, -1)) for x, y in zip(e_orig, e_mean)]
# _fai = [decrypt(priv, pub, i) for i in e_fai]
e_p = []
for i in range(len(M)):  #99
    row = [int(j) for j in M[i]]
    temp = [e_mul_const(pub, x, y) for x, y in zip(e_fai, row)]
    ans = reduce(lambda x, y: np.mod((x * y), pub.n_sq), temp)
    e_p.append(ans)
time2 = time.time()

print(e_p)
print(len(e_p))
p = [decrypt(priv, pub, i) for i in e_p]
print(p)
print((time2 - time1)*1000)


