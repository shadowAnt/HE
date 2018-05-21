from pg2.paillier_gmpy2 import *
from numpy import *
import numpy as np
import random

def mycmp(e_a, e_b, pub, priv):
    #TODO 服务方计算[a+b]
    e_aaddb = e_add(pub, e_a, e_mul_const(pub, e_b, -1))

    #TODO 用户解密，返回响应的结果
    aaddb = decrypt(priv, pub, e_aaddb)
    ans = encrypt(pub, aaddb) if e_aaddb < 0 else encrypt(pub, 0)

    #TODO 服务方计算[min(a,b)]
    min = e_add(pub, ans, e_b)
    return min

def smallest(list):
    temp = reduce(lambda x, y: mycmp(x, y), list)

if __name__ == "__main__":
    priv, pub = generate_keypair(512)
    e_1 = encrypt(pub, 45)
    e_2 = encrypt(pub, 22)
    t_mycmp = timing(mycmp, 3)
    e_small, funOftime = t_mycmp(e_1, e_2)
    print(e_1)
    print(e_2)
    print(e_small)
    print(decrypt(priv, pub, e_small))