import sys
from time import time
import numpy as np 
import re
import matplotlib.pyplot as plt
import prettyplotlib as ppl

'''
preprocessing part
预处理阶段，去除测试和训练中无效的样本
faces是训练系数集合，X是其对应的矩阵 1997×99，y是对应的age标签
facest是测试系数集合，Xt是其对应的矩阵 1996×99，yt是对应的age标签
'''

faces = [] 
""" faces is 2000*99 as training images"""
with open('../faces/faceR', 'r') as fDR:
    for line in fDR:
        faces.append([float (x) for x in line.split()[1:]] )
# print(len(faces[0]))

y = []
"""y is age(adult, child, senior, teen) of faces(training images)"""
wrong=[]
with open('../faces/faceDR', 'r') as fDR:
	i=0
	for line in fDR:
		tokens = re.split(r'[( )]', line)
		try:
			y.append(tokens[10])
		except:
			#print tokens 
			wrong.append(i)
		i+=1
# print(len(y))   len(y) = 1997
# print(wrong)    wrong = [5, 9, 585]

#TODO delete faces of training images which doesn't have label
wrong.sort(reverse=True)
# print(wrong)     wrong = [585, 9, 5]
for i in wrong:
	# print(i+1223, faces[i])
	del(faces[i])


X = np.array(faces)
# print(len(y), X.shape) y 1997  X(1997, 99)
facest = []
"""facest is 99 of testing images"""
with open('../faces/faceS', 'r') as fDR:
    for line in fDR:
        facest.append([float (x) for x in line.split()[1:]] )
# print(len(facest[0]))  facest is 2000*99

yt = []
wrong=[]
with open('../faces/faceDS', 'r') as fDR:
	i=0
	for line in fDR:
		tokens = re.split(r'[( )]',line)
		try:
			yt.append(tokens[10])
			#print y
		except:
			wrong.append(i)
		i+=1

wrong.sort(reverse=True)
for i in wrong:
	# print(i+3223, facest[i])
	del(facest[i])

Xt = np.array(facest)
# print(len(yt), len(Xt))


# data mining part
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing

from sklearn.neighbors import KNeighborsClassifier

k_range = range(1, 31)
k_score = []
for k in k_range:
	neigh = KNeighborsClassifier(n_neighbors = k)
	neigh.fit(X, y)
	pred = neigh.predict(Xt)
	# print(classification_report(yt, pred))
	accuracy = neigh.score(Xt, yt)
	print(k, "KNN accuracy",  accuracy*100 , "%")
	k_score.append(accuracy*100)

k_range = list(k_range)
plt.plot(k_range, k_score, color="blue", linewidth=2.5, linestyle="-", label="cosine")
plt.xlabel('value of K for KNN')
plt.ylabel('accuracy')
plt.show()

# fig, ax = plt.subplots(1)
# ppl.bar(ax, k_range, k_score)
# ax.set_xlabel('value of K for KNN')
# ax.set_ylabel('accuracy')
# plt.show()
# fig.savefig('bar_prettyplotlib_default.png')

# def get_weight():
# 	weights = {}
# 	weights['child'] = 1997. / y.count('child')
# 	weights['teen'] = 1997. / y.count('teen')
# 	weights['adult'] = 1997. / y.count('adult')
# 	weights['senior'] = 1997. / y.count('senior')
# 	return weights

# from sklearn.svm import SVC
# clf = SVC(kernel="rbf", class_weight=get_weight() )
# clf.fit(X, y)
# pred = clf.predict(Xt)
# print(classification_report(yt, pred))
# #print pred [3]
# #print yt[3]
# print("SVM accuracy",  accuracy_score(pred, yt)*100 , "%")

# from sklearn import tree
# clf = tree.DecisionTreeClassifier(min_samples_split=4,  class_weight=get_weight())
# clf.fit(X, y)
# pred = clf.predict(Xt)
# print(classification_report(yt, pred))
# accuracy = clf.score(Xt, yt)
# print("dt accuracy",  accuracy*100 , "%")
#
# clf = GaussianNB()
# clf.fit(X, y)
# #print clf.class_count_
# pred = clf.predict(Xt)
# #print pred [3]
# #print yt[3]
# #clf.fit(Xt, yt)
# #print clf.class_prior_
#
# print(classification_report(yt, pred))
# print("Gaussian BN accuracy",  accuracy_score(pred, yt)*100 , "%")




#weights = [2000./y.count('child'), 2000./y.count('teen'), 2000./y.count('adult'), 2000./ y.count('senior')]
#size = min( y.count('child'),  y.count('teen'),  y.count('adult'), y.count('senior') )
#print size 
#Xp=np.array([[0]*99 for i in range(4*size)]) 
#yp=[0]*4*size 
#c_child, c_teen, c_adult, c_senior = 0, 0 , 0, 0
#j=0 
#sample_weights= [0]*2000 
#for i in range(2000): 
	#print c_child, c_teen, c_adult, c_senior 
	#if y[i]=='child' and c_child<size : 
	#	c_child+=1
	#	Xp[j]=X[i]
	#	yp[j]=y[i]
	#	j+=1
	#elif y[i]=='teen' and c_teen<size:
	#	c_teen+=1 
	#	Xp[j]=X[i]
	#	yp[j]=y[i]
	#	j+=1
	#elif y[i]=='adult' and c_adult<size: 
	#	c_adult+=1
	#	Xp[j]=X[i]
	#	yp[j]=y[i]
	#	j+=1
	#elif y[i]=='senior' and c_senior<size: 
	#	c_senior+=1
	#	Xp[j]=X[i]
	#	yp[j]=y[i]
	#	j+=1
#print y.count('child')
#print y.count('teen')
#print yt.count('adult')
#print y.count('senior')
#print Xp 
#print yp 
#print sample_weights 
#min_max_scaler = preprocessing.MinMaxScaler()
#min_max_scaler.fit_transform(Xp)
#print min_max_scaler.data_min_
#print min_max_scaler.data_max_
#print X[0]
#X=min_max_scaler.transform(Xp)
#y=yp
#print X 
#print y 
#print X[0]
#print Xt[0]
#Xt=min_max_scaler.transform(Xt)
#print Xt[0]
#X = scaler.transform(X)  
#Xt= scaler.transform(Xt)
