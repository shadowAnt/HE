from pg2.paillier_gmpy2 import *
import numpy as np
import random

if __name__ == "__main__":
    priv, pub = generate_keypair(512)
    a = [8, 7, 5, 2, 1]
    # a = [random.randint(1, pub.n_sq) for i in range(2000)]
    e_a = [encrypt(pub, i) for i in a]
    r = [random.randint(1, pub.n) for i in range(len(a))]
    e_r = [encrypt(pub, i) for i in r]
    e_c = [e_add(pub, x, y) for x,y in zip(e_a, e_r)]
    c = [decrypt(priv, pub, i) for i in e_c]
    print(a)
    print(r)
    print(c)
