# Q1
p = 0.7
print p*(1-p)*p*p*(1-p)

def read_file(filename):
	return [line.strip() for line in open(filename)]

def dist1(DataPoint1, DataPoint2, n):
	return sum([(DataPoint1[k] - DataPoint2[k])**2 for k in range(n)])

import numpy as np
from math import exp, sqrt

def dist2(d1, d2, n):
	return sqrt(dist1(d1, d2, n))

def ExpectationMaximization(Centers, Data, k, m, n, beta):
	
	x = np.array([Centers[i,:] for i in range(k)]) # centers
	#print x
	for iter in range(100):
		#Centers to Soft Clusters (E-step): After centers have been selected, assign each data point a 'responsibility' value for each cluster, 
		#where higher values correspond to stronger cluster membership. 
		Z = [sum([exp(-beta * dist2(Data[j,:], x[i,:], n)) for i in range(k)]) for j in range(m)]
		HiddenMatrix = np.array([[exp(-beta * dist1(Data[j,:], x[i,:], n)) / Z[j] for i in range(k)] for j in range(m)]).T
		#Soft Clusters to Centers (M-step): After data points have been assigned to soft clusters, compute new centers.
		x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
	for i in range(k):
		print ' '.join(map(str, x[i,:]))

lines = read_file("inp.txt")
k, n = map(int, str.split(lines[0]))
beta = float(lines[1])
Centers = []
for line in lines[2:4]:
	Centers.append(map(float, str.split(line)))
Data = []
for line in lines[4:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
#print Centers
#print k, m, n, beta

x = np.array(Centers) # centers
Z = [sum([exp(-beta * dist2(Data[j,:], x[i,:], n)) for i in range(k)]) for j in range(m)]
HiddenMatrix = np.array([[exp(-beta * dist1(Data[j,:], x[i,:], n)) / Z[j] for i in range(k)] for j in range(m)]).T
print HiddenMatrix

lines = read_file("inp1.txt")
k, m, n = map(int, str.split(lines[0]))
Data = []
for line in lines[1:1+m]:
	Data.append(map(float, str.split(line)))
HiddenMatrix = []
for line in lines[1+m:]:
	HiddenMatrix.append(map(float, str.split(line)))
Data = np.array(Data)
HiddenMatrix = np.array(HiddenMatrix)
#print Data
#print HiddenMatrix
x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
print x		
#ExpectationMaximization(Centers, Data, k, m, n, beta)

def Dmin(D, C1, C2):
	D = [D[i][j] for i in C1 for j in C2]
	print D
	print min(D)

C1, C2 = [0, 3], [1, 2]
D = [[0, 20, 9, 11], [20, 0, 17, 11], [9, 17, 0, 8], [11, 11, 8, 0]]
Dmin(D, C1, C2)