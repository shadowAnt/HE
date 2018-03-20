''' this code takes one face number as input 
and computes the euclidean distance to all the training 
faces, then it returns the k nearest ones''' 

import os
import sys 
import math
import re

#define k 
k = 15

#function of distance but I use it!
def euclidean_distance(x,y): 
    return math.sqrt(sum(pow((a)-(b),2) for (a), (b) in zip(x,y)))

#load training data in one dict once for all 
faceR = {}
faceDR = {}
distTo = {}

#TODO get the discriptions of training image
with open('../faces/faceDR', 'r') as fDR:
    for line in fDR:
        coef = line.split()
        faceDR[int(coef[0])] = line

with open('../faces/faceR', 'r') as fR:
        lines= fR.readlines()
        for line in lines:
            v = line.split()
            faceR[int(v[0])]= [float(x) for x in v[1:]]

def classify(w , wlabels, k):
    '''
    :param w: 99系数
    :param wlabels: w的标签
    :param k: knn系数
    :return: knn结果和实际wlabels的比较
    '''

    # compute k nearest neighbors 
    for f in faceR.keys():
        distTo[f] = euclidean_distance(w, faceR[f])

    #get sort (index, distance) 按照距离从小到大排列
    distances = [(x, distTo[x]) for x in distTo.keys()]
    distances.sort(key=lambda x: x[1])
    
    Lgender, Lage, Lrace, Limpression = [], [], [], []
    i, nei= 0, 0

    while (nei < k): 
        try:
            # print(i, distances[i][0])
            line = faceDR[distances[i][0]]
            
            tokens = re.split(r'[( )]', line)
            #print(tokens)
            #print(tokens[1], tokens[5], tokens[10], tokens[14], tokens[18])
            
            #if tokens[5] == wlabels["gender"]: 
            if len(tokens) > 18:
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
            i += 1
            continue 

    #print(Lgender)
    from collections import Counter
    Cgender = Counter(Lgender)
    """Counter({'male': 10, 'female': 5})"""
    Cage = Counter(Lage)
    Crace = Counter(Lrace)
    Cimpression = Counter(Limpression)

    """cGender.most_common()     [('male', 10), ('female', 5)]"""
    res = (wlabels["gender"] ==  Cgender.most_common()[0][0] ,\
     wlabels["age"] == Cage.most_common()[0][0] ,\
     wlabels["race"] == Crace.most_common()[0][0], \
     wlabels["impression"] == Cimpression.most_common()[0][0])
    print(res)
    return res

if __name__ == "__main__": 
    print("choose from testing dataset (3223-->5222)")
    nb = int(input())
    #nb = 4100

    #check up the face 
    w=[]
    with open ("../faces/faceS") as faceS:
        found = False 
        for line in faceS:
            if not line.startswith(" %d " % nb ):
                pass
            else:
                w = [float (x) for x in line.split()[1:]]
                found = True 
                break  
        if not found:
            print("face not found!")
            sys.exit()

    wlabels = {}
    with open ("../faces/faceDS") as faceDS:
        found = False 
        for line in faceDS:
            if not line.startswith(" %d " % nb ):
                pass
            else:
                tokens  = re.split(r'[( )]',line)
                 
                wlabels["gender"]= tokens[5]
                wlabels["age"]= tokens[10]
                wlabels["race"]= tokens[14]
                wlabels["impression"]= tokens[18]
                #print wlabels
                found = True 
                break  
        if not found:
            print("face not found!")
            sys.exit()

    classify (w, wlabels, k)