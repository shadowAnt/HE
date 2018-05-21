import rsa
import time
from hashlib import sha256
from itertools import combinations
from json_stuff import *
from random import SystemRandom
from next_prime import next_prime
from mulinv import mulinv

RSA_bits = 512

cryptorand = SystemRandom()
def randint(n):
    return cryptorand.randrange(n)

def moddiv(a, b, n):
    return a * mulinv(b, n) % n

def prod(x, G):
    p = 1
    for i in x:
        p *= i
    return p

def hasher(b):
    return sha256(b).hexdigest()

def lagrange(x, y, G):
    assert len(x) == len(y) and len(x) > 0, "Lengths of x and y must equal and non-zero."
    x_len = len(x)
    f = [0] * x_len
    for i in range(x_len):
        partial = []
        combo_list = list(x)
        combo_list.pop(i)
        for j in range(x_len):
            c = 0
            for k in combinations(combo_list, j):
                c += prod(map(lambda q: -q, k), G)
            partial.append(c)
        d = 1
        for j in range(x_len):
            if j != i:
                d *= x[i] - x[j]

        partial = map(lambda q: moddiv(q * y[i], d, G), partial)
        f = [(m + n) % G for m, n in zip(f, partial)] # also needs % G

    for i in range(x_len):
        assert compute_poly(f, x[i], G) == y[i], i
    return f

def bytes_to_int(m):
    return int.from_bytes(m, byteorder="big")

def int_to_bytes(i):
    return i.to_bytes(RSA_bits//8, byteorder="big")

def strip_padding(b, secret_length):
    return b[(RSA_bits//8 - secret_length):]

def compute_poly(f, x, m):
    y = 0
    for i in range(len(f)):
        y += f[i] * pow(x, len(f) - 1 - i, m)
    return y % m

class Alice:
    def __init__(self, M, t, secret_length):
        assert secret_length < RSA_bits//8, "Secret length too long for RSA key size"
        for m in M:
            assert len(m) == secret_length, "Messages must have same length as secret_length"
        self.M = M
        self.t = t
        self.secret_length = secret_length

        (pubkey, privkey) = rsa.newkeys(RSA_bits)
        self.pubkey = pubkey
        self.privkey = privkey
        self.G = next_prime(self.pubkey.n)

        self.hashes = []

        for m in self.M:
            self.hashes.append(hasher(m))

    def setup(self, file_name = "alice_setup.json"):
        j = {
                "pubkey": {"e": self.pubkey.e, "n": self.pubkey.n},
                "hashes": self.hashes,
                "secret_length": self.secret_length,
                }

        write_json(file_name, j)
        print("Pubkey and hashes published.")

    def transmit(self, file_name = "alice_dec.json", bob_file_name = "bob_setup.json"):
        f = list(map(int, read_json(bob_file_name)))
        assert len(f) == self.t, "Bob is requesting a different number of messages than expected"

        G = []
        for i in range(len(self.M)):
            F = pow(compute_poly(f, i, self.G), self.privkey.d, self.pubkey.n)
            G.append((F * bytes_to_int(self.M[i])) % self.pubkey.n)

        # write_json(file_name, G)
        print("G has been published.")
        return G

class Bob:
    def __init__(self, des_messages):
        self.num_des_messages = len(des_messages)
        self.des_messages = des_messages

    def setup(self, file_name="bob_setup.json", alice_file_name="alice_setup.json"):
        alice = read_json(alice_file_name)
        self.pubkey = rsa.PublicKey(alice["pubkey"]["n"], alice["pubkey"]["e"])
        self.hashes = alice["hashes"]
        self.secret_length = alice["secret_length"]

        self.R = []
        T = []
        for j in range(self.num_des_messages):
            r = randint(self.pubkey.n)
            self.R.append(r)
            T.append(pow(r, self.pubkey.e, self.pubkey.n)) # the encrypted random value

        G = next_prime(self.pubkey.n)
        f = lagrange(self.des_messages, T, G)

        string_f = [str(x) for x in f]

        write_json(file_name, string_f)
        print("Polynomial published.")

    def receive(self, G):


        decrypted = []
        for j in range(self.num_des_messages):
            d = moddiv(G[self.des_messages[j]], self.R[j], self.pubkey.n)
            dec_bytes = int_to_bytes(d)
            decrypted.append(strip_padding(dec_bytes, self.secret_length))

            if hasher(decrypted[j]) != self.hashes[self.des_messages[j]]:
                print("Hashes don't match. Either something messed up or Alice is up to something.")

        self.decrypted = decrypted
        return(decrypted)

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

if __name__ == "__main__":
    import random
    # length of the keys (the messages Alice has) in bytes secret_length
    # alphabet = "abcdefghijklmnopqrstuvwxyz"
    # secrets = [bytes("".join(random.choice(alphabet) for _ in range(secret_length)), "ASCII") for __ in range(8)]
    # secrets = [b'Secret message 1', b'Secret message 2', b'Secret message 3']
    same = []
    for i in range(2000):
        if i < 10: same.append('000' + str(i))
        elif i < 100: same.append('00' + str(i))
        elif i < 1000: same.append('0' + str(i))
        elif i < 10000: same.append(str(i))
    secrets = [bytes('Secret message ' + i, 'ASCII') for i in same]
    secret_length = len(secrets[0])
    print(secrets)

    t = 1

    # alice = Alice(secrets, t, secret_length)
    # bob = Bob(random.sample([i for i in range(1000)], t))
    t_Alice = timing(Alice, 1)
    t_Bob = timing(Bob, 2)

    alice, aliceTime = t_Alice(secrets, t, secret_length)
    bob, bobTime = t_Bob(random.sample([i for i in range(1000)], t))
    time1 = time.time()
    alice.setup()
    time2 = time.time()
    bob.setup()
    time3 = time.time()
    G = alice.transmit()
    time4 = time.time()
    M_prime = bob.receive(G)
    time5 = time.time()
    print(M_prime)
    print('sever.setup():  ', (time2-time1)*1000.0, 'ms')
    print('user.setup():  ', (time3-time2)*1000.0, 'ms')
    print('sever.transmit():  ', (time4-time3)*1000.0, 'ms')
    print('user.receive():  ', (time5-time4)*1000.0, 'ms')




