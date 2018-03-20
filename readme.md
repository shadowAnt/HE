pg2
    primes_gmpy2.py
        生成指定长度的大素数

    paillier_gmpy2.py
        加解密，同态加法运算

    demo_gmpy2.py
        加解密实例

    ImageWithEnrcyption.py
        从测试集中选一个图片，把99个系数加密解密下

    distance2vectors.py
        两个实例的距离平方和加解密

    DistanceEuclideanEncrypted.py


src
    mean_face.py
        meanFace is 1 * 16384 ,return type is numpy.array float

    eigenfaces.npy
        99*16384

    show.py
        PCA reconstructed = eigenFace.T * faceR(list) + mean_face.T
        16384*1           = 99*16384.T  *  99*1  + 1*16384.T

    ImageWithEncryption.py
        从测试集中选一个图片，把99个系数加密解密

    faceEuclideanDistance1.py
        takes one face number as input and computes the euclidean distance to all the training faces, then it returns the k nearest ones

    TestingAllImageForStatistics1.py
        have the testing of 2000 face of FaceS, classify each face in the faceS (testing dataset)

    encryptedDistance.py
        takes one face number as input and computes the encrytion of euclidean distance to all the training faces, then it returns the k nearest ones

    classifiersSKlearn.py
        几种机器学习的性能对比