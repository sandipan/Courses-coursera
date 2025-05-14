from PA4 import read_file

def delta(i, j):
	return 0 if i == j else 1

def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

def SmallParsimony(T, Character, parent, leaves, alphabet, root):
	
	#Tag = {}
	s, a = {k:{} for k in alphabet}, {k:{} for k in alphabet}
	
	for v in T:
		if v in leaves: # if v is leaf
			#Tag[v] = 1
			for k in alphabet:
				if Character[v] == k:
					s[k][v] = 0
				else:
					s[k][v] = float('inf')
		#else:
		#	Tag[v] = 0

	queue = list(set([parent[leaf] for leaf in leaves]))
	while len(queue) > 0: 	 # there exist ripe nodes in T
		v = queue.pop(0) 	 # a ripe node in T
		#Tag[v] = 1
		daughter, son = T[v]
		for k in alphabet:
			# s[k][v] = minimum over all symbols i {s[i][Daughter(v)] + delta(i,k)} + minimum over all symbols j {s[j][Son(v)] + delta(j,k)}
			mdv, mda = min([(s[i][daughter] + delta(i, k), i) for i in alphabet])
			msv, msa = min([(s[j][son] + delta(j, k), j) for j in alphabet])
			s[k][v] = mdv + msv
			a[k][v], a[k][daughter], a[k][son] = k, mda, msa
		p = parent.get(v, None)
		if p and not p in queue:
			queue.append(p)
	
	# minimum over all symbols k {s[k][root]}
	return min([(s[k][root], k) for k in alphabet]), a

'''	
alphabet = ['A', 'C', 'T', 'G']
#lines = read_file("inp16.txt")
#lines = read_file("inp17.txt")
#lines = read_file("Small_Parsimony.txt")
lines = read_file("Small_Parsimony_Unrooted_Tree.txt")
#lines = read_file("dataset_10335_10.txt")
#lines = read_file("dataset_10335_12.txt")
n = int(lines[0])
T, parent, leaves, id, strings = {}, {}, [], 0, {}
for line in lines[1:]:
	p, c = str.split(line, '->')
	if not p.isdigit():
		continue
	p = int(p)
	if not c.isdigit():
		strings[id] = c
		leaves += [id]
		T[id] = []
		T[p] = T.get(p, []) + [id]
		parent[id] = p
		id += 1
	else: 
		c = int(c)
		T[p] = T.get(p, []) + [c]
		if p > c:
			parent[c] = p


root = list(set(T.iterkeys()) - set(parent.iterkeys()))[0]
inodes = list(set(T.iterkeys()) - set(leaves))
#print T
#print parent
#print leaves
#print root

score = 0
for inode in inodes:
	strings[inode] = ''
	
for k in range(len(strings[0])):
	Character = {leaves[i]:strings[i][k] for i in range(n)}
	#print Character
	(s_k_root, a_k), a = SmallParsimony(T, Character, parent, leaves, alphabet, root)
	score += s_k_root
	strings[root] += a_k
	#print s_k_root, a_k
	queue = [(root, a_k)]
	while len(queue) > 0:
		v, a_k_v = queue.pop(0)
		daughter, son = T[v][:2]
		if not daughter in leaves:
			strings[daughter] += a[a_k_v][daughter]
			queue.append((daughter, a[a_k_v][daughter]))
		if not son in leaves:
			strings[son] += a[a_k_v][son]
			queue.append((son, a[a_k_v][son]))

print score	
#print strings

for inode in strings:
	for node in T:
		T[node] = map(lambda x: x if x != inode else strings[inode], T[node]) 
	T[strings[inode]] = T.pop(inode)
	
#print T

edges = {}
for (node, nbrs) in T.iteritems():
	for nbr in nbrs:
		#edges[node, nbr] = hamming_distance(node, nbr)
		edges[node, nbr] = edges[nbr, node] = hamming_distance(node, nbr)

for (node1, node2) in edges:
	print node1 + '->' + node2 + ':' + str(edges[node1, node2]) 
'''
	
def get_directed_tree1(T):
	for node in T:
		T[node] = [n for n in T[node] if n < node]
	return T

def get_directed_tree(T, root):
	queue, visited = [root], set([])
	while len(queue) > 0:
		node = queue.pop(0)
		for child in T[node]:
			T[child].remove(node)
			if not child in visited:
				queue.append(child)
		visited.add(node)
	return T
	
def get_rooted_tree(T, parent):
	nodes = [node for node in T.iterkeys() if len(T[node]) > 2]
	n = len(nodes)
	#assert(n == 2)
	if n == 0:
		return T, parent
	node1 = nodes[0]
	node2 = parent[node1]
	id = max(T.iterkeys()) + 1
	print 'hhh', id, node1, node2, T[node1], T[node2]
	T[id] = [node1, node2]
	T[node1] = T.get(node1, []) + [id]
	T[node2] = T.get(node2, []) + [id]
	parent[node1] = parent[node2] = id
	T[node1].remove(node2)
	T[node2].remove(node1)
	return T, parent
	
def toposort(T):
	nodes = list(T.iterkeys())
	indeg = {node:0 for node in nodes}
	for node in nodes:
		for child in T[node]:
			indeg[child] += 1
	to = []
	while len(indeg) > 0:
		#minindeg, node = min([(indeg[i], i) for i in range(len(indeg))])
		#indeg = indeg[:node] + indeg[node + 1 :]
		minindeg, node = min([(indeg[i], i) for i in indeg])
		del indeg[node]
		for child in T[node]:
			indeg[child] -= 1
		to += [node]
	return to	

from copy import deepcopy
	
