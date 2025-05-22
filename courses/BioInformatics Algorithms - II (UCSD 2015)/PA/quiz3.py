from PA4 import read_file
#import numpy as np
import math

def dist(Data, i, j, n):
	return math.sqrt(sum([(Data[i][k] - Data[j][k])**2 for k in range(n)]))

def MaxDistance(Data, k, m, n):
	#DataPoint <- an arbitrary point from Data
	#Centers <- the set consisting of the single point DataPoint 
	Centers = list(range(k))
	dmax = -1
	for i in range(m):
		if i in Centers: continue
		d, c = min([(dist(Data, i, j, n), j) for j in Centers])
		#print i, d, c
		dmax = max(d, dmax)	
	#add DataPoint to Centers 
	print dmax
	
lines = read_file("inp20.txt")
lines = read_file("inp21.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
MaxDistance(Data, k, m, n)

def sqrdist(Data, i, j, n):
	return sum([(Data[i][k] - Data[j][k])**2 for k in range(n)])
	
def Distortion(Data, k, m, n):
	#DataPoint <- an arbitrary point from Data
	#Centers <- the set consisting of the single point DataPoint 
	Centers = list(range(k))
	dsum = 0.0
	for i in range(m):
		if i in Centers: continue
		d, c = min([(sqrdist(Data, i, j, n), j) for j in Centers])
		#print i, d, c
		dsum += d
	#add DataPoint to Centers 
	print dsum / (m - k)
	
lines = read_file("inp21.txt")
#lines = read_file("inp20.txt")
k, n = map(int, str.split(lines[0]))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
#print k, m, n, m - k
Distortion(Data, k, m, n)