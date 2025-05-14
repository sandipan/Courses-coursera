# Quiz 1

def LongestCommonSubsequenceProblem(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def backtrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ""
    elif  X[i-1] == Y[j-1]:
        return backtrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backtrack(C, X, Y, i, j-1)
        else:
            return backtrack(C, X, Y, i-1, j)

'''
s1, s2 = 'CTCGAT', 'TACGTC'
tbl = LongestCommonSubsequenceProblem(s1, s2)
print backtrack(tbl, s1, s2, len(s1), len(s2))
'''

import itertools

def numLinearPeptides(aminos, peptide):
	count = 0
	for i in range(peptide / aminos[0] + 1):
		for j in range(peptide / aminos[1] + 1):
			if i * aminos[0] + j * aminos[1] == peptide:
				print (i,j)
				all_peptides = set(itertools.permutations(['X']*i + ['Z']*j))
				#print all_peptides 
				print len(all_peptides)
				count += len(all_peptides)
	print count

#numLinearPeptides([2, 3], 24)
# 1 + 9!/(3!6!)	+ 10! / (6!4!) + 11! / (9!2!) + 1 = 1 + 7*8*9/6 + 7*8*9*10/24 + 10*11/2 + 1 = 351

#numLinearPeptides([2, 3], 22)
# 1 + 8! / (6!2!) + 9! / (5!4!) + 10! / (8!2!) = 1 + 7*8/2 +6*7*8*9/24 + 9*10/2
 
def read_file(filename):
	return [line.strip() for line in open(filename)]

def InDegreeArray(edges, n, m):
	degrees, nbrs, in_nbrs, W = [0]*(n + 1), {}, {}, {}
	for e in edges:
		u, v, w = map(int, str.split(e))
		degrees[v] += 1
		nbrs[u] = nbrs.get(u, []) + [v]
		in_nbrs[v] = in_nbrs.get(v, []) + [u]
		W[u, v] = w
		
	return	degrees, nbrs, in_nbrs, W

def topological_sort(indeg, nbrs, n, m):
	V = set([])
	for v in nbrs.keys():
		V.add(v)
		for u in nbrs[v]:
			V.add(u)
	#Input: A DAG G
	#Output: A list of the vertices of G in topological order
	S = [] #S = Stack()
	L = [] #List()
	for v in V: #O(|V|)
		if indeg[v] == 0:
			S += [v]
	while S: #O(|V| + |E|)
		v = S.pop()
		L.append(v)
		for w in nbrs.get(v, []):
			#delete e
			nbrs[v] = [x for x in nbrs[v] if x != w]
			indeg[w] -= 1
			if indeg[w] == 0:
				S += [w]
				
	acyclic = 1 if sum([len(nbrs[x]) for x in nbrs]) == 0 else -1 # If there are still edges left in the graph at the end of the algorithm, that means there must be a cycle.

	return acyclic, L	

from copy import deepcopy 	
def LongestPathDAG(edges, n, m):
	indeg, nbrs, in_nbrs, W = InDegreeArray(edges, n, m)
	acyclic, ordered_vertices = topological_sort(indeg, deepcopy(nbrs), n, m)
	print ordered_vertices
	D, P = {}, {}
	for v in ordered_vertices:
		D[v], P[v] = max([(D[u] + W[u, v], u) for u in in_nbrs.get(v, [])] + [(0, None)])
	d, v = max([(D[v], v) for v in ordered_vertices])
	print d, v
	path = ''
	while v:
		path = str(v) + '->' + path
		v = P[v]
	print path

'''	
lines = read_file('lpdag.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
LongestPathDAG(lines[1:], n, m)
'''

# Quiz 2

def ScoreAlignment(s1, s2, match, mismatch, indel):
	score = 0
	for i in range(len(s1)):
		if s1[i] == s2[i]:
			score += match
		elif s1[i] == '-' or s2[i] == '-':
			score += indel
		elif s1[i] != s2[i]:
			score += mismatch
	return score
	
#print ScoreAlignment('TCGAC--ATT', 'CC---GAA-T', match=1, mismatch=-1, indel=-2)
#print ScoreAlignment('ACAGTAGACAC', 'ATAC-AGATAC', match=1, mismatch=-3, indel=-1) 			# Local: 	TACTATTTACAGTAGACACGT AACAGAC-ATAC-AGATACCT
#print ScoreAlignment('AGTT-ACATACTAACG', 'AGTTCACAGGCTA-CG', match=1, mismatch=0, indel=-2)  	# Overlap: 	AGTACATCAGAGGAGTT-ACATACTAACG AGTTCACAGGCTA-CGTACAGATATTACGACAGGCAGA

def GlobalAlignment(s1, s2, match, mismatch, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = [[0 for _ in range(n)] for _ in range(m)], {}
	for i in range(m): tbl[i][0]=i*indel
	for j in range(n): tbl[0][j]=j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = match if s1[i-1] == s2[j-1] else mismatch
			tbl[i][j] = max(tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
	i, j = m - 1, n - 1
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if (s1[i-1] == s2[j-1] and tbl[i][j] == tbl[i-1][j-1] + match) or (s1[i-1] != s2[j-1] and tbl[i][j] == tbl[i-1][j-1] + mismatch): #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i][j] == tbl[i-1][j] + indel: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i][j] == tbl[i][j-1] + indel:  #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1		
	while i > 0:
		s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
	while j > 0:
		s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
		
	return tbl[m-1][n-1], s1_, s2_

#print GlobalAlignment('TCGACATT', 'CCGAAT', match=1, mismatch=-1, indel=-2)

def LocalAlignment(s1, s2, match, mismatch, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl = [[0 for _ in range(n)] for _ in range(m)]
	for i in range(m): tbl[i][0]=i*indel #0 #i*indel
	for j in range(n): tbl[0][j]=j*indel #0 #j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = match if s1[i-1] == s2[j-1] else mismatch
			tbl[i][j] = max(0, tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
	maxscore, imax, jmax = -1, -1, -1
	for i in range(m):
		for j in range(n):
			if tbl[i][j] > maxscore:
				maxscore, imax, jmax = tbl[i][j], i, j
	i, j = imax, jmax
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if tbl[i][j] == 0:
			break
		elif (s1[i-1] == s2[j-1] and tbl[i][j] == tbl[i-1][j-1] + match) or (s1[i-1] != s2[j-1] and tbl[i][j] == tbl[i-1][j-1] + mismatch): #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i][j] == tbl[i-1][j] + indel: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i][j] == tbl[i][j-1] + indel:
		#else: #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
		else:
			print 'Error'
		
	return maxscore, s1_, s2_
	
#print LocalAlignment('TACTATTTACAGTAGACACGT', 'AACAGACATACAGATACCT', match=1, mismatch=-3, indel=-1)

def FittingAlignment(s1, s2, match, mismatch, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = {}, {}
	for i in range(m): tbl[i,0]=0 #i*indel
	for j in range(n): tbl[0,j]=0 #j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = match if s1[i-1] == s2[j-1] else mismatch
			tbl[i,j] = max(tbl[i-1, j-1]+score, tbl[i, j-1]+indel, tbl[i-1, j]+indel)
			if tbl[i,j] == tbl[i-1, j-1] + score: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + indel: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + indel: 
				path[i,j] = 'U'
	maxscore, imax, jmax = max([(tbl[i,j], i, j) for i,j in tbl if j == n-1]) # align pattern with any position of text
	i, j = imax, jmax
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
	#while i > 0:
	#	s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
	#while j > 0:
	#	s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
		
	return maxscore, s1_, s2_
	
#print FittingAlignment('GTTGGATTACGAATCGATATCTGTTTG', 'ACGTCG', match=1, mismatch=-1, indel=-1)

def OverlapAlignment(s1, s2, match, mismatch, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl = [[0 for _ in range(n)] for _ in range(m)]
	#prev_row, cur_row, last_col = [0]*n, [0]*n, [0]*m
	#for i in range(m): tbl[i][0]=0 #i*indel
	for j in range(n): tbl[0][j]=j*indel #0
	for i in range(1, m):
		for j in range(1, n):
			score = match if s1[i-1] == s2[j-1] else mismatch
			tbl[i][j] = max(tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
			#tbl[i,j] = max(tbl[i-1, j-1]+score, tbl[i, j-1]+indel, tbl[i-1, j]+indel)
			#cur_row[j] = max(prev_row[j-1]+score, cur_row[j-1]+indel, prev_row[j]+indel)
		#last_col[i] = cur_row[n-1]	
		#prev_row = cur_row
		
	maxscore, imax, jmax = max([(tbl[m-1][j], m-1, j) for j in range(n)])
	i, j = imax, jmax
	
	s1_, s2_ = '', ''
	#print i, j, s1_, s2_
	while i > 0 and j > 0:
		if (tbl[i][j] == tbl[i-1][j-1] + match and s1[i-1]==s2[j-1]) or (tbl[i][j] == tbl[i-1][j-1] + mismatch): #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i][j] == tbl[i-1][j] + indel: 
		#elif tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i][j] == tbl[i][j-1] + indel:
		#else: #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
		else:
			print 'Error'
		
	return maxscore, s1_, s2_

def SemiglobalAlignment(s1, s2, match, mismatch, indel):
	
	m=len(s1)+1
	n=len(s2)+1

	#tbl, path = {}, {}
	tbl = [[0 for _ in range(n)] for _ in range(m)]
	#prev_row, cur_row, last_col = [0]*n, [0]*n, [0]*m
	#for i in range(m): tbl[i,0]=0 #i*indel
	#for j in range(n): tbl[0,j]=0 #j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = match if s1[i-1] == s2[j-1] else mismatch
			tbl[i][j] = max(tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
			#tbl[i,j] = max(tbl[i-1, j-1]+score, tbl[i, j-1]+indel, tbl[i-1, j]+indel)
			#cur_row[j] = max(prev_row[j-1]+score, cur_row[j-1]+indel, prev_row[j]+indel)
			'''
			if tbl[i,j] == tbl[i-1, j-1] + score: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + indel: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + indel: 
				path[i,j] = 'U'
			'''
		#last_col[i] = cur_row[n-1]	
		#prev_row = cur_row
		
	maxscore, imax, jmax = max([(tbl[i][n-1], i, n-1) for i in range(m)] + [(tbl[m-1][j], m-1, j) for j in range(n)])
	#maxscore, imax, jmax = max([(tbl[i,j], i, j) for (i,j) in tbl if i == m - 1 or j == n - 1])
	i, j = imax, jmax
	
	s1_, s2_ = '', ''
	if i == m - 1 and j < n - 1:
		s1_, s2_ = ''.join(['-']*(n-1-j)) + s1_, s2[j:] + s2_
	if j == n - 1 and i < m - 1:
		s1_, s2_ = s1[i:] + s1_, ''.join(['-']*(m-1-i)) + s2_
	
	#print i, j, s1_, s2_
	
	while i > 0 and j > 0:
		if (tbl[i][j] == tbl[i-1][j-1] + match and s1[i-1]==s2[j-1]) or (tbl[i][j] == tbl[i-1][j-1] + mismatch): #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i][j] == tbl[i-1][j] + indel: 
		#elif tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i][j] == tbl[i][j-1] + indel:
		#else: #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
		else:
			print 'Error'
	while i > 0:
		s1_, i, s2_ = s1[i-1] + s1_, i - 1, '-' + s2_
	while j > 0:
		s2_, j, s1_ = s2[j-1] + s2_, j - 1, '-' + s1_
		
	return maxscore, s1_, s2_

# Quiz 3
def ScoreAlignmentAffine(s1, s2, match, mismatch, gap_opening, gap_extension):
	score = 0
	for i in range(len(s1)):
		if s1[i] == s2[i]:
			score += match
		elif s1[i] == '-':
			if i >= 1 and s1[i-1] == '-':
				score += gap_extension
			else:
				score += gap_opening
		elif s2[i] == '-':
			if i >= 1 and s2[i-1] == '-':
				score += gap_extension
			else:
				score += gap_opening
		elif s1[i] != s2[i]:
			score += mismatch
	return score

#print ScoreAlignmentAffine('TCGAC--ATT', 'CC---GAA-T', match=1, mismatch=-1, gap_opening=-4, gap_extension=-1)

def backTrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ""
    elif X[i-1] == Y[j-1]:
        return backTrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)

def LongestCommonSubsequence(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    #return C
	return backTrack(C, X, Y, m, n)
	
#print LongestCommonSubsequence('CCAATACGAC', 'GCCTTACGCT')
#print LongestCommonSubsequence('CCCTAGCGGC', 'GCCTTACGCT')
#print LongestCommonSubsequence('CCAATACGAC', 'CCCTAGCGGC')

def NumberOfBreakPoints(perm):
	elements = map(int, perm.split())
	#print elements
	n = len(elements)
	elements = [0] + elements + [n+1]
	nbp = 0
	for i in range(len(elements) - 1):
		pair = elements[i:i+2]
		#print pair
		if not (pair[1] == pair[0] + 1):
			#print pair
			nbp += 1
	return nbp
	
#print NumberOfBreakPoints('+20 +8 +9 +10 +11 +12 +18 -7 -6 -14 +2 -17 -16 -15 +1 +4 +13 -5 +3 -19')

def changeSign(p):
	op = p
	for i in range(len(p)):
		op[i] = p[i] if p[i] == '0' else ('-' if p[i][0] == '+' else '+') + p[i][1:]
	return op
	
def getAllReversals(p):
	p = str.split(p)
	n = len(p)
	s = set([])
	for i in range(n):
		s.add(' '.join(p[:i] + changeSign([p[i]]) + p[i+1:]))
	for i in range(n):
		for j in range(i + 1, n):
			s.add(' '.join(p[:i] + changeSign(p[i:j+1][::-1]) + p[j+1:]))
	return s - set(p)

def GreedySortingByReversal1(p): 
	min_bp = NumberOfBreakPoints(p)
	print p
	queue, d, par = [p], {p: 0}, {p: None}
	while True: #NumberOfBreakPoints(p) > 0:
		p = queue.pop()
		par_bp = NumberOfBreakPoints(p)
		reversals = getAllReversals(p)
		bp_reversals = [(NumberOfBreakPoints(reversal), reversal) for reversal in reversals]
		min_breakpoints, min_p = min(bp_reversals)
		if min_breakpoints == 0:
			print p
			return d[p] + 1, p, par
		if min_breakpoints < min_bp:
			print min_breakpoints 
		min_bp = min(min_bp, min_breakpoints)
		if min_breakpoints > par_bp: #min_bp: #par_bp:
			continue
		for s in [reversal for (bp, reversal) in bp_reversals if bp == min_breakpoints]:
			if not s in d:
				queue += [s]
				d[s] = d[p] + 1
				par[s] = p

from heapq import *

def GreedySortingByReversal(p): 
	min_bp = NumberOfBreakPoints(p)
	print p
	queue = []
	heappush(queue, (NumberOfBreakPoints(p), p))	# min heap
	d = {p: 0}
	while True: #NumberOfBreakPoints(p) > 0:
		pr, p = heappop(queue)
		par_bp = NumberOfBreakPoints(p)
		reversals = getAllReversals(p)
		bp_reversals = [(NumberOfBreakPoints(reversal), reversal) for reversal in reversals]
		min_breakpoints, min_p = min(bp_reversals)
		if min_breakpoints == 0:
			return d[p] + 1
		if min_breakpoints < min_bp:
			print min_breakpoints 
		min_bp = min(min_bp, min_breakpoints)
		if min_breakpoints > par_bp: #min_bp: #par_bp:
			continue
		for s in [reversal for (bp, reversal) in bp_reversals if bp == min_breakpoints]:
			if not s in d:
				d[s] = d[p] + 1
				heappush(queue, (d[s] + min_breakpoints, s))

#for p in sorted(getAllReversals('0 +1 -2 +3 +4')):
#	print p
	
p = '0 +6 -12 -9 +17 +18 -4 +5 -3 +11 +19 +14 +10 +8 +15 -13 +20 +2 +7 -16 -1 +21'
p = '+6 -12 -9 +17 +18 -4 +5 -3 +11 +19 +14 +10 +8 +15 -13 +20 +2 +7 -16 -1'
p = '-16 -20 +11 +12 -14 -13 -15 -6 -8 -19 -18 -17 -10 +4 -5 -2 +7 -3 +1 -9'
#p = '-16 -20 +11 +12 -14 -13 -15 -6 -8 -19 -18 -17 -10 +4 -5 -2 +7 -3 +1 -9'
print NumberOfBreakPoints(p)
p = '+20 +7 +10 +9 +11 +13 +18 -8 -6 -14 +2 -4 -16 +15 +1 +17 +12 -5 +3 -19'
p = '0 +20 +7 +10 +9 +11 +13 +18 -8 -6 -14 +2 -4 -16 +15 +1 +17 +12 -5 +3 -19 +21'
print GreedySortingByReversal1(p)	
d, p, par = GreedySortingByReversal1(p)	
while p:
	print p
	p = par[p]
print d

def hamming(p1, p2):
	return sum([p1[i] != p2[i] for i in range(len(p1))])
	
#print bpdist('2 4 3 5 8 7 6 1', '1 2 3 4 5 6 7 8')
	
from heapq import *
	
def ReversalDistance(p1, p2): # A* search
	print 'convert', p1, '->', p2
	queue = []
	heappush(queue, (0, p1))	# min heap
	d = {p1:0}
	while len(queue) > 0:
		pr, p = heappop(queue)
		print p
		if p == p2:
			return d[p]
		children = getAllReversals(p)
		for child in children:
			if not child in d:
				d[child] = d[p] + 1
				heappush(queue, (d[child] + hamming(child.split(), p2.split()), child)) # A* search: heuristic: hamming distance: # points @ right position
				
#print ReversalDistance('+6 -12 -9 +17 +18 -4 +5 -3 +11 +19 +14 +10 +8 +15 -13 +20 +2 +7 -16 -1', '+1 +2 +3 +4 +5 +6 +7 +8 +9 +10 +11 +12 +13 +14 +15 +16 +17 +18 +19 +20')

		