
def count_in_out_degrees(adj):
	n = len(adj)
	in_deg, out_deg = [0]*n, [0]*n
	for u in range(n):
		for v in adj[u]:
			out_deg[u] += 1
			in_deg[v] += 1			
	return in_deg, out_deg
	
def get_start_if_Euler_path_present(in_deg, out_deg):
	start, end, path = None, None, True
	for i in range(in_deg):
		d = out_deg[i] - in_deg[i]
		if abs(d) > 1:
			path = False
			break
		elif d == 1:
			start = i
		elif d == -1:
			end = i
		path = (start != None and end != None) or (start == None and end == None)
		if path and start == None: # a circuit 
			start = 0
		return (path, start)
	
def dfs(adj, v, out_deg, path):
	while out_deg[v] > 0:
		out_deg[v] -= 1
		dfs(adj[v][out_deg[v]], path)
	path = [v] + path

def compute_Euler_path(adj):
	n, m = len(adj), sum([len(adj[i]) for i in range(len(adj))])
	print(n, m)
	in_deg, out_deg = count_in_out_degrees(adj)
	path_present, start = get_start_if_Euler_path_present(in_deg, out_deg)
	if not path_present:
		return None
	path = []
	dfs(adj, start, path)
	print(path, len(path))
	if len(path) == m+1:
		return path
	return None
	
def DegreesNbrs(edges, dir = True):
	vertices, indegrees, outdegrees, nbrs = set([]), {}, {}, {}
	for e in edges:
		e = e.replace('->', ' ')
		#print e
		u, vs = str.split(e)
		u = int(u)
		vertices.add(u)
		vs = vs.split(',')
		for v in vs:
			v = int(v) 
			vertices.add(v)
			outdegrees[u] = outdegrees.get(u, 0) + 1
			indegrees[v] = indegrees.get(v, 0) + 1
			nbrs[u] = nbrs.get(u, []) + [v]
			if not dir:
				nbrs[v] = nbrs.get(v, []) + [u]
	vertices = list(vertices)		
	return vertices, indegrees, outdegrees, nbrs

def read_file(filename):
	return [line.strip() for line in open(filename)]

lines = read_file('e1.txt')
vertices, degrees, nbrs = DegreesNbrs(edges, dir = True)
adj = [[] for _ in range(len(nbrs))]
for i in range(len(nbrs)):
	adj[i] += nbrs[i]
compute_Euler_path(adj)
