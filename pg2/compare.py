from pg2.paillier_gmpy2 import *
from numpy import *
import numpy as np
import random

rand = random_state(random.randrange(sys.maxsize))

def cmp(e_a, e_b):
    a = decrypt(priv, pub, e_a)
    b = decrypt(priv, pub, e_b)
    mod = mpz(2 ** 512)
    modl = mpz(2 ** 511)
    e_mod = encrypt(pub, modl)

    e_z = e_add(pub, e_mod, e_a)
    e_z = e_add(pub, e_z, e_mul_const(pub, e_b, -1))
    r = mpz_urandomb(rand, pub.bits)
    while True:
        r = mpz_urandomb(rand, pub.bits)
        if r > 0 and r < pub.n / 2:
            break
    # r = 100
    e_r = encrypt(pub, r)
    e_d = e_add(pub, e_z, e_r)

    z = decrypt(priv, pub, e_z)
    d = decrypt(priv, pub, e_d)
    # d_ = z + r
    # print(d, d_)
    d_mod = np.mod(d, modl)
    e_d_mod = encrypt(pub, d_mod)

    r_mod = np.mod(r, modl)
    e_r_mod = encrypt(pub, r_mod)
    e_z_ = e_add(pub, e_d_mod, e_mul_const(pub, e_r_mod, -1))
    # z_ = decrypt(priv, pub, e_z_)
    # print(z, z_)

    lmd = 1
    if d_mod > r_mod:
        lmd = 0
    e_lmd = encrypt(pub, lmd)
    e_z_mod = e_add(pub, e_z_, e_mul_const(pub, e_lmd, modl))
    # e_zl = e_mul_const(pub, e_add(pub, e_z, e_mul_const(pub, e_z_mod, -1)), _modl)
    e_zl = e_add(pub, e_z, e_mul_const(pub, e_z_mod, -1))
    zl = decrypt(priv, pub, e_zl)
    zl = np.right_shift(zl, 511)

    e_small = e_add(pub, e_mul_const(pub, e_add(pub, e_a, e_mul_const(pub, e_b, -1)), zl), e_b)
    # small = decrypt(priv, pub, e_small)
    # print(small)
    return e_small
    # return e_small

if __name__ == "__main__":
    priv, pub = generate_keypair(512)
    e_1 = encrypt(pub, 45)
    e_2 = encrypt(pub, 22)

    t_cmp = timing(cmp, 3)
    e_small, funOftime = t_cmp(e_1, e_2)
    print(e_1)
    print(e_2)
    print(e_small)
    # small = decrypt(priv, pub, e_small)
    # print(small)

    # a = mpz(2 ** 512)
    # print(a)
    # modl = mpz(2 ** 512)
    # _modl = 1/modl
    # print(modl)
    # print(_modl)

    # a = bin(2 ** 512)
    # print(type(a))
    # print(a)
    # b = list(a)
    # print(b[2:])
    # print(len(b[2:]))
    # c = np.right_shift(pub.n, 511)
    # print(c)

    # a = 8
    # b = np.right_shift(a, 3)
    # print(b)