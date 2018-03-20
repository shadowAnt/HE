'''
this script shows the original = eigenFace.T * faceR + mean_face.T .reshape(128, 128)
and the PCA reconstructed images,
you just have to supply a faceEuclideanDistance number from the data set
133 is meanFace from mean_face.py
'''

import os
from src.mean_face import mean_face
#from eigenfaces import eigenfaces  
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm # color map

#E = eigenfaces.split('\n')
#M = np.matrix([[float(x) for x in e.split()] for e in E])
#np.save("eigenfaces", M)
print(os.getcwd())
print(mean_face.shape)

M = np.load("eigenfaces.npy")

print("give me a faceEuclideanDistance number...")
print("from training dataset (1223-->3222)")
nb = input()

with open("../faces/faceR") as faceR:
	w = []
	for v in faceR:
		if v.split()[0] != nb:
			pass
		else:
			w = [float(x) for x in v.split()[1:]]
			print(len(w))
			break

	if v.split()[0] == nb:
		print("PCA reconstructed ...")
		f = plt.figure(nb)
		a = f.add_subplot(131)
		a.set_title('a')
		i = M.transpose().dot(w) + mean_face.transpose()
		print(i.shape)
		plt.imshow(i.reshape(128,128), cmap = cm.Greys_r)
		
		print("original ...")
		b = f.add_subplot(132)
		b.set_title('b')
		orig = np.fromfile("../faces/rawdata/rawdata/"+nb, dtype=np.uint8)
		print(orig)
		plt.imshow(orig.reshape(128,128), cmap = cm.Greys_r)

		print("meanFace ...")
		c = f.add_subplot(133)
		c.set_title('c')
		j = mean_face
		plt.imshow(j.reshape(128, 128), cmap=cm.Greys_r)

		plt.show()

with open("../faces/faceS") as faceR:
	w = []
	for v in faceR:
		if v.split()[0] != nb:
			pass
		else:
			w = [float(x) for x in v.split()[1:]]
			print(len(w))
			break

	if v.split()[0] == nb:
		print("PCA reconstructed ...")
		f = plt.figure(nb)
		a = f.add_subplot(131)
		a.set_title('a')
		i = M.transpose().dot(w) + mean_face.transpose()
		print(i.shape)
		plt.imshow(i.reshape(128, 128), cmap=cm.Greys_r)

		print("original ...")
		b = f.add_subplot(132)
		b.set_title('b')
		orig = np.fromfile("../faces/rawdata/rawdata/" + nb, dtype=np.uint8)
		print(orig)
		plt.imshow(orig.reshape(128, 128), cmap=cm.Greys_r)

		print("meanFace ...")
		c = f.add_subplot(133)
		c.set_title('c')
		j = mean_face
		plt.imshow(j.reshape(128, 128), cmap=cm.Greys_r)

		plt.show()