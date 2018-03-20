'''
X is faceR 1223
Y is faceS 3223
'''
from pg2.paillier_gmpy2 import *
from functools import reduce

#TODO import dataset
X = [int (float (x)) for x in "-1779.619019 2107.301270 807.759949 -654.226135 322.416931 1075.673706 559.180786 452.465454 -561.820374 74.668030 67.978477 198.796906 22.676338 -172.910126 306.917023 154.041595 -403.840271 -66.760246 100.143784 -189.239578 35.033672 -291.399200 -12.720598 120.488663 -325.439758 -237.672791 -162.531113 -184.136658 214.378540 -168.662018 193.702835 -253.508377 -270.742218 293.662354 -15.763512 130.660538 -39.088024 -209.809036 112.635559 -54.906422 -223.773926 151.183868 -174.183105 311.799347 -131.172348 100.358414 -39.231071 143.831268 -26.763599 -134.834457 22.852604 37.737930 61.850765 -220.789551 127.344765 42.378975 25.868210 -40.372673 -97.774818 144.796448 13.325173 -80.345116 20.910030 -85.240402 -57.382092  9.731221 64.159706 41.712112 139.698776 131.256653 -123.708351 -81.298141 -85.131653 39.110416 229.450867 -74.828201 164.768158 76.867096 -55.710514 -38.793930 146.945541 -168.382278 16.658672 257.251373 140.037918 131.178085 -97.415123 185.057739 -91.611031 117.541168 -12.968436 253.902130 -180.755005 120.390350 207.105194 144.583420 -86.194237 12.877232 23.882339".split()]
Y = [int (float (y)) for y in "1509.810059 -258.181854 -1190.012451 -1037.669922 -1188.631470 818.807190 -471.177979 -208.943344 449.044403 -780.172485 321.551300 864.010132 -390.810883 173.809250 683.781982 643.608826 451.915771 141.310333 -76.486908 183.826935 318.284149 644.307434 -431.986542 227.587723 14.175001 -27.727854 16.711973 644.640930 672.497437 -215.462265 188.154007 -214.503250 506.547668 93.807892 -434.446411 -159.584045 -374.567413 -144.292999 -12.633429 250.253510 -6.646331 -130.159882 -109.816933 55.415783 -155.051193  0.495085 -50.177628 201.995667 -53.390995 92.968117 91.921387 -8.088350 31.098257 42.542473 -253.944458 74.592117 -58.572212 -156.825851 121.438957 -137.321198 19.722845 -137.223740 -284.360596 28.395737 -79.323524 -40.672832 236.605408 88.930946 87.252899 220.377228 172.345139 25.654402 138.034622 -142.959030 253.537369 -40.584583 239.124023 -2.309621 77.095047 119.168510 220.420303 -95.924782 19.305809 -92.400146 -11.840094 266.022888 57.265312 149.599121 57.345749 -58.652893 38.077988 -109.674408 97.710808 136.022873 -112.564461 -84.589500 -156.004730 -24.142797 -30.994535".split()]

#TODO to compute D^2 = sum[(Vi-V`i)^2]
print("D^2 = sum[(Vi-V`i)^2]", sum([(x - y)**2 for x, y in zip(X, Y)]))

#TODO generate keyPair
priv, pub = generate_keypair(512)

#TODO encrypt X and Y, get cX and cY   get E(Vi) and E(V`i)
cX = [encrypt(pub, x) for x in X] 
cY = [encrypt(pub, y) for y in Y]

#TODO encrypt X^2 and Y^2, get E(Vi^2) and E(V`i^2)
cX2 = [encrypt(pub, x*x) for x in X]
cY2 = [encrypt(pub, y*y) for y in Y]

#TODO encrypted distance computation
d1 = [e_add(pub, x, y)  for x, y in zip(cX2, cY2)]
d2 = [e_mul_const(pub, x, -2*y) for x, y in zip(cX, Y)]
d3 = [e_add(pub, x, y)  for x, y in zip(d1, d2)]
d = reduce(lambda x, y: e_add(pub, x, y), d3)

#TODO decrypt
decrypted_distance = int(decrypt(priv, pub, d))
print(decrypted_distance)