import re

def bfs(s, alist):
	queue, visited, dist = [s], set({}), {s:0} # fringe
	while len(queue) > 0:
		u = queue.pop(0)
		for nu in alist[u]:
			v, w = nu[0], nu[1]
			if not v in visited:
				dist[v] = dist[u] + w
				queue.append(v)
		visited.add(u)
	return dist

def DistancesBetweenLeaves(n, alist):
	#print n	
	leaves = sorted([v for v in alist if len(alist[v]) == 1])
	nodes = sorted(alist)
	#print leaves
	#print nodes
	for leaf in leaves:
		dist = bfs(leaf, alist)
		print ' '.join(map(str, [dist[v] for v in leaves]))
	
def read_file(filename):
	return [line.strip() for line in open(filename)]

pat = '(\d+)->(\d+):(\d+)'
#lines = read_file("inp.txt")
#lines = read_file("Distance_Between_Leaves_inp.txt")
lines = read_file("dataset_10328_11.txt")
n = int(lines[0])
alist = {}
for line in lines[1:]:
	m = re.match(pat, line)
	u, v, w = int(m.group(1)), int(m.group(2)), int(m.group(3))
	alist[u] = alist.get(u, []) + [(v, w)]

#print n, alist	
#DistancesBetweenLeaves(n, alist)

def LimbLength(n, D, j):
	
	lengths = []
	for i in range(n):
		for k in range(n):
			if i == k or j == k or i == j: continue
			lengths += [(D[i][j] + D[j][k] - D[i][k]) / 2.0]
	#print lengths
	return min(lengths)

'''	
#lines = read_file("inp1.txt")
lines = read_file("dataset_10329_11.txt")
n = int(lines[0])
j = int(lines[1])
D = [[0 for _ in range(n)] for _ in range(n)]
i = 0
for line in lines[2:]:
	d = map(int, str.split(line))
	for k in range(len(d)):
		D[i][k] = d[k]
	i += 1
#print n, j
#print D
print LimbLength(n, D, j)
'''