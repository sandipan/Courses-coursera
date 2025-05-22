from PA4 import read_file
#import numpy as np

def dist(Data, i, j, n):
	return sum([(Data[i][k] - Data[j][k])**2 for k in range(n)]) 

def FarthestFirstTraversal(Data, k, m, n):
	#DataPoint <- an arbitrary point from Data
	#Centers <- the set consisting of the single point DataPoint 
	Centers = [0]
	while len(Centers) < k: 
		#DataPoint <- the point in Data maximizing d(DataPoint, Centers) 
		dmax, imax = -1, -1 
		for i in range(m):
			if i in Centers: continue
			d, c = min([(dist(Data, i, j, n), j) for j in Centers])
			if d > dmax: dmax, imax = d, i	
		#add DataPoint to Centers 
		Centers.append(imax)
	return [Data[c] for c in Centers]

'''
#lines = read_file("inp11.txt")
lines = read_file("dataset_10926_14.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
for DataPoint in FarthestFirstTraversal(Data, k, m, n):
	print ' '.join(map(str, DataPoint))
'''

import math
def dist1(DataPoint1, DataPoint2, n):
	return math.sqrt(sum([(DataPoint1[k] - DataPoint2[k])**2 for k in range(n)]))

def SquaredErrorDistortion(Data, Centers, k, m, n):
	SSE = 0
	for i in range(m):
		d = min([dist1(Data[i], Centers[j], n) for j in range(len(Centers))])
		SSE += d
	return (1.0  * SSE) / m

'''
#lines = read_file("inp12.txt")
lines = read_file("dataset_10927_3.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data, Centers = [], []
for line in lines[1:1+k]:
	Centers.append(map(float, str.split(line)))
for line in lines[1+k+1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
print SquaredErrorDistortion(Data, Centers, k, m, n)
'''

from copy import deepcopy
def centroid(D, C, n):
	c = [0.0 for i in range(n)]
	for j in range(n):
		for p in C:
			c[j] += Data[p][j]
	return [x / len(C) for x in c]		

def LloydAlgorithm(Data, k, m, n):
	Data_Center = {i:i for i in range(k)}
	Centers = [[i] for i in range(k)]
	max_iter = 100 #00
	for iter in range(max_iter):
		#print Centers
		#print [centroid(Data, Centers[j], n) for j in range(k)]
		changed, Temp_Centers = False, deepcopy(Centers)
		for i in range(m):
			prevc = Data_Center.get(i, None)
			d, c = min([(dist1(Data[i], centroid(Data, Centers[j], n), n), j) for j in range(k)])
			#print 'Assigned point', i, 'to cluster', c
			if prevc != c:
				if prevc != None: Temp_Centers[prevc].remove(i)
				Temp_Centers[c].append(i)
				Data_Center[i] = c
				changed = True
		if not changed: break		
		Centers = Temp_Centers	
	return [centroid(Data, Centers[j], n) for j in range(k)]

'''
#lines = read_file("inp13.txt")
#lines = read_file("Lloyd.txt")
lines = read_file("dataset_10928_3.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
#print Data
for center in LloydAlgorithm(Data, k, m, n):
	print ' '.join(map(str, center))
'''