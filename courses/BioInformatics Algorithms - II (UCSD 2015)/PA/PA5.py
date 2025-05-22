from PA4 import LimbLength, read_file

def bfs(s, e, alist):
	queue, visited, par, dist = [s], set({}), {s:None}, {s:0} # fringe
	while len(queue) > 0:
		u = queue.pop(0)
		if u == e:
			return par, dist
		for nu in alist[u]:
			v, w = nu, alist[u][nu]
			if not v in visited:
				par[v] = u
				dist[v] = dist[u] + w
				queue.append(v)
		visited.add(u)
	return None

def get_i_k_x_y(i, k, x, y, T):
	path, (par, dist), s = [], bfs(i, k, T), k
	while s != i:
		path = [s] + path
		s = par[s]
	path = [s] + path
	#print 'path:', path
	j = 0
	while j < len(path) - 1 and T[path[j]][path[j + 1]] < x:
		#print path[j], path[j + 1], T[path[j]][path[j + 1]], x
		x -= T[path[j]][path[j + 1]]
		j += 1
	i, k, y = path[j], path[j + 1], T[path[j]][path[j + 1]] - x
	return i, k, x, y		
		
def AdditivePhylogeny(D, n, T):
	global idl, idi, limbLengthA
	if n == 1:
		T[idl] = {idl+1: D[0][1]}
		T[idl+1] = {idl: D[0][1]} #the tree consisting of a single edge of length D1,2
		idl += 2
		return T
	#limbLength = limbLengthA[n] 
	limbLength = LimbLength(n + 1, D, n) 
	for j in range(n):
		D[j][n] -= limbLength
		D[n][j] = D[j][n]
	i, k = 0, 0
	while i < n:
		while k < n:
			if i != k and D[i][k] == D[i][n] + D[n][k]: break
			k += 1
		if D[i][k] == D[i][n] + D[n][k]: break
		i += 1
	x, y = D[i][n], D[n][k]
	
	#remove n-th row and column from D
	T = AdditivePhylogeny([[D[p][q] for p in range(n)] for q in range(n)], n - 1, T)
	
	i, k, x, y = get_i_k_x_y(i, k, x, y, T)
	
	#v = the (potentially new) node in T located at distance x from leaf i on the path between i and k
	T[idi] = {i: x, k: y}
	T[i][idi], T[k][idi] = x, y
	if k in T[i]: del T[i][k]
	if i in T[k]: del T[k][i]
	oid = idi
	idi += 1
	#add leaf n back to T by creating a limb (v, n) of length limbLength
	T[idl] = {oid: limbLength}
	T[oid][idl] = limbLength
	idl += 1
	return T

#lines = read_file("inp4.txt")
#lines = read_file("Additive_Phylogeny.txt")
lines = read_file("dataset_10330_6.txt")
n = int(lines[0])
D = [[0 for _ in range(n)] for _ in range(n)]
D = [map(int, str.split(line)) for line in lines[1:]]
#print D
idl, idi = 0, n
limbLengthA = [0] * n
limbLengthA = [LimbLength(n, D, i) for i in range(n)]
T = AdditivePhylogeny(D, n - 1, {})
for node in T:
	for node1, edge in T[node].iteritems():
		print node, '->', node1, ':', edge