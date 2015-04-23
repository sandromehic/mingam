import numpy as np
from itertools import product

def getA(n, m):
	return float(np.power(2,m))/n

N = range(51,550,50)
M = range(2,11)

for n,m in product(N,M):
	print "n: {}, m: {}, alpha: {}".format(n,m,getA(n,m))