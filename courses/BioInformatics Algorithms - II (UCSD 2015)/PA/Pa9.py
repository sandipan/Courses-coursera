from PA4 import read_file
from PA8 import dist1
import numpy as np
from math import exp
	
def ExpectationMaximization(Data, k, m, n, beta):

	x = np.array([Data[i,:] for i in range(k)])
	#print x
	for iter in range(100):
		#Centers to Soft Clusters (E-step): After centers have been selected, assign each data point a 'responsibility' value for each cluster, 
		#where higher values correspond to stronger cluster membership. 
		Z = [sum([exp(-beta * dist1(Data[j,:], x[i,:], n)) for i in range(k)]) for j in range(m)]
		HiddenMatrix = np.array([[exp(-beta * dist1(Data[j,:], x[i,:], n)) / Z[j] for i in range(k)] for j in range(m)]).T
		#Soft Clusters to Centers (M-step): After data points have been assigned to soft clusters, compute new centers.
		x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
		#print x
	for i in range(k):
		print ' '.join(map(str, x[i,:]))

'''		
#lines = read_file("inp14.txt")
lines = read_file("dataset_10933_7.txt")
k, n = map(int, str.split(lines[0]))
beta = float(lines[1])
Data = []
for line in lines[2:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
#print Data
#print k, m, n, beta
ExpectationMaximization(Data, k, m, n, beta)
'''

def dist(C1, C2, D):

	DC1C2 = 0
	for i in C1:
		for j in C2:
			DC1C2 += D[i,j]
	DC1C2 /= (1.0 * len(C1) * len(C2))
	return DC1C2
	
def HierarchicalClustering(D, n):
	#Clusters = n single-element clusters labeled 1, ... , n 
	#construct a graph T with n isolated nodes labeled by single elements 1, ... , n 
	#while there is more than one cluster 
	#find the two closest clusters Ci and Cj 
	#merge Ci and Cj into a new cluster Cnew with |Ci| + |Cj| elements
	#add a new node labeled by cluster Cnew to T
	#connect node Cnew to Ci and Cj by directed edges
	#remove the rows and columns of D corresponding to Ci and Cj
	#remove Ci and Cj from Clusters
	#add a row/column to D for Cnew by computing D(Cnew, C) for each C in Clusters 
	#add Cnew to Clusters 
	#assign root in T as a node with no incoming edges
	#return T 
	clusters, T = {}, {i:[] for i in range(n)}
	for i in range(n): clusters[i] = [i]
	cids, id = range(n), n - 1
	#while there is more than one cluster	
	while len(clusters) > 1: 
		min, imin, jmin = float('inf'), -1, -1
		#find two closest clusters C1 and C2 (break ties arbitrarily)
		for i in cids:
			for j in cids:
				if i != j and D[i,j] < min: min, imin, jmin = D[i,j], i, j
		#merge C1 and C2 into a new cluster C
		i, j = imin, jmin
		id += 1
		clusters[id] = clusters[i] + clusters[j] #number of leaves in cluster C.
		print ' '.join(map(str, [c + 1 for c in clusters[id]]))
		T[id] = [i, j]
		T[i] = T.get(i, []) + [id]
		T[j] = T.get(j, []) + [id]
		#print 'merging', i, j
		D[id, id] = 0
		for m in cids:
			if m == i or m == j or m == id: continue
			D[m, id] = D[id, m] = dist(clusters[id], clusters[m], D)
		cids += [id]
		#remove rows and columns of D corresponding to C1 and C2
		del clusters[i]
		del clusters[j]
		#for p in cids:
		#	for q in cids:
		#		if (p == i or p == j or q == i or q == j) and (p, q) in D: del D[p, q]
		cids.remove(i)
		cids.remove(j)
	
	return T
	
#lines = read_file("inp15.txt")
lines = read_file("dataset_10934_7.txt")
n = int(lines[0])
D, i = {}, 0
for line in lines[1:]:
	dists = map(float, str.split(line))
	for j in range(n): D[i, j] = dists[j]
	i += 1
#print D

T = HierarchicalClustering(D, n)
#for node1, node2  in sorted(T):
#	print node1, '->', node2, ':', T[node1, node2]