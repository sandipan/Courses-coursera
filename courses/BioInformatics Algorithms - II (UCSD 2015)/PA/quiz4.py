from PA4 import read_file
import numpy as np

def dist1(DataPoint1, DataPoint2, n):
	return sum([(DataPoint1[k] - DataPoint2[k])**2 for k in range(n)])

# (0.8)**3 * (0.2)**2
# (0.8)**5 * (0.2)**1
# (0.7)**5 * (0.3)**1
# (0.7)**3 * (0.3)**2

def HiddenMagtrixWithNewtonInverseSquare(Data, k, m, n):
	x = np.array([Data[i,:] for i in range(k)])
	Z = [sum([1.0 / dist1(Data[j,:], x[i,:], n) for i in range(k)]) for j in range(k, m)] # partition function for normalization
	HiddenMatrix = np.array([[(1.0 / dist1(Data[j,:], x[i,:], n)) / Z[j-k] for i in range(k)] for j in range(k, m)]).T
	print HiddenMatrix

lines = read_file("inp22.txt")
k, n = map(int, str.split(lines[0]))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
HiddenMagtrixWithNewtonInverseSquare(Data, k, m, n)

def WeightedCG(Data, HiddenMatrix):
	x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
	print x

lines = read_file("inp22.txt")
lines = read_file("inp23.txt")
k, n = map(int, str.split(lines[0]))
Data = []
for line in lines[1+k:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
#HiddenMatrix = np.array([[0.5, 0.3, 0.8, 0.4, 0.9], [0.5, 0.7, 0.2, 0.6, 0.1]])
HiddenMatrix = np.array([[0.6, 0.1, 0.8, 0.5, 0.7], [0.4, 0.9, 0.2, 0.5, 0.3]])
WeightedCG(Data, HiddenMatrix)

def Davg(D, C1, C2):
	return sum([sum([D[i][j] for i in C1]) for j in C2]) / (1.0 * len(C1) * len(C2))
	
def Dmin(D, C1, C2):
	return min([min([D[i][j] for i in C1]) for j in C2])
	
D = [[0, 20, 9, 11], [20,  0, 17, 11], [9, 17,  0,  8], [11, 11,  8,  0]]
#C1, C2 = [0, 2], [1, 3]
C1, C2 = [0, 3], [1, 2]
print Davg(D, C1, C2)
#C1, C2 = [0, 3], [1, 2]
C1, C2 = [0, 2], [1, 3]
print Dmin(D, C1, C2)