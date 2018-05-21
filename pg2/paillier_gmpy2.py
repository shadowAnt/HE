import time
import random, sys 
from pg2.primes_gmpy2 import generate_prime
from gmpy2 import mpz, powmod, invert, random_state, mpz_urandomb, rint_round, log2, gcd

rand = random_state(random.randrange(sys.maxsize))

#TODO paillier: n = pq, g = n+1, l = (p-1)(q-1), m = l**-1 mod n, pub = (n, g), prv = (l, m)
class PublicKey(object):
    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1
        self.bits = mpz(rint_round(log2(self.n)))

class PrivateKey(object):
    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invert(self.l, n)#l  mod n 的乘法逆元

def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

#TODO c = g^m * (r^n mod n^2) mod n^2
def encrypt(pub, plain):
    while True:
        r = mpz_urandomb(rand, pub.bits)
        if r > 0 and r < pub.n and gcd(r, pub.n) == 1:
            break
    x = powmod(r, pub.n, pub.n_sq)

    cipher = (powmod(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    return cipher

#TODO m = (c^l mod n^2 - 1) / n * m mod n
def decrypt(priv, pub, cipher):
    x = powmod(cipher, priv.l, pub.n_sq) - 1
    plain = ((x // pub.n) * priv.m) % pub.n
    if plain > pub.n/2:
        plain = plain - pub.n
    """// 取整除 - 返回商的整数部分"""
    return plain

#TODO E(m1)E(m2) mod n^2 = E(m1+m2)
def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a * b % pub.n_sq

#TODO E(m1 + n) = E(m1) * (g^n mod n^2) mod n^2
def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * powmod(pub.g, n, pub.n_sq) % pub.n_sq

#TODO a = E(m1), E(m1*a) = E(m1)^a mod n^2
def e_mul_const(pub, a, n):
    """Multiplies an encrypted integer by a constant"""
    return powmod(a, n, pub.n_sq)

#TODO return function's result and runtime
def timing(f, c=0):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        clockTime = time2 - time1
        print('%s function took %0.3f ms' % (f.__name__, (clockTime)*1000.0))
        if c==0:
            return ret
        else:
            return ret, clockTime
    return wrap

if __name__ == '__main__':
    # p = generate_prime(1024)
    # print(p)
    # print(p.bit_length())

    priv, pub = generate_keypair(1024)
    t_encrypt = timing(encrypt, 1)
    t_decrypt = timing(decrypt, 2)
    clockTime_avg = 0
    clockTime_avg1 = 0

    # c_1 = encrypt(pub, 1)
    # c_2 = encrypt(pub, 2)
    # c_2 = c_2 ** 5
    # ans = c_1 * c_2
    # m = decrypt(priv, pub, ans)
    # print(m)

    c_1 = encrypt(pub, 1)
    c_2 = encrypt(pub, -2)
    c_3 = e_add(pub, c_1, c_2)
    m = decrypt(priv, pub, c_3)
    print(m)

    # for i in range(10):
    #     cx, clockTime = t_encrypt(pub, i)
    #     print('encrypt x=', i)
    #     clockTime_avg += clockTime
    #     x, clockTime1 = t_decrypt(priv, pub, cx)
    #     print('decrypt x=', x)
    #     clockTime_avg1 += clockTime1
    #
    # print("Average time for generating a prime of length %d: %f ms" % (512, (clockTime_avg*1000/10.)))
    # print("Average time for generating a prime of length %d: %f ms" % (512, (clockTime_avg1*1000/10.)))


    # def encrypt(pub, plain):
    #     while True:
    #         r = mpz_urandomb(rand, pub.bits)
    #         if r > 0 & r < pub.n & gcd(r, pub.n) == 1:
    #             break
    #     x = powmod(r, pub.n, pub.n_sq)
    #     cipher = (powmod(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    #     return cipher