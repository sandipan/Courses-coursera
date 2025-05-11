def week1():
	def extended_euclid(m, n):
		q, r = None, None
		s, t, s1, t1 = 1, 0, 0, 1
		while n > 0:
			q, r = m // n, m % n
			m, n = n, r
			s, t, s1, t1 = s1, t1, s - q*s1, t - q*t1
		return m, s, t

	def phi(n):
		count = 0
		for i in range(1,n):
			m, _, _ = extended_euclid(n, i)
			if m == 1:
				count += 1
		return count
		
	m, n = 19, 11
	g, s, t = extended_euclid(m, n)
	print(g, s, t, s*m + t*n)

	m, n = 32, 24
	print(extended_euclid(m, n))

	print(phi(11), phi(33), phi(12))
	print(extended_euclid(20, 7))

import numpy as np

def week2():

	def apply_quantum_op(U, s):
		return U @ s
		
	s = 1/np.sqrt(2)*np.array([1, 1])
	U = 1/np.sqrt(2)*np.array([[1,1],[1,-1]])
	print(s, U)
	print(apply_quantum_op(U, s))
	print(apply_quantum_op(U, apply_quantum_op(U, s)))

	def order(x, n):
		r = 1
		i = 1
		while True:
			r = (r * x) % n
			print(i, r)
			if r == 1: 
				return i
			i += 1
				
	#order(7, 15)
	r = order(7, 55)
	print(r)
	print((7**(r//2) + 1) % 55, (7**(r//2) - 1) % 55)

	#A = 1/np.sqrt(2)*np.array([[1j, -1j], [1, 1]])
	#Adag = A.conj().T
	#print(A)
	#print(Adag)
	#print(A@Adag)

#import cmath
	
def get_qft_unitary(n):
	w = np.exp(1j*2*np.pi/n)
	M = np.zeros((n,n), 'complex')
	for i in range(n):
		M[:, i] = [np.round((w**i)**j,2) for j in range(n)]
	M /= np.sqrt(n)
	return M
	
n = 4
U = get_qft_unitary(n)
#print(U.shape)
s00, s01, s10, s11 = np.array([1,0,0,0], 'complex'), np.array([0,1,0,0], 'complex'), np.array([0,0,1,0], 'complex'), np.array([0,0,0,1], 'complex')

print(np.round(U @ (s00 + s10) / np.sqrt(2), 2))
print(np.round((s00 + s10) / np.sqrt(2), 2))

print(np.round(U @ s11, 2))
print(np.round((s00 - 1j*s01 - s10 + 1j*s11) / 2, 2))

print(np.round(U @ s00, 2))
print(np.round(U @ s11, 2))

print(np.round(U @ s00, 2))
print(np.round((s00 + s01 + s10 + s11) / 2, 2))

print(np.round(U @ s10, 2))
print(np.round((s00 - s01 - s10 + s11) / 2, 2))

print(U)
print(U@U.T)


'''
def get_suffix_link_for_dest_node(edge):
    p = edge.src
    n = edge.dest
    assert p.suffix_link != None, f"parent {p.id} has no suffix link but asking for the suffix link of a child"
    assert not edge.is_leaf_edge()
    orig_str = edge.orig_str
    lo = edge.lo
    hi = edge.hi
    assert 0 <= lo <= hi and hi < len(orig_str)
    ## TODO: implement the algorithm to find the suffix link of n 
    ##       given that of p and the data for the edge from p -> n
    print('here0', p.suffix_link.id, p.id, n.id, lo, hi)
    # your code here    
    if hi == -1:
        hi = len(p.orig_str)
    if lo+1 > hi:
        print('here1')
        return p.suffix_link
    else:
        s = 1 if p.suffix_link == p else 0
        snode, suffix, cur = p.suffix_link, p.orig_str[lo+s:hi+1], ''
        while cur != suffix:
            print('suffix', suffix, 'cur', cur)
            for (_, e) in snode.outgoing_edges.items():
                if e.hi == -1:
                    e.hi = len(e.orig_str)
                cur_str = e.orig_str[e.lo:e.hi+1]
                print(e.src.id, e.dest.id, e.lo, e.hi, lo+s, hi, cur_str)
                if cur_str == suffix:
                    print('here', e.dest.id, cur_str)
                    return e.dest
                elif suffix.startswith(cur_str):
                    snode = e.dest
                    lo += e.lo
                    cur += cur_str
                    if cur == suffix:
                        return e.dest
                    break
    #raise NotImplementedError
'''

def dfs_iterative(snode, suffix):
    visited = set()
    traversal = []
    stack = [(snode, '')]
    while len(stack) > 0:
        node, str = stack.pop()
        if node not in visited:
            visited.add(node)
            traversal.append(str)
            if type(node) is not SuffixTrieLeaf:
                for (_, e) in node.outgoing_edges.items():
                    stack.append((e.dest, e.get_sub_str(-1)))   # add vertex in the same order as visited
    return traversal
	
print(dfs_iterative(root, suffix=''))	