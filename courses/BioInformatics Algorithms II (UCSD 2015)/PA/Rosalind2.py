from collections import defaultdict

def find_all_parents(G, s):
	Q = [s]
	parents = defaultdict(set)
	while len(Q) != 0:
		v = Q[0]
		Q.pop(0)
		for w in G.get(v, []):
			parents[w].add(v)
			Q.append(w) 
	return parents
	
def find_all_paths(parents, a, b):
	return [a] if a == b else [y + b for x in list(parents[b]) for y in find_all_paths(parents, a, x)]

#def create_spectrum_graph():
	
'''	
#G = {'A':['B','C'], 'B':['D'], 'C':['D', 'F'], 'D':['E', 'F'], 'E':['F']}
G = {'A':['B','C'], 'B':['C'], 'C':['D', 'E', 'F'], 'D':['E'], 'E':['I'], 'F':['G', 'H']}
s = 'A'
par = find_all_parents(G, s)
src, sinks = None, []
src = list(G.keys() - par.keys())
sinks = list(par.keys() - G.keys())
		
print(par)
print(src, sinks)
start = 'A'
end = 'E' #'F'
paths = find_all_paths(par, start, end)
for p in paths:
	print(p)

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

g = nx.DiGraph(directed=True) #nx.Graph()
for n in set(list(G.keys()) + list(par.keys())):
	if n == start or n == end:
		g.add_node(n, style='filled', fillcolor='#ffbbaa')
	else:
		g.add_node(n, style='filled', fillcolor='#ffffff')
for u in G:
	for v in G[u]:
		g.add_edge(u, v)
#G.add_node(1,color='red',style='filled',fillcolor='blue',shape='square')
#G.add_node(2,color='blue',style='filled')
#G.add_edge(1,2,color='green')
#G.nodes[2]['shape']='circle'
#G.nodes[2]['fillcolor']='red'
j = 0
for p in paths:
	g1 = g.copy()
	for i in range(len(p)-1):
		g1.add_edge(p[i], p[i+1], color='red')
	A = to_agraph(g1)
	A.layout()
	A.draw('color_{}.png'.format(j))
	#print(A.to_string())
	j += 1
'''

from time import time

def read_file(filename):
	return [line.strip().replace('10', '0').replace(' ', '') for line in open(filename)]

def rev(str, i, j):
	return str[:i] + str[i:j+1][::-1] + str[j+1:]
	
def dif(s1, s2):
	return sum([s1[i] != s2[i] for i in range(len(s1))])
	
#strs = read_file('test.txt')
strs = read_file('rosalind_rear.txt')
#print(rev('1234567890',0,9))

def bfs(s, t):
	if s == t:
		return 0
	Q = [s]
	d = {s:0}
	m = dif(s, t)
	while len(Q) != 0:
		v = Q[0]
		Q.pop(0)
		m = dif(v, t)
		#print(v, len(Q))
		for i in range(len(v)):
			for j in range(i+1, len(v)):
				r = rev(v, i, j)
				if (not r in d) and (dif(r, t) <= m):
					d[r] = d[v] + 1
					Q.append(r) 
				if r == t:
					return d[r]
	#print(len(d))

'''
strs = [str for str in strs if str != '']
#print(strs)
	
start = time()
i = 0
while i < len(strs):
	s, t = strs[i] , strs[i+1]
	#print(s, t)
	#print(dif(s, t))
	print(bfs(s, t))
	i += 2
print(time() - start)
'''

inp = '(+3 +4 +5 -12 -8 -7 -6 +1 +2 +10 +9 -11 +13 +14)'
p = inp[1:-1].split(' ')
p = ['0'] + p + ['+' + str(len(p)+1)]
#print(p)
count = 0
for i in range(len(p)-1):
	if int(p[i+1]) - int(p[i]) != 1:
		count += 1
print(count)