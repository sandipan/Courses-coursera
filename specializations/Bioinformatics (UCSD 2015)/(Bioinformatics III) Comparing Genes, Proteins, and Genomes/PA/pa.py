def read_file(filename):
	return [line.strip() for line in open(filename)]

def GlobalAlignment1(s1, s2, matchmat, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = [[0 for _ in range(n)] for _ in range(m)], {}
	for i in range(m): tbl[i][0]=i*indel
	for j in range(n): tbl[0][j]=j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = matchmat[s1[i-1], s2[j-1]]
			tbl[i][j] = max(tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
	i, j = m - 1, n - 1
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if tbl[i][j] == tbl[i-1][j] + indel: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i][j] == tbl[i][j-1] + indel:  #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
		elif tbl[i][j] == tbl[i-1][j-1] + matchmat[s1[i-1], s2[j-1]]: #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
	while i > 0:
		s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
	while j > 0:
		s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
	
	#for i in range(m):	print tbl[i]
	
	return tbl[m-1][n-1], s1_, s2_

from copy import deepcopy
def GlobalAlignment(s1, s2, matchmat, indel, k):
	n=len(s1)+1
	m=k+1
	cur_col, prev_col = [0] * n, [0] * n
	for i in range(n): prev_col[i] = i * indel
	cur_col = prev_col
	#print cur_col
	for j in range(1, m):
		prev_col = deepcopy(cur_col)
		cur_col[0] = j * indel
		for i in range(1, n):
			score = matchmat[s1[i-1], s2[j-1]]
			cur_col[i] = max(prev_col[i-1]+score, cur_col[i-1]+indel, prev_col[i]+indel)
		#print cur_col #, prev_col
	return cur_col

def MiddleEdgeinLinearSpaceProblem(s1, s2, matchmat, indel):
	n = len(s1)
	m = len(s2)
	middle = m / 2
	#print middle
	mid_col1 = GlobalAlignment(s1, s2, matchmat, indel, middle)
	mid_col2 = GlobalAlignment(s1[::-1], s2[::-1], matchmat, indel, m - middle - 1)
	max, node1, node2, nextnode1, nextnode2 = float('-inf'), -1, -1, -1, -1
	for i in range(n + 1):
		if mid_col1[i] + mid_col2[n - i] + indel > max:
			max, node1, node2, nextnode1, nextnode2 = mid_col1[i] + mid_col2[n - i] + indel, i, i, middle, middle + 1
		if i > 0 and i < n and mid_col1[i] + mid_col2[n - i - 1] + matchmat[s1[i], s2[middle]] > max:
			max, node1, node2, nextnode1, nextnode2 = mid_col1[i] + mid_col2[n - i - 1] + matchmat[s1[i], s2[middle]], i, i + 1, middle, middle + 1
		if mid_col1[i] + mid_col1[i - 1] + indel > max:
			max, node1, node2, nextnode1, nextnode2 = mid_col1[i] + mid_col1[i - 1] + indel, i, i, middle, middle
		#print (node1, middle), (node2, middle+1), max
			
	return ((node1, nextnode1), (node2, nextnode2)) #, mid_col1[imax] + mid_col2[n - imax]
	#print mid_col1
	#print mid_col2

lines = read_file('BLOSUM62.txt')
aminos = str.split(lines[0])
lines = lines[1:]
n = len(aminos)
matchmat = {}
for i in range(n):
	cells = str.split(lines[i])
	camino = cells[0]
	scores = map(int, cells[1:])
	for j in range(n):
		matchmat[camino, aminos[j]] = scores[j]
#print matchmat
lines = read_file('inp.txt')	
#lines = read_file('linear_space.txt')	
#GlobalAlignment(lines[0], lines[1], matchmat, -5, len(lines[1]))
#print GlobalAlignment1(lines[0], lines[1], matchmat, -5)
#print MiddleEdgeinLinearSpaceProblem(lines[0], lines[1], matchmat, -5)

s1_, s2_ = '', ''

def LinearSpaceAlignment(s1, s2, matchmat, indel, top, bottom, left, right):
	global s1_, s2_
	if left == right:
		s1_, s2_ = s1_ + s1[top:bottom], s2_ + ''.join(['-']*(bottom - top))
		return
	if top == bottom:
		s1_, s2_ = s1_ +''.join(['-']*(right - left)), s2_ + s2[left:right]
		return
	middle = (left + right) / 2
	edge = MiddleEdgeinLinearSpaceProblem(s1[top:bottom], s2[left:right], matchmat, indel)
	#print s1[top:bottom], s2[left:right]
	midNode = top + edge[0][0] #MiddleNode(top, bottom, left, right)
	if edge[0][0] == edge[1][0]:
		midEdge = 'R'  
	elif edge[0][0] + 1 == edge[1][0]: #MiddleEdge(top, bottom, left, right)
		midEdge = 'S' if edge[0][1] == edge[1][1] else 'D'
	#print midNode, midEdge
	#print s1[top:bottom], s2[left:right], top, bottom, left, right, middle, left + edge[0][1]
	LinearSpaceAlignment(s1, s2, matchmat, indel, top, midNode, left, middle)
	#print midEdge
	if midEdge == 'D':
		s1_, s2_ = s1_ + s1[midNode], s2_ + s2[middle]
	else:
		s1_, s2_ = s1_ + '-', s2_ + s2[middle]
	
	if midEdge == "R" or midEdge == "D":
		middle = middle + 1
	if midEdge == "S" or midEdge == "D":
		midNode = midNode + 1 
	LinearSpaceAlignment(s1, s2, matchmat, indel, midNode, bottom, middle, right)

#lines = read_file('inp.txt')	
#lines = read_file('linear_space2.txt')	
lines = read_file('dataset_250_14.txt')	
#print GlobalAlignment(lines[0], lines[1], matchmat, -5, len(lines[1]))[-1]
#LinearSpaceAlignment(lines[0], lines[1], matchmat, -5, 0, len(lines[0]), 0, len(lines[1]))
#print s1_
#print s2_
#out = GlobalAlignment1(lines[0], lines[1], matchmat, indel=-5)
#for i in range(len(out)):
#	print out[i]

