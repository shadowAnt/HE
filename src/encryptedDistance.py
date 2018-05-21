'''
this code takes one face number as input
and computes the encrytion of euclidean distance to all the training 
faces, then it returns the k nearest ones
'''

import os
from pg2.paillier_gmpy2 import *
import sys 
import random
from functools import reduce
import time 
import re
print(os.getcwd())
from time import time 


#define k 
k = 10
index = 0
t0 = time()
list_decrypt = list()
list_dist = list()
liist = list()
distances = list()

#function of encrypted distance, I use it!
def encrypt_euclidean_distance(X, Y):
    '''
    tdist:加密所用时间
    tdecrypt:解密所用时间
    :param X: testing image
    :param Y: training image
    :return:
    '''
    cX = [encrypt(pub, x) for x in X]
    cY = [encrypt(pub, y) for y in Y]
    cX2 = [encrypt(pub, x*x) for x in X]
    cY2 = [encrypt(pub, y*y) for y in Y]

    # encrypted distance computation 
    d1 = [e_add(pub, x, y)  for x, y in zip (cX2, cY2) ]
    d2 = [e_mul_const(pub, x, -2*y) for x, y in zip (cX, Y) ]
    d3 = [e_add(pub, x, y)  for x, y in zip (d1, d2) ]
    d = reduce(lambda x, y: e_add(pub, x, y), d3)
    tdist = round(time() - t0, 3)#小数点后保留3位
    # print("encryption time of distance euclidean:", tdist, "s")

    decrypted_distance = int(decrypt(priv, pub, d))
    tdecrypt = round(time() - t0, 5)
    t4 = tdecrypt - tdist
    # print("decryption time of distance euclidean:", t4, "s", tdecrypt,"s")

    list_decrypt.append(decrypted_distance) 
    return decrypted_distance

#load training data in one dict once for all 
faceR = {}
faceDR = {}
distTo = {}
with open('../faces/faceDR', 'r') as fDR:
    for line in fDR:
        coef = line.split()
        faceDR[int(coef[0])] = line

with open('../faces/faceR', 'r') as fR:
        lines = fR.readlines()
        for line in lines:
            v = line.split()
            faceR[int(v[0])] = [int(float(x)) for x in v[1:]] #直接舍弃小数部分 没有进位
# print(faceR[2000])  [-1790, -973, 161, 140, 890, 888, 901, -1...]

def classify(w , wlabels, k):
    '''
    :param w: testing image
    :param wlabels: the label of testing image
    :param k: knn
    :return: true or false of prediction
    '''
    # compute k nearest neighbors
    cX = [encrypt(pub, x) for x in w]
    tencrypt = round(time()-t0, 3)
    t2 = tencrypt - t1
    print("encryption time of input image:", t2, "s")
    for f in faceR.keys():
        distTo[f] = encrypt_euclidean_distance(w, faceR[f])
        list_dist = list()
        list_dist.append(f)
        list_dist.append(distTo[f])
        liist.append(list_dist)
    timeclass = round(time()-t0, 3)
    #t2 = timeclass
    print("classification time :", timeclass, "s")
    # print(liist)
   # distances = [ (x, liist[x] )for x in liist]
    for s in range(len(liist)) :
        x = liist[s]
        y = x[1]
        distances.append(x)
    distances.sort(key=lambda x: x[1])
    # print("distance sort", distances)
    Lgender, Lage, Lrace, Limpression = [], [], [], []
    i, nei= 0, 0
    print(nb, wlabels.values())
    print("nei |gender | age | race | impression ")
    while (nei < k):
        try:
            #print i, distances[i][0]
            line = faceDR[ distances[i][0] ]
            #print line
            tokens = re.split(r'[( )]',line)
            print(distances[i][0], tokens[5], tokens[10], tokens[14], tokens[18])
            #if tokens[5] == wlabels["gender"]:
            if len(tokens)>18:
                Lgender.append(tokens[5])
                #if tokens[10] == wlabels["age"]:
                Lage.append(tokens[10])
                #if tokens[14] == wlabels["race"]:
                Lrace.append(tokens[14])
                #if tokens[18] == wlabels["impression"]:
                Limpression.append(tokens[18])
                nei+=1
            i+=1
        except:
            input()
            #print line
            #print "error in faceDR parsing!"
            #print sys.exc_info()[0]
            i+=1
            continue

    from collections import Counter
    Cgender = Counter( Lgender)
    Cage = Counter (Lage)
    Crace = Counter (Lrace)
    Cimpression = Counter (Limpression)
    res = (wlabels["gender"] == Cgender.most_common()[0][0], wlabels["age"] == Cage.most_common()[0][0], wlabels["race"] == Crace.most_common()[0][0], wlabels["impression"] == Cimpression.most_common()[0][0])
    print(res)
    return res

if __name__ == "__main__":
    '''
    t1 输入图片的时刻
    '''
    print("Generating keypair... %d bits" % 512)
    priv, pub = generate_keypair(512)
    print("choose from testing dataset (3223-->5222)")
    nb = int(input())
    t1 = round(time()-t0, 3)
    print("time of the input image :", t1, "s")

    #check up the face
    w = []
    with open ("../faces/faceS") as faceS:
        found = False
        for line in faceS:
            if not line.startswith(" %d " % nb ):
                pass
            else:
                w = [int(float(x)) for x in line.split()[1:] ]
                found = True
                break
        if not found:
            print("face not found!")
            sys.exit()
    # print("testing image:", w)

    # check the labels
    wlabels = {}
    with open ("../faces/faceDS") as faceDS:
        found = False
        for line in faceDS:
            if not line.startswith(" %d " % nb ):
                pass
            else:
                tokens = re.split(r'[( )]',line)
                wlabels["gender"]= tokens[5]
                wlabels["age"]= tokens[10]
                wlabels["race"]= tokens[14]
                wlabels["impression"]= tokens[18]
                print("testing image's label:", wlabels)
                found = True
                break
        if not found:
            print("face not found!")
            sys.exit()

    classify(w, wlabels, k)
print("classification time:", round(time()-t0, 3), "s")

'''
E:\PycharmProjects\HP\src
Generating keypair... 512 bits
choose from testing dataset (3223-->5222)
4000
time of the input image : 2.539 s
testing image: [4348, -414, 502, 45, 227, 753, -328, -42, -174, 15, -82, 341, 120, 29, -232, -20, 47, 126, -137, 42, -27, -28, 41, -189, -106, 221, -9, -24, -131, 12, 11, -63, 269, -340, -5, -258, -6, -40, -61, -90, 43, 24, -114, 97, -74, 57, -68, 87, 19, -16, -194, -14, -24, -73, -8, 167, -21, 15, 156, 93, -288, -51, -12, 47, 92, 53, -85, 50, -6, -32, 33, -18, -42, -81, -69, -187, -135, 13, 164, 77, 104, -30, -87, -190, -124, 36, -136, 169, -106, 14, 36, -118, 7, 55, 12, 104, -25, -39, 76]
testing image's label: {'gender': 'female', 'age': 'adult', 'race': 'black', 'impression': 'smiling'}
encryption time of input image: 0.07799999999999985 s
classification time : 518.069 s
1473 female teen white smiling
2888 female adult white smiling
1422 female child white smiling
3003 female adult white smiling
2788 female adult white serious
1990 male adult white serious
3208 female senior white serious
2467 male adult white smiling
1567 male teen white serious
1541 female teen white smiling
(True, False, False, True)
classification time: 158.438 s

'''