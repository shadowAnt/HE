'''
generate a prime of bits length
'''
import random
import sys
from gmpy2 import mpz, is_prime, random_state, mpz_urandomb
import time

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

#TODO choose a number from [0, sys.maxsize-1] to be seed
rand = random_state(random.randrange(sys.maxsize))

#TODO generate an integer of b bits that is prime using the gmpy2 library
def generate_prime(bits):
    bits -= 1
    base = mpz(2)**(bits)
    while True:
        add = mpz_urandomb(rand, (bits))
        possible = base + add
        if is_prime(possible):
            return possible

#TODO for example, bits = 4, base = 2**3 = 8, add = [0, 8-1]
def gp(bits):
    bits -= 1
    base = 2 ** (bits)
    while True:
        add = mpz_urandomb(rand, (bits))
        possible = base + add
        print("%d + %d = %d" %(base, add, possible))
        # if is_prime(possible):
        #     return possible
    # 8 + 1 = 9
    # 8 + 6 = 14
    # 8 + 7 = 15
    # 8 + 7 = 15
    # 8 + 2 = 10
    # 8 + 6 = 14
    # 8 + 7 = 15
    # 8 + 3 = 11

if __name__ == '__main__':
    # p = generate_prime(1024)
    # print(p)
    # print(p.bit_length())

    t_generate_prime = timing(generate_prime, 1)
    clockTime_avg = 0
    for i in range(10):
        p, clockTime = t_generate_prime(1024)
        clockTime_avg += clockTime
        print(p)
        print(p.bit_length())
    print("Average time for generating a prime of length %d: %f ms" % (1024, (clockTime_avg*1000/10.)))