def SmallParsimony_UnRooted(T, Character, parent, leaves, alphabet, root, order):
	s, a = {k:{} for k in alphabet}, {k:{} for k in alphabet}
	for v in T:
		if v in leaves: # if v is leaf
			for k in alphabet:
				if Character[v] == k:
					s[k][v] = 0
				else:
					s[k][v] = float('inf')
	queue = list(set([parent[leaf] for leaf in leaves]))
	while len(queue) > 0: 	 # there exist ripe nodes in T
		v = queue.pop(0) 	 # a ripe node in T
		children, a[k][v] = T[v], k
		for k in alphabet:
			# s[k][v] = minimum over all symbols i {s[i][Daughter(v)] + delta(i,k)} + minimum over all symbols j {s[j][Son(v)] + delta(j,k)}
			s[k][v] = 0
			#print 'H1111', v, k
			for child in children:
				#mcv, mca = min([(s[i].get(child, float('inf')) + delta(i, k), i) for i in alphabet])
				mcv, mca = min([(s[i][child] + delta(i, k), i) for i in alphabet])
				s[k][v] += mcv
				a[k][child] = mca
			#print 'H2222', v, k, s[k][v]
		p = parent.get(v, None)
		if p and not p in queue:
			queue.append(p)
	# minimum over all symbols k {s[k][root]}
	return min([(s[k][root], k) for k in alphabet]), a

alphabet = ['A', 'C', 'T', 'G']
lines = read_file("inp18.txt")
lines = read_file("Small_Parsimony_Unrooted_Tree.txt")
#lines = read_file("dataset_10335_12.txt")
n = int(lines[0])
T, parent, leaves, id, strings = {}, {}, [], 0, {}
for line in lines[1:]:
	p, c = str.split(line, '->')
	if not p.isdigit():
		continue
	p = int(p)
	if not c.isdigit():
		strings[id] = c
		leaves += [id]
		T[id] = [p]
		T[p] = T.get(p, []) + [id]
		parent[id] = p
		id += 1
	else: 
		c = int(c)
		T[p] = T.get(p, []) + [c]
		if p > c:
			parent[c] = p

T, parent = get_rooted_tree(T, parent)	

root = max(list(T.iterkeys()))
inodes = list(set(T.iterkeys()) - set(leaves))

T = get_directed_tree(T, root)
for node1 in T:
	for node2 in T[node1]:
		print str(node1) + '->' + str(node2)
#print parent

'''
order = toposort(T)
print order 


#print parent
#print "L", leaves
#print "Root", root

score = 0
for inode in inodes:
	strings[inode] = ''
	
for k in range(len(strings[0])):
	Character = {leaves[i]:strings[i][k] for i in range(n)}
	#print Character
	(s_k_root, a_k), a = SmallParsimony_UnRooted(T, Character, parent, leaves, alphabet, root, deepcopy(order))
	score += s_k_root
	strings[root] += a_k
	#print s_k_root, a_k
	queue = [(root, a_k)]
	while len(queue) > 0:
		v, a_k_v = queue.pop(0)
		print 'HHH', k, v, a_k_v
		children = T[v]
		for child in children:
			if not child in leaves:
				strings[child] += a[a_k_v][child]
				queue.append((child, a[a_k_v][child]))

print score	
print strings

for inode in strings:
	for node in T:
		T[node] = map(lambda x: x if x != inode else strings[inode], T[node]) 
	T[strings[inode]] = T.pop(inode)
#print T

edges = {}
for (node, nbrs) in T.iteritems():
	for nbr in nbrs:
		#edges[node, nbr] = hamming_distance(node, nbr)
		#print 'HHHH', node, nbr
		edges[node, nbr] = edges[nbr, node] = hamming_distance(node, nbr)

for (node1, node2) in edges:
	print node1 + '->' + node2 + ':' + str(edges[node1, node2]) 

	
	
from copy import deepcopy

def NearestNeighbors(T, a, b):
	
	w, x = [n for n in T[a] if n != b] 
	y, z = [n for n in T[b] if n != a]
	
	T1 = deepcopy(T)
	nbr_a, nbr_b, nbr_x, nbr_y = T1[a], T1[b], T1[x], T1[y]
	# remove b-y
	nbr_b.remove(y)
	nbr_y.remove(b)	
	# insert b-x
	nbr_b += [x]
	nbr_x += [b]
	# remove a-x
	nbr_a.remove(x)
	nbr_x.remove(a)	
	# insert a-y
	nbr_a += [y]
	nbr_y += [a]

	T2 = deepcopy(T)
	nbr_a, nbr_b, nbr_x, nbr_z = T2[a], T2[b], T2[x], T2[z]
	# remove b-z
	nbr_b.remove(z)
	nbr_z.remove(b)	
	# insert b-x
	nbr_b += [x]
	nbr_x += [b]
	# remove a-x
	nbr_a.remove(x)
	nbr_x.remove(a)	
	# insert a-z
	nbr_a += [z]
	nbr_z += [a]

	return T1, T2
	
#lines = read_file("inp19.txt")
lines = read_file("dataset_10336_6.txt")

a, b = map(int, str.split(lines[0]))
T = {}
for line in lines[1:]:
	p, c = str.split(line, '->')
	p, c = int(p), int(c)
	T[p] = T.get(p, []) + [c]

#print a, b
#print
#print T
#print

T1, T2 = NearestNeighbors(T, a, b)

for node1 in T1:
	for node2 in T1[node1]:
		print str(node1) + '->' + str(node2)
print
	
for node1 in T2:
	for node2 in T2[node1]:
		print str(node1) + '->' + str(node2)
print
'''
