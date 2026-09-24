import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def optimize(cs, k):
	cxs, cys = [0]*k, [0]*k
	for i in range(k):
		c = cs[i]
		#print(c)
		cxs[i] = np.mean([x for (x,y) in c])
		cys[i] = np.mean([y for (x,y) in c])
	return cxs, cys

def assign(ps, cs):
	cxs, cys = cs
	k = len(cxs)
	ass = {i:[] for i in range(k)}
	for p in ps:
		x, y = p
		ci = np.argmin([(cxs[i]-x)**2+(cys[i]-y)**2 for i in range(k)])
		ass[ci].append((x,y))
	return ass

def obj(ass, cs):
	cxs, cys = cs
	k = len(cxs)
	s = 0
	for i in range(k):
		ps = ass[i]
		for p in ps:
			x, y = p
			s += (cxs[i]-x)**2 + (cys[i]-y)**2
	return s

'''
k = 2
ps = [(2,5),(1,4),(2,4),(2,3),(4,3),(5,3),(3,2),(4,2)]
cs = ([1, 4], [5, 3])
cxs, cys = [x for x,y in cs], [y for x,y in cs]
ass = assign(ps, (cxs, cys))
print(ass)
print(obj(ass, cs))

cxs, cys = optimize(ass, k)
cs = list(zip(cxs, cys)) 
print(cs)
print(obj(ass, (cxs, cys)))

kmeans = KMeans(n_clusters=k, init=cs).fit(ps)
print(kmeans.labels_)
print(kmeans.cluster_centers_) 
print(kmeans.inertia_)
'''

k = 3
ps = [(5,8),(2,4),(0,0),(5,6),(3,3),(2,1),(9,8),(3,6),(5,1),(9,3)]
cs = ([0, 0], [3, 3], [9, 8])
cxs, cys = [x for x,y in cs], [y for x,y in cs]
niter = 1
for iter in range(niter):
	ass = assign(ps, (cxs, cys))
	print(ass)
	cxs, cys = optimize(ass, k)
	cs = list(zip(cxs, cys)) 
	print(cs)
	#print(obj(ass, (cxs, cys)))

kmeans = KMeans(n_clusters=k, init=cs).fit(ps)
print(kmeans.labels_)
print(kmeans.cluster_centers_) 
