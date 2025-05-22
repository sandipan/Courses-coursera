from PA4 import read_file

def LimbLength(n, D, j):
	
	lengths = []
	for i in range(n):
		for k in range(n):
			if i == k or j == k or i == j: continue
			lengths += [(D[i][j] + D[j][k] - D[i][k]) / 2.0]
	#print lengths
	return min(lengths)

lines = read_file("quiz2_4.txt")
n = int(lines[0])
j = int(lines[1])
D = [[0 for _ in range(n)] for _ in range(n)]
i = 0
for line in lines[2:]:
	d = map(int, str.split(line))
	for k in range(len(d)):
		D[i][k] = d[k]
	i += 1
print LimbLength(n, D, j)

def NeighborJoining(D, n, T, idlist):
	global id
	if n == 2:
		T[id - 2] = {id - 1: round(D[0][1], 3)}
		T[id - 1] = {id - 2: round(D[0][1], 3)} #the tree consisting of a single edge of length D1,2
		return T
	#D* = neighbor-joining matrix constructed from D
	TotalDistanceD = [sum(x) for x in D]
	#print 'Tot', TotalDistanceD
	Dstar = [[(n - 2)*D[i][j] - (i != j) * TotalDistanceD[i] - (i != j) * TotalDistanceD[j] for i in range(n)] for j in range(n)]
	print 'D*', Dstar

lines = read_file("quiz2_5.txt")
n = int(lines[0])
D = [[0 for _ in range(n)] for _ in range(n)]
D = [map(int, str.split(line)) for line in lines[1:]]
#print D
id = n
T = NeighborJoining(D, n, {}, list(range(n)))