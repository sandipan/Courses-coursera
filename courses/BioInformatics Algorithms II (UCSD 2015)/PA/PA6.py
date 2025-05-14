from PA4 import LimbLength, read_file

def dist(C1, C2, D):

	DC1C2 = 0
	for i in C1:
		for j in C2:
			DC1C2 += D[i,j]
	DC1C2 /= (1.0 * len(C1) * len(C2))
	return DC1C2

def UPGMA(D, n):
	
	clusters, T, Age = {}, {}, {}
	#form n clusters, each containing a single element i (for i from 1 to n)
	#construct a graph T by assigning a node to each cluster (without adding any edges) 
	#for every node v in T 
	#	Age(v) = 0
	for i in range(n):
		clusters[i], Age[i] = [i], 0
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
		#add a new node C to T and connect it to nodes C1 and C2 by directed edges
		T[id, i] = T[id, j] = 0
		DCij = D[i, j] #D[i, j] #dist(clusters[i], clusters[j], D)
		#Age(C) = DC1,C2 / 2
		Age[id] = round(DCij / 2.0, 3)
		#add a row and column to D for C by recomputing DC,C* for each C* != C
		#print 'merging', i, j
		for m in cids:
			if m == i or m == j or m == id: continue
			D[m, id] = D[id, m] = round((1.0 * (len(clusters[i]) * D[i, m] + len(clusters[j]) * D[j, m])) / (len(clusters[i]) + len(clusters[j])), 3)
		cids += [id]
		#remove rows and columns of D corresponding to C1 and C2
		del clusters[i]
		del clusters[j]
		for p in cids:
			for q in cids:
				if (p == i or p == j or q == i or q == j) and (p, q) in D: del D[p, q]
		cids.remove(i)
		cids.remove(j)
	#root = the node in T corresponding to the cluster C
	#for each edge (v,w) in T
		#Length(v,w) = Age(v) - Age(w)
	edges = T.keys()
	for (v, w) in edges:
		T[v, w] = T[w, v] = Age[v] - Age[w]
	
	return T

'''
#lines = read_file("inp7.txt")
#lines = read_file("UPGMA.txt")
lines = read_file("dataset_10332_8.txt")
n = int(lines[0])
D, i = {}, 0
for line in lines[1:]:
	dists = map(int, str.split(line))
	for j in range(n): D[i, j] = dists[j]
	i += 1
#print D

T = UPGMA(D, n)
for node1, node2  in sorted(T):
	print node1, '->', node2, ':', T[node1, node2]
'''

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
	#print 'D*', Dstar
	#find elements i and j such that D*i,j is a minimum element of D*
	vmin, imin, jmin = float('inf'), -1, -1
	for i in range(n):
		for j in range(n):
			if i != j and Dstar[i][j] < vmin: 
				vmin, imin, jmin = Dstar[i][j], i, j
	i, j = imin, jmin
	Delta = (TotalDistanceD[i] - TotalDistanceD[j]) / (n - 2.0)
	limbLengthi = round(0.5 * (D[i][j] + Delta), 3)
	limbLengthj = round(0.5 * (D[i][j] - Delta), 3)
	#add a new row/column m to D so that Dk,m = Dm,k = (1/2)(Dk,i + Dk,j - Di,j) for any k
	#m = len(D)
	for k in range(n):
		D[k].append(0.5 * (D[k][i] + D[k][j] - D[i][j]))
	D.append([0.5 * (D[k][i] + D[k][j] - D[i][j]) for k in range(n)] + [0])
	#remove i-th row and column as well as j-th row and column from D
	D = [[D[p][q] for p in set(range(n + 1)) - set([i, j])] for q in set(range(n + 1)) - set([i, j])]
	iid, jid, mid = idlist[i], idlist[j], id
	idlist.append(id)
	idlist.remove(idlist[max(i, j)])
	idlist.remove(idlist[min(i, j)])
	id += 1
	T = NeighborJoining(D, n - 1, T, idlist)
	#add two new limbs (connecting node m with leaves i and j) to the tree T
	T[mid], T[iid], T[jid] = T.get(mid, {}), T.get(iid, {}), T.get(jid, {})
	T[mid][iid], T[mid][jid] = limbLengthi, limbLengthj
	T[iid][mid], T[jid][mid] = limbLengthi, limbLengthj
	#assign length limbLengthi to Limb(i)
	#assign length limbLengthj to Limb(j)
	#L[i], L[j] = limbLengthi, limbLengthj
	return T
	
#lines = read_file("inp10.txt")
#lines = read_file("Neighbor_Joining.txt")
lines = read_file("dataset_10333_6.txt")
n = int(lines[0])
D = [[0 for _ in range(n)] for _ in range(n)]
D = [map(int, str.split(line)) for line in lines[1:]]
#print D
id = n
T = NeighborJoining(D, n, {}, list(range(n)))
for i in sorted(T):
	for j in T[i]:
		print i, '->', j, ":{0:.3f}".format(T[i][j])
#idl, idi = 0, n
#limbLengthA = [0] * n
#limbLengthA = [LimbLength(n, D, i) for i in range(n)]
#T = AdditivePhylogeny(D, n - 1, {})
#for node in T:
#	for node1, edge in T[node].iteritems():
#		print node, '->', node1, ':', edge