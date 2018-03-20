'''
ImageWithEncryption.py
choose a image from training dataset
x = one of 99 coefficients
cx = En(x) join in coefficient_encrypted
dx = De(cx)
compare x with dx
show coefficient_encrypted
'''
import os
from pg2.paillier_gmpy2 import *
import sys
import random
import time
print(os.getcwd())
coefficient_encrypted = list()
print("give me a faceEuclideanDistance number...")
print("from training dataset (3223-->5222)")

nb = input()


with open ("../faces/faceS") as faceR:
    w=[]
    for v in faceR:
        if v.split()[0] != nb:
            pass
        else:
            w=[u for u in v.split()[1:]]
            break

print("Generating keypair... %d bits" % 512)
priv, pub = generate_keypair(512)

for iss in range(0,99):
    x = w[iss] #99 coefficients of each image in FaceS
    print("index= %d/99, x = %f" % (iss, float(x)))
    #TODO float -> int
    xx = float(x) * (10**6)
    
    #print "Encrypting x..."
    encryptx = encrypt(pub, int(xx))
    print("cx =", encryptx)
    
    print("Decrypting cx...")
    z = decrypt(priv, pub, encryptx)
    
    if z > pub.n/2:
        print("dx=", round(z-pub.n)*(10**-6))
    else:
        print("dx=", round(z)*(10**-6))
    print()
    coefficient_encrypted.append(encryptx)

print("coefficient_encrypted  ", coefficient_encrypted)