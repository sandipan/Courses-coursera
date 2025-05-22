def read_file(filename):
	return [line.strip() for line in open(filename)]

def BioinformaticsArmory(string):
	count = {'A':0, 'C':0, 'G':0, 'T':0}
	for ch in string:
		count[ch] += 1
	string = ''
	for ch in sorted(count.keys()):
		string += str(count[ch]) + ' '
	print string

'''	
#string = 'AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC'
string = 'ATCGCGCGCCGTATAGTGCAATTGCCGAACATTAATCGCTGAAGCCATTCAAAGCCGGAGAGGTGAGGGTGCTAACTTTTGAGATAGTAGCACTGGACGATCCTACTCCCGCAGTACGTTAGCTCGTTTAGGTGGGGATTTCGGTACACAATTTAAGTTCAGCGTGGTGCTTCTGTGCGTCACCTCTAACCAGCTCTGATCAGAATGCGTGGACGATTCGTATGAGTTGTCAAAGTGAAAATTTGCCTGGTAGTTAAAACACTTAACACACTGGTATCGAATGCGATTTAGGCCGGCTCAGCGGAGGATATGTCTAGCCCCTCCCGGTGACTTCATTAGTGGACAATCTCGTAGCTATCCGACGGTTCGCCCATGACCAACCGCAAATACTTTACTACGCTTCCCTAGCTTTGTGGCAATTGCTGCTCACTTTAGACCTGTAGCACCGACTAATCTAGGCGACGCTTAACTAATCGGCTGGTGACAGTAAAATTCACCGAGGCACTACTCCCCGCGAGGATACTACGGGTCAAGTTGGTCTCCTTGCTGAGCAACTCCATAGTAGTTCATTTACGTCTGATTGATTACAAAAAGATACAAGACATGCTGCGCCTATCCCCCGCATAACTCCCTGTCGCGCCCTCTTACAAGTGTGTTCGTGTTCTTCCGTGCAGAAAATAGTAGGGCTTAGATTTCATTCGTGGCCAAACAGGGACCGTCTGTATAGGGGTCCACATGAGCGATAAGTCAAAATAGGTAACCAAAAACATTTTCCCCGAGGTAGCGGTGGACGTTGCCTTTAGTCCCCCAGCTAGCTTACCTGACTAATGATGGCGCGTATTGGGGGAACTTAGAGAATCGTTTCTCCGTAAAACTCACAGCCTTGCATTTGCTTAAACCATTGAACTACGTTACGTCGTGCAGCCACCATCTGCGATTACTTTT'
BioinformaticsArmory(string)	
'''

import urllib2, re  # the lib that handles the url stuff

def ProteinDatabases(protein):
	process = re.compile('.*GO;\s+GO:[0-9]+;\s+P:([^;]+);.*') #GO;\s+GO:[0-9]+;\s+P:[^;]+;')
	target_url = 'http://www.uniprot.org/uniprot/' + protein + '.txt'
	#print target_url
	data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
	for line in data: # files are iterable
		#print line
		if process.match(line):
			print process.match(line).group(1)

'''
protein = 'Q01549' #'B5ZC00' 'Q5SLP9'
ProteinDatabases(protein)
'''

def get_seq_fasta(lines):
	sequences, sequence, ids, id = [], '', {}, lines[0].split()[0][1:]
	ids[id] = 0
	for line in lines[1:]:
		if line[0] == '>':
			sequences.append(sequence)
			sequence, id = '',  line.split()[0][1:]
			ids[id] = len(sequences)
		else:
			sequence += line
	sequences.append(sequence)
	return sequences, ids

import os.path

def ReverseComplementProblem(Text):
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
	return ''.join([complement[x] for x in Text])[::-1] 

import re
def GetNbrEdges(edges, splt=None, dir = False, indeg=True, outdeg=True):
	
	W = {}
	#degrees = [0]*(n + 1)
	degrees = {}
	nbrs = {}
	vertices = set([])
	for e in edges:
		u, v, w =  map(int, re.split(splt, e)) if splt != None else map(int, str.split(e))
		vertices.update([u, v])
		nbrs[u] = nbrs.get(u, []) + [v]
		W[u, v] = w
		if indeg:
			degrees[v] = degrees.get(v, 0) + 1
		if outdeg:
			degrees[u] = degrees.get(u, 0) + 1
		if not dir:
			nbrs[v] = nbrs.get(v, []) + [u]
			W[v, u] = w			
	
	vertices = list(vertices)
	return vertices, degrees, nbrs, W	

def StringComposition(Text, k):
	return sorted([Text[i:i+k] for i in range(len(Text)-k+1)])

'''
lines = read_file('inpros60.txt')
lines = read_file('rosalind_3aba.txt')
k, Text = int(lines[0]), lines[1]
for kmer in StringComposition(Text, k):
	print kmer	
'''

def Fib(n):
	if n <= 1:
		return n
	else:
		f1, f2 = 0, 1
		for i in range(2, n + 1):
			f1, f2 = f2, f1 + f2
	return f2

#n = 21 #6
#print Fib(n)

def bsearch(a, l, r, k):
	if (l <= r):
		m = (l + r) / 2
		if a[m] == k:
			return m + 1
		elif a[m] < k:
			return bsearch(a, m + 1, r, k)
		elif a[m] > k:
			return bsearch(a, l, m - 1, k)
		else:
			return -1
	return -1

'''	
lines = read_file('inpros2.txt')	
lines = read_file('rosalind_bins.txt')	
n, m = int(lines[0]), int(lines[1])
a = map(int, str.split(lines[2]))
ks = map(int, str.split(lines[3]))
#print ks
print [bsearch(a, 0, n - 1, k) for k in ks]
'''

def MajorityElement(a):
	elem, freq, n = -1, 1, len(a)
	for i in range(n):
		if elem == a[i]:
			freq += 1
		else:
			freq -= 1
			if freq == 0: elem, freq = a[i], 1
	if (len([1 for i in range(n) if a[i] == elem]) > n / 2.0):
		return elem
	return -1

'''
lines = read_file('inpros3.txt')	
lines = read_file('rosalind_maj.txt')	
k, n = map(int, str.split(lines[0]))
print [MajorityElement(map(int, str.split(lines[i]))) for i in range(1, 1 + k)] 
'''

def heapify(a, i, n):
	leftchildindex, rightchildindex = 2 * i, 2 * i + 1
	childindex = leftchildindex
	if rightchildindex <= n:
		childindex = max((a[leftchildindex], leftchildindex), (a[rightchildindex], rightchildindex))[1]
	if childindex <= n and a[childindex] > a[i]:
		a[i], a[childindex] = a[childindex], a[i]
		heapify(a, childindex, n)
	
def BuildHeap(a, n):
	i = n / 2
	while i >= 1:
		heapify(a, i, n)
		i -= 1
	#print a

'''
lines = read_file('inpros22.txt')	
lines = read_file('rosalind_hea.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
a = [-1] + a
#print n
#print a
BuildHeap(a, n)[1:]	
'''

def HeapSort(a, n):
	BuildHeap(a, n)
	while n > 0:
		a[1], a[n] = a[n], a[1]
		n -= 1
		heapify(a, 1, n)

'''
lines = read_file('inpros30.txt')	
lines = read_file('rosalind_hs.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
a = [-1] + a
#print n
#print a
HeapSort(a, n)
print a[1:]
'''

def PartialSort(a, n, k):
	a = [-1] + map(lambda(x): x * (-1), a)	# use max heap as min heap
	elems = []
	BuildHeap(a, n)	
	i = k
	while i > 0:
		a[1], a[n] = a[n], a[1]
		elems += [a[n]]
		n -= 1
		heapify(a, 1, n)
		i -= 1
	print map(lambda(x): x * (-1), elems)

'''
lines = read_file('inpros28.txt')	
lines = read_file('rosalind_ps.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
k = int(lines[2])
#print n
#print a
PartialSort(a, n, k)
'''
	
def InsertionSort(a, n):
	swap = 0
	for i in range(1, n):
		k = i
		while k > 0 and a[k] < a[k - 1]:
			a[k], a[k - 1] = a[k - 1], a[k]
			swap += 1
			k -= 1
		#print i, a, swap
	return swap		

'''
lines = read_file('inpros4.txt')	
lines = read_file('rosalind_ins.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print n
#print a
print InsertionSort(a, n)
'''

def MergeTwoSortedArrays(a, n, b, m):
	c, i, j, k = [0] * (n + m), 0, 0, 0
	while i < n and j < m:
		if a[i] < b[j]:
			c[k] = a[i]
			i += 1
		else:
			c[k] = b[j]
			j += 1
		k += 1
	while i < n:
		c[k] = a[i]
		k, i = k + 1, i + 1
	while j < m:
		c[k] = b[j]
		k, j = k + 1, j + 1
		
	return c

'''
lines = read_file('inpros5.txt')	
lines = read_file('rosalind_mer.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
m = int(lines[2])
b = map(int, str.split(lines[3]))
print MergeTwoSortedArrays(a, n, b, m)
'''

def merge_sort1(a, i, j):

	if i < j:
		m = (i + j) / 2
		a[i : m + 1] = merge_sort1(a, i, m)
		a[m + 1 : j + 1] = merge_sort1(a, m + 1, j)
		a[i : j + 1] = MergeTwoSortedArrays(a[i : m + 1], m + 1 - i, a[m + 1 : j + 1], j - m)
	else:
		return [a[i]]
		
def merge_sort2(a):
    if len(a) < 2:
        return a
    m = len(a) / 2
    return MergeTwoSortedArrays(merge_sort2(a[:m]), m, merge_sort2(a[m:]), len(a) - m)

def mergeSort(alist):
    #print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i]<righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i<len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    #print("Merging ",alist)

'''
lines = read_file('inpros6.txt')	
lines = read_file('rosalind_ms.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#mergeSort(a)
#print a
print merge_sort2(a)
'''

def CountingInversions1(a, n):
	inversions = 0
	for i in range(n):
		for j in range(i + 1, n):
			inversions += a[i] > a[j]
	return inversions

def CountingInversions2(a, n):
	return InsertionSort(a, n)

def CountMerge(alist, lefthalf, righthalf):
	i, j, k, inv = 0, 0, 0, 0
	while i<len(lefthalf) and j<len(righthalf):
		if lefthalf[i]<=righthalf[j]:
			alist[k]=lefthalf[i]
			i=i+1
		else:
			alist[k]=righthalf[j]
			j=j+1
			inv += len(lefthalf) - i
		k=k+1
	while i<len(lefthalf):
		alist[k]=lefthalf[i]
		i += 1
		k += 1

	while j<len(righthalf):
		alist[k]=righthalf[j]
		j += 1
		k += 1
	return inv

def CountingInversions(alist):
    if len(alist) > 1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        return CountingInversions(lefthalf) + CountingInversions(righthalf) + CountMerge(alist, lefthalf, righthalf)
    else:
        return 0

#from random import randint
#a = [randint(1, 1000) for _ in range(100)]		
#print CountingInversions1(a, len(a))
#print CountingInversions(a)
'''
lines = read_file('inpros14.txt')	
lines = read_file('rosalind_inv.txt')	
#lines = [5, '2 1 35 4 5']
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print n
#print a
print CountingInversions(a)	
#print CountingInversions3(a)	
'''

def TwoWayPartition1(a, n):
	pivot, i, j = a[0], 0, n - 1
	while True:
		while a[i] <= pivot and i < n:
			i += 1
		while a[j] > pivot and j >= 0:
			j -= 1
		if i >= j:
			break
		else:
			a[i], a[j] = a[j], a[i]
	if j > 0:
		a[j], a[0] = pivot, a[j]
	return a

def TwoWayPartition(myList, start, end):
    pivot = myList[start]
    left = start+1
    right = end
    done = False
    while not done:
        while left <= right and myList[left] <= pivot:
            left = left + 1
        while myList[right] >= pivot and right >=left:
            right = right -1
        if right < left:
            done= True
        else:
            # swap places
            temp=myList[left]
            myList[left]=myList[right]
            myList[right]=temp
    # swap start with myList[right]
    temp=myList[start]
    myList[start]=myList[right]
    myList[right]=temp
    return myList

def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)

def quickSortHelper(alist,first,last):
   if first<last:

       splitpoint = partition(alist,first,last)

       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)

def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and \
               alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and \
               rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp

   #print alist

   return rightmark #alist #rightmark

#alist = [54,26,93,17,77,31,44,55,20]
#partition(alist, 0, len(alist) - 1)
#quickSort(alist)
#print(alist)

'''	
lines = read_file('inpros7.txt')	
lines = read_file('rosalind_par.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print TwoWayPartition(a, 0, n - 1)
partition(a, 0, n - 1)
'''

'''
lines = read_file('inpros30.txt')	
lines = read_file('rosalind_qs.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print TwoWayPartition(a, 0, n - 1)
quickSort(a)
print a
'''

def ThreePartition(a, n):
	lo, hi = 0, n - 1
	lt, gt = lo, hi
	v = a[lo]
	i = lo
	while i <= gt:
		if a[i] < v:
			a[i], a[lt] = a[lt], a[i]
			lt += 1
			i += 1
		elif a[i] > v:
			a[i], a[gt] = a[gt], a[i]
			gt -= 1
		else:
			i += 1
	
	print a

'''	
lines = read_file('inpros19.txt')	
lines = read_file('rosalind_par3.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print a
ThreePartition(a, n)
'''

from random import randrange

def Partition(arr,start,end,pivot_idx):
    '''
    Partitions array in-place around the given pivot value
    '''
    pivot = arr[pivot_idx]
    arr[end],arr[pivot_idx] = arr[pivot_idx],arr[end]
    inc_idx = start
    for i in xrange(start,end):
        if arr[i] <= pivot:
            arr[inc_idx],arr[i] = arr[i],arr[inc_idx]
            inc_idx+=1
    arr[end],arr[inc_idx] = arr[inc_idx],arr[end]
    return inc_idx

def KthSmallest(arr, k, start=0, end=None):
    '''
    Find kth minimum element in a array (in-place randomized algorithm, similar to quicksort)
    assumption: Input will only contain unique elements'''
    if k > len(arr):
        raise Exception("k should be less than length of the input array")
    if not end: end = len(arr) -1 #Get last index value
    pivot_ridx = randrange(start, end)     #Get a random array element as pivot value
    pivot = arr[pivot_ridx]
    pivot_idx = Partition(arr,start,end,pivot_ridx) #partition to partition array around the pivot value in place
    if pivot_idx+1 == k:
        return pivot #Well, there is your answer
    elif pivot_idx+1 > k:
        return KthSmallest(arr,k,start,pivot_idx) #lies somewhere in the first partition
    else:
        return KthSmallest(arr,k,pivot_idx,end) #lies somewhere in the second Partiton

#if __name__ == '__main__':
#    from random import shuffle
#    test_input = range(100000)
#    shuffle(test_input)
#    assert KthSmallest(test_input,50000) == 49999
	
'''
lines = read_file('inpros29.txt')	
lines = read_file('rosalind_med.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
k = int(lines[2])
#print a
print KthSmallest(a, k)
'''

def LongestIncDecSubsequence(a, n):
	
	I, D = [0] * n, [0] * n
	I[0] = D[0] = (1, -1)
	for i in range(1, n):
		I[i] = max([(I[j][0] + 1, j) for j in range(i) if (a[i] > a[j])] + [(1, -1)])
		D[i] = max([(D[j][0] + 1, j) for j in range(i) if (a[i] < a[j])] + [(1, -1)])
	#print I
	#print D
	indinc, inddec = max([(I[i], i) for i in range(n)])[1], max([(D[i], i) for i in range(n)])[1]	
	inc = []
	i = indinc
	while i >= 0:
		inc = [a[i]] + inc
		i = I[i][1]
	dec = []
	i = inddec
	while i >= 0:
		dec = [a[i]] + dec
		i = D[i][1]
	print inc
	print dec

'''	
lines = read_file('inpros20.txt')	
lines = read_file('rosalind_lgis.txt')	
n = int(lines[0])
a = map(int, str.split(lines[1]))
#print a
LongestIncDecSubsequence(a, n)
'''	

def TheChangeProblem(money, coins):
	N = {coin: 1 for coin in coins}
	N[0] = 0
	for m in range(1, money + 1):
		N[m] = min([N[m - coin] + 1 for coin in coins if m >= coin])
	print N[money]	

'''
lines = read_file('inpros41.txt')
lines = read_file('rosalind_5a.txt')
money = int(lines[0])
coins = map(int, lines[1].split(','))
#coins = map(int, str.split(lines[1]))
TheChangeProblem(money, coins)
'''

def backtrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ""
    elif  X[i-1] == Y[j-1]:
        return backtrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i,j-1] > C[i-1,j]:
            return backtrack(C, X, Y, i, j-1)
        else:
            return backtrack(C, X, Y, i-1, j)

def LongestCommonSubsequenceProblem1(s1, s2):
	m=len(s1)
	n=len(s2)

	tbl, path = {}, {}
	for i in range(m+1): tbl[i,0]=0
	for j in range(n+1): tbl[0,j]=0
	for i in range(1, m+1):
		for j in range(1, n+1):
			tbl[i,j] = tbl[i-1, j-1] + 1 if s1[i-1] == s2[j-1] else max(tbl[i, j-1], tbl[i-1, j])
			if tbl[i,j] == tbl[i-1, j-1] + 1: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1]: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j]: 
				path[i,j] = 'U'
	s, t, i, j = '', '', m, n
	while i > 0 and j > 0:
		if path[i, j] == 'D':
			s = s1[i-1] + s
			t = s2[j-1] + t
			i, j = i - 1, j - 1
		elif path[i, j] == 'U':
			i = i - 1
		elif path[i, j] == 'L':
			j = j - 1
	
	print tbl[m-1,n-1]
		
	return tbl, s, t
	
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
'''			
import sys
sys.setrecursionlimit(1500)
lines = read_file('inpros43.txt')	
lines = read_file('rosalind_5c.txt')
s1, s2 = lines[0], lines[1]
#print s1
#print s2
tbl, s, t = LongestCommonSubsequenceProblem1(s1, s2)
#print s
#print t
print backtrack(tbl, s1, s2, len(s1), len(s2))
tbl = LongestCommonSubsequenceProblem(s1, s2)
print backTrack(tbl, s1, s2, len(s1), len(s2))
'''
	
def LongestPathManhattanTouristProblem(n, m, D, R):
	P = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
	for i in range(1, n + 1):
		P[i][0] = sum([D[j][0] for j in range(i)])
	for j in range(1, m + 1):
		P[0][j] = sum([R[0][i] for i in range(j)])
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			P[i][j] = max(P[i - 1][j] + D[i - 1][j], P[i][j - 1] + R[i][j - 1])
	print P[n][m]
	#print P

'''	
lines = read_file('inpros42.txt')
lines = read_file('inpros99.txt')
lines = read_file('rosalind_ba5b.txt')
n, m = map(int, str.split(lines[0]))
D = [[0 for _ in range(m + 1)] for _ in range(n)]
lines = lines[1:]
for i in range(n):
	D[i] = map(int, str.split(lines[i]))
R = [[0 for _ in range(m)] for _ in range(n + 1)]
lines = lines[n+1:]
for i in range(n + 1):
	R[i] = map(int, str.split(lines[i]))		
#print n, m
#print D
#print R
LongestPathManhattanTouristProblem(n, m, D, R)
'''
	
def getPairDiffs(x):
	d, n = [], len(x)
	for i in range(n):
		for j in range(i+1, n):
			d += [abs(x[i]-x[j])]
	return sorted(d)
			
def valid(d, xs, newx):
	d2 = [abs(x - newx) for x in xs]
	d1 = d
	#print 'x', newx
	#print 'd2', d2
	#print 'd1', d1
	for y in d2:
		if y in d1:
			iy = d1.index(y)
			#print 'hh', iy	
			d1 = d1[:iy] + d1[iy+1:]
		else:
			return False, d
	return True, d1

def TurnPike(d, x, sols):
	newx = d[-1]
	isvalid, d1 = valid(d, x, newx)
	#print 'h1', isvalid, newx, d1
	#print 'h1', newx
	if (isvalid):
		if len(d1) == 0:
			sols.add(' '.join(map(str, sorted(x + [newx]))))
		else: 
			TurnPike(d1, x + [newx], sols)
	newx = max(x) - d[-1]
	isvalid, d1 = valid(d, x, newx)
	#print 'h2', isvalid, newx, d1
	if (isvalid):
		if len(d1) == 0:
			sols.add(' '.join(map(str, sorted(x + [newx]))))
		else: 
			TurnPike(d1, x + [newx], sols)

'''			
#lines = read_file('inpros31.txt')	
#lines = read_file('extra_dataset_turnpike.txt')	
#lines = read_file('rosalind_2i.txt')	
lines = read_file('rosalind_4iba.txt')	
d = map(int, str.split(lines[0]))
n = sum([1 for i in range(len(d)) if d[i] == 0])
#print n
d = d[n*(n+1)/2:]
#print d
sols = set([])
TurnPike(d[:-1], [0, d[-1]], sols)
for sol in sols:
	print sol
#print d == getPairDiffs([0, 4, 13, 23, 33, 41, 46, 54, 66, 78, 81, 89, 96, 114, 133, 151, 164, 169, 184, 197, 212, 224, 227, 244, 255, 271, 288, 292, 293, 311, 317, 336, 349, 353, 360, 373, 384, 396, 399, 417, 419, 435, 438, 448, 467, 471, 487, 502, 504, 508, 527, 536, 550, 560, 579, 596, 599, 615, 621, 637, 644, 655, 657, 672, 683, 684, 702, 717, 728, 742, 754, 769, 784, 785, 789, 805, 823, 825, 826, 835, 845, 855, 873, 879, 881, 884, 898, 904, 920, 934, 950, 964, 978, 991, 999, 1016, 1035, 1041, 1055, 1070, 1081, 1090, 1109, 1112, 1113, 1130, 1138, 1150, 1152, 1153, 1161, 1174, 1179, 1197, 1204, 1223, 1235, 1250, 1260, 1270, 1285, 1289, 1299, 1306, 1324, 1326, 1329, 1331, 1348, 1362, 1381, 1386, 1402, 1405, 1423])
#print d == getPairDiffs([0, 14, 28, 40, 56, 61, 77, 94, 111, 119, 138, 153, 166, 178, 185, 188, 203, 209, 222, 228, 232, 247, 251, 256, 270, 275, 277, 281, 287, 289, 304, 310, 328, 344, 356, 367, 382, 400, 414, 432, 442, 446, 455, 471, 486, 498, 506, 512, 514, 531, 536, 554, 561, 577, 596, 613, 622, 630, 641, 647, 659, 662, 664, 671, 679, 681, 682, 688, 697, 715, 730, 746, 760, 769, 784, 802, 812, 830, 849, 854, 858, 863, 868, 878, 887, 897, 911, 912, 926, 932, 949, 965, 976, 986, 996, 1015, 1034, 1038, 1055, 1072, 1077, 1084, 1103, 1105, 1120, 1133, 1148, 1163, 1178, 1181, 1196, 1211, 1225, 1242, 1260, 1268, 1287, 1301, 1318, 1332, 1333, 1340, 1357, 1369, 1383, 1394, 1402, 1418, 1419, 1424])
#print getPairDiffs([0, 10, 3, 8, 6, 5])
#print getPairDiffs([0, 10, 2, 7, 4, 5])
'''

def BWT(pat):
	pats = []
	for i in xrange(len(pat)):
		pats += [pat[i:]+pat[:i]]
	#print sorted(pats)
	print ''.join([x[-1] for x in sorted(pats)])

#BWT('GCGTGCCTGGTCA$')
#BWT('GTCCCCGTTCTCCGATACAGTCTTTGGTCGGGATGAGCGAATCATTTGAAACTACTACTTACGTCCGTTGATGACTTGGCCGCAAATTAAGAGAAATGCTTGATCGACGTGCAAGCGATACTTAGGTGCCGTGGTACATCATGATTGCACTTTCCAAGTCTAGTTTAGGCGAACGGTCGGCGGTACGCCTTCAATCGTGCCCTGTCGAAGGGATCATTGGGAGGCAAGGGCTCTAGCATGTGCTATAGTGAGTACGAGTCGGCACCAGAATCATGTTCGCCGGCGTTACACGACCAACTCGGATTTTAAGTCGACGCTTAAGGATCGGAGTAGCCCGGCACAAACAACATAGCAACTCTGTAGAAATGCCTAGAGCAGGTCATGGTTTACTTGGGCTATAATGATTTAAGCTATTACATCCTTAGCGTAGTGGCGTTTTTCCTTCGGGTTCTATCGACTCATCGTGATATCGGGACGCCCTAAAGCGTAGTAGGCGGGAGTCACTTGGGCAGCGACTTCTACGTCTGCGTCCTCTGACTTGGTTACGACTGGGAAGACCCTATTGCATGGAGTAAACCCGTTCGAGAGGCATTTAGTATAATTCCGAGCAGATGTTAAACCATCGGCCGCTGGCACCACATTGGACCAGTGGCGTCTGTACTCCGCCTAATATGCAGCCATCTACAATATCCAAAATAGCGTAAGCACATTATAAACCTATATGGCCCGGACCCTCTTCCGCAAGGCCCGGAGGGCGCTACTCAGACACTGGCAGCTTTACCGCCACATTACGCAGTGTGATGTAAGAGGTACCACGCTCGTAGCTTTAAGTTCACGACAGATCCACCCTACAGCGAGCACTACACTGCCAAGCCCCATACATCCGAAAACCCTACCACCGCAAGCCGGCTGCTCAGTTCGACGCGTCAAGGACTAAAGAGACCGTATACGAGTTCTAGTAATCTTGCCTCTGTACACTGCAACA$')
#BWT('CAGCCATAAGTCTGGAAAGATGAAAACAGGTTAACATGTCATGGAGGTTGGACTGGGGTTCTACTTTCTAAGTTTGCCAGACCCTCACTAACGTACTGGCAGGGTGGTCTAACCGACACTAATGAGACAGAATTGCGACTATGCAGCAAACCTGGGTTAAGTGCGGGTTCAGTTCGTAGGGGAGACCCAATTTACGAGGTATCTGACTCATGCCCGACATCGTCTACGGTCCAATGCGTCTCACTGAACATTCTGGCCTAAGTCCCTCCACTTTGACTTACCGCAGCATCTTTGTAGAACAGCCCCGCGCTGGTGCTAATGCTTCGCTAAACTACCTCTATTGCCCTGTTGTGCCACATTCCACTTCTGTCCGGAGCCACGAACGTATCGCGTAAAACCCTCCGTCTGGCTAGAATTCGTGGCTAAGCTATAAAACCCTCGAGACGTGTCTTGCATACGATATCGTAGAGCCCCGTGTTCAACTCTTAAGCGAGTTAACTGTGAGAGAAAGAGGTTCTTTTGCGATTCTCGGTAGAACCAATGTAGGACCTCATTCAAATATTAGGGTCTTACAGGTTGGGAGGGTCCTACGACGGCTTGCTTACAATCAAGACTCGGTTAGCGCTGAAGTCTAGGTATCCCGACCCTTGACTTCTGCACTATAGTATATGGGGGCGGCCCAAATAGCGACCCGGCGGGGCAGATGCCCGCGTCGGCTTTAACAGCGTTGGGCCATGTCTAACGTAAAACATTTATCACGTCGGTATAACCTAGATGGCAAAACAGTGAGGTGGTTGACCAAAATGTAGGAATCCCTCTAGCTCACGTGCACCTGACCAGGGCCCGTGGCTATAGGGACTCCTGGGGCAATTCACAGCTCAACAATG$')
	
def IBWT(pat):
	n = len(pat)
	pat1 = sorted(pat)
	while(True):
		pat1 = sorted([pat[i] + pat1[i] for i in xrange(n)])
		#print pat1
		if (len(pat1[0]) == n):
			break
	print ([x for x in pat1 if x[-1] == '$'][0])

#IBWT('TTCCTAACG$A')
#IBWT('GCTTACTGGGCCATCTCACCTATTGCTGACATCTCTTAGAGCCCAATATCCTAAGTTAACACAGCGAAGATAATTAACTGCACGACATGACGTCATAGTGCCGGCCGAGGCAATCGTCCCGCGCCGACGGTTTGCCCTCGTTGCCCGCTGCCTCATACACCAAGCATAGAGTTGTAGAGATATTCACATGGCGATGGCGAGGTACGGTTGATGGTTGGCTGAACTGTGATTGTAGGACCTCCTTGGTGGACGCATTAAGCCCCAGTGTACCGCTCCGATGAGAGTTCCTTGATAAGGATTCGCAGCGAAGGACTTAAGGCGCAACGGAAGACCCCCCATGATTGCGTCGGCTCGTGTAGAATGGATAGCTACTGTCCGTTAGTCAAGCCATAGAAGGTTCGGATAAAATACCCATTTCTATTGAGGGGTGGGGATGGCAGTAATTAATCTAGCCTATTTCTGTTAGTGATTGGTTAGGTGGTAGCGGATTTTAT$TAAGCTATTTCCAGTTATTGGCTTCCAGCGTGTTAAGGAAGCGTCTTTCCGGCGCCGATTACATCGGAACGGAGGGGACACAGATACTGATGTTCACTATGTCTGCCATACAAGAATACATTTGTATTTGGACGTACGGAGTTGGTGTTCCGTAGCCGTGAAATCGAAACATAGCTCCGGATAAGTGATCGGTGCTGGGCAACCGCTAGACCGGCGGGCCCGATTTCAACAATTTTTGCGACTTAGGTTTGTACAGGAGTTGTATGACACGGCACTCCATTGCCATCCCAACACCACTGGCCGTGCATCGTGACCGCTTCGTTTTTAGGCATTGC')

def ProfileMostProbablekmerProblem(text, k, mat):
	maxprob, maxkmer = 0, None
	symmap = {'A':0, 'C':1, 'G':2, 'T':3}
	for i in range(len(text)-k+1):
		prob, kmer = 1, text[i:i+k]
		for j in range(k):
			prob *= mat[symmap[kmer[j]]][j]
		#if prob > maxprob:
		if prob > maxprob or (prob == maxprob and kmer < maxkmer):
			maxprob, maxkmer = prob, kmer
	#print maxprob, maxkmer
	print maxkmer
	#prob, kmer = 1, 'CCGAG'
	#for j in range(k):
	#	prob *= mat[symmap[kmer[j]]][j]
	#print prob

'''	
#lines = read_file('inpros33.txt')
lines = read_file('rosalind_2cba.txt')
text = lines[0]
k = int(lines[1])
probmat = [[0 for _ in range(k)] for _ in range(4)]
for i in range(4):
	probmat[i] = map(float, str.split(lines[2+i]))
#print probmat	
ProfileMostProbablekmerProblem(text, k, probmat)	
'''

'''
def GreedyMotifSearch(Dna, k, t):
	symmap = {0:'A', 1:'C', 2:'G', 3:'T'}
	mat = [[0 for _ in range(k)] for _ in range(4)]
	for i in range(k):
		for j in range(4):
			mat[j][i] = sum([Dna[si][i] == symmap[j] for si in range(t)]) / (1.0 * t)
	#print mat
	for Text in Dna:
		ProfileMostProbablekmerProblem(Text, k, mat)
'''

'''
lines = read_file('inpros73.txt')
lines = read_file('rosalind_2dba.txt')
k, t = map(int, lines[0].split())
GreedyMotifSearch(lines[1:], k, t)
'''

def hamming(s1, s2):
	return sum([1 for i in range(len(s1)) if s1[i] != s2[i]])

'''
#lines = read_file('inpros83.txt')
lines = read_file('rosalind_ba1g.txt')
print hamming(lines[0], lines[1])
'''

import itertools

def dist_str(s, strings):
	total, k = 0, len(s)
	for string in strings:
		total += min([hamming(s, string[i:i+k]) for i in range(len(string)-k+1)])
	return total
	
def MedianStringProblem(k, dstrs):
	kmers = map(''.join, itertools.product('ACGT', repeat=k))
	min_dist, medianstr = float('inf'), None
	for kmer in kmers:
		d = dist_str(kmer, dstrs)
		if d <= min_dist:
			min_dist, medianstr = d, kmer 
	print medianstr

'''	
lines = read_file('inpros32.txt')
k = int(lines[0])
MedianStringProblem(k, lines[1:])
'''
		
def ConsensuStringProblem(k, dstrs):
	symbolmap = {'A':0, 'C':1, 'T':2, 'G':3}
	symbols = ['A', 'C', 'T', 'G']
	freq = [[0 for _ in range(len(symbols))] for _ in range(k)] # A C T G
	for dna in dstrs:
		for i in range(len(dna) - k + 1):
			for j in range(k):
				freq[j][symbolmap[dna[i + j]]] += 1
	print freq
	consesnsus_str = ''
	for i in range(k):
		consesnsus_str += symbols[max([(freq[i][j], j) for j in range(len(symbols))])[1]]
	print consesnsus_str

def ImplantedMotifProblem(dstrs, k, d):
	print 
	#matched = set([dstrs[i:i+k] for i in range(len(dstr[0])-k+1)])
	#unmatched = set([])
	#for j in range(1, len(dstr)):
	#	kmers = list(set([dstrs[i:i+k] for i in range(len(dstr[j])-k+1)]))
	#	for mkmer in matched:
	#		for kmer in kmers:
	#			if hamming(kmer, mkmer) <= d:
					
				

def DegreeArray(edges, n, m, dir = False, indeg=True, outdeg=True):
	
	degrees, nbrs = [0]*(n + 1), {}
	for e in edges:
		u, v = map(int, str.split(e))
		if outdeg:
			degrees[u] += 1
		if indeg:
			degrees[v] += 1
		nbrs[u] = nbrs.get(u, []) + [v]
		if not dir:
			nbrs[v] = nbrs.get(v, []) + [u]
	
	return	degrees, nbrs

#lines = read_file('inpros8.txt')
#lines = read_file('rosalind_deg.txt')	
#n, m = map(int, str.split(lines[0]))
#print DegreeArray(lines[1:], n, m)[0][1:]
	
def DoubleDegreeArray(edges, n, m):
	
	degrees, nbrs = DegreeArray(edges, n, m)	
	#print degrees, nbrs
	return	[sum([degrees[v] for v in nbrs.get(u, [])]) for u in range(1, n + 1)]

'''
lines = read_file('inpros9.txt')
lines = read_file('rosalind_ddeg.txt')	
n, m = map(int, str.split(lines[0]))
print DoubleDegreeArray(lines[1:], n, m)
'''

def reachableCount(nbrs, v):
	queue, visited, count = [v], [v], 0
	#print nbrs
	while len(queue) > 0:
		u = queue.pop(0)
		count += 1
		for v in nbrs.get(u, []):
			if not v in visited:
				queue.append(v)
				visited.append(v)
	return count

def DegreesNbrs(edges, dir = True):
	vertices, degrees, nbrs = set([]), {}, {}
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
			degrees[u] = degrees.get(u, 0) + 1
			degrees[v] = degrees.get(v, 0) + 1
			nbrs[u] = nbrs.get(u, []) + [v]
			if not dir:
				nbrs[v] = nbrs.get(v, []) + [u]
	vertices = list(vertices)		
	return vertices, degrees, nbrs

from copy import deepcopy
def EulerCycle(edges):
	vertices, degrees, nbrs = DegreesNbrs(edges, dir = True)
	#print vertices
	path = ''
	start = vertices[0]
	u = start
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		path += str(u) + '->'
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	assert(u == start)	
	path += str(u)
	print path

'''	
#lines = read_file('inpros49.txt')
#lines = read_file('rosalind_4e.txt')	
lines = read_file('inpros64.txt')
lines = read_file('rosalind_3eba.txt')
EulerCycle(lines)
'''

def EulerPath(edges):
	vertices, degrees, nbrs = DegreesNbrs(edges, dir = True)
	#print degrees
	odd_deg_vertices = [i for i in degrees if degrees[i] % 2 == 1]
	#print odd_deg_vertices
	path = ''
	start = vertices[odd_deg_vertices[0] if len(odd_deg_vertices) > 0 else 0]
	u = start
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		path += str(u) + '->'
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	path += str(u)
	print path

'''
#lines = read_file('inpros49.txt')
#lines = read_file('rosalind_4e.txt')	
lines = read_file('inpros65.txt')
#lines = read_file('rosalind_3eba.txt')
EulerPath(lines)
'''

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

from copy import deepcopy
def EulerTour(edges):
	vertices, indegrees, outdegrees, nbrs = DegreesNbrs(edges, dir = True)
	start = [v for v in vertices if (outdegrees.get(v, 0) + indegrees.get(v, 0)) % 2 == 1 and outdegrees.get(v, 0) > indegrees.get(v, 0)] # start with odd degree vertex
	#print vertices
	#print nbrs
	#print outdegrees
	#print indegrees
	path = ''
	start = vertices[0] if len(start) == 0 else start[0]
	#print start
	u = start
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		path += str(u) + '->'
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	path += str(u)
	print path

'''
#lines = read_file('inpros50.txt')
#lines = read_file('rosalind_4f.txt')	
lines = read_file('inpros65.txt')
lines = read_file('rosalind_3fba.txt')
EulerTour(lines)
'''

def get_vertices_degrees_nbrs(edges, n, m, dir=True, indeg=True, outdeg=True):

	degrees, nbrs = DegreeArray(edges, n, m, dir, indeg, outdeg)	
	V = set([])
	for v in nbrs.keys():
		V.add(v)
		for u in nbrs[v]:
			V.add(u)
	return V, degrees, nbrs

time = 0

def dfs(vertices, nbrs): # Main program
	
	global time
	color, pred, d, f = {}, {}, {}, {}
	for u in vertices: # Initialize
		color[u], pred[u] = 'white', None
	
	time = 0
	count = 0
	for u in vertices:
		if color[u] == 'white': 
			#print u, time
			DFSVisit(u, nbrs, color, pred, d, f) # Start new tree
			count += 1
			#time += 1
	#print '#compoents: ', count
	return f, count
	
def DFSVisit(u, nbrs, color, pred, d, f): # Process vertex u

	global time
	color[u] = 'gray' # Vertex discovered
	time += 1
	d[u] =	time # Time of discovery
	for v in nbrs.get(u, []):
		if color[v] == 'white': # Visit undiscovered
			pred[v] = u 
			DFSVisit(v, nbrs, color, pred, d, f) # neighbours
	color[u] = 'black' # Vertex finished
	time += 1
	f[u] = time # Time of finish

def toposort(edges, n, m): # Main program
	
	global time
	vertices, degrees, nbrs = get_vertices_degrees_nbrs(edges, n, m)	
	color, pred, d, f = {}, {}, {}, {}
	for u in vertices: # Initialize
		color[u], pred[u] = 'white', None
	time = 0
	for u in vertices:
		if color[u] == 'white': 
			DFSVisit(u, nbrs, color, pred, d, f) # Start new tree
	f = sorted([(val,key) for (key, val) in f.iteritems()])
	#print f
	print [pair[1] for pair in f]

'''
lines = read_file('inpros53.txt')
lines = read_file('rosalind_ts.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
toposort(lines[1:], n, m)
'''
'''
lines = read_file('inpros96.txt')
#lines = read_file('rosalind_ts.txt')	
m = len(lines)
#import itertools
#n = len(set(list(itertools.chain(*[line.split('->') for line in lines])))) #.ravel()))
edges, vertices = [], set([])
for line in lines:
	u, v = line.strip().split('->')
	u, v = u.strip(), v.strip()
	vertices.add(u)
	vertices.add(v)
	edges += [u + ' ' + v]
n = len(vertices)
#print vertices
print edges
#print n, m
toposort(edges, n, m)
'''

def VerticesInDegreesNbrsDir(edges):
	vertices, degrees, nbrs = set([]), {}, {}
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
			degrees[v] = degrees.get(v, 0) + 1
			nbrs[u] = nbrs.get(u, []) + [v]
	vertices = list(vertices)		
	return vertices, degrees, nbrs

def topological_sort(vertices, indeg, nbrs):
	#Input: A DAG G
	#Output: A list of the vertices of G in topological order
	S = [] #S = Stack()
	L = [] #List()
	for v in vertices: #O(|V|)
		if indeg.get(v, 0) == 0:
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

'''
lines = read_file('inpros85.txt')
lines = read_file('rosalind_ba5n.txt')
vertices, indeg, nbrs = VerticesInDegreesNbrsDir(lines)
(acyclic, L) = topological_sort(vertices, indeg, nbrs)
print L
'''

'''	
lines = read_file('inpros15.txt')
lines = read_file('rosalind_dag.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	#print lines[j:j+m]
	indeg, nbrs = get_vertices_degrees_nbrs(lines[j:j+m], n, m, dir=True, outdeg=False)
	out += [topological_sort(indeg, nbrs)[0]] 
	#print 'h1', lines[j]
	#print 'h2', lines[j+m-1]
	#print 'Done'
	j += m
print ' '.join(map(str, out))
'''

'''
lines = read_file('inpros53.txt')
lines = read_file('rosalind_ts.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
indeg, nbrs = DegreeArray(lines[1:], n, m, dir=True, outdeg=False)
print topological_sort(indeg, nbrs, n, m)[1]
'''

def TransposeGraph(nbrs):
	
	tr_nbrs = {}
	for v in nbrs:
		for u in nbrs.get(v, []):
			tr_nbrs[u] = tr_nbrs.get(u, []) + [v]
	return tr_nbrs
	
def StronglyConnectedComponent(edges, n, m):
	
	vertices, degrees, nbrs = get_vertices_degrees_nbrs(edges, n, m)	
	#print n, len(vertices)
	#npoints = n - len(vertices) # disconnected points
	vertices = range(1, n + 1)
	f, count = dfs(vertices, nbrs)
	f = sorted([(ftime,v) for (v, ftime) in f.iteritems()], reverse=True)
	#print f
	vertices = map(lambda(x): x[1], f) # sorted descending finish time
	nbrs = TransposeGraph(nbrs)
	#print nbrs
	f, count = dfs(vertices, nbrs)
	print '#components:', count

'''	
#lines = read_file('inpros75.txt')
lines = read_file('rosalind_scc.txt')
n, m = map(int, lines[0].split())
StronglyConnectedComponent(lines[1:], n, m)
'''
	
def GeneralSink(edges, n, m):
	
	vertices, degrees, nbrs = get_vertices_degrees_nbrs(edges, n, m)	
	vertices = range(1, n + 1)
	f, count = dfs(vertices, nbrs)
	f = sorted([(ftime,v) for (v, ftime) in f.iteritems()], reverse=True)
	vertices = map(lambda(x): x[1], f) # sorted descending finish time
	f, count = dfs(vertices, nbrs)
	return vertices[0] if count == 1 else -1

'''
lines = read_file('inpros76.txt')
#lines = read_file('rosalind_gs.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	out += [GeneralSink(set(lines[j:j+m]), n, m)]
	j += m
print ' '.join(map(str, out))
'''

#Semi-Connected Graph
'''
#lines = read_file('inpros78.txt')
lines = read_file('rosalind_sc.txt')
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	out += [-1 if GeneralSink(set(lines[j:j+m]), n, m) == -1 else 1] 
	j += m
print ' '.join(map(str, out))
'''

def PatternInText(pat, text, forbidden):
	i, j, m, n = 0, 0, len(text), len(pat)
	pos = []
	while i < m and j < n:
		if pat[j] == text[i] and not i in forbidden:
			j += 1
			pos += [i] 
		i += 1
	return [] if j < n else pos
	
def MinglePatterns(pat1, pat2, start=0):
	if len(pat2) == 1:
		return [pat1[:i] + pat2 + pat1[i:] for i in range(start, len(pat1))]
	else:
		return MinglePatterns(pat1, pat2[0], start) + MinglePatterns(pat1[start:], pat2[1:], start)
	
def FindingDisjointMotifsinaGene(pat1, pat2, text):
	#sorted_pat = sorted(pat1 + pat2)
	#k = len(sorted_pat)
	k = len(pat1 + pat2)
	for i in range(len(text)-k+1):
		kmer = text[i:i+k]
		pos1 = PatternInText(pat1, kmer, forbidden=[])
		pos2 = PatternInText(pat2, kmer, forbidden=pos1)
		#if sorted(kmer) == sorted_pat and PatternInText(pat1, kmer) and PatternInText(pat2, kmer):
		if len(pos1) == len(pat1) and len(pos2) == len(pat2):  #and len(set(pos1).intersection(pos2)) == 0:
			print pat1, pat2, kmer
			return 1
	return 0
	
'''
lines = read_file('inpros79.txt')
#lines = read_file('rosalind_itwv.txt')
text = lines[0]
pats = lines[1:]
n = len(pats)
#print pats
mat = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
	for j in range(n):
		mat[i][j] = FindingDisjointMotifsinaGene(pats[i], pats[j], text)
for i in range(n):
	print ' '.join(map(str, mat[i]))	
'''
	
def MaximizingGapSymbolsOptimalAlignment():
	pass
	
def ShortestPathDAG(edges, n, m, s):
	vertices, indeg, nbrs, W = GetNbrEdges(edges, dir=True, outdeg=False)
	acyclic, ordered_vertices = topological_sort(indeg, deepcopy(nbrs))
	D, P = {s:0}, {s:None}
	for v in ordered_vertices:
		for w in nbrs.get(v, []):
			if D.get(v, float('inf')) + W[v, w] < D.get(w, float('inf')):
				D[w], P[w] = D.get(v, float('inf')) + W[v, w], v
	
	print ' '.join(map(str, [D.get(v, 'x') for v in sorted(ordered_vertices)]))

'''
#lines = read_file('inpros55.txt')
lines = read_file('rosalind_sdag.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
ShortestPathDAG(lines[1:], n, m, 1)
'''

def LongestPathDAG(edges, src, sink):
	vertices, indeg, nbrs, W = GetNbrEdges(edges, splt='->|:', dir=True, outdeg=False)
	acyclic, ordered_vertices = topological_sort(vertices, indeg, deepcopy(nbrs))
	#print ordered_vertices, src, sink
	D, P = {src:0}, {src:None}
	for v in ordered_vertices: #[ordered_vertices.index(src):]:
		#print v
		for w in nbrs.get(v, []):
			if D.get(v, None) == None: # not on the path from src to sink
				continue
			if D[v] + W[v, w] > D.get(w, -1):
				D[w], P[w] = D[v] + W[v, w], v
	
	#print ' '.join(map(str, [D.get(v, 'x') for v in sorted(ordered_vertices)]))
	print D[sink]
	path, v = '', sink
	while v != None:
		path = str(v) if path == '' else str(v) + '->' + path
		v = P.get(v, None)
	print path	

'''	
lines = read_file('inpros88.txt')
lines = read_file('rosalind_ba5d.txt')	
src, sink = int(lines[0]), int(lines[1])
#print n, m
LongestPathDAG(lines[2:], src, sink)
'''

def DegreeArray1(edges, n, m, dir = False, indeg=True, outdeg=True):
	
	degrees, nbrs, V = {}, {}, set([])
	for e in edges:
		u, v = map(int, str.split(e))
		if outdeg:
			degrees[u] = degrees.get(u, 0) + 1
		if indeg:
			degrees[v] = degrees.get(v, 0) + 1
		nbrs[u] = nbrs.get(u, []) + [v]
		if not dir:
			nbrs[v] = nbrs.get(v, []) + [u]
		V.add(u)
		V.add(v)
	
	for v in V:
		degrees[v] = degrees.get(v, 0)
		
	return	degrees, nbrs

def HamiltonianPathDAG(edges, n, m):
	indeg, nbrs = DegreeArray(edges, n, m, dir=True, outdeg=False)
	acyclic, ordered_vertices = topological_sort(indeg, deepcopy(nbrs), n, m)
	if not acyclic or len(ordered_vertices) != n:
		return -1 
	for i in range(n - 1):
		if not ordered_vertices[i + 1] in nbrs.get(ordered_vertices[i], []):
			return -1
	return ' '.join(map(str, [1] + ordered_vertices))

'''
#lines = read_file('inpros56.txt')
lines = read_file('rosalind_hdag.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	#j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	#print lines[j:j+m]
	print HamiltonianPathDAG(lines[j:j+m], n, m)
	#print 'h1', lines[j]
	#print 'h2', lines[j+m-1]
	#print 'Done'
	j += m
'''
	
def topolgical_sort(graph_unsorted):
    """
    Repeatedly go through all of the nodes in the graph, moving each of
    the nodes that has all its edges resolved, onto a sequence that
    forms our sorted graph. A node has all of its edges resolved and
    can be moved once all the nodes its edges point to, have been moved
    from the unsorted graph onto the sorted one.
    """

    # This is the list we'll return, that stores each node/edges pair
    # in topological order.
    graph_sorted = []

    # Convert the unsorted graph into a hash table. This gives us
    # constant-time lookup for checking if edges are unresolved, and
    # for removing nodes from the unsorted graph.
    graph_unsorted = dict(graph_unsorted)

    # Run until the unsorted graph is empty.
    while graph_unsorted:

        # Go through each of the node/edges pairs in the unsorted
        # graph. If a set of edges doesn't contain any nodes that
        # haven't been resolved, that is, that are still in the
        # unsorted graph, remove the pair from the unsorted graph,
        # and append it to the sorted graph. Note here that by using
        # using the items() method for iterating, a copy of the
        # unsorted graph is used, allowing us to modify the unsorted
        # graph as we move through it. We also keep a flag for
        # checking that that graph is acyclic, which is true if any
        # nodes are resolved during each pass through the graph. If
        # not, we need to bail out as the graph therefore can't be
        # sorted.
        acyclic = False
        for node, edges in graph_unsorted.items():
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))

        if not acyclic:
            # Uh oh, we've passed through all the unsorted nodes and
            # weren't able to resolve any of them, which means there
            # are nodes with cyclic edges that will never be resolved,
            # so we bail out with an error.
            raise RuntimeError("A cyclic dependency occurred")

    return graph_sorted

'''
graph_unsorted = [(2, []),
                  (5, [11]),
                  (11, [2, 9, 10]),
                  (7, [11, 8]),
                  (9, []),
                  (10, []),
                  (8, [9]),
                  (3, [10, 8])]
from pprint import pprint
pprint(topolgical_sort(graph_unsorted))
'''

def bfs(edges, n, m):
	
	degrees, nbrs = DegreeArray(edges, n, m, dir=True)	
	queue, d, visited = [1], {v:-1 for v in range(n + 1)}, [1]
	d[1] = 0
	#print nbrs
	while len(queue) > 0:
		u = queue.pop(0)
		for v in nbrs.get(u, []):
			if not v in visited: 	#if d[v] == -1:	# not visited
				queue.append(v)
				#print v
				d[v] = d[u] + 1
				visited.append(v)
	return [d[v] for v in range(1, n + 1)]

'''
lines = read_file('inpros10.txt')
lines = read_file('rosalind_bfs.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
print bfs(lines[1:], n, m)
'''

def ConnectedComponents(nbrs, n, m): #undirected graph
	
	visited, component = [], 0
	for v in range(1, n):
		if v in visited: continue
		stack, visited = [v], visited + [v]
		#print v
		while len(stack) > 0:
			u = stack.pop()
			for v in nbrs.get(u, []):
				if not v in visited: 	#if d[v] == -1:	# not visited
					stack.append(v)
					#print v
					visited.append(v)
		component += 1
		#print 'component', component
	return component	

'''	
lines = read_file('inpros12.txt')
lines = read_file('rosalind_cc.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
degrees, nbrs = DegreeArray(lines[1:], n, m)	
ConnectedComponents(nbrs, n, m)
'''
	
def TestingBipartiteness(edges, n, m):
	
	degrees, nbrs = DegreeArray(edges, n, m)	
	visited, vclass = [], {}
	for v in range(1, n):
		if v in visited: continue
		stack, visited = [v], visited + [v]
		vclass[v] = 0
		#print v
		while len(stack) > 0:
			u = stack.pop()
			for v in nbrs.get(u, []):
				if vclass.get(v, None) == vclass[u]: return -1
				if not v in visited: 	#if d[v] == -1:	# not visited
					stack.append(v)
					#print v
					visited.append(v)
					vclass[v] = (vclass[u] + 1) % 2
		#component += 1
	return 1

'''
lines = read_file('inpros13.txt')
lines = read_file('rosalind_bip.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	#print lines[j:j+m]
	out += [TestingBipartiteness(lines[j:j+m], n, m)] 
	j += m
print out
'''

def GetNbrs(edges, n, m, dir = False):
	
	nbrs = {}
	#W = {}
	for e in edges:
		u, v, w = map(int, str.split(e))
		nbrs[u] = nbrs.get(u, []) + [(v, w)]
		#W[u, v] = w
		if not dir:
			nbrs[v] = nbrs.get(v, []) + [(u, w)]
			#W[v, u] = w			
	return nbrs #, W	

def Dijkstra(edges, n, m, source):
	
	nbrs = GetNbrs(edges, n, m, dir=True)	
	#print nbrs
	dist, prev, queue = {}, {}, []
	dist[source] = 0                             # Initialization
	for v in range(1, n + 1):           
		if v != source:
			dist[v] = float('inf')                          # Unknown distance from source to v
			prev[v] = None		                             # Predecessor of v
		queue.append((dist[v], v))
	#print queue
	while len(queue) > 0:                              	# The main loop
		d_u, u = min(queue)                              # Remove and return best vertex
		queue.remove((d_u, u))
		for (v, w) in nbrs.get(u, []):
			alt = dist[u] + w 
			if alt < dist[v]:
				old_dist, dist[v] = dist[v], alt
				prev[v] = u
				queue[queue.index((old_dist, v))] = (dist[v], v)		# Q.decrease_priority(v, alt)
	return [dist[v] for v in range(1, n + 1)]

'''
lines = read_file('inpros24.txt')
lines = read_file('rosalind_dij.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
print Dijkstra(lines[1:], n, m, 1)
'''

def GetNbrEdges(edges, n, m, dir = False):
	
	nbrs = {}
	W = {}
	for e in edges:
		u, v, w = map(int, str.split(e))
		nbrs[u] = nbrs.get(u, []) + [(v, w)]
		W[u, v] = w
		if not dir:
			nbrs[v] = nbrs.get(v, []) + [(u, w)]
			W[v, u] = w			
	
	return nbrs, W	
	
def BellmanFordHelper(W, vertices, source):
	
	# print W
	# Step 1: initialize graph
	dist, prev, n = {}, {}, len(vertices)
	dist[source] = 0                             # Initialization
	for v in vertices:           
		if v != source:
			dist[v] = float('inf')                           # Unknown distance from source to v
			prev[v] = None		                             # Predecessor of v

	# Step 2: relax edges repeatedly
	for i in range(len(vertices)):
		for (u, v) in W:
			if dist[u] + W[u, v] < dist[v]:
				dist[v] = dist[u] + W[u, v]
				prev[v] = u

	return dist
	
def BellmanFord(edges, n, m, source):
   
	nbrs, W = GetNbrEdges(edges, n, m, dir = True)
	
	dist = BellmanFordHelper(W, range(1, n + 1), source)

	return [dist[v] for v in range(1, n + 1)]

'''	
lines = read_file('inpros25.txt')
lines = read_file('rosalind_bf.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
print BellmanFord(lines[1:], n, m, 1)
'''

def NegativeWeightCycle(edges, n, m, source):
	
	nbrs, W = GetNbrEdges(edges, n, m, dir = True)
	vertices = list(set([u for (u, v) in W] + [v for (u, v) in W])) 
	vertices = [v for v in vertices if len(nbrs.get(v, [])) > 0] # vertices with 0 indegree can't be part of cycle
	#for v in vertices:	print nbrs[v]
	edel = []
	for (u, v) in W: 
		if not u in vertices or not v in vertices:
			edel.append((u, v))
	for e in edel:
		del W[e]
	
	while True:
		
		#print len(vertices)
		if len(vertices) == 0: break
		dist = BellmanFordHelper(W, vertices, vertices[0])
		# Step 3: check for negative-weight cycles
		for (u, v) in W:
			if dist[u] + W[u, v] < dist[v]:
				return 1
		vertices = [v for v in vertices if dist[v] == float('inf')]
		edel = []
		for (u, v) in W: 
			if not u in vertices or not v in vertices:
				edel.append((u, v))
		for e in edel:
			del W[e]
	
	return -1

'''
lines = read_file('inpros27.txt')
lines = read_file('rosalind_nwc.txt')	

N = int(lines[0])

i = 1
for j in range(N):
	#i += 1
	n, m = map(int, str.split(lines[i]))
	#print n, m
	i += 1
	#print lines[i:i+m]
	print NegativeWeightCycle(lines[i:i+m], n, m, 1)
	i += m
'''

import numpy as np

def getAdjMat(edges, n, m):
	degrees, nbrs = DegreeArray(edges, n, m)	
	#print nbrs
	adjmat = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
	for u in nbrs:
		for v in nbrs[u]:
			adjmat[u][v] = adjmat[v][u] = 1
	#return np.matrix(adjmat)		
	return adjmat

def matMult(A, B, C, n):
	C = [[[] for u in range(n + 1)] for v in range(n + 1)]
	for i in range(1, n + 1):
		for j in range(1, n + 1):
			for k in range(1, n + 1):
				if i != k and j !=k and i != j and A[i][k] and B[k][j]: 
					C[i][j].append([i,k,j] )#A[i][k] * B[k][j]
	return C	

def SquareinGraph(edges, n, m):
	adjmat = getAdjMat(edges, n, m)
	M = [[[u, v] for u in range(n + 1) if adjmat[u][v]] for v in range(n + 1)]
	print M
	M = matMult(M, adjmat, M, n) #adjmat * adjmat
	#for i in range(n): M[i, i] = 0
	print M
	M = matMult(M, adjmat, C, n) #M * adjmat
	print M
	#M = matMult(M, adjmat, n) #M * adjmat
	#print M

'''
lines = read_file('inpros16.txt')
#lines = read_file('rosalind_bip.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	#print lines[j:j+m]
	SquareinGraph(lines[j:j+m], n, m)
	j += m
#print out
'''

def TestingAcyclicity(edges, n, m):
	
	degrees, nbrs = DegreeArray(edges, n, m, dir=True)	
	vertices = set([])
	for v in nbrs:
		vertices.add(v)
		for w in nbrs.get(v, []):
			vertices.add(w)
	#print nbrs
	marked = {}
	done = {}
	par = {}
	for v in vertices: #range(1, n + 1):
		if not marked.get(v, False):
			if not search(nbrs, v, marked, done, par):
				return -1
	return 1
 
def search(nbrs, v, marked, done, par):
	marked[v] = True
	print 'here0', v, marked[v], nbrs.get(v, [])
	for w in nbrs.get(v, []):
		if not marked.get(w, False):
			print 'here', v, w
			par[w] = v
			return search(nbrs, w, marked, done, par)
		elif not done.get(w, False):	# already marked and not done => cycle
			print v, w, marked[w], done.get(w, False)
			cycle = [w]
			while v != w:
				cycle = [v] + cycle
				v = par.get(v, -1)
				if v == -1:
					break
			cycle = [v] + cycle
			print cycle
			return False
	done[v] = True
	print 'here1', v, done[v]
	return True
'''
lines = read_file('inpros15.txt')
lines = read_file('rosalind_dag.txt')	
ngraphs = int(lines[0])
j, out = 1, []
for i in range(ngraphs):
	j += 1 # skip white line
	n, m = map(int, str.split(lines[j]))
	j += 1
	#print lines[j:j+m]
	out += [TestingAcyclicity(lines[j:j+m], n, m)] 
	#print 'h1', lines[j]
	#print 'h2', lines[j+m-1]
	#print 'Done'
	j += m
print ' '.join(map(str, out))
'''

def getAllReversals(p):
	p = str.split(p)
	n = len(p)
	s = set([])
	for i in range(n):
		for j in range(i + 1, n):
			s.add(' '.join(p[:i] + p[i:j+1][::-1] + p[j+1:]))
	return s - set(p)
	
#print getAllReversals('1 2 3 4 5')

def hamming(p1, p2):
	return sum([p1[i] != p2[i] for i in range(len(p1))])
	
def bpdist(src, target):
	n = len(src.split())
	src, target = '0 ' + src + ' ' + str(n), '0 ' + target + ' ' + str(n)
	bp_dist = 0
	for i in range(0, len(src)-2, 2):
		pair = src[i:i+3]
		#print pair
		if not (pair in target or pair[::-1] in target):
			bp_dist += 1
	return bp_dist	
	
#print bpdist('2 4 3 5 8 7 6 1', '1 2 3 4 5 6 7 8')
	
from heapq import *
	
def ReversalDistance(p1, p2): # A* search
	#print 'convert', p1, '->', p2
	queue = []
	heappush(queue, (0, p1))	# min heap
	d = {p1:0}
	while len(queue) > 0:
		pr, p = heappop(queue)
		#print p
		if p == p2:
			return d[p]
		children = getAllReversals(p)
		for child in children:
			if (not child in d) or (d[child] > d[p] + 1):
				d[child] = d[p] + 1
				heappush(queue, (d[child] + hamming(child.split(), p2.split()), child)) # A* search: heuristic: hamming distance: # points @ right position
				#heappush(queue, (d[child] + bpdist(child, p2), child)) # A* search: heuristic: breakpoint distance
				#heappush(queue, (hamming(child.split(), p2.split()), child)) # A* search: heuristic: hamming distance: # points @ right position
				#heappush(queue, (bpdist(child, p2), child)) # A* search: heuristic: breakpoint distance

'''
lines = read_file('inpros23.txt')
#lines = read_file('rosalind_rear.txt')	
i, d = 0, []
while i < len(lines):
	p1, p2 = lines[i], lines[i + 1]
	d += [ReversalDistance(p1, p2)]
	i += 3
print ' '.join(map(str,d))
'''

from copy import deepcopy
def EulerCycle(nbrs, start):
	u, path = start, ''
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		#path += str(u) + '->'
		if path == '':
			path = str(u)
		else:
			path += str(u)[-1] 
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	#assert(u == start)	
	path += str(u)[-1]
	return path

def FindSimpleCycle(nbrs, v, marked, done, par):
	marked[v] = True
	for w in nbrs.get(v, []):
		if not marked.get(w, False):
			par[w] = v
			return FindSimpleCycle(nbrs, w, marked, done, par)
		elif not done.get(w, False):	# already marked and not done => cycle
			cycle = [w]
			while v != w:
				cycle = [v] + cycle
				v = par.get(v, -1)
				if v == -1:
					break
			scycle = cycle[0]
			for v in cycle[1:]:
				scycle += v[-1]
			print scycle
			return False
	done[v] = True
	return True
	
def ConstructingDeBruijnGraph(strings, unique=True, revcomp=True):
	if revcomp:
		strings += [ReverseComplementProblem(string) for string in strings]
	if unique:
		strings = set(strings)
	adjlist = {}
	for string in strings:
		adjlist[string[:-1]] = adjlist.get(string[:-1], []) + [string[1:]]
	return adjlist

#lines = read_file('inpros54.txt')
#lines = read_file('rosalind_dbru.txt')
#adjlist = ConstructingDeBruijnGraph(lines)
#for u in adjlist:
#	for v in adjlist[u]:
#		print '(' + str(u) + ', ' +  str(v) + ')'
#path = EulerCycle(adjlist, adjlist.keys()[4])
#print path
#marked, done, par = {} , {}, {}
#FindSimpleCycle(adjlist, adjlist.keys()[4], marked, done, par)

import copy
def FindMinimalCycle(strings):
	prefix_map = {}
	for string in strings:
		prefix_map[string[:-1]] = string
	start = strings[0]
	n = len(strings)
	m = len(start)
	mstr = start
	cur = start
	i = 1
	while i < n:
		cur = prefix_map[cur[1:]]
		mstr += cur[-1]
		i += 1
	#print mstr
	j = n
	while j >= 0:
		if mstr[:j] == mstr[-j:]:
			break
		j -= 1
	min_str = mstr[-(j+1):] + mstr[j:n-1]
	print min_str

'''	
lines = read_file('inpros94.txt')
lines = read_file('rosalind_pcov.txt')
FindMinimalCycle(lines)
'''

import copy
def FindMinimalCycleWithRevComp(strings):
	strings += [ReverseComplementProblem(string) for string in strings]
	adjlist = ConstructingDeBruijnGraph(strings)
	for u in adjlist:
		for v in adjlist[u]:
			print '(' + str(u) + ', ' +  str(v) + ')'
	#path = EulerCycle(adjlist, adjlist.keys()[4])
	#print path
	#marked, done, par = {} , {}, {}
	#FindSimpleCycle(adjlist, adjlist.keys()[0], marked, done, par)
	j = n
	while j >= 0:
		if mstr[:j] == mstr[-j:]:
			break
		j -= 1
	min_str = mstr[-(j+1):] + mstr[j:n-1]
	print min_str

#lines = read_file('inpros95.txt')
#lines = read_file('rosalind_pcov.txt')
#FindMinimalCycleWithRevComp(lines)

import numpy as np
def LastToFirstMapping(str, i):
	return sorted(range(len(str)),key=lambda x:str[x]).index(i)
	#n = len(str)
	#cols = [['_' for _ in range(n)] for _ in range(n)]
	#for j in range(n):
	#	cols[j] = [c for c in str[j:] + str[:j]]
	#print sorted(cols)
	#cols = np.array(cols)
	#print np.lexsort(cols.T)
	#cols.sort(axis=0, order=range(n))
	#print cols#[np.argsort(cols[:, 0])]

'''	
#print LastToFirstMapping('T$GACCA', 3)
print LastToFirstMapping('TAGCAATCCGGTATTTGCTACGATCTTACCAACACAAGGGTATATAGTTTGCTAAGTAGAGCGCTTAATAAACACCCGTTTTTACCACCTCCAGGAGTGCGTTCGACGTATTGGAGTTAATCTTCCGGCACGATTTCCACGAATCCATCATCAAATAGGTCCCCACTGTAGAATTGAACCTATAGCGGGCACAAGGTTGCTGCTACCATATGAGATGAGATGGTAGCACATGTGACCCTCAACCAATGCTACGTCAGTCGAGGATAGTGCGGTCGCGCTCCCCGTTAAAACTGTGGCAGCCAAAAGTCACCGTTAGTTCCGAGTTGTTTAAGGGAAGGGGCGGCCACGTAACATTCAGACAATCCTGATCCCGCGTGTGTCGCGATTCGTCTTGGTTGTTTTATCCAAACCATTCTCTGAGTGGGCCTTAACCTACCCCCTGGATCGCCAAGAAGTTAACGACCCCTACCAAGATCAGTACGTAAGTAAACTTACGCTTTGGCGGTTCCCCATATGGGTAAGGGGGGCCCCGCGCTACAATGCACATGGATGCCTCTCGATCATTGATTCGATCAAACCTATTTACCCTCCTAACGAGCTCAAATACAATGAGCTCCGCTCATTCCTCCGCTGCCTGGTACCCCCGCCCAACTACCACAGCTTTGGGAACCACATTTTGATTCCCCTCATCAAGGTTCATGCCCGATGAACGCAACCCTTTATAGCCATGCCCGTTTCACCTGGCGTCATTCACATATTCGGCATTTGTAGGAGTTTGGCGACAGCTTAAGCTTCCCTCTCTTTGCCAACGCGCGCAACTAACCCTCCCAACTTGA$', 497)
'''
		
def ConstructingDeBruijnGraphFromString(Text, k):
	adjlist = ConstructingDeBruijnGraph([Text[i:i+k] for i in range(len(Text)-k+1)], revcomp=False)
	for v, nbrs in sorted(adjlist.iteritems()):
		nbrs = ','.join(sorted(nbrs))
		if nbrs[-1] == ',':
			nbrs = nbrs[:-1]
		print v, '->', nbrs

'''
#lines = read_file('inpros62.txt')
lines = read_file('rosalind_3cba.txt')
k, Text = int(lines[0]), lines[1]
ConstructingDeBruijnGraphFromString(Text, k)
'''

def DeBruijnGraphfromkmersProblem(strings):
	adjlist = ConstructingDeBruijnGraph(strings, unique=False, revcomp=False)
	for v, nbrs in sorted(adjlist.iteritems()):
		nbrs = ','.join(sorted(nbrs))
		if nbrs[-1] == ',':
			nbrs = nbrs[:-1]
		print v, '->', nbrs

'''		
#lines = read_file('inpros63.txt')
lines = read_file('rosalind_3dba.txt')
DeBruijnGraphfromkmersProblem(lines)
'''
		
def GenomeAssemblyShortestSuperstring(strings):
	
	m = len(strings)
	while m > 1:
		#string = ''	
		#D = [[0 for _ in range(m)] for _ in range(m)]
		for i in range(m):
			M = {}
			for j in range(i + 1, m):
				n = min(len(strings[i]), len(strings[j]))
				if strings[i] in strings[j]:
					string = strings[j]
				elif strings[j] in strings[i]:
					string = strings[i]
				else:
					k = n / 2
					while k < n and strings[i][:k] != strings[j][-k:]:
						k += 1
					if k < n and strings[i][:k] == strings[j][-k:]:
						string = strings[j] + strings[i][k:]
						#D[i][j], D[j][i] = 1, 2
						M[j] = k
					#if string != '':
					#	strings = strings[:j] + strings[j+1:]
					#	strings = strings[:i] + strings[i+1:]
					#	strings.append(string)
					#	break
					k = n / 2
					while k < n and strings[i][-k:] != strings[j][:k]:
						k += 1
					#print k, n
					#print 'h1', strings[i][-k:]
					#print 'h2', strings[j][:k], strings[i][-k:] == strings[j][:k], i, j
					if k < n and strings[i][-k:] == strings[j][:k]:
						string = strings[i] + strings[j][k:]
						#D[i][j], D[j][i] = 2, 1
						M[j] = -k
					#if string != '':
					#	strings = strings[:j] + strings[j+1:]
					#	strings = strings[:i] + strings[i+1:]
					#	strings.append(string)
					#	break
			#if string != '':
			#	break
			#print i, M
			if len(M) > 0:
				v, k, j = max([(abs(M[j]), M[j], j) for j in M])
				print v, k, j
				string = strings[j] + strings[i][k:] if k > 0 else strings[i] + strings[j][-k:]
				strings = strings[:j] + strings[j+1:]
				strings = strings[:i] + strings[i+1:]
				strings.append(string)
				break
		m = len(strings)
		print 'h', m #, strings
		#for i in range(m): print D[i]	
		#print 'h', strings
'''
lines = read_file('inpros21.txt')
lines = read_file('rosalind_long.txt')	
i, n = 0, len(lines)
strings = []
while i < n:
	if lines[i][0] == '>':
		i += 1
	string = ''
	while i < n and lines[i][0] != '>':
		string += lines[i]
		i += 1
	strings += [string]

#print strings
GenomeAssemblyShortestSuperstring(strings)	
'''
	
def catalannumbers(n):
	C = [1] * (n + 1)
	for i in range(2, n + 1):
		C[i] = sum([C[k - 1] * C[i - k] for k in range(1, i + 1)])
	print C
	
#catalannumbers(10)	
	
def CatalanNumbersRNASecondaryStructures(string):
	C = [1] * len(string)
	for i in range(2, n + 1):
		C[i] = sum([C[k - 1] * C[i - k] for k in range(1, i + 1)])
	print C

def TwoSUM1(a):
	#aua = map(lambda(x): abs(x), set(a))
	aua = map(lambda(x): abs(x), a)
	saua = set(aua)
	for e in saua:
		aua.remove(e)
	lst = []
	for k in range(len(aua)):
		num = aua[k]
		#print num
		if num in a and -num in a:
			i, j = (a.index(num) + 1, a.index(-num) + 1)
			#if i < j: lst.append((j, i))
			if i != j:
				lst.append((max(i,j), min(i,j))) 
	#print sorted(lst)
	if len(lst) > 0:
		pairs = sorted(lst)[0]
		#print a[pairs[1] - 1], a[pairs[0] - 1]
		return pairs[1], pairs[0]
	return -1	

def TwoSUM(a):
	absmap = {}
	for i in range(len(a)):
		key = abs(a[i])
		absmap[key] = absmap.get(key, []) + [i]
	lst = []
	for key, indices in absmap.iteritems():
		n = len(indices)
		#print key, indices
		if n == 1: continue
		for i in range(n):
			if a[indices[i]] == key:
				break
		for j in range(n):
			if a[indices[j]] == -key:
				break
		if i < n and j < n and indices[i] != indices[j] and a[indices[i]] == -a[indices[j]]:
			lst.append((max(indices[i] + 1, indices[j] + 1), min(indices[i] + 1, indices[j] + 1)))
	if len(lst) > 0:
		pairs = sorted(lst)[0]
		#print a[pairs[1] - 1], a[pairs[0] - 1]
		return pairs[1], pairs[0]
	return -1			

'''	
lines = read_file('inpros11.txt')
lines = read_file('rosalind_2sum.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
for line in lines[1:]:
	print TwoSUM(map(int, str.split(line)))
'''

def FindLongestMultipleRepeat(text, k):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	repeated_texts = {}
	for suffix in suffixes:
		node, done = root, False
		repeated_text = ''
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						del tree[node][string]
						repeated_texts[cp] = repeated_texts.get(string, 1)
						id += 1
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
					elif lcp == lstr and lcp == lsuffix:
						done = True
					repeated_text += cp
					repeated_texts[repeated_text] = repeated_texts.get(repeated_text, 1) + 1
					#print suffix, cp, repeated_text, repeated_texts[repeated_text]
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		#print suffix, tree
	
	#print tree
	#texts = sum([x.keys() for x in tree.values()], [])
	#for x in texts:
	#	print x
	#for k, v in repeated_texts.iteritems():
	#	print k, v
	#repeated_texts = {pat:repeated_texts[pat] for pat in repeated_texts if repeated_texts[pat] >= k}
	repeated_texts = [(len(pat), repeated_texts[pat], pat) for pat in repeated_texts if repeated_texts[pat] >= k]
	print sorted(repeated_texts, reverse = True)[1][2]

#text = "CATACATAC$"
#text = "GAATGCGATTTGACATGTTGAAAGTTACGATGCACAGGCGGCCTATCGTTCTTCTACACCTAGAAGACTGTCTGTTCAGCTAAGATCACAACGCGGGCTAAATTACTTAGGGAGGAAGACCACCGGCCGCACCAAGCTGCCTACTTTTCACAGTTCTTCTCGGACAAGGACTCTTGGGTTAAGACTTTGTTGCACCTTGCGTGCACAATGAATGAACTGTACCGGGGGACGGGTCGGATTAGGAGCCGGTAATTCTGTGAAAAAGGCTGCGGTTGTAAATCGACGGACCGAACGTCAAGTCCGCGTCTGACTAGGTCCAGGGAACTTGTACATGGACACTCGTACCCTGCAACGCTGTGAATGACGGAACCATAGGCGAAGACTGATTAGGAGGCTGGCGTATTGAGACTCAGACCGCAAGCTGTTGTCAGGGCATCTCTGAGTAACGGTCGCCAGAAGACACCGTCTCTGAATGGCGGACATACGACGTCCGTGCTGCCGCCCGGGACAGCAGTTAGATCGTAACCACTCATAAACGGCCCTTCAGTGACGTTGTAGAACGCTGTCTATATAGAGCAAGGCTACGGTCCAATCTAGGAGTTCGAGGCAGCCGAGATGGGTTGCGCAAATGAGCACAGGACTGGCCGTTCCACTAGTTGGGATAGCTGGTGCGAAGGTGGCCTTGCTGCCCAGGGTAGAGGCTTCTCCAACCCTCGCTGCGGCGGCGTCTTTCGCAGCTTGTACAGGGTTCGTTGCTCACAGGCATGCCAGAAGCGTGAGTTGTCGCGGAGGAACGGGGGACTTTAAAAGAGCTGACCGTCGTGAAAGGCCTATGCCGTAAGATGCTGCTTGGCTAAAATCGCGGGAACACTGATGACGTCGGTGGATTAGACTCTGTCAGTACATCGGTGCTACTTGTTCTGTCGTCTTCTCGCTCCGAAGGATGTGCGGGGAACGGATCGGGTCCCTCCAATATCCTTGTAGTGCCGCATATTTTAATTTTCTAATTCGGTTAGTAGTGCGACCCGATTACCATTCGAGAATGTGCGCATACCAAGGTCGTCTGATTAGCATATAGGTCCCATGATACGAGGGTACGTAGCGATCAATAGTGGCGGAGAGGCCAGAGTGAGCCCTTTCCACAGTATGGATGGCCGAGAAGACCCGGGTGCATGCTGTCCACTTGCCTTTCGAAGCGTTTTATTCCGGGCCAGTGCCTCTTGTGCGGATTTCCTCCTAGCTCTGCGGGAAAACTCCCCCCAAGCGGTCCCGGTCGGATGACTTGGCCGAACCATCGTTTTAAAGGCAGGAGCTTATCTTAAGACCTCTAAACGTTGAAAAGCCCCGATGTTGGTCATCTTGGAACCTGCCATTGTATCCGCATCAAACTACTGGGCTCTCGCAATCGTCGTTAGCAAGCTGGATAAAGCTCAACATGACTGGGGACCATCTACGTCGCAGGCGAGTCCCTATTAGTCATCGGCGACTTTGATGCATCAGTAGACCAGAATTGAGTATACTCAGGGAGTCTTGACCAGAACGCGCCTGCTCTGGCAATCGATGCCGGTGCCACTCGAACGAGTCACCTTGGCAGAGCGTCTTGCCATACAAACGTCCGGAACCACAGGTAGTACCCTAGTGAGGCCGCCATAGCCTGGGAGATTGGTCGGACTCTTCCCAATAGTACCACATGTAGTGATGGTGATGCAATCTTCAACCCGGCACTGCATACTACAGTCATTTTACCAATCTTGACGTCGCGAGTGCAGGGCACGAGATCTGTGGACGTATTGCTGTCGCTATTCTGGAAAATGGAACTCTAGGCCCGGAGCCTCTTTGTACAGAGATATGTCCCAGTTTTCTATTAATAGGTTGTACCCTGCATATATCGTCTGTTCGATGATCATCACAACAACACGAAAAAAAACTGAAGTCAGACGGCCGTGCACGAATGGGTGTCGGGGCGCACAACTAGCCCCACCTTCTGATAAACAATCCGAACTCAGATGGCAGTAGCTTTCGGCTCTGTGTACGGCTGGACTTGTACTAACACGGGCACTGAACTATCTGTGATCTCGATTCGGCCCTGGATTCGCGGAGAAACTTTGATAGGATTATTTCTTGGTTTTCACCGTTAGTGACCCACTTTCATTCCAACATCGCTCCGTAATGGTCTTATTCTAATATTGAGGAGAGCTTCTACCAAAATAGCTAACTAGACCCTGCAGGTAAAATGAACAACTGACCGAACGCTTGACCCGGCGTAGGTCTCCGCGAGACTACCAGCCGCTGGGTGTGAATCCCTTTTAAGAACGTTTTACACCGCTTGCCGCCCAGCCGAGCGAATCTATACTTAACAACTGGTCGTTTCGTGGACAACCTAGGTCTCCCTGCATGTGATCCCCGATAAGCGGACTTGAGTAGCCCACCGTGCGTAACTGCTAGAGACACTTGAAAGACTGGACTCGGGGTGGGTCCGTATCTGATAGGCCGCTCCCGAATCAATTGCTGTTAGGTCAAAACTTCAAACCAAGGTAAGGATACTGCGACAACATACACATTTTGAGTTAAGATATGTCGAATGGAGCGAGCTACAGTCGTTACTCGTGTAACAGCCACGGAGATCCCCTCCGAAACGTCATCCTCTCCAGTGGGCTTGCTTGCAACATAGTGACACTACTCGTGCTTGTAACATATTTGGCCCGCGACTAAAGAGAAAGAACAAACGTGATCCAAGCTGTGTGATGGTGGTTCTCGTTTTAAGCAGGTCTTGGGAATCTACATATACACTCGATCAGTCCGTCTAGCGAGTTTTCGCGAGCGTCCCACTTCCCTTCTTACGTGATGCCGGAGTGGCAGAGGGTGCGCAAAGCCTACGATTGAGGAGTGCCGTCCTTTCACCATAGTCCACGGGTTCTGCTGCCTTATAAGAAGTTCTTAAATAAATAGCAGAATATATCGAGTCGGTCCCTATGTGACCAAGCACTGTCAAAGTATGTGCCATAGTCTAGATCGTGGTTGGATCGTTCCATTCGTAGAAGAGTAAGAGTACGTAGATGGCACCCGTAAGGGAACGCTTGGTAACATCCTCCGGCGCACTTACCATCCGTGCTGCAGGTAGCAATGGCCGAGTGTATACAACATCCCGGCTGAGTTCCTGAACTAAGGCTATTGTGGGCTGTCGTACCTTTGCGCGTGAAGAGCGGTATATGACTCTAACAATCGTTAACAGATGTGGTAAATCGCGCCGTCAGGACACCGCCCACCGAATTTCTTGCGTGGGCTGATATGGACGGTGATAACCAGGGTAACGACTAAGGGCCATTGGTATACTGCGTGGTAGACAAAAGTTCCTACAGTCATCCAGGCAGATTCCGCAACAAACAAGGCGGGAGGGTTCGACACTGGGGGCCCTTACACGAACTATGGATAGATCCAGGCAAAGGAATGTGCTAGCTCCGGCCATACATAACTGCCCCCATTGTTAGCCAAGGCACTCGCGGACCTCGAGCAATGGGATGTCGGCCCAAGTCGTGAATGGTTTCCAGGCTGCATGGAGGTCTGCGCGGCTTAATCTCAATATTGTATCGTAGTTCGAGCTGGAGACGGCTTGTAAGTGCAACCTGTTGACACGCCGTGAACCTCGCATCGGGACTGCGGATTCCTATAGGGATGGGTCACTTCCCAGCCTCGACTAAACGTAGCCGCATGTGAAATTTTAGGAACTTATCTAGTAAGACTAGATATGCTTCATATGTCCCCACTCCCGTGTCACCCAGATGGTAGACAGAGGTCTCGATGTCCTATTAAAACAACGCTAGAGGCATTACTGGCCTAATAAGCATATTTAACTGCCCGATGGTATATTCAACGGTTGACACTGCGCGCTAGGCCTACTGCCCAGACTAACAGATCGACTCCGTGTTCCGTCCGAAACAATCAACAATTGTGTGTCTGAGCTAGCTACTTGTCCGCACCCCCAAATCAGGCGTGAGGGAAAATTTATTGCATGAAGAAGATGACGTAAAAAACTGTTTAGGTGTTCCCTCCTGAACCGCTGTACGCATCCACATTAATTTGGCCGAGTCAGGCCCTCGTCCGTTTCTAGTTGTATTAAAACCAGCTAACTTGGTTCAGACGCACCAATCATGTACCTGGAGCCCCAAAATCCTGACTAGCCTCGAACGGGCTCCCAACTCTTGTAAATATGATCGTGAGAGTGAGGCCGCCTGGCTCTGAACTGTCCTGACGGACGGTGAGGTACTCTAGGCCAGGTGGACCGCTTCTGCTGGCCTTGGCCCCTGTCATCGTCCTGTGCACATCAGCCATTAATATATGTTTCCAGTCAATCGCGAACGAATCACTAATAAAGGATCGTCTACAGCTGGGCCCTCTGCTACGAGCCGCCAAATTATCGGGGATGACGAGGTCCCTCAAGTACATCGAGCACAAGGCCACTCTGTGTAAACAAGTCTAAGTGGGTACTTCTAGATAGATTACCTCCCCGCTTACAGTGCAGTGAATCGATCCGAAACTTGTTTCGATGAGTACAAGATTACTATCCGCCCATGTCCAAACGGGTTCTACGGGGGGATGTCATTTTCCAGCCATCATGCCAAACAATTCAGTAATTATTCTGCCAGGTAATTCACTCAAACGACGCCATGTCTGCCATTACCCTTCGTGCTAAGCGTGAATCAGCCTTGGGTTCCAACGTACGAAGATGCGTACGCGCATAACCCGGCGTTACACCCTACACACGACCGGCTTTAGCCTCCATATCCGCGAATACGACTCGGGTTAATAGCAATACCCATCTACGCGCAGCTCGAAATACATGGGGCCTAAGGTTCTCTTACGGAACGTAAGCCTTGCGTTGGACACCTGACTGGTTGCTGGTGAACCGAGAATTGTTACTTGACAAAATTCTGTTATCGTGTCTCGATCAAATTCATTGCAAGAGAAGCAATGCACTCTATATTGTTCATGCCGGTGTTAATAGCTGAGTGAACTCACCTCAACACGTGCGGCCCCGGACCCCTCGGCATGATACAGATGTAGCCCGTGCAGTAGTAGTCGGTTTCCCAGATGTAGTGTTGGTATACATCATTTCCCGCATCACGTGGCTCCCCCGACACGAAGCTAGCGCAGTCTAGTCCATGACAGTTCGGGCTTTGCTAGCCAAGTTTTTGTGTTAACTATGCGGATAAGTCTCCTAACACTGTGGAAGTTTGCTCGCAACTCTCGAAACATGAATCGTTATAAGAAGGTGACGGATGGAAAAAGCCGCAAAGTCTTCGCCCATTTGACGCAGGGATTTATTTCCGCAGTTACTTCAGGAAAGAAGAGAAAAGATAGTGTTCGTTTACCATATCGAGCCATTACCTCTAGCGCAACCAACAGCTGTACAAGAACCAACAATTCCACACCGAATACACATGGGTCGGCGGGGTCAGGGTAAAGTGACGAGTCACCCCCTGAGCTCCGGTGTAGGGCTAAAAGGCGGCGGCGAAATATGAATCCAGAGTCGAGGGCAGCGACAGTTACGGAGGCTAGTCAAACTGTGACCCGACACTACACTGCACCTGTGAGATTATTTGTTCCGGGTGCGACAGAGCAATACAAAATTTAGCCTGGCCGTTAGTTTTAATACTGGCATGGAAGTAACGCAAGTTCAAACCTCCAGCCCCGAGCGCGCGATGGGTTGGTTCCTCAACGCGCTTTTATGGAATATATCAAAGAGATAACCATGTTAAAGTTATACACGACAACTACTCGTTTCGTGGCGACCGTTGTGAGGGTTAGCAACCTGGCTACTCTATGTGGTACGTGCCTAAATTGTTTCGCCTTGTAAGCGTAGTCGCCGGGTGAATCCCTAACTCTCGGCTATCCAATCGTACTTGAACCAGCGCCGTGCGAGCACGATTTATGAAATGCCGGATATCCGCGGTGGCTAGTCCGGGTTGTTGAATTTTAAATGATTAGTTACAAGATAGCATCAGAGCTAGCGCAGATCGGCCTTTTCGGGGCTGATAGCCGGCACCTTTATTAGATGTGAAGACGTTGTATTTTGCAGTGACACATACGGTGCTAAATGGTTCGACGGTTGAGAAGGGTGCTCACCTGATATTCGATTGCAAGCTATTTGAAAGGTCGGGAAAAGTCCGTATACGAACATCCCTCATCGCGCGCGGCATTCGTACTTGATGTCACGCCCATGATTGTTCTTCAGAGTACCCGCGTTTCGGCTGCGATCACTGAAACGCAACATAAAGTAAGCGTCCCTTTTAGTCGACGGTGTCAGAACTCCTGTGAAAAGAGCCATGATGCGAGCGATGGCGCTCTCGAGTGACCATCCGCGATTAAATCTGTAACTCGTTTCATGGCCTGACTATTATGCATCGTTAGAACAACCAACCCGTGACAACAACCGGTGACGTGTGTCCAAGCATCTCCTGCTCCACTTGGGTGGAAAATGGGCCCTGTGGGGGAGTGGCGCGTGCCAGATAGTCGACAGTTTTCTGCGGCTTGGTATGACGCCTTGTTTCATCAATTTAAATGCGATCAGGTATGGCGTATACATGAAGTCGGTCCAGGTGTGCGTAGCACTTTGTACCTCCTCCAAAAGCGCCGGGTATTCCTTCTCAACGAATGCCCTGAATACGCTCGCCCGAAGGATAGCGGTTCAGCCGCGAGGCCGCACTTAGAAGGAATGTAAGAGTCGGATTTAGTACCTAGTGCGGTCGCCACTGGACGGCATGAGATTTCTATCTGAAGGAGTTGGCCCCAGCGCAATAGGAGTCGTGGCCCGGTGTTCTAGGCAGCTCTAGATTGCAAAAGTGTTGTGGGGTCGCACTTTCATGGCGTAGCACAATCTCCAGCGGCAGCCAACGCCAGGTTACTACCTACCCCCTGTGGAATACGCCGAACGGCACCGATCGGCCTCTGCAATCTGGTCCGGTCGTTAGACCTTCTATTTTGGTCGAGACTAAACGTTTAGACGGTCTGGTGTGTTACGTCGCCCTCGTTTGGCTCATCTTTGAGTAAACCAGCTATTTCGTGCCACCCGGTGAGGTTCATAGTACCTCCCAATCAAAAGTCTAGGTGGCCCTTTTGTACCTACGGTATTGACCAATGCTGATATGGGACTCTGACACTGGAACCGGCATTCACTGCCCCAGACAGCGTATATCATTGAATATAGGAAGCATTATTTATCTCTCATTTGATGGAGAGTATCTGCTTCTCCATGACCAGCCACCCATTTATCATTCGCCCTACTGAAAATTCGCAAGAGATGTCCAGTGGTTCACCCTTTCCTCAATTTTATCTAAACGGGCCGCGCGAGGGCTCAATGGGGGGTCTCAAAACCTATAGTCAAACTACCTTGCTATAGATAAATGGTATATTGCTGTTTTGGGCGCAATGTGAACCTCAGACACCACTGAAATAGAAATCTGTGTGCACCGACACGGGCTAGCTCGGCAAAGGTCGTTACGGGCACATTGGACTTGCTCCGTAACATACGGCGGGACCCGGGTTAAAACACAACGCCCCCCATAGTAGCGCACTAAGGCCGACCGGCGAGGGCGCCTTGCGGACGAAATCCCCGTTGTATATCGCCGTGCGATGGACTTAAATGGAATTAGGCCTCTGAAACGTGATGCGCATCTGTTCCATCTTTCGGTCTCGCACACACGAGTTACGACTTTTTACTAGCATGTTTTTTAGACCCCATGCGGACGTTGAAATTACGAGCTTTGGTCCGGCTAGAACGCGACCGAAATGCTACTCTTTAAAGTCAGGGAGCCTGGAGCGCCCCTTCCCTAGTACGCCCTGAGGCGAGCTATATAAGATCGTGGGCAACTATGATACCGGAACGTTTGGATAGCCATGGGTACATTGATCCCCAATTACATGTCATGGAGGGTGAGCAATTATCGACCAAGCCGCGGTGGGATTTCCAACAACGCAAGTTGACAGGACTAAACCTGGCGGTGCATTCAGTCCCTACTGCTACCGCGCATCTCCTGCACTGAAATAAGGTGTGCGTAATACCTCATAGCTGGAGGCGCTCCGTAGTGGGAGAAAAACTGCACGAATTGACGTTACTGGGGTATGTTGCCAAGCAGGTGTCGAGGTAACTCGGACGATGTCTTATGATTCACGATTGTACGTTCTCCCGATCATATAATTTCATCCCTTCAATAGTCCGTAGAACGCTCCCACGAGAACTTACTCGATTAACGTCCGTGTTTGCTATTTCAGCTCAGACGAATACATGCCCTACGGTCCTTCTTGGCTGAAGATATGTCAGTAGGCACTGATCGGCCTAGACGCTGGTGTACTACAATCCATGAGCCCGTAGATATTTACGAAGCAATGTAAGACGCGTCACCATCACCCTTGTACCCCTAGAACGTCAAGCCAACACGTCACTGGATGGCCTCTAGTACATGGAGGCGTTGTGTCGTTCGGGCGGGCCGTCTATCAAATTAGGTTCAAGAACCTCGGAGCCGACAAAACGTGAATTTTTTAGCCTCCAATGGGATTAAGATCCGACCCTAACGGTTCTGCGAATCGATTAGGAACTAGTGCCTCATAGACCGCAGCTCTCTGCTAGAGGACCGAGTTGGAGGCGGCCTTCTAGAAACGAGGATATACGGGAAGGTACTGACAGGACCGGGGATTTTAGGACGGACACAGGATCTGCCCTAACGAGGATCGTATCCCGGAACCGGAAAGAGTCGAGTAGCGCTCCTGACCTAACTATTGTCCCATTACCGCACAGCACTAGGAACAGCCTTTCTGCCTGCAGGCGATTTGCGAGCCTATGATGACCATTATGGTTTTCCTTGGCAAGCCTCGTGAAAGGCACATCCCGGGCCTAACCAGTACGGCATCACGATTCAGTAGCCGGCCTCGAATCTGTGTGGAACCTGTAAAGCGTTTATGTTGGCCTCAATAGACAAGCATAGAGTTGTAACCACCTCTTCCTCCTATCCAATACTAATAAGAGGCCAGTGTGACCGCAAGACCATGTGACTCTCGTACTAATAGGACGAAGTGAACCTTGTGGGGGGGGACGGAATAGGGACCCGATGCTCAAGGCCATCTTGATGTCTAGACACGCGTGGCAGCTAATGCCCACTGCTCTCACTGCCGGGGCTAGAACGGGCAGGAGGAAGACGTACTAGCCGTCTAACGGGTATTAAGGAGACATGTCAGAGGCCGTTGGTACAACCAGGTCTTCTATTATACTCGTCTCGCAGAGCCTGGACGGCTTAGCTAACCTTTTTCACCGACTCCCTCGCCCCCTTTCGTTGTACACAAGGGCCTTGCACGCAACCGAATCCGTAAAGAAGAGCACCAAAAGTGAGGGTTGATTAGAGCTAACGCTAGACGGCTGCTACCGTTTTGCGCCCTCACTTGCCTGACGGCATCAGGCATATTTGCGATCCAATTCTAGTCGCACCAATTTGAACCAAGCTCGCGTCACGGTTTTAGCCGTATCCTGTGTGATCCGCCTATTCGGGAACTATAGATTGCTGCATCTGCATGGGGCCTTCCCGTTAAAATCATGGGCCATACATTTAGACTGATACATATCACACGATCAGGACCTTGTTGATAGCCCTGAAGTGAACAGATAAGCTCTAGGTAGCTTAGTGAGTGACAGCGGTATGAAAGGCAGAAGGCAGATATCCGCTATGAGGGTCAAACCTAATGCGAATCACCATTACGATTAAACCTCTTCTCCTCCCAGGCGAAGGAAGTAATACAGCTTCCGATATTACCAGTGTTGACGCAAGCTGGCTATTTTGTTAGGCGAACTTCTAGACCTAGGTTTGTTGTGAAATTGGTCTTGGACCCAATAGAGTGGGATGCCGACTCTATAGATGGCGCCGCAGACTGCTGATCGCAACCTTTTCTGGAGCGACACTGCAAATTGGTATGTGGCGACGCGAAGTCCTCAGCAGAGATGATATGGTAGACCCATTTTTCCCATGATTCACGGTCCAACACGCGTGTGGATTGAAGCTACCCGACGAGTAAAACCGGGACGGGACCAAACTGATAAAGTAACGTAGACGTGTTCACCTTAAACGTCGGGACCGTGTCGTATACCGGAGGAGTTGAGATAGATGAGTAGCTCCCTTAGAACGCCGCATGACGGGCGTATGTCAACGTTGAAAGTGTGGCTGCCCGGTAAGAGCTATGGTGTTGGCCATAATAAAGCCCTCAGGATAACACCTCTTGAGGAAAGACGATACATTAAATGCTCATACGTTGCAACATTTAAAGAGGCTGGTAGCTCACGTTCTAAAGTTTAATACTTTGTCATTTTATGTGTCCTCCAAGTGGATAGATGTCCAAGTTTAGGTTTGCGGACGGCATTGCACGAACACACCCATGGTCTACTTGTCTTGGGTGTTCTCGCCATATTGTGTGCGCACCGTCGAGGAAGGTCATGTACTTTAGGAGCTCTCGCATTTGTATTATAGGACATCGTATTAGATACGACCAGGTGGTAACGTGCATCGGATTGCGGCAACACGCCCGTGCAAAAGCGGTCAGGCGTACGAGCGATGACACTACATACTTCAAATGCCGTAATTGCATCCCCCAGGCGTAGATTAGTCTTTGATCAAGGTTAAATGCACACCATAAAACATAAAGTTCAAATGGTCACCTAGTAGGGATTATGGATTTATTCATCACCGCCAACATACATTAAACGGTGCAGAGGACGCTTGTTCTGCAGCTCAAGAAATCGACCGTCTCAGTCATGGAAGCCATACTTAAGTTCAATGTATGTCCAGCCACTGGTATCCCGAGTCTGGAACTAGCAGTCCATAGACGACTTGAACTTGGGCCGGTACGTGCGTTCCGAATCAACCTGTACTTCTTTGGACCAGAAACGGGTCCTGGGCCGAAATCAAAGACATCCCCTCTGGGTTGAAGGACATAGCCACTATATTAGATACGGCCGCCCAAAAATACTAGTTTACGCTGGGATACGTACACGAGGCGTTAGACATTCTCCCTTTACCCGATGGAATCCCGCCCCTTCGTGTTTCTGTAGTAAAAGACTTTTCGCAGAAGATAGAAGAGACTATGTCATAACTGTAATAACCTTCTCAGGCGTATAGGTGCCCTTGTACTGTGTTGTCCAGATCACAGGGGAGAGTCGGATAACAAGGAATGAGTTTTTGATCGGACGCGGGTGGTGCAGGGACCAGCGTCCATCGCCAGGGGCAGGCATGCAATTCGGAGCATGGAGCCGAGTTGACGAACCGAGGCTTCCCCATTGCGGACACAGTTCAAGCGACATACACGTCTCAATCAGTCATCCTTACTTGCTCGTCGTATACAAGAATCTCGGAACCGAGTAGTTGTCAGCACTTTCCGAAGACATGCTTCAACTAAGAACGCACCTGACAGTTAAGTGCGGGCGCAACTGCCGAGAGAATCGACGCGACCGCCGTTTTAGTTTGCTTTGCAATCGCAGGGTAGTATCATAAATCGGCGCTGTAAACGTCTAGGATATTAATTATTCGCAACCCAGGAAACGAAATGGCTAACACAAGAGACGCTGGTAGCCGGGAATTGAGAAGCTGAGGGAATATTATGTCATGGCCCCTGCGGCATAAAACACAAAAAAGGAACGAGGCCTCCATATAATTCGGTAATAGGCTTTTAGTATAAATTGCCACTAAGATAACATTCTCTCCGCACCCAGAATCTCGGGTCGTGTAGCGTATTGCAGTAGAATCATTCCACAATTGATGTGGGGAATTAGCGCGCCTTACGACTCGTCACTCACACGTATCGATCGACATAGGGCCGGAGCTCCCGCCTAGCTATTCGGTCACTAACCTCGGGCTGTATGACCTTTCAACCTATAGATTGACTTACAGAGTCTGAGCCTTCGCTAAGCGGAACAAGATGTCGCACGCCTGACATCTAGCTCGTACATTGCTGACCAGTTGATAACACCTCGGTTGTTTTTCAAAAACCATTTAGAACAGGGCAATTATAACTCGTGTTAGAAGGCGGCCCAATTACGTCACAGGCCTTGTATTTGGGGCAATCTCAAATATGTTCACCCAATGTCTACACCCTTCTTGCTAGCTACGTCTACTGGAGAGAAAGTCGCTTTAGGGAAACTTGCAATATACGATTTCGAAAATCTACTGAGTAACTAGCCGGTGGTTGCCTTCTTGCCACTCTGTAAATGTGACTTCCAGCGTCTCGTCTAATGTGGGAAAAACCGTGTGGCGTTCCCCGGGACTGATGCACTGGCTCTACAGCGGGTAAATAATTATTAGTTCCACCGCCGAATATCAGCAGCCTGAGGACTCTCGGTGCCTCTCACTGCATAAAAAGCCTCCTTAGTCTTCGGCGAAGAACGAACCAGGCTCGAGGGTCGGGAGCCTTTAACGCTCCGACAAGTGAACACACGATTCGCCTCCAATTGGGGTCCATGGCGGAATCTCACCGCCTTCATGAGGTACCCGGAGCGCAGTACCCGGTTTTAAGATGGGGAATGCAATAGTAACTACGAAATAAAGAGTTTGCGTACGTGTCGGCACTGTAGATATCCTAAAATGAAACTCAATCCGAGCCTACAATTGTGTAGCAGTGCGTAGTAAGTATCCTAGCCCTCATAAGGCCGAATTTCGTTGGCCACTGTAGTCCGCACAAAGACCAGGCGGGCCATCTAGTACTTGTTTACCAGCTATGGTTCTTAGCGTGTCGAAATGGGAGGATAATAATACCATAGATGATAGGAGATCGACCCTCGTTCATGCAGGAACGTGGCATTCAATTCGTTTCACACGAGTCCTGGTGAATTATCTGAAGGCACACGGTAGCGGTATCATTGGACGCAGGTCACTAACGTTCAGCGGAGAGCGTAGCCCGACGGTTACCCGGCTAAGCGTCTTTAGATCCACCTTCGAAAACAAGGTCTGAATCTAGCGCTTCGGCCGCGTTCTGACAACCGCGGAGTGGAGCCGGTCACGAATTCTATTGGACTCGTCTGCTTGTTCTGATTCGGTTCCGAGGCGTTATGGAAGAGGGGAATATTATTCTCCTTCCGCAATCAAAAGAGTATCCTAGGCCCTAGACCCACCATTTGAGCTTTTCTGATCGAAGATGTGACACCAAGCTGGCCGCCTCGGTTTGGAGCGACTCGTCACAACTGCGTAGGTAGAGGCTGGGTCGTCGATACCACTTGAACTTTCGAGTATCCCTTTAACTATTCGGTTGCAAGTAATGCACCTAAAGAGTTAGAATGACCACATTATTGCCTTCACCGGTCCACGGCACTAGTCAGGTGAATTACCTGCAATGGTCTTGACGTGAGCGAGGTACTAGCAGAACGCCCATGCGAAGAGTACCGCTTCATTTAATCTGGCTATCCCTAAGGACGCTGTTGTGGGACGTGTAGATTCTAGCCCCGACTTGCCAGAAATCAGTCTCTCCAATCCGCAATCACTTATCCAAAGTGCTCTGCGCCGTAGCAGCCGATGTGGTAAGGCGCATGGGCGGCATCCGTACGTGGGGCGTTACACAAGAGCTCAAGTCCAACTCTATATCGTGTTTGAGCACCTCTCCTATTAGCGATTGGACAGACTCGATTCTGTACTCACCCCCTCTGTCTAAGTTTTATATTGAACATGCTAAATCGACATACAAAAGGCGATTTTTAATTGTAGTACATTGAGATATAAATCGAATTCTTTACGCGCCATTAAATAATGCGTTGCGGTACGCTCGTGGAGATATTAAGTTAAACTTCCGAATGAAGTTTTTTCATCGGATATTCTCAGTTATTCGTGTCTCCCCACTCTAATACGAATGACGCTGCCGTTAAGTTCACACCTCCAGCTGCTGGTGAGCCGTTCTATATCACTTGTCGAACCTCCGGATTGCGGGGGTGTTCATGGATGTTCAACCACGCGCATCGCTCTTCCGGATTGGGGCTACCGGGACTGCACAGTCACTAAGATATTCCGGTAGAGTGTAGTACAGAATTGGGTCACGTTAGGTACGCCCAAGCGCCGACCTCATGGTCCAAGGAGAGGCACAACGACCCAAGTTTAGTTCATTTCCACGGATGGACCGCAAACGAGATGAATGAGAGCCCGGGTCGGCTGTGGAAGTTGGCTGCGCTTCCAGATCACACCGGCAAGCGCGGCAACTAGCCTGAAGCCTTTAGCTGTCTCCGCTACCCCAAAATCAGTGCTGAATTCTGATGAACATCCATATAGGACTCAACCCCTTTCAAATAACAAGGGAGGCTCCTCCATAAGCCTGCGATGACCAGAGCGCGATAATTCACATGAAATCGAGGGAATTTGTATTCCTCGCTGCCACTTAATTGATATATAAGCCAATCACTGATCTAGAGTTCAGATTGCGGTGGGCCAATGACCCCTCGCGGATCCGGATCCAACTCTAATAGGACCAAACATCAAGCACAACTTGCAGGCCATTTAACCTGCGGCTGCTTGCCTCAGTATTGGATTGTAGCTTAGTTTCTGCCTGATGTGAGCTCAAACTCGGCGGCGTCCCTGTTTAGTCCTGTACTTGGGCGATGAACCAACAGGACTGCATACATGCGCATTGGGGTCTTTTCCGAATGACAACCATCCATCCCATGGACAATCTGTTCTAATCGCACTCTCAGGCACTGGTAGGCAGATGATGCGGCAATGACTAAGTGGTGTTCTGTGGATGGACAAATGGGAGCGCAGCAGTCCCACCCCGGCCATCATCTTGGACTCCATTTAGTGTCTACGCCCAAGGGTCTAGGGCAAACTCAGCGCGGCGTCGCAGTGCATAGTCCTCGAACGCAATTTCTAATTTGTTCAAGGAGTCAGTAGGTTATTCTGTTGGGCGTGAGCCTTCACAAAGGGTTTTCTGAAGTCTAACAAATAGAGTCATCGTTTAAGTATTCTAATCTTTTCCGGCCGACATACTGAGCTGACCTGATCCTTGTCGGGGTGGGCCCTCATGGCCGTTTTAAGAAATAGCGTTGCGCTCAAACGTTGCAAAACCTGCGCGAACAACCTCCCATTTTTGGTTCTACAGACATTTATTCGCGCGTGACTGCTGGGTAAGAAATGCGACTTCGCTTGCGCGTCCGTTGAACCGAACCGGTGCTTCCCTCGATAGATCGCGGCCTTGGACACATTTGGGCTATAGTCTCTAACGTCTAGCACTTCCCGTGTGTGTGACGCGGCAATTATGCCGATCCCCACCTTGCTCAGCAAAACACCTGGGCAGGACGATAGCGCAGTTAGACTGTGACGTCATAGATAGTGTACACAGCTCTCTTCCCCTGCCAACTTAGCATCATCGACGCTGACCGATCTCTGGGTTGGAAGAATAGACTCGCTATGTAGAGGGCCACGGGTTTTGCTGAGGGTACCGTGGTATCACATCTCTGGGCGATACATTTTCGGAAGTGTCTTATGACCGTCAATCCAAACAACTAAACATTTACGCGGTTTGTGTGAAACGCGGACTTGCATCTCGTAAATTACTGCACACCTTACACCGAGGCGCGTGGAGTCCCCGCGTGGGATACGACATAAGCGGCTTGAGTCACTCTCGTAGAATCTCGTGATCTAAATCTCCGCTAGATTTCGAAATCGGGCGCGTAACACACAATTGTGAAAGATTGGATATAATAAAACTAGCACATGATCACAGATGGTTGATGTACACCTCCCAAATCCCTGTGCCCTGAGGACAATGTCGGTGACGCACGAGAGCAGCATTAACAGGGGGGTATCAGAACAGTGGACGGGCTACAAGACGCTCTTAAGGGGCAGGCCGTGAGATCGATGAGCTGGTCGTCTGTAACAGCTAATGTTCTTCATGACCAGCTAGCGGGTGTCTTGAAGCTTCATTCTCTCATCCGGTTGTGCGTGCGACGTTTGGTCTGATACACCGCTCCGAAAAGATATTTATATGTCGAGGTGTCCGACTAGTCACCTCCTTGCGGTCATTTTTCGAATCTAGGTGAGATAGTAGAACTCTATTAGTAAATATCTAGGATGATAGTACCTATGACGACAGCGAGGCGGAGTTCTATTCAAGAATCCACCTCTGCTCCTGTAAAAAACGTAACCGAGTAAGACAGGCACGAAGTACTGGCAAGCCATGTTCCAGTCAAACCTCTTCATAAACATGGTTTCATACTCAGATGGCTTACGACTGGCGTTTTCCCGGACGCTGTAGATGCATACCCCGGTCGCTTCCGACCATAGCAAGAAAATGACCGACGCGGCTCTTGCGGCTACTAGGCTGCTCGTTTCAAGGTGCGTGCCGCAGGCAGCGCAGCTATTCAATTTCTCGAACAGAATGAGACCAACACATGTTTGTTATACGTACATCTCACGTCCGAAACGGCGTACGCGTGCACGACGGAGTCTCGTAAGATGACTTGGGCAAAACGCATACATGAAGTCTGTTTAGTCAGGTCGACATGCGTTCTAGCCTGGCCACGATTTAAGCGCTACGCGACGCTCGAACACCGCGTAGATGCCTTCAGACTAGGGCATCGTTTGCTTCGTGCTGCCCGAAGGAGGGCCGATGGTACGCAGGGTCGTACGCGACGCTAAACGGACAGCGTAAGTTTCCTGAGCAAAGGCAGACTTGCACCTAGAAAGTGAGGTTAACTTCCCTCCGAAAGAATAAGCAGCGTCTCAATGAAAACTCGAGTCTCTACGTTGGTTTTTGTCTCCTCGTAAGCGATCTTAAACTAGGAGTTTCAGCCCGGCTGGCGCTGATTCCGCAACTCGTTGCCTCGAGAGTGTAAGGCGAACGTCGGTTTCTCCGGAACCTACGACTTAGGGCCTTTCAGTCCGGATGGTACCATCGCTTCCGGAAAACTATCGTCATTTGTAAAGGAGATCGTGGTGCAGGATTTAACCATATTCATGAAAGGCATGTCCTAATCAAAGAAGCTTAGGCCCCCAAACTCTCTCTCGCCGCGCTTTGTTTGGCCGGATAGAGTAGAACAATGCTGCGCAGCACCATAGTCCCAACGTCGTTACGCATCAAATTCAGCACGCTAGTAACATACACTCTGACAAATTCCTGGACCCAGAGCAAGGGTCAGGACGAGCGACTACTTATGTAACGCCCGAGCTGACTCAACTCCGACAATCCTCTATCCCACCGACTCACTCTTAATCCGAGCTATATCACGTTCTCACTCCGTATCAAGTATTGCTGATGAATATTACACTACATTGGCGCTTAAAATGGTACTAAAATATCTACATTCCCAGTATGTTGCCATTGTAAAATACCGTCGTCGAGTCTAGTAGTCGGTGGACAACAGACCCGAAGTGGTTATTAATGTTTTAACGTGGATTATTTTCCTACCAAAGAGTTAGATCTAACACCGTTCCTGGCCGCCAAGTACGGGTCGGTATTGTTAATACACCTCCGCGAAAACTTACCATCTTAGAGACTAAGGTTTACTCTCTTTAATTGCATTACGGTAGGACCAAGCCCCTTATCGTTCGTGCTTGTCGCGAGATACTCCAAATAGAGAAATATGGCCCTGACTCGTTTTGGGACCGACGAACTTAAACCATGCGGAGGCTCTGTAAGAACCGAATTCGCTTCAGTAGGCCCGTGGCTAATCGTAGCCCGCCATTACTCAGACGTGCACCACGTATCAGGAGGCGGTGGATTTTCGGTACACCGACGCTAGGACTAGTCAGTGAGTTTGAGCCTACAGACCTCGCTTCAATCGGATCCCGTAGTGCGATGCCACCTTGCGTACGCTTACTTAGGGACGACCATACCACCGCAGTGCGTTTTCTCGAGAAGCATCTGGTCCGTACGTTCCAGTCATCACGGGTCAACAAAATAGCCTTATTAAAATCAACCCTGCGTCTGATCGGTGGTCAGACTAGCCCATACTTCCTCTAGCTATCGTATACGGCGAATATCTCGCACAACCGTACGATATCGCCGAACTCGAAGATCGCTTCACGGATGCTGACTTGGCACTTACTGACTTCTGAATAGGTTTTACCTATTGATGGACTTCGCCAGTGTCGCGCCGCTAGTCAATGTCATGTTGTTTCCGACAATGCATCGTATGCCTGTGTGATAATCCTGCTCCCTGAGGACGCACAGGGAGGAGCAACTGTGAAGAGCATGCGTCGCCGCTACCTCTAGAGCTAATCCATCTCGGCTTGACAGGAAAAGTCCCCAGATAAATTACGAGGTGTACCATTTCGCTAGCGCTCTTGCCACAGGAGTTAGTTGTATTGTAAGCTACCGCCTTGATACGGAGCCAGCGGGGTATTGCTACTGCCGGGTCGGCTGTCCCGGTCCAGTTCATCACACATGGACAAGGTCAACTTTGAGTGACCATGGTGCCTTGTGCCACTAGTTTATGCAGTGGAATAATCGAGGCTAGAACGCCTCAACCTTAGATCTGTACTCGGCTCACGTGGAGTCGTGTTACTATCATCCTCTAAGATGTTCAAATAGCCGTCTTACACCTGAGATAAGTCTTAAGTATCTTCGGGTCCACCATGGACATGGTACGCTAATTGTCACGTAGTATCCGACGCCACATCAAAAGCAACTCAACGTGGGCCCTCCGGTTTTGTTTGACTACTACACGGTTCCATCGTTTGCTGTACTTCATAATATTGTCTATTGGAATGACAGGCCCTGAGTACATAGCACCTAACGGGCTACCCGACTTTCATTCAGTCAAACTTCGGGTTGGGTCCCGGCTTTGTACCGCCGGTCCGCGGGGTATTGGCTCCCGCGGCATACA$"
#k = 16
#FindLongestMultipleRepeat(text, k)

def EncodeSuffixTrees(text):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	for suffix in suffixes:
		node, done = root, False
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						id += 1
						del tree[node][string]
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
					elif lcp == lstr and lcp == lsuffix:
						done = True
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		#print suffix, tree
	#print tree
	texts = sum([x.keys() for x in tree.values()], [])
	for x in texts:
		print x

#text = "ATAAATG$"		
#text = "ACAGGCAGAGCATTCGGGGCTCCTCTGGCGTAGTGGTTCCAACCGGCGGTATGTTATTTCCTCCACACCGCGTAACAAATAGAGTAGCTTTTACCGTGGTTAATTGCGAAATTTGGCCGACCATCCGTCACTCAGTGACAGTCCGACCCGAAGAATAGCATAAATTGGAACATCCGTTGTCGCTAGCCCGAGCGTGCACACGCCCCAGGCCTCAGATCTAGCCGAACGAGCTCAATTAGAGACTTGGAGCGAGTTGCGTCGACATCTCCCATCAACATGAGGTTACCCCTAGTCACAACCCCTCGACTGGCACAATGTGGCATAGTCCATCTGGTAATTGTTCAAGATCCAAAGCCGTTCTGCATACGGAGCATCGCCAATATCATATAATTACGTGTCACGACAAGCTGCGCCGACTCGTAGTTGGGTCCCTCACGGTGGGATATACATGCACGCATCCCGTCGATCTCAGTTATCCCTGTATTTTTAGATAGCCTGGTAGTGCGCTACTTGCGCCGCACACCGTGTATCAGCTATTAATATCCGGCCAGTAACACTCTAGTCTTTGATGGTTTCATCGGACCGGTCTTCGTATTGTACGCCCTCCCACCCCTGTACTGGTCGTAACTGTGGCAACTAAAAAAAGTCGTGCGATATGCACTTGGAGATGTCATCGAGAACTAACCGACAAGAGGCTCTATTTAGCTTGCAGAGTGCTCGACCATCGCGGTACATCGCGCCGCTAAGGGATAGCCTCCGATGCTCGGTGACGGAAATGATACGATTTAACCCAATTCAAGAGGTGGGGGGGCGCGTGCTCTTTCTTACCTTGCGTCCCTCCGTCGCTGCCGCAAAATCCAGTCGAAGCCACTCACTTACATGCGTACTGAAAAGAGCAGGAAATTAATTACGCCCGTATTTGAAGCCCGAGCGAGTGGCCTTCATTGCGAATACCAACTAACAGTCCCGCTGGTCG$"
#text = "ATTTGGATT$"
#EncodeSuffixTrees(text)

def MortalFibonacciRabbits(n, m):
	N = [[0 for _ in range(m)] for _ in range(n + 1)]
	N[1][0] = 1
	for i in range(2, n + 1):
		for j in range(1, m):
			N[i][0] += N[i - 1][j]
		for j in range(1, m):
			N[i][j] = N[i - 1][j - 1]
	#print N
	total = 0		
	for j in range(m):
		#print N[n][j]
		total += N[n][j]
	print total

#n, m = 6, 3	
#n, m = 93, 18
#MortalFibonacciRabbits(n, m)

from math import factorial

def comb(n, x):
	return factorial(n) / (factorial(x) * factorial(n-x))

def binprob(n, p, x):
	return comb(n, x) * (p)**x * (1-p)**(n-x)

def IndependentAlleles(k, N):
	prob, n, p = 0, 2**k, 1.0 / 4 
	for x in range(N, n + 1):
		prob += binprob(n, p, x)
	print prob

#k, N = 2, 1
#k, N = 6, 16
#IndependentAlleles(k, N)	

def MatchingRandomMotifs1(N, x, s):
	# num n1 CG n - n1 AT in length n string => C(n, n1) * 2**n1 * 2**(n - n1) = C(n, n1) * 2**n, with n1 = x*n, with n = len(s)
	# binomial trial (N, p) with p = C(n, n1) * 2**n
	n = len(s)
	n1 = int(n * x) #round(n * x)
	p = 1.0 / (comb(n, n1) * 2**n)
	print 1 - (1 - p)**N
	
def MatchingRandomMotifs(N, x, s):
	prob = {'C': x / 2, 'G': x / 2, 'A': (1 - x) / 2, 'T': (1 - x) / 2}
	p = 1
	for i in range(len(s)):
		p *= prob[s[i]]
	print 1 - (1 - p)**N

#N, x, s = 90000, 0.6, 'ATAGCCGA'
#N, x, s = 85455, 0.505382, 'GTTAACACC'
#MatchingRandomMotifs(N, x, s)

def bfs(s, alist):
	queue, visited, dist = [s], set({}), {s:0} # fringe
	while len(queue) > 0:
		u = queue.pop(0)
		for v in alist[u]:
			if not v in visited:
				dist[v] = dist[u] + 1
				queue.append(v)
		visited.add(u)
	return dist
	
import re
def DistancesinTrees(strtree, xk, yk):
	
	strtree = strtree[:-1]
	id = 1
	tree = {}
	#pat1, pat2 = '\(?([a-zA-Z]+)\)?,\(?([a-zA-Z]+)\)?', '\(([a-zA-Z]+)\)([a-zA-Z]+)'
	pat1, pat2 = '([a-zA-Z0-9_$]+),([a-zA-Z0-9_$]+)', '\(([a-zA-Z0-9_$]+)\)([a-zA-Z0-9_$]+)'
	pat3, pat4, pat5 = '\(([a-zA-Z0-9_$]+)\),([a-zA-Z0-9_$]+)', '([a-zA-Z0-9_$]+),\(([a-zA-Z0-9_$]+)\)', '\(([a-zA-Z0-9_$]+)\),\(([a-zA-Z0-9_$]+)\)'
	
	done = False
	while not done:

		done = True
		for m in re.finditer(',,', strtree):
			p = m.group(0)
			ul = ',w' + str(id) +','
			#print p, ul
			id += 1
			strtree = str.replace(strtree, p, ul, 1)	
			done = False
	
		for m in re.finditer('\(,', strtree):
			p = m.group(0)
			ul = '(w' + str(id) +','
			#print p, ul
			id += 1
			strtree = str.replace(strtree, p, ul, 1)	
			done = False

		for m in re.finditer(',\)', strtree):
			p = m.group(0)
			ul = ',w' + str(id) +')'
			#print p, ul
			id += 1
			strtree = str.replace(strtree, p, ul, 1)	
			done = False
		
		for m in re.finditer('\(,\)', strtree):
			p = m.group(0)
			ul1, ul2 = 'w' + str(id), 'w' + str(id + 1)
			id += 2
			strtree = str.replace(strtree, p, '(' + ul1 + ',' + ul2 + ')', 1)	
			done = False

		for m in re.finditer('\(\)', strtree):
			p = m.group(0)
			ul = 'w' + str(id)
			id += 1
			strtree = str.replace(strtree, p, '(' + ul + ')', 1)	
			done = False
	
	#print strtree
	
	done = False
	while not done:
		done = True
		for m in re.finditer(pat2, strtree):
			p, u, v = m.group(0), m.group(1), m.group(2) 
			#print u, v
			if '$' in u: u = str.split(u, '$')[1]
			if '$' in v: v = str.split(v, '$')[0]
			ul = u + '$' + v
			#print p, u, v, ul
			tree[u] = tree.get(u, []) + [v]
			tree[v] = tree.get(v, []) + [u]
			strtree = str.replace(strtree, p, ul)
			done = False
		#print tree	
		#print strtree
		matched = list(re.finditer(pat1, strtree)) + list(re.finditer(pat3, strtree)) + list(re.finditer(pat4, strtree)) + list(re.finditer(pat5, strtree))
		for m in matched:
			p, u, v = m.group(0), m.group(1), m.group(2) 
			#print u, v
			if '$' in u: u = str.split(u, '$')[1]
			if '$' in v: v = str.split(v, '$')[0]
			ul = 'w' + str(id)
			#print p, u, v, ul
			tree[u], tree[ul] = tree.get(u, []) + [ul],  tree.get(ul, []) + [u]
			tree[v], tree[ul] = tree.get(v, []) + [ul],  tree.get(ul, []) + [v]
			id += 1
			strtree = str.replace(strtree, p, ul)
			done = False		
		for m in re.finditer('\(\(([a-zA-Z0-9_$]+)\)\)', strtree):
			p, v = m.group(0), m.group(1)
			ul = 'w' + str(id)
			id += 1
			strtree = str.replace(strtree, p, '((' + v + ')' + ul +')')	
			done = False
		#print tree	
		#print strtree
	
	#print tree	
	print strtree

	dist = bfs(xk, tree)
	print dist[yk]
	
'''
DistancesinTrees('(C,D,(A,(B)E));', 'A', 'B')
#lines = read_file('inp2.txt')
lines = read_file('rosalind_nwck.txt')
for i in range(0, len(lines), 3):
	strtree, (xk, yk) = lines[i], str.split(lines[i + 1])
	DistancesinTrees(strtree, xk, yk)
'''

from math import factorial, log10

def IndependentSegregationofChromosomes(n):	# multinomials

	prob = {i:0 for i in range(2*n+1)}
	for x0 in range(n+1):
		for x1 in range(n+1):
			for x2 in range(n+1):
				if x0 + x1 + x2 == n:
					prob[0 * x0 + 1 * x1 + 2 * x2] += (factorial(n) * (0.25)**x0 * (0.5)**x1 * (0.25)**x2) / (factorial(x0) * factorial(x1) * factorial(x2))
	#print prob
	cumprob = [0] * (2*n + 1) 
	cumprob[0] = prob[0]
	for i in range(1, len(cumprob)):
		cumprob[i] = cumprob[i - 1] + prob[i]
	#print cumprob
	logcumprob = map(log10, cumprob) #map(lambda(x):round(x,4), map(log10, cumprob))
	print logcumprob[::-1][1:]
	
#n = 42 #5 #42
#IndependentSegregationofChromosomes(n)

from math import sqrt
def GeneticDriftAndTheHardyWeinbergPrinciple(probs):
	print map(lambda(x): 1-(1-sqrt(x))**2, probs)	# p(Recessive individual) = x = (1-p)**2, p(At least one recessive allele) = 1 - p**2, p = p(Dom allele)

#lines = read_file('inpros.txt')
#lines = read_file('rosalind_afrq.txt')
#print lines
#GeneticDriftAndTheHardyWeinbergPrinciple(map(float, str.split(lines[0])))

def WrightFisherModelofGeneticDrift(N, m, g, k):
	#prob, q = 0, m / (2.0 * N) 
	#p = 1 - m / (2.0 * N)
	#for i in range(k, 2 * N + 1):
	#	prob +=  (p ** i * q ** (2 * N - i)) * factorial(2 * N) / (1.0 * factorial(i) * factorial(2 * N - i))
	#print prob
	prob = [0] * (2 * N + 1)
	prob[m] = 1.0
	sumprobs = []
	for gen in range(g):
		nprob = [0] * (2 * N + 1)
		for i in range(2 * N + 1):		# current generation has i dominant alleles
			nprob[i] = 0
			for j in range(2 * N + 1):	# past generation has j dominant alleles
				p = j / (2.0 * N)
				nprob[i] += prob[j] * p ** i * (1 - p) ** (2 * N - i) * factorial(2 * N) / (1.0 * factorial(i) * factorial(2 * N - i)) 
		#print prob
		prob = nprob
		#print prob	
		sumprobs += [sum(prob[:2 * N - k + 1])]
	return sumprobs
	
#N, m, g, k = 6, 9, 4, 5 # 4, 6, 2, 1
#print WrightFisherModelofGeneticDrift(N, m, g, k)

from math import log10
import numpy as np
def TheFounderEffectandGeneticDrift(N, m, k, A):
	#logprobs = [[0 for _ in range(m)] for _ in range(k)]
	B = [[0 for _ in range(m)] for _ in range(k)]
	for i in range(k):
		B[i] = [log10(1 - p) for p in WrightFisherModelofGeneticDrift(N, 2 * N - A[i], m, 1)]
	print np.array(B).T
	#print len(B), m, k
	#print zip(*B)	

'''
lines = read_file('inpros18.txt')	
lines = read_file('rosalind_foun.txt')	
N, m = map(int, str.split(lines[0]))
A = map(int, str.split(lines[1]))
k = len(A)
#print N, m, k
#print A
TheFounderEffectandGeneticDrift(N, m, k, A)
'''

def WrightFishersExpectedBehavior(n, probs):
	return [round(n * p, 6) for p in probs]

'''
lines = read_file('inpros17.txt')	
lines = read_file('rosalind_ebin.txt')	
n = int(lines[0])
probs = map(float, str.split(lines[1]))
print WrightFishersExpectedBehavior(n, probs)
'''

#solve(matrix(c(0.1^2, 0.1, 1, 0.5^2, 0.5, 1, 0.8^2, 0.8, 1), nrow=3, ncol=3, byrow=T)) %*%(matrix(c(0.18,0.5,0.32),nrow=3,ncol=1))
def ChromosomesDetermineSex(probs):
	print map(lambda(p): 2*p*(1-p), probs)	# p(Recessive allele) = p = (p|M) = (p|F), p(Recessive carrier) = 2*p*(1 - p)
	
#lines = read_file('inpros1.txt')	
#lines = read_file('rosalind_sexl.txt')	
#ChromosomesDetermineSex(map(float, str.split(lines[0])))
		
def ExpectedRestrictionSites(n, s, A):
	k, B = len(s), []
	for i in range(len(A)):
		x = A[i]
		prob, p = {'C': x / 2, 'G': x / 2, 'A': (1 - x) / 2, 'T': (1 - x) / 2}, 1
		for i in range(len(s)):	p *= prob[s[i]]
		max_times = n / k
		print max_times
		exp = 0
		for time in range(max_times):
			exp += time * binprob(max_times, p, time)
		B.append(exp)
	print B
	
#n, s, A = 10, 'AG', [0.25, 0.5, 0.75]
#ExpectedRestrictionSites(n, s, A)
	
def FrequentWordsProblem(Text, k):
	counts = {}
	for i in range(len(Text) - k + 1):
		kmer = Text[i:i+k]
		counts[kmer] = counts.get(kmer, 0) + 1
	maxcount = max([counts[kmer] for kmer in counts])
	print ' '.join([kmer for kmer in counts if counts[kmer] == maxcount])

'''	
lines = read_file('inpros37.txt')
lines = read_file('rosalind_1bba.txt')
Text = lines[0]
k = int(lines[1])
FrequentWordsProblem(Text, k)
'''

def ReverseComplementProblem(Text):
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
	return ''.join([complement[x] for x in Text])[::-1] 

'''
Text = 'AAAACCCGGT' 
Text = 'CCGTTCCTTCAGATGGCTCTGGCCTGGCAACCGAATTCGGTGGCCGAGTTGAAACGATCGAGCAACTTAGCAGTTAAGAATACAGAATACGGAGCCTTTACTCGGGATGGCCCGCGACGCTAACCGCTGTGTCAGCGTGATAGCAGATTCGCGTTTGACGATATTGAGAGTGTCCTAACCAAATATAGTTGATGAGCACTCGGGGGATCAACCCCGGAGATACCCGCCATCCCTATACATCACGTTGACTGCCTGGCTGATGTGCCTGGACGCGGCCTCGAATTGATATCCCGAAGCGGAGTGCCAACGTACCTCCGAAAATACGCTTGGTTGACGCGTAGGCGGTGGTATTGCCCCTCTGGTCCCCTTCCCTATAGCGGTGGCTGGCGCGGGCGCTAAGACTATGACGTAACACACCTGTCGAACTGCTCCAAGATCAACGATGAACAGAATGGCAATCAAAAATCCCCGACCCTCATTCCGATCTTTCTGCAGGTTGTGCTAAGGGGCTGACAAACTTGATCGGCAAAGACTCCTGGCCTTATCACCCAACTGCCATTTAATTGGATGCGAGATGTCCAATAATCGCGGCCCTCCGGAATTGATGCCAATCAGCTCACCCATGATTCGCGATCATGTACTACGTATAGTATAACAGAAAGAGCATTTCTTCGGCTGCATCGTGTGCGGTGAGATGATGAGCAGCGTTACGATGAAACGCAAGATGTGTGAAGGGGGGTCAGCTAATACAAGCTTATCGTACAGTCTCGTCCCGCGCAGGAAAGGACGCAATGAAAAATTAGCTTTCGGCACGCGACGCACGTAAGGAGCGACTATTTGACTGGAGGATTTCCAGCTTGGCCAGATCGGATCGGGTTTTACTACGTAAAAATGACACGAATCATCGGTGGTATGGGCCCCGGCGCACAGTTGATCCGAATGTCTATGTAAGGGGCGCGTTCAAATTTTTCACGCCGGGCATAGGCTTACTTCCTATAACAGCAACTACCATGTGCGAGATTTCAGTATTATGATCGCGTTGCCGCTCATACCCTGGGAAGGAATAGCATATTTAAGCGATCTTGCGCTTATTCTGCCCAGTCACCAGAATCATCAAAAGCCGAAAGGGAGCTTGTCGCTACTAGGCGAGTGTAAGGAGAGTTCCGCCCGAGAGGATGTGCGCCATTATGGTGCCTTCGTATGACAGATGGTACGTCCCCGGACTTTTATCCTGCGTTTTAGACCGCTTGATTTAACATGGACTATAGTACGAGTGATACTTCCGTATAATCGCCCACTGTAAGTGAATAATTAAGTTTTCCCTGAGTATATGCCGATGCAGAGGCCCCTCCAAAAACTATCTTCGCTGTATACGGAAGCCCCGTGTGTCCGAAATGTTATATAAAGACTTCAGGAGCAGCACAGCTACATCTTCTTGTTAATAGTGTCTTTTCCGACCCCGCGAGCGAACCCAAGTAAGGAACAAGAGTTATCGATCAAGTTCCATCGGTTTACTTTAGTGACCCAACTGTTGAGGCACGCCCGAATCTGTACTCTACGCGTCGTGCAGCGATCTAGTGACCGGCTTATGACCGTGTAAGGCCTCTTTTATAAACGGCCTATGACTCAGAGTATCTATAGACATAATTTCGCAGAGAAATGATTGAAGAGTCCGAATAGAGAAGATGTAAAAGTACGTACTACGTATCAATGTCCCATTTATTATACTTTGAGAGGGGAGGGGATACCGGAGTAAAACTCACCACAGGGATAAGCACGCGCACGCAGTAACGTACTCACTCGCCGACTTGGTGCATGCCATGTCATTCTCAGGCCCGTACAGCCTCAGAAGTCTTCAGGATATCTCTTGTCGCGCTTGAGCGCGGGGCGACCCCAAGGGACATCCGGTCGTGGGCCCCAGGGATGACGTAGACTGCTCCATATAAATTTATTCTCAAGACTGCTTACGCAACCTGAAACCATTATGGCAGCGCCTCGCCCGTCATAAAAGCAACCTCAAGCAATCTTAGTACGTGACTAATGGGTCACTACCCGCCAATAGTAGACGCCTGTTAAAAACGATTATTGGAGACTTGCCCGTTAAATATACATACCCCGGAAAGCGCTGACCTCCGAAAAAGTGTCTTGCACCACGCACAAAAATCAGGAGGGGCATGGTTTCATGCTCCAGACCGCGCCTTGGTTCTCTGCCAACGTGTTAGTTCTAATCAACCCAATTAGAGTCACTAATGATCGTAGATTTTACTAGTCACTATCGCCCTGTGATGCCAACATACACTAATATGGATGACGTCTCCACGGGGCGCATGCTTAGACGAGACGAAGTACAGAGCCAGCACGGGGTCATAGCGTGGTCTCCAAGCAACTCCTAACCCAATTAGGCATTGGTGCACAGAACTTTTCTAGCTATACGCACGCAGGAAGATCTCTTCTATTCCCACATACCTGGCCACATCGTGTCGAGTGTGACAAGTAGCTAGCGCGGCCCGCTGCATCTGTATGTTATTTACAGAACGTCACACTCTTAAAAGAACCAGTGGTACTTTACCCACCGTTACCCACATAGGTTCTCAGCGAACGGCTCCTTCCACCCCAAAGCGCCAGCTCTTGTAGGAAGTTGCCCCATCCTTACGATTGACCGGCTCCTATAGACGCATCGCTAATAGGCATTGAGGGTCGCACGGGGGATGGTGGTAATGACTCACGCCTGAGATGTCGGGCTAATCTATGCGCCCATACATACGGATGAAGTCATAGCCCTCGTCCCAACAAGAGCCACGCCGACCGCGAAAGTCGCAGGAAGTCCCTTCTTGAGCACGCATAGAGATTCACCAGCGACGCAGGGTCAGATTAGGCGCGCATAGGTAAGAAGCCGTGCCCAAGCTTACAACTCTCCTATGTTCGAAACTCTTGGGGCCGCGAAGGGCGCTTGGTCTGGTCTCTTCTAGTGCTCCAAGGGGCTTGTGCGCACTCCCACGGGTGGAACAATCGATTTATTGACCAGTCGCTTACTTACCCCCCCGGTTAATGTACAGAAATCACTGGATAGAGGCCTCTCAGACTTCTATCTTACCTAAGCACTAACTATTGAGGTAACTGTTAGTCTAACGGAGGATCGGGGGTGGAATGCCAGTAACTTCGAAATCCAGTTGAGACTACCTTTTTTAAGGCCTCTGCTTCGCATTGGTTCGATTCATTTTGACAAGGGACTGGAGAACCCGCGGTGCGCTATAAAGGTAAGATGTGTCATACTTCCTGTGGAGGATCGGTCAATCGGTCCTGGCGTCTGAAGCCATATAAGAGCTAAAAAGCTTTAGCTCGTTTGCCCTCACGGTTGGAGCTACCCCCGTGACGCGACATGATGTTGCGTATGCCTTTTTGACTGGCCTGCGCATTCCAGCCTAAGCAGATCGCGCGATTAATCGGTATACCCTGCGCAGGCTCCCCTTTGTACGTTCATGGAGTGTAGAGACTTAGACTGTCTTATTGACTGAACAATCTTTGCGTCCGGGGTTAGCCACAAGTTGTAAATAGTAACTGGGCCCAATCGATACAGAGATACAGCCATCGATGAGAGGAAGAAGCCTCCCACGACCAGATCTCCACTACTAACTACAGTTGGCTTGGCGAGCATCGGTTCGACCGAATGCGGGCATGCTACGACGCGCGCCCTCGCTGAATCTATTTGTGCACCTGGCAATGTATGGCTGAACAGGAGCGTCTGGGCGGATTAGTCCGGACTGTGGAACGAATCGCCTTTAGTAAGCAAAATAGTCTGCGAAATTGGCACACGACTATAGAATTAGCGGAAAGAGCGGAAAAAGCCGTAACCTTTAGAATTACGCGCTAACGCATGGCGCCAACCTAGCTCGCTACTGTGACGTTAGAAAAAGGTTATGTATACCTGGCTCTACGAGGGTTGTAGCACTGTACAGACCGTAAAAACAGGGCACGCCCGACCATAAAAAGCGATCCAAGGGATCGTCTATGCCTCGGCGCGGATATCAGCAGTTATTGTATAGATGCACCAGTTGCCTCATGGCCTCAGGACGGAGGTTTAATTACTCTAGATATAGGGTCCCGCACAGAGCGACCGGATTCATTTGACCTATCCGTTGTGCTATATTCTTTAACTAGCGCATGCTTCGCGGCCGTCTTTCGTAGTTGCGGGTCGAGGGAAACCCCCCGTCGCGAGATTTGGTGTAATAGTAAGCTCTTTACAAACAAGGGGCAGACTGCGCTCCAACTTATCGTTCTTGCGCCTGGAGTGCCCAGTTCTTTGCCCTGCAGACCCTAACCGAACGCAAGCGGAGGTGTCTCTAAGGGCTTGCCCAAAAAATTGTTATCTTGACTAGATAGTTCGGGTTGCTGCAACCGTTTTCGTGAGTCCAAGGAGGAGCAGGGGTTCGCGCCTCCGACCGGTGCGATTCACCGGCAGAGACCCAGTCGTGCCCGGGGTGACGGTTCCAGCGTGGTCCTTCCGAGCCATCCCTTAGCGGATTTGCGAGAATAAACAGCTTAGGGAGGGGCTCTGAATCTCCCAGGATTGCTAAAAGTATTGAGGTTCAGCCATGCAAGTCTCCAACTAAATTCTGGAAGAGCCAAACTCTAGAAATGCTCCTACATACAAAGAAACTGGCGGATCGTAGGATCATTCACTACCCTTTTAACGTACGAGGGGCTGTGAGTAAACGATAAGTTAAGTCATCTGTTCGGATAGAGGCTGAACTGACGGGACACAGTTGCAGCACGGCCGTGAGGCTAACGAGGATATGGGTATCTTGAAAATGAGGTTCCTTATTCTCGAGACTGCTTCAAGACTAAAGAATTATTACTGCAGTGGTGATCCACCTCCGCTTTATGGAATGGGTCCTCGATGCGATCATCTGGGGCCATTAACGTTAATAGTGTGATGTCCAAATCTTGAGTGGAGAGGGCTGGGGGGAGTTATTGGACATTAGCTTAGATCCTCTTGGGCCCAGAGCAGGATGGAATTTAGCCAGCCCTCCACCAAAGGCTTCGCTATCCACGATGCGGACCCAACCCCGTTACGGCCCGCATCCGCCGAACCAAGCTTTCGGTCCGCAGCGTTTATTGAAAGAACTTTATGCCGTGTGGGGAGTGAGGGACCCAGATAAGCTTAAGTAATGGTCACAGCGAGAGGAACCATCATTTCGAGTTCGTCGGGCATGACGTCTAGAGGCTGCACACGCACTCCGTAAATTAGGACCGGCACTCTTATACGCTCGCTGCCGATTCGATCATCTTTGGTTCGTGTCCGGTACCGAAAAAACTTTTACAACGAAATAGACATTTTCTCCAGCCATTACACGACGTCTTTACAGCCGCTACGTTGACCTTGCGCCAGCTAGTGCGGGTAAGGCCGGGACTGACCGAACGTCTCTGACGGAAGTGGGTGCTAACAATTCAATATCGTGCCTCCGATCATCTATGAGATGATAGACAACGATGTCGAATAAGACTGTTAGAAGGCATTCGGCGAATTATTCTACCAGTGGGACATGGAGCCTACCTGGCTATATTACGGCTGTAATTCAATTAGGGCTAGTCCATAGCAAGCGTAGGACTTTACACTAAGCAGATTTTTTATTCCTCGCCTGAACAGATCTGATGTTCAGCCTAGTCGGACTGATAAATGCGCAGAGACGGGTATTGGAATGCATCGCAGTCCTTTATAAGCCTCGCTTCTCGAGAGGCGGACTCTTGAGTGGACAACCTGACAACCGCATAGCCCAGGACGATGACACGTGTTTGTAGGTTTGCTCAGGAGCAGGCGCCTTATGCCTACAATCCGACTGTGATTACAACCATCATGCTTCCCTGTCCTGCTCAAGCGTGTGATTGATTCGTTGCGTTACGTACAATGGTAAGGATCGCCTGCCATGCATGCTCGCTGAGGACGGCGATCCCGCGGTGCGACGAGTCGCCGACCTGATTTAGAGAGGAGCCTCCCGTTCGGCCGCTACCAACACGGAAATTCTACATCATACTTCGTAGATCTGCTATAACATGCTCAGCAACCAGGTGTGTCCATTGTGTGAGTTCGCCCACCGCGGGTCTCTCAATTGTCCACTGATGACCATAATCACCTAGTGTATCAACGTACCAGCACTTGGTCGCAAATAAATTCGCTGTACCCGTGCTCTAGGGTGCAATCATACTTATCACTTCTTAAGGCATATAGGTAGCAAGACAACTCAATATTTTGGCATTGTTTATTATCAAAGATATTACGTCAGTGTTAGTGCATACGTTTTTGAGCGTAACACCAGCGAAGTGACTTCCTATCCATGTGCTATGTCACTCAGTCCGCTGCGTGAGTCTAGGGCGAGCATTACATGATTGCGATGCCCTAAATATGGGTATAAGGGGACCCTCTTAAATTCTGAGAGAACCCATGCCTACGAGCGAGCCCATATATTGATTAAGACGCGACAGCGTCGATGGCATCACCTTGAGGCGGGGCAGACATAGCCAGCTGTTTTGCACTACCCGTGTTCAAGGATAGTCACCACCCCGGGACCCCCACATCAACATGGTCTACGTCAAGCTCATATTGTATCTAAGTTTTAGTTGGCTGGCGTACGAATGCAATATCTTGGATGCCAATAACAGTTTACCCCAAATTTACGAGATTGGTGGCGCCTGGACAAAGCTGCGTCAGCCTTAGCAGACATGGTCTATGATGATTTGGACCAAGAAGGGGACGGATATACTATGCCCGGGGATACCTGAAGCGCAGACGTTGGGATCTCTGCTATTTAGGCGGCGAACCTTGGGTTTAGCATATTCCATAATCACATATAACATAATACGATGCTTCTACTAGCACCGCGCGGCACCCCTATATATCCGATTTCAAGAACTCCTATTAGTAATGCTAAAAGTTACGACTTGGGATTAATGGCGTGATTACCTCACCCCATCGTGTCTTTGTATAGCGTAAGCCCCGTACGAGTGAGTAGGTGGGTCTAATTCGCGGCTTGCAGACATCTGAGGCTTGCACAAGGTACTCGCGGTAGATTGTTCTTGATATATTCCGGATAGCCCGGTGTGGGCCCGATCAGGTTGCACGGCAGATCTTAAAGTCAGCAACGTGCCGGCGAAATCTCGAGCAATAGCTCCTTTGTTGCTTATACTTAAAGTACTGGGAGGATTCTAAGCTTTGCTGCGTAGAGCGTGCAGAACCATGTCGAATAACCGTACCCGTCTCGAGCGATGAAAGCCCGGGCGTTGCACGTCGAAGGGAACTATGCCAACCTAGAGAAAACGGCCTTTAGCGTCTCTAGCTTTTGAGCGTCAGAAAACAGCGACGCAACCACCGCAGGATCCCCATCGACTGGGGTTGCGACCGCCCGCATACTACTTCAATACGGGGAGTCAAGATGTTGTCTCCCCTTAGAATGGACTACGGGGACTTTTAGTCCCGGTAACCCTGAATCGGTTTTATATCACTGACTGGCTGTTTCCTCCTCTTAGCGATCGCAACACCGGTCGAGCTGCTATCTTTGCTCAATAACATATTACATAGACTGCGAGATAAGTCGTCCATAGTAACTTTCACCTGTGGGTATCGAGGGATACACCGATTAACACAGAACTTTCGTTGATCGAACTTCCCTTGCATAACCCAAAGGCTCTCCCAAGCATATTACAACCTGAGTGGGTACGGAAACTAGCAAGTCCCAAGGTAAGAACAGGGACAATCTGCATCATGAGGATCCACGCCGGTGCCAACTCAGAATCTATTAAGCTCTGATTAAATCGAGTGCATCCCGGGACAGGTGGTATTTTAAGAGGTGCGACTTAACGTTTAAGCGGACGAATGGGGTTCTTTTCTCGGCTGTTGCTAAGTATTTAAGCTAATCTATACTCCAACGCCTCAGACGACCGGTCGCGCTATTTTTCTCTTAATAACAATAACTCCATGGAAAAGATGTACGGGTACTGGCGATTTGGGAAGCATGGTACCGCGATGATCAGGTACGTTTGGACTACTGGAAGTGCCGCTGCCATCAGACTGTTATTGGGAGATATGTGGCGGCAGATGAAGGAGGACGCCGATGACAAGCGCGAAAGTCTATTTTCTTCTAAGGAGCCTGTATGAGTGTTCAATATCCCCCCCATGTTGGCCGTTCGCTATTTTAACAAGGATTCTCTCTTAGGTAGCATAGACTCACCTTCTGTAAACTTTAACGCACGCGCGGACCATATTCAAGCCCGTTGTCATTGAGACTGGGTCTCCGATAGACAAAGTGGAGGTCGGGCACATAACGGTAACTCTGGGCTCATATATATTACTACTTGAGAGAGGCATAGTCGCTAGATACTTACTGAACCAGGGTGTACTCATAGGCGGAAAGACTATTAAAGTTCAGACAAAGATTGAACCGGGGGAGAGTGCCTTTCCGCTCGCGAACGGGAGAGCATTAAATCGAAAATTACATGCCTTCTAGATAGCGTGTGGAACGACCCTCAGAGCCGAGGGCCATCCCTGCTGAAACTTATAACCGCCCTGCGGCCGTCGCCGCTGGCGTATCATGTCCATTCCCGATTACATTAACATGCCACCACCTCGCGGGCGAGTTTCCACTCTTTAGTACGGAAGAGGGTCTTTATAATCGCTTGTGATCCGTGCCAGAAAGGCTGGGTCCGAATTTGCGATCGTTTTGCCGTTCAGCTAAGTACGCCGCAGGGTTTAAGAAATGACCAACGATCTCGTAAGCTGCTGGGCATTCGGGGGATGTGTCAATGATCGTACCACGTTGCCTATCGAAAGGCATCGGCCACGCGCGACTCGCGCCCCGCAAGATCCTACCACACAACCACCACGTTAACGGGACGACAAAAACCTCGGGTGGGAACTGTTTGCAATATGAGTACTGGGCCATCCGGCAAGTGCCACTGGTTGTCGGCGCGGTACGCGATCGAGCTGGAATTGCGCCGGGCCGCGATTCGAGGATCAGTGACAACCCGATACAGGATGCGCATTCTTCCTAATTAAAGCTCAACGCTAAGCGAACAACTGCATTAGTAGGCATTGCGTCGCGAGTAGTTGAACAGTACTGGGCCGCGCCTGACTGCACCCGGCACTACGGAGGATCCGCTCAAGAACGATTACTCATAGGCTTTGCGCAGTCAGTGGCGTTCCTTTGCGAGGCATTTGTCACCCCATTCAGTCGCATTCATGTCTACGGACATCACGACCGTCACGTGAGAGACTCCTAAGCCACGCCATCCGTGATGGTCTTAATGTGCGTAAGATTGGCTCTTGCCAAAATGGACGTCGGGTCACTCGGCGACATTCACGCTCTGCGTGTCCTTGGTTTCCACCCATCCGCCGAACCAAGTTAATCCGTAAGCCTTATAGGTATTAGACAGTCTGTTGTGGTCAACCTTGCCGGAATAAGAGTAGCCTGTTCCGCCATCGCGGATGTGATGGGCTCGAGCTCGGGAGAGATGCCAACTACCAAAAAGTGATCCGAGAGCAATTGCGGTTACATTATAGTGGGACGATGCTGTTGGGCTCATCACTCTGACGATCCAGGAATCAACGTTCTTCACTGCT'
print ReverseComplementProblem(Text)
'''
	
def PatternMatchingProblem(pat, Text):
	m, n = len(pat), len(Text)
	pos = []
	for i in range(n - m + 1):
		if pat == Text[i:i+m]:
			pos.append(i) 
	print ' '.join(map(str, pos))
	return pos

'''	
#lines = read_file('inpros38.txt')
lines = read_file('rosalind_1dba.txt')
PatternMatchingProblem(lines[0], lines[1])
'''

'''
lines = read_file('inpros84.txt')
lines = read_file('rosalind_ba1a.txt')
print len(PatternMatchingProblem(lines[1], lines[0]))
'''

def ClumpFindingProblem(Text, k, L, t):
	clumps = []
	pos = {}
	for i in range(len(Text) - k + 1):
		pos[Text[i:i+k]] = pos.get(Text[i:i+k], []) + [i]
	for kmer in pos:
		count = len(pos[kmer])
		i = 0
		while i + t - 1 < count:
			if pos[kmer][i + t - 1] - pos[kmer][i] <= L:
				clumps.append(kmer)
				break
			i += 1
	print ' '.join(clumps)

'''
lines = read_file('inpros39.txt')
lines = read_file('rosalind_1eba.txt')
Text = lines[0]
k, L, t = map(int, str.split(lines[1]))
ClumpFindingProblem(Text, k, L, t)
'''
	
def MinimumSkewProblem(Text):
	numG, numC, skew = 0, 0, [0]
	for i in range(len(Text)):
		numG, numC = numG + (Text[i] == 'G'), numC + (Text[i] == 'C')
		skew.append(numG - numC) 
	minskew = min(skew)
	print ' '.join(map(str, [i for i in range(len(skew)) if skew[i] == minskew])) 

'''
Text = 'CCTATCGGTGGATTAGCATGTCCCTGTACGTTTCGCCGCGAACTAGTTCACACGGCTTGATGGCAAATGGTTTTTCCGGCGACCGTAATCGTCCACCGAG'
Text = 'TAGAGTTGGTCTATACCCGCAAGGCTGGGCACCAGGGATGGTGGCTACTCCTACCATGACTCCTACCGGGTAATTTGGCCGTATTGACTCGCACCACTCACCGCAAGCCATAGCCGCAATCCGTGTACACAGCGACCAGTCATTCTTGCTCCTATGGTGCCACCGCATTCGCTACCTTGGGGCCCTTGTCTCGGGTCTAAACGGGGTAACTGGCTCGGGGGAGAAATTAGGTCAGGACTACAACACTTGGTCGAAGCAGTTCCAACCACAACAAAGTCCACCATATGAAAATCAGGCGAGGGCTAAACACAGCGGTGTTCGCGTCGAAAGGTTGGAAATCTCTATCAACATGCGTCAACCCTCTACGAGGGGTCAAGGTTTGTCTAATGCCGTCGTGCGCCAACGGCTTAGCACCGCGCAGAGGGTTAACCATAGCGACTATTTGCTCATGACTCAGGCGTCAGATCAAGATAATCCGACAACCTCGTGTATCCGCGTGCCTCGAAGTTCCACGCTTCCTAATCAACAATGCTCGGCACGACCTAATACCGCAGTATCTGAGCGTTGGCGCCATCTCGGGAAATGCTAAGAGCAGAATGTAAATGGTATACGGGAGACAGGGTTTCCCTCTTCTTTCAGGAAGCCGAGGTGCTGCGACGGGTAACGGATTGGGCATCTTAGCAGGTATATACGATAGTTTGCATAATGCCCAGCGTAGCCTCACCCTCTCAGGGAAACAAAGCCTAATGCACTCCTACAGGTCCTCTTATGGTTTGGTGCGCCTCCTAGACTATGTAGCGCCAGGTAAATATTTATCTAGGTAGATCATCTCCGGCCCAGGTCGCACTGCGCAATCTCAAAGGAGCAATCAGTTGGTTTCCGCTCGAGAGTCAGAGCGCCCATTAGCCAGAACGAAGCCTAAATCACTTGAGTAACCGAGGGCGAACTCCTCGCAGTATCATCGCCGTAGCGCGATATTACTCTGTGACAGTTCATGCTGCCTTGTCGATGAACTATAACTGCCTCTTTCCACCCCTTTGATATGCCGCAGATTCTCCTTCTCGTCAACCCAAACCTATCCGCGCGGCTAGTTGGAGTTTGCCATAGAAAGCGCTTGTTGATCCTACCTCGCCCATGTGCTAGACGCGATGTCCGTCACATGTACTGTAACGGCGGAAAATTGCAGGTGGCGCTATCGGGCTCAGAACCACCTTTTAGGCTCAACCCCTCTTCAGTTCTCCTTGTCATCCTCCAAAGTAAAACGTATGGTGGGGAAATCCACCGAGTTGAGCTCGTCACATCTACGGTGTACTCATGTTTCATCCGATGTTAGCACACGTACACTACCCTCATTTTAGGCTCCGCGCTCTTGCTTAGCCGCTCACTACTGGGAGTAACATGTCCAATAGGGCATATCTAGAAGGATCGTAGTACTGGGTGAGTTCCGGTACATACGGAAACCCCCGCCCTCTAAAGGGTCTCCGTACCACAGTAGCTTTCCACCCGCCTTGGAGAGATCCCGGGGGGATATACACTGCTAGGATTAATGATGACCACTAAGAAGGTCGTTTTGAACGACAGCAGAGAACTTTCCTCCGCATATCTGTACGCGACATGGTGGTAGCTATCGGTCCCTCCATAGTAGGATTTTACCACTGTAAACCAACGATTCGACAGGAGACAGGAAATTAGTGACGCTCCGGCGAGATGTTGTCGAACTTACGCGACCAGGAGCTGGTCCGGGCGGCTGGGTCGAGTGATTCATAAGACCGTTCTTGTATTCGGACATCGAGCAAGTCGAGCCGGATTGGCTTATACCACCGCAGCCGCGGCTCCTGGCCCCGCAAAGCCATTGAACCATAGTAGTATGTTGCAACACTACCGACAAGCCTATGGGGGCGAGAATTGGCACGTCATTCGCCTCTGCGACAAAATCAATCCAATCAGGGCGACACACTATCATAAGTCCAGAGCAGATCTACTAAAGCTAAACAACTGCCAGGCACACCCCCCTAATCACTGTCCCAATTACATTCAGAGTATCACCTCGCTTAATCTACGGAGCCCATGGATGGTACCACTAAAGCCCGGACTAGCCTAGCGGGTTTCCCACGGATCCGGCATGTAGAAAGAATCCGCCACTTGATCAGTATAGTATCGCAAAAAGTCCCAGTTAAATGTCTTGAACCCCAAACTGTGGTAGCTCTGACGGCGTAACAGACGGGAACGATCAGCTGAGTCGGGTAAGCAACGCACTTCCCCGGTACGCGTGAATCCAGAGTAAACTCAAGACTCGGAGCCTAATCCGTTCCGCTGTTTTACCAGGTGGTCTGGTAAGTTTTGCCGGCTTATCCTGGCTGACAGCGGAGTCCACGCAGCTGTCGTTTGATTTCTCGAGATTAAACAACCGGATTGGTATCGCTCTTAAACCTTTGCCAATCGTGAATTTTTGAGGTTCGAAACTCCGTAACGAACCACCAGTCAGCTCCCTAAGGTTGGTCTAGTAATGTGAACAATCGTAGGGAGAAAACAGCTACGATCCTAGAGCAGCGAACATAATCAATCTATAGCAGTCCTCATTATTAATACGGTCAGTTAATCGAGCGCGAGACGTCAACCCTAATGCATGCAAGGGAGTTTTTGACTGCTGCTTATACACCACACTCATCAACTACAACAAGCTCACCTTGTCGTTAAGCTCGTACTGCATAGGAGGATTCATTTCATGAGGAATCTCTCGACGCAACGTTTCCCACCTCTTTACTGTGCGGGATCGCCGAATCCGCTTCCGTTCAGGTACAAGCTATTGTTGCTCAGACGTGAAACTATGCGTAATGCTCTTGAGTCAGACTCGTGTAAATGTTCCTCCCTAAGCCATACCCACCTCCATCGTTCTCTGTTCTTCAGAAGTTTACTACCTGAATACCAGACTATACGACATCGTAACGGCTAGATGTAGCGTCAGGGGAACCTCTCCCGCATCGAGTAACGGGTGGGCGGGTACGCTGGCAGTCATATAAAGGCTAAAACCTAGATACAAGCGAACGTCACTCGTCGGCCATAAGTCTTCCCTCGTCTCTCGAGGCATAAGCAAGATTTCAGGTGATCTGGTAATCAGAGCCTCCATACAACCTCGCTAGACGCGCGAGGATTATGACTGTATGATTCGTTGTTAGGACAAGTTACAATTGCGCTGGTGCACACATGAGTCGCAAGTGGCAAGACTGGTTCTGGTTGCTGTAAGGCTGCCAAGGATCCGGTCGACTGAAGGAGGGCGTAGTAGCTCCTTACGATCCCCTTCCACGTGGGCTTAGTAGTTCGACTAGATTAGTCCGACGGCTCAGTCATATGAGGTTGGGCGTTATCATGATCCCGCTTTTGCCTGCTGGCGGGGCGGGTTAAAGCAGTAAATCAGCGCGATTTTCCTCAGATACAGATTTATTTCTTGCTCGTATTTCTCATATCACAGCGTTTGATTCCATTCCAGCTCGGGTACCCATTCCCAGGCATAAAGCATCGCCTGTGGGGTTCTATGGTTGCGATTTGATTGTACTCTGAAGCAGGTGTCAAGACATTTTATATTCTTACGGAAATACTAGTCCTTAGAGCCTCATCGGGGCCTTCGCGCGGCGGGCGTAGGCTGCATGGCTGCGGCCGCGTTTTAATCTCCTGCACTGAAATTAACTGAGCGATGTGTCGTGATTAACCCGTTTATGGTGCTGCAGTTCCTCTATAGGACTACGTTCTTAACTATTGAAACTAAAGTGTGTGACGTATTCGTCTACGTAGCTACGCCCGCGAATCTTTCCTGGCCCCTTATAGGTCCTTCACTCAAAGCACGTGTTGCCGGATAAACAAGGCGCTTGACGCGGAGGATAACTCACTGGACTGCGCGGTAAGCCTTCATTATACAGGAGAGGTCAGTGCTCAGCCTGTTCCTTTATTGAGACTCTCTAAGTGGAGTCCTAGATCCACTACCAGCGATATACTTTGCTTGGCTTTAGAGGGTAAGGCGACGGGAGGGTTTGTTGTCCCTGATGACCACAGTGTCACATTTCTGTCGTATCACAACAGGCTGCCGCGATTTGCGCTTCGAGCAAAGGCTGTAGGCGCATTGGAGAAATGGATCTACCGATCTATCCGCTCACCGATCGATGACGATTCGACCGTCGCTGGCCCCTGCACGGAAGACATAATTGCACGACAACGCAACCAAATCAGTGTGGAGCCGTCTGAGTCCCCTTACGTTACGGCTGGTTAACCTGCTATGACATCCTCCATTGTGACCTATCTGGGTCGCCGGGCTCAAGGAGTGTCGAGGACCGAACCTAGATCAAGCCTTTTCCGGCTCCGCAAACAACTAGCGATATAAGTGAATTTAGACCTGTAGCGATTCCCGTGGCACCTGGCTCAAGATAAAATTATTTCCTACAATACAATGAAGGTCGGCTTATACAGTCCCGACTTTGTAGCCCGCATGACTGGTTGGTACCGAATCGACCAATTTTGACCATTAGACGGCTGCGCCGACTATGGTCACGCCGCTCCTTATCTTTCTCCTCGTGAGAATATCTTTTATTAACCGGGTATGCGCAAAAACTTCAGTACTTACGTGGCGCCGGTCATATGCGGTAGCACGGAGGACAAAGGAAAATGGGTACGGAATAAGTTGACTAGAACGATAGCCACGGTAATCACCATTGATCTCATAGGCGGAGACATTTCGTTCAATCTAACCGGGGGGCCTCTCTAAGGTAGCGTCGTTACGTAATAGCACTGCCGTTACGCTTCTATTGGGGCATCATAAGTAACGACACCTTTGGTCCTGTTCCTTGGTAGAAGTGATCAACCGGATTAGAAGTTTATGCAAATAACAACGTGTCGGTGCGAGCCTGACAACGTACGACAGGTGTATTTCAAAGTCCTACGCAGGATGGCTGGTGATCTTTCGAGTTATGGTCATAATCTGCTTGGCGGTCTGGTATTCTACGCTTGTTACTGGGGCCCATGCAAATCGCAGAAGGGCATATTCCACTTAGTATGTTTTACGAACATTGCGGCGGGACTCACAATAGTTGGTTGGTCGCTCGTAGGTGTAAGATCCCGCAGTTCACCGCATCGGATCCTCTTTCAATCTTATATGGAGGCATTCTATTGGCGGGCATATCCATCAGCGCTGTAGTGTGGCCCGACTGCGAATGAAGTTACCACGACTCAGAACTGGCAATTCTATGTGTTGTTTCCACTCCCGAACTGCCTTTTAGTTCCATTAAAGCATACAGTTCATAGCGTCATAGTGAGCCTGTATTGCATTATCTCCCTATCTTTGGGGATCGGGATAGCACAATATTCGATAGCGCCCGACGAGCAGAAGCCTGATGCCTGCGCCCTGGGGCGTTCGTGCTCCCGCCCTGCCTGCAATGACGTTACTACTAAGAACTTAGTTACCTGACATAGTATTGCTCCACGTAAAGCTCGGGGCGATCTGAGGAAGTCAGGCCGTTTGGTTTACCAAAAATTAGGGCTCCCTAAACAATACCTCAGTACGAGCCTGACTGTAGTTACGTACTGAGCCCTCCAGCTAAGGCGTCTATGGCGATCGTGGGAAACATATTTACTCAATGTATCAAGAACGGACTAGGGTTGGGTACGGATTGAGATGCGCTTTCAGGACTTGTTTACAACGACTTGTAGGCATCTCGAGGTGAACCTATTTTGCGAGAATGGTTGTTTGATAGCCCACGAGTCTTTATTTGGAGCCGGACAACGAGTCATCGGCATGGGCCCAGGGCTGTTCCCGCGAACGGGTGTAGACCTACAATACACGCGCTCTGGGAAGCAGCTGTATTTGAGATCTAGCAGTCGCAACGTCGTCTGCCCTGGGTGTTAACGTGCGGGTCTCGGAAAGTTGCCCGAGTTATTTCGTCGGATGACGGGTGTCAGGGCATTCCGGCACAATGTAGAGCGGATTTTGGCCTGCCTCGACGCTGGAGTCGGGGGAGAGAGCCCGCAGAAACAGGTCGAGATTTGGTATTTCCCTGGATCTCGACGGACGTCAGGATCTGACGCCAACCAGTGCGAGAAGCCTCAATGAGTATGCTCTCGAGTCATGTGCTTGACATTCGGAAAGATCGAATTCGCATGAATTTGGCTATACAGTCCATCACCCCTTGCCGTCGTGACACACACACGTACGTTTTTGGTAGCACACCCTAGTAATTTGATCCGTCACGATGGTAGCGGGGGTGTAGGACATTGTGCGGTCAAGTACCCGTGCCCGGTCACCAAATTTACTGCTCAGTCAAATTTAAACTGTTTATCAAGGGGCGTTCGCCCTTTCGGGGCTGGGTGCGGAGAGCGCTCGGCGGTGGAATTCGGGAGCCTCTTGTGGGTCTAACGTTCGATGCGCTTGGGAGGTAGCGCTCGGACGACCCCAAACGTGGGGGCGCCGAATCGCGCATCCTTAATGGAAGTCTGAGAGGACAAGCCCCAATGCCACACTTAAAGCTCGTTTAGAGGGGGACTCGCCTGAGCAAAAGGTAGTCTTCCCCACGGTGGAGATCCGCAGATGTCGTCGAATGACGGACGGGCGGCACCATAGGATACACCAGCCACGGAGAGCCTTTGCGACGCATATGACAGCCTGAGCAAGGATGGAGGTTTCTCTAGCAGAAGCCTCTAGGCCGAACCTAGCAGTGCTTGCCACCGATTAGACTGACGTCAGCCCCAAGGAGGATAGCGAACACCCTCGGGGTTTACTAACGCATCAGTGTAGAGTTCCCTGGTCCGTCGATATTACTTCGTATACCGCTGTCGACTTTCATGATGATGGCCCACTGTATAAGGGCAGCGCTTTGGCGGTATCCCATGTACTCATAGGGGTGAAGCATTGCGGCGCGACATAAACTGCTTCAAGCGCACTTTTTGGAGTATCAGCGCATAGACTCGTTGATCAGTCTTTCTTATTCTCTAAATGGTGCAAATATTGCGTTCGTGCGCTGAGTGACATAATTCTCACTAGTGACCCGAGCAAAAATTCCCAGTTTGGTAGTCGACAGTATGAAGCAAGCGATGAAGTGAGGCTGACTATGAGTGCGAATGCTCTCCGGCACCTAACTCTTTACTTTCCAGACGCTGTCCAGGCACCGCTTAAGCTCGATAGATAGTCTGCGCACAGACACTCATGCACATGTTTTTGTGTGACTATGACAGTGACTAAAACGCTCCCCACGATGTGCTAGTCTCGGAGATTATGGACGCGAATCGAAGCAACCCAAGCCGACGATTACCTTTATCGTACATTTAGACTCTTGGGGAGCGGAATTGGGAGTAGTTTTCTAGGGATCCTAAAGGATCGGAACCGCTAAGGTTGCAGCTCTGCTCGTCTTCTAGCATCTAACTGCCACACCAAGTGTGTGAAAGGAACGGAGCGCTGGAAGCGGCAAATAAATCGTTAGTAGCGTTTTCGACCACCTCCACTGTACGCTACTGTGCTTTCGTCAACTGAGGTAGTGTATATGCGTGCGCCAATGATAACCACGACCTAAATAATGTTGGGGCATTGGGGAGGCACCCGCCAACTCTCCATACCTACTATCGGATCACATGCCAGGGTGGGCGTGTCGGGAACTCAGATGGGGGTCAATAAAGTGCAGTGACATCCTCAAGCTACGCTTCTCCGTAAGTTTTTGGAGGATATGCGTTCGGAATATTACAAAGCCACGCCACTACGCTGGACATTTTTACAGGACCGTAGAAGGGAAGTCGCTCTGTACCATAGTAGGTTAGATCGCGTAACAGTCACGGTGATATAAGCCTAGTGCACCTGTGCTGAACCCTAACATGCAGGGAACCAGCTAAATCTTTGTCTGGAACAGTAGTAGGATGCGGGACGGCGAGTGTTAGTCCATTGGTCCCACTACCCTGATCGTACTCGTCTTCATTATGTGCGGGTTGGTGTACTGGATGTCGTACGTACCGAGCCAGAAACGGACTGCGCCGGACGAAATGTGCCCTCTTGACCGCCGTGCGATAGGGGAATATAACGCCGGTGACCTTACGAACTAGATACGACGGTTGTCTTGGCTGGATCACGGGGTTTTGATCCTCGGGGTAAACTCAGGATCGGAAATACCTTCCGTAGACTGCCAGAATGGATTTGACGTGGTGTCCACCTTGAACAACCTGTCAATATAAGTGGGATCGACGAAAATTATCCCTCGTCCTCTCTTAGCCAGAGAGGGATCGTAGTTGGCACCTGACCCCGAAGGCGCTTCATTAGAATTGTGTAATAATCTCAAGTCAAGTATGATCCCGAACCCTGCAACTGTTAAACGTCCAGGTTGTAATATGTATAATTCCTTACACCGCAATGAAGTTCCGCGTTCCAAGAACGGGACCTCAGTTAGGTGGCTGGACCGAGCACGTTCAATCTGAGTTTTACTTATTTGTTCAACCTCAGATACGAGGCGTCTGTGGGTTACCGGTAAGCCTCTGGCACCCACTGTCGGCGAGTTCTATCTGGCTACTGTCCTTTGTTCAAGATAGTCAATAGGTGGGGGGGCCTGTGAGCGTGCCGCAGGCTCGGAAATCTGACACGTATACTGAACGTTACCTGCTGCGCAGTTTTCCGGTGCCATTCAAGCTTCATCCCCTGCGAAAGCGCCGTCAGTCGCTGACACATAACAGAGTCCAGAGCATCAGCTTCGACCCTGCCACCCGTGCTGATGGTTTCGGTCGATTTGAAATGGCTTGAACCTAACGATGGGCAGGATGCACGAGCTGCGGTTCTGTCCCCCCCTGGCGGACATTGGCGACTCCCAGGAGAAGAGGCTTCTTCTATGGGATTAGCTGGCGGTAAAGCTGGGTCTAGAGAAATGCCGAACGTACTGCACGAAATGGAGTTTTACTGTGCCAGACTGCTATTGCCACGGTCTGATAGGCTGTGAGCAGCTGACCTCGGGTCACACATAGTGTCTTTAAAAACCCGCCTAGCTCTAACTAGCGGCCTGTGTTTCTCAGCTTACAGATTAGTGATCTGTACTAGGGTAAGGGTGAAGTTGATGCAAATAGTTAAAGGGACTGACCCTCTAGCATGAAGAGCAAGGAACGCGTTACATCTAGGCACTAAGCGAGGGTCGTGCACTGCCCGCAAGACGGGCGAGCGTGTGCGAGGCCTAAAGACTTCGAGCCAGTGTCAATGCGTTGGGCGGACCGTAGAACATCTATATCCTGATTCCACAAGTAGTCATTCCCAACTCGAAAACTAGCCCCCTATGTCAAACAGAGTGGGCTCCTAACCATTCCAGAGTGCAAAATGAGGCGGAGTCTCGGCACGCACACTAATACATTTAATGGCTTAGACCTGCCGATCAACCTAGGTGAACACCGTGGGTCTGGTGCTGTTCGCAGTGCGTGACCCGCATCATACATTAATTATTCAAAGCCACGCCAAAAAGACCTCTATGGCTAGACGCGGCCCACTAACTCGTAGAGTCAGCGGTTAGTGTGCTTAGGAGAGAACTTCCTTTCGGATTCCTTCCTACATTCGGTCACCTGTCAGGCTAGTAGGTTATGGTTCTCCACCTACAAATTTCTCGTCTGCTGTGGAAACGACCGTAAAACTTATTTGGGTGGATGTAGAGTAGCCCATGTAGCTCAAGTGCCGTCTCAGTCGACGTTAATGCTGAGGCTCTACCATAGGCGAACGGCCTTACCAATGGGTAGGCAAGGGTCGGTTTCACACCGCCTTTGTTCAACCGGTTGCGCGTGGCTCTCCCAGATTATACTAAGGCTCCTGGTATGGACTCCGCAAACTCTTGGCTGGGCATTGTATCAGAACAGTGCCTCCGTTATTGGTGGGACTAACGCAGACGTTCTCGTTCTTCTCTATGTTGCCGTTACCGCGAAACGTATAACATCCCCTCCAAGTTGACCCCATCCCCCCCACCCATACGCCAGGATAACAGTACGGAGCTATCAACCTACGCTAGCCGACCATTGTAGAGTCCGCTTCGTAGACTTACCTAAAGCGATGTTCCTTAATTCGAAGTACAGTGGCCTGAGGCTGGGTCGGTGCATGTATTGGAACTTAATCAGGGTTGGTACTGAGGCGTTCTGCCACCTACCCAGAAACAGCGTCCCTTTTGGGCGCGGGTGGATGCATCTCAAATAGATACAATTAGGTGGATTGTCATTGCCCCGTCAAGGCTGAGCACACGTCACCAGCCCGTCCATATTGTACTACGGACCACATGGTCTCGAGGCAAGTGTCCTTGGCTTATAAAGTGTCCACTATTAGGGGGTAAAGGACAGGCCAAATAGGGCGGGCAGTAACGAGCACATGCATAACAACAGACCAGATACGAAGGGGAATCTTTTTCACCCGGAGGGTGGGGCAGTCGCAGTAGCGGCAAATGACACCGGATGGAGTTGCGCAGGCCTAGGCGCAATTACGGGCAAGTTTCCCACGTTTGGGAGGCGCCGACGACATCGATATATTGAGTTCCGAATTATCGAAATGATAGTTGGTCATTAACCCTTCGATATACCCAAATTAGGAATTAGGATTGATGCATTCTCCTCGACGAGCAGCTTGTTCTAAGCCCCCCCACTACCAACTTGCTCTGGCTTCAACCACTAAGTTAATGTGGTGTAATCGAACTTCGCCATGCGGGATTTACCAGGTTGGTTGATCAACCGAAACTCGTAACCGGGGACTGCCGTAGGTCACCCGTTATTACACAGCCTTGTGCAAGTTGGATGGCTATAGTAAGTCAGCGGTGGGCGTTAGCATGTTCTGATTAGGATCGCCTAAGCCGAAAAAGTACAAATACTTACACCATTTGAACGCCTATTTACGTTCATCTAGGCTATAAGATTCGTCCGTGTCCTCATCTTGGGAGAACGCGAGTGATCTTTCCGAAATTCCCTCTCGTTCCACCCAAACAAGCACGTAAGCAGGACAACATCGCGTCCCTCGCGACTGCAGTGACGTGACACTCATTACGCACCGGCATGGGGTATTACACGGGTAGTGGGTGTAACCTTGCACCGATTCTTGATCGTGGCGGCGTTCCACAAGATGTGACCGCGTTGTTTACCACATAATCTCACTTTGCCGCAACACGCCGCCCAGGTGAACCTGGTCTGCGTCGGCAGTAGAAAGTGTTCGCGCCATGCCCTTCACCCTGTCTGCTTCGTGATCTTGTCGCCCCAAGATGCCATTACAGAACAGAAGACGGGCCGTTGAGTTAAGAAAAGTGTTTGATGGCGGAAAACGGGTGCTGGGTCAATAGAAGACACTGGCAGACGAATTCAATTGATCGCAATTAGTTCTTAATCCCATTCTCTCGACGGGGCTAGCTTCTATGCAAGTGGGATCCTCACATGGCATTAACCTGCAATCTTACGTGATAATCCGGGATGCTAGTCTGATGCTGCTATAGAGATCGGGTGGTGGGGCGTACATGCGGAGAAACTATGAGTCGACACACAGACTTTCTGCCGAAGTTTTGGTATCCAGGTCCATATGATAGTAAAGCTCATCGTAGGTAACGTACCAAACAAGTTCCTAGGCAGGCGATACTAAAAGCGTGTCACTAAGCCCTCCAAGCAGGGACTCCGATTTCCGAGCGGCATTCGTATGATCTCCAACGTGGATTCCCACCCGGTAGAGTACAAGCTCCACTCGCGTTCTTATAACTGTGAGATTAGAAGGTACGAAACTATCGGTTCTGCAGGGCACATAATAGGCCGTACCAAGTGTGAGATATGAGTCCCGACTACGTTTCGCATTACTGCCCCGAACGTGAGAGTCTCCGCCCTATGCACGCGATTAAGATGAGGCACCTTGTCCTCCCTCTGCCCAACCCTGACGTAACCTGCCGTCGTAGAGCACAGCGCTTGCTACACCAACTAAGAAATCTTTGCTGAATCAAGGGCGCTCACACTATTAGCGAGGAATGGGTACCGCGTTAGCGCCGCACACTCCGGAGAAGTCCTCCGCTAGTATAGACCCGTCTTGATTTTAAATGCCCGTAACCCAGTATCATGTGTGGGGATCTGTGGACCCTACAACTCCTCGGCGAATGCTAGGTATAAGCCCAAGGCAGTATCGCTGGGTGGGGAGCTAACTCTCCGCTATCGGCCGATGATACGTGATATCCGACAGTAGGCCCTCCCGCGACCAAACTCATGTAGCGAGCCGAGTCAACGTCCGGTCGCAAGTACGGAAGTGCCTACGTCATCGGCCGCTGTCATCTCTAGAGTTAACACAAATTGTTCAGGACGCAGACGCCGAAGGGAGATAGTGCCTCGCGAGCGTAAACGAACGGGTCGTGACAACTAGTGTCTCCCCGGAAAAGTCCCCGCACCAGCGGGTAGATACTTGGGAGGGGCAAGTGTCCAGAAACCACTATATTCAAGTACTTGAGAAACGCACACGGCGCAATGTATAGACGCGTGCTTCAGTCGTCCCAGAGAATCTGCGCACGGGATAGTTACATCGCAATGTTTTATGCATGCGTGTAGGAAAAATTCCCCACGATCCGAGCGGGCTGGTAGTTTGAATCTACTAATGTCATTTGCGCCTGACCAGTTCCTAGAAGAGTGGGATAGGGCTCGGTCGGTGCAGCTCTCAAGTCTAATCACACAACAGAAATGCCACTTGTAGGGAAGTGAATTTGAAACGGGACATTGATTAGAGTCGAGGTTGGGAATGGCCTGAATAGTGTTGATAGTACCTACACTGTATCATTCTAGCCCCTAACGGTGTGTCGTCGACACGTAAATCTCGCAGTTAAGACCTCCACTGGCAGGCCTTCCCAGAAAGGTAACCTATTCCACTACCTGCGGCCCCCAACACCGGTTTTCCACTGCACATATTGCTAGAGACCCATCTAGTATAAGAATCGAGTACACTATGTACTATGGACCCGTGGAGACTTAGGGTAGTATCGAAGCAGGTAGTCTTAACGTGGAGCGTTTCTGAGTAATCCCTTCCCAACTAGGGAACCTTTTAGCTAAGAAGTATTTGGCCCCGGTACTCGTCCCGCCACTGTTAAGGAATAAACATAGCGCTCAATTATCATCGTTAGTTAATGGCCCATAATAGAAAAAACGTGAATGAAAGATATTATGCACAGACGGATTAAAGTAAATTCGTTGGTCCTGTGAAGACAGCAGTGCATCCACCCCAGCTTTCAGAGCATTGACAGGGCCATTTCGTAATGGAACTTTAATTGAGTTCTCTAAGATAATAAATACGATAGGGAGTGGGGACCACCGCGAGCGTCCCGCCAGGAACTATAATGCTCTTAGCGGCCTTCCTACAAAGCATGCAAACACAAGTGCGGTACATAATCTCCAGAGCGTCACCCTAGCAATACTAAGTACATCGATCACACGCCTAGGGCCTGGGTGGACCGAAAAGCATATATCAGTGCGCCTCGCCGTGTTACGTAGATGGCTCAGTAATAAGACCTAGGACTGACCTTATGTGCAGGCCCCGGCGTGTGTCTTTGACAAGAGCCTCCCGTTTTGCCCATCAGAGGGAATAACCCGAGTAGATCAGATCCGTGATCTCACGAATCGGTGAGCACGTAGTCGAATACGGACATTTCTACCTCCTTGCCCTGTTCCACACGGCGAGTCTTCTCTTCTTGGAGTAGGGATCTTGATAGTGATCGGTAGTGTAGGATATTGTCAGGACATCCTTGTCGATTGATCCCGTAACCGTCAAAGCCCACAGTCGAGCGGGCCACTGTATGCGGGTTTCGGCTGAAAATGTCAAGGGAGCAGACATAAGTCGTTCGCTCTCAATAGTTATATCTCATAGCTCTGTAGTGTTGAGTGACCTGCAGCTTTTCATGTTCCAAGCATCGGGAGATTACGGACGCCATGGATGTGTCATCAGGATCGAACATCCGGACACGTCCTGGTGTCTAGCGAGAAGAGTCAACTGCGCCTCCGGTTACTGGAGGTGTAACGCGCTGTGCGTGCGCGTGCATCGTTAGATGCACGACCGTTAGCGATCACGAGGGTTGACTCCGACCGTTACCTTTATTGGATAGTCTTAGTGATTGGTTTTTACCATGCACAATACCCAGGAATCTCATTAGTGCGCCAACTATCGAGGATGGACCCCTGCTTGTCCGCGACAAGGCATCACATGATCGAGCATCGCATTATCATATGATTGCGCCCCTTACACTTGAAATGATACTGCAGGGGTTAGTCGGAGAGCTCTGATATTTAGGACAGCGCATGCAGAACTTAACCTCCGTCGGATGAGAAAAGCCCTTGTTCTGCCTTCGTGGTTAGAGTGTGGACCTGAGTGGCGGCAAGCCTTGCGAGAGAGGACATAACATGTTTCGACCCGATGTGTAGTTATGTGTGTTTTCCAAGGGCCGGTTGCTCATTTCCGCTTTATAAAACGTTGTACCGGTGCAGTAACATGAGGACTTCATTGCGGATTCCTGTCCGCTGTGCATTCTCTGTTTCATTAAAAGCCCCCTAATACGCAGGATTCCCTCCTTATGTAGACTGCCTCAAGCTATAACATGCTCGTCACATACCTCAGCCAATCTCACCCAATAGGGTCCCACACAATTGTGCCGGCCCGGGAGTGCACTATTTTCTGGGGTTGGATAATGGTCCTTACTTGTGACACCCTGCAGGCAGGTAGGTATCGAAGTCAGTAGCTCACTTAAGTCCGAGTCGATGAAGCAGAGACGCTGACACGTCGCCGCAACACGACGTCTCGTACACCAGTCAATGGGTCCGGGTGTGCGGCCGCTATAGTCCACCAGGGGTGAACCTTTCGTTACGAGAAATAGATGGAGTCACGCCGAAGGCTACTAGTACGACTCTAGAATTAACGGCGTGGGATATCTACGAACACTGTTAACTGATACACCATTTTCAGCGAAAAGATACGCAGTGACGGAGGAGTCTTTATGTCCTCAAGACGCATATACGAATGGACGCGTGCCTAGCAAACCTTATACGATCTGTCCTGGAAGATATTGCCGGGGGTGCGGTTACAGGGATTCGGCCACGTTACGCAAAATCACCCGCTCTGTGATGAATGTGCACATGCGTGCCGCCTACGGACTTTGATAGCTGTCTCCATTTTACCGATAAACGTATGAGACACTTCTGTTGACCGTCCTCTAACATGTCTCCGGCGACTCTAGCCCAATAGGAAGCACGTGATCATGCGCGGCCGGAGCTTATGACGTTTGTTTGCACGCTGTAGCGTTCCGCACAGGATAGCTGACCCCTGGCTAGCGAAAAGGGGTAGCGTCAGAACATGGGCGTGCTAACGGCCACGGAATTAAGACACATTCTCTGGTCTATGTCCGAAGCGGCACATCCCAGGACACTAGTTGATCCTAGGCCGCTCCTTTCTCCCGGCTTTCGTCACCGGCATTATCGTAGCCCTCCTATCAGAGATTGCACGCATGGGCGTTATATCGGTACGATAGACCCTAATCTGCGACTCATAGGCCAAAGGGCGCTACGTGGAGTCATGTAATAGTACTCAACGAGGCCAGGAGATAGTCCTACGCGTACTGTCCTAGCTGTCAGCGGTGGATAAACGGGTGCATCAAGTTGGATAATCCCACGTGATTTAAGCCCTTGCCTTTAAGACCAGAGGTGCCACCTATGGTGGCTTCTCTAATCTGGAGTGCTAAGGGACCGGGTTAGTAGAGCCTTGTAGTGGTACATGCGGCCTCCTAATGGAACCGGTTAACGAGCTCAGGGCCTAGGACGCCACATGGTTCTCTAATCCCTGCAATCCCCAATTCCTGGCTTGTTGACCAGACGGAGCGAATGGCCTTATGGACGTGGCACCCGTCTGGCCTGCTGTAGGTGTTTCACGGTAGGCGCTCAATCGGGGGATATCTCACACAGGACGACCGGAACGTGTGTGCGCACGTTACGCTTCTATCAATAACCGTGATTAGCCGTGGACGAGAATTGCTCCACTTTCGATTTGAAACGGCAAGGAGATGAAGCTACAGGGGCCGTGTAGAGACGTCGGTGCGAAGGCTCTCCACAGCATCGGAGGGTTCGTTCTACGCTCTCACACACTGACAGAGTTAGGACCTCGCACTAATATCATCATACGCTCCTGAGGACACGAGACCGAGCGATTAGGTTATTTAGCTATCAGGTTCATACGTCCTTCATCCCATGACTAGCTAGATCTCGCGCGGCAACTCCGGGGATATAGGGGGGGTTAGAACGATTTCCTAGTACTATGTGTGTATCGTCGCCTGTACCTCATATCGCTATCACCGCATGTTCCCGCAACTTGTGGAGCCAATGGCCTTAGGTTTTCGAGCAAAATACTCGCTTTTCTCGCCAATCATTGACTACGGATCATTGGACATTTTTTGGAGGACAGGTACGTTTCGTATGGTCAGCTATAAATGACGTCGGAACACTAGTAGGTCGTGTTCGACCCAGCCGTGAGTGACAGTGGAGAGCGCGCCACAGGCCGGCCACGCGAACGCTCTAAACGGGAAAGTCGGTGAACGCCGTTTGCGTCAAGAATTTTACTGGAGATACGAGATCAGAGCACTAATTCGCCGGTCTAACTGACTCTAACGGGCTCTGAGACTAAATATCAGAGCTTTATTGATGGTCTCAGTCGGTTGCGGATGGTATATCGCTCGGTGCTTTTATTAGGGGTGCCGCTCGGCTAACCTGGGTAATCAACTTTCCTGACCTGTCATTTTTTCCTCTAAGATCTTAAACGAGCTTCTTTTGGTTCAATGCGATGTTCCCGCTGAATATCATCAACCCAGACTCTCACCACACCAGACCTAAAAAATAAACGTTTCACGATAGAACGAGGACCTCAAGTGATATCTCAGTACAAACTCCGTTCCCTTTAGGACGGTACTATGAGTGAATAATCGCTGGAGCACGTAATTGGCGCTGTCTTACTGTGGGCACAGGGTGAGATGCGCCGAAGCGTATGAGGTCCGCGGGCCCGACTAGTTAGCCAGCTCAATCGGTTATACCGATGACGTGGATTGATTGGTCAGTCACAGCCGCTGATCTATCGGCCCTCCACTCAGTATGTTCATGAAGGAAAACCTATTCCACTTAATCAGTAACTGGGTCGCTGTTAATGACAAGTCCGGCGTCGGGGTAATAAGTGGCATGAGTGGTTGAGAGTAGAATCCCTCTACTTCCGGGTTGTATTCCCATCGGCTAACTGGAGCAAACATGGATTAGGTCAATAAACCCTGGCACTACGGTGCAGCCCTTGGGTGGTTGAAGCGTCTGAGCTGGAACCTTAAATGGGGGCACGACGCTCCTGGTCCAATACAATACCGTTTCTGACTGACTCCTAGTCGCAGGGCCAAAAGTCGACTGAGGGCTAGTGGAATATCCTTTCTGAACCTATTTTGAATTTGTTGTCAGGACCGCAGTCCTTGCCCAGCTCACATAATCCGATTGGGTGGGCGAGTACGCACAAGTCGTGGATCGCGTCCAGCTGAGCTCTAATATCCAACCTCATGCTCCAATATATCCGCCACTTGGGCATCAAGGAAGCGTCGTAATTGAATTGGGATGGGTACCATCTCCGTTATGTATGCAAAGTCTTGCAATATAGGGCTATAGAAAGACTAACTTCTCTAATACGTACGTCACGCACCTCTTTCCGAAAGGCATTGGTGCTGTCAGTAGATGCGCGAACAGCACCTATGCTTGCACACGAAACATGATACTTCAGATCTGGTGATCATTTCGATTCGTAACCTACCCGCCGGAACCGTACCCCAAGCATGGGACAGATCTCGGCAGACGGTTGTTCTGTCCAGAAGGGGGATATGGGACGTATACGGCTGTCCCAAATCACTGTACCGCCAACGATCGGTACGCCTACAGGGATTCACGGGTGCCATTCATTCCCGATGTCGCCTATCTATATGGAACCTCTCCTAGGGTAGAGTGACACTACTGCGCCGTCGGATCTCGCAGTTGGCGAGTAAATTGGATAATGAGAGTGCGGAGTTCGATGGCAGCTCCCCGCAGGAGCGAGAACACATATCAGAGTTGCCCGCCGGCTATGGGGTCGGACGTTTAGCAGTAAACTTTAATCATCAATCAGCCGCCGTCAATCATCAGCTGCGACGCACTGATTACGCAATCGACAATTAGTGCATGCTCATGAACAAAACTGATAGTGGCCATATCCCCAGTACAGCAACTAAACCTTTTGGGCGCGAACGTTCCCAAGTAGAAATGATGGAGGGACTGAACATGTCAATCCGGCTGTCGCTTTTAGAACAACTACATCGTTCATTAAGGAACTATTGATCAGGGTACCATCTATAAGCAATGTTTGATTGCATAATAGCTCAGCGCGTCTGTTCATCGGGACTATGCATCCTCTGGTATGTAGATTGGGCCCTCCTTTGTGTCGCCAGCGCACCTTCGAAGACTAGTCAGCACTTTTGTGTAGATGCTCAAGAACCGTAGAAAATCTGCTGATTCAAGGTCGTATCTCCGGAATGTGATCGGCCTAACTATTCTGTGATCTATGTTATGAGTACGAACTTAGCACTACCACTGGACGATGAAAGAGGGCTTCCAACGGCGGTGACTCTCGTGATGTTCCTACGCTGTCACCTGGGGTTCTTTTCGACAGTTGATAGCTAGTAACGGGTTTACACGAATACTCGCGAGAGAACGCTCGAGCACACGCTCTACCGAAGCAATATCACCATCGGCTGGACATAGCACTTTGTAGATCCATCTACATGTTCATTGAAATACCATGTCTAACACGTCCTCGAGGTTTTTTTTTGTTCGCATTCCGTTAAACCTAAACGGGAAGGTTTAATTGGGGGGTGACTGAAATCCAAAACCGTTTTTCTCCGCCTGTTATGCCTTCGGCGTCGAATCCAGTCTATTCCAGCGGCCGCCACAGGGGGCTTTTGTATCGCGAAGATCGGCCCACGGGGAAACATGATATTCACAAGTCCCAACAGATGTAATTTCGCCCCTGGGTTGTCTCGACTCATCAACTTCCATTTTTTGGGACTCGGGCCAGGACTAGGACAAGAACCGCTCTAAATGACTAATTTGGAAGGACCATAGTCACCGTGCTGGGGGCTTTCCGACATGTCGCCTATCCCGACCCAAACACGGGCTTACGCATTAAAGTTGTCAAACTATCCCCCAATAGGACAACCGTGTTAAGACCTCGGACAGTCCAGTTCGGAACGTCTGTAGGAGTAACGGTTATTACCAGAGGGTTACGCCTCCGTTACCTGGACGGTTAATGGGGGAATTTATCCCATGCGCTCTTCGATCCGAACTACCATCAGCCAGGTTGGAACGGAGAACTCCTCCGTTCAATTTGCACACCAACGGTCGGCTCACTCCATTCCCTTCTGGTAACGAATAGTAGCCTAGTTATGAACAAAAGACAGTCAGAACGGCGAACTCGAGCAGTTTTGCAATCATTTAAAGTTGATTTTAACCCCCCATATAGGATCTTATGACGCACCCTGAGGTAAGTTGGGTGATCATGCATTTAAGTTGGGGGGGTCCGCAACCGAACTATTTAACTGTTCGCGGATTGCGAGCCATGAGAGTTACCTCCTGTTTGTAGTACTTGGAGGATCCCCTCCTTGAAGAAGGGCGCCGGACACCCGATCACTTGAGGTTTTAAAAGCCCCGGTCATGATGCACAGACTCAGTCGGTTGCGTCAGTCGAAATCATCTCCTTGACCTCGCTAGCGATGATCGTTAAGGGACTTGCATGCCGGCCAATAGTCGTAGGGCGAATCCAGTAGTATTATACTGTCGTTCTAGCTAGAGGGTAACACTCATTAGGTCACTTCCCCTACTAGTCAGTATCTTTGCAGGCCGCTTATCACGGGACCGGAGCACACGTAACTCTTGTCGGAAAACTCTCGGCCCGGCACTAAGCGGTTTCGACACGGATATTTGCACAACCACGGCCGGGTGGCTTCGTTGTAAATGCGTGGCTCTAGACGATCGCCCAAACGTACGCGCCCGCCTAGGTCCAACGAGGAAGAACAGCTAGACACTCGGTGCTAATAAAAACACGTCATAAAATCTAGCGTCTAGCGACTAAGGGCCCTTAGTATTAGATCTCTCTAGGAGCAAACCTGATCCTAATTAGCGGTACGCAAATGTAACTCGTGAGTCGAGATAACCCGACTAATGGCATTTAGATGGAGGATGCTGAGTACCCTCTCAGTTTATAATTCGAGGCCGACGTTACGGAGCCGCCGTTTAGTGCTTAACGGCTAAATCCGTTATCCGGGTTCTTGGTACACTAGCCATCGATAAGCAATTTCACTTCCGACTTACGCGCGTTCTCTTCTGCGCCAGACACAGCAGAAATACACCCACACACCAGAGTAATCCTTGTCTTATTCCCGGGGGGATGGGTTGCTGGATTTCTGCGGTTCCCGGGGCCATGTAAAGAGAACATAATGACTTTCCGAACAAACCGATGGAGCAAGGTGCGAGTGTACCCTGATCCCAAAAAACTATGAGCTTAGACGGGATACACGTCCACGTTTAACGTTTATTCCGGGACGTTCAGCTCGCCGGACCTTCTCGTGTTGGTTGGGATAGAAACCGTATGGTAGTCGCCACATAGCGGCGATATTACTTCATAGGAAGCCGAGTCTGACTCGCACCCAGAGCCATGGGCGAGAAGGTTCCAGGCGTCCGTCATGAGAGAAGTTGATCGCTTTTCGGTCGCGCAGATGAAGCGGTCGATTCGTCACCCAGAGCACTATGGCACTCCTGTAAGGGTTCGTACACCCAAATTCTGCTACCCGCTCCTCCGAGGGTTCCTATGGTTTGAATGTTACCCGATCGCACGGCTCGGCGCCGATATTGGATGTGGTACAGACCTGCGCTTTATTAGGTTTTGGCTGGCACTGGTGTTTAGGTGGTGCTCTTATGCGATTCCGTGATTCTGGATCGATATATTAACACTAGATATCGAGTCTACTACGTCGCGCCGATAACGAAAGCTGACCATGTATCTTCCTAGCCTCTCCAGCATGGACCCATGAATGTTGAGTGGTTACTTCCGTGAAAACTGTAACAACCGGTGCAATGGAAGCCTTCTTAGAGTTGGGTGTGTCCCGACTGCACCGGTTATAACAGCAACGGCCTCCCACCCCTAGACTTAGACGCTGCGGATCTCCGCCGATAACGTCCTTGAACATTCCCAGTCGCCATAAGAGTGGAGACTTGCCGGAGCGGAGGTAATTGGGTCCGATTCAGATAAGCCGTTGTGTAGTGCTCCGCTGCACCTGTGGCGAAATGCACGGGCCAACCAGCTAAGACACTGGATGGTTGTGCACCTGGCAAGTGCTAGGTGTCTGGGCAGCCAAGATAACCACTAGCGCAAAAACAAGTTGGACAAAAACGTCTAATTTAAATCGTAGAGGAAGAATGTATAGGTGGGTGGCTTATTTACCTTGCACTCTCCGCTAAGTCTATCTCGCAACGGCCCGGGAAGCAGACATGAGTGGCCCCTTCGTTAAGCTTATCCAGTGCAGTAAATCCTCCGTTACGGATCGATCATGGTTACTGTAACATCGTCTAAGCATGCCGTCCGCGTGTGTCTAAAACTCCTCAGCTGAACAGCCTGCGAAAATGCTCCGAAGCTCCCACCCTTGAAACTTGGAATGAGCTCGCCTCCTGGCGTTGGTTCGGCAAGATCGAGGCGCATTCTAATTGAGTGCCAGTATAATACTATGACTAACAGTTAATGGTTGCTCACAATCTAGTCGACATAATGCTTTGCCTGGGCGAGCGTTCACAAGCGACGTAAGAGTTATTGTATAGGTCGACCTCGCCTTCAAGAATCTTAACGGCAACTCAAAGGCATTGTGCCATCAGCTGAGGAACGATTCCGCGCGTAGGACCCTCACGTCCTTGGTAGGCGCCACGATGATGTTCCAGAATTTTGCGTCGCCGGGGGCGGCGTATGTAGAGGCTCTGATCGTTAGACTGCAAGACCCCAGTCATGAGTCTTCTACTAACCCAAATGAACGGCTATGATTGTTTGTCCCAAGGCGTAATCCACTAGGTGACCCGTGGAACAGTGAGCATCACACGCGAGAACAAGTTCTAAGTGCTCGTATCCTACACTTTGGCATCGCCTTGGCATTGTGGGCCAGTAGGTCGTGCGATAAGTTGTTCGACCGCGCAGTACCATTAGCAAAGGACTGTTATCCTTAGGGTAGCCAGCTACTTTCAGCGTCTTCGCCCTATTTTATGGATAATTTCAAAGGATTCCTCGCCGTTGGGTCTGAACAGGGACTTGAGTGAGATAATATATAGTTCGCGAAGTACTTTTACTAAAACTCATTATCAATGCATAACGCCAGAGGTGTCATTTTTAGGCCAGGTCATCATGTTTTACACGCACCGACGAAACGCGATGGTGTTCCACCGCTGACGTCTGACACGGTTCATCAGTCGACTACAAGGCTATCAAAGGCTAAAATATCGCTCAAAATGACAAGCCACACCAACATGCAGTTGCCTTACAAGCGCAAGATTCCGACTCTGACATTTATTTTGCCTTGAATAGATGTGCAACTGTCTGTGGTTTCGCGCGTATGACGCAGTAGAAGAGCTTTCCGTGCTAGGCTGTGAAGATTAGTTTCATTTTGAGATATTGTCTTGACTCAACGACCGCTACCGGCTTGAGGACATGCATTCGATCATATACATTAAGGCGTTACTGTCAGGGTACTAGTTTTCAGACTGGACCGATCAGTCTGAGCCACGCAACCAGGCTTCGCATCCTACCAGGATAGAGTGCTTCTACATACACGACGATTCGTGTTCCAAGAAATCCGAAAATGGGAGAAGTTTATCACAACCACGAGGGTTACCCTCATCAGAGGATGAGACAGCGTTTACCTATACATTTGGTCCATGCCCGCTAATGGAGCGTGCTATAATGTCTTGGCTACAGCTGCGTCCATCAGCGCTGTCTCCGTATAAACGGGAACGTCCGACAGATTCGGTACCCGTAGCGTCCCGGGAGATTCCGACGTAACGGGTGGCACTACAAGAATAACTTAGTATTATCGAAGAACCCAGTAATCAGTACGTGCGACCCGATCTAGAGCGCTTAAAAGTCGTCCCAAGTAAACGAGGTTGACCTTACATCTCTCAAGCGCCAGCCACCTGTCCAGTCTTGGAGTATTGAAAAGGCCCAAACTTATGACGCGAACTCGTCAACACACTGCCAATGAAATCGCCCACGGGGCGCTTCTCACTGCTATTCCTGACCTAAGAGCGAGTCCACATGTATCCCTCCCGCCGAAAAGTCACAAGCGCATGCGAGAGGAGCACGACGCTCTACAGGCGTGCGAAAATTAAAATGTTACGCCATGGCTACTGATTCCCTCGGTCACTGTCTTAATATCGGGTGCTAATTTCAAGTGGTTACAGTAAAGAATCGTCCAGTTACCTTCTGGCATACTTGTATGCAAAGGATCTCCGATATGCACGGAGCTGTTGGCTTGTGCACGCTGTCTGTGGTAGGACAAGGTAAGGACCGTGTGTCGAGGCTTCAACGTTCGGGCAGTCGCTACCTACTACGCAAGACTCGCAACCGCTCGAGGGAAATCGGAACTTTATAGGGGATACTCGAATTAATTTCGGGTCTGGGCTGATATGATCAATGACGTAGCACAGTGTGCGCCACCGGATAGTTGCGTCTCGAATATATCTAAGCAAAATGACTGCAGCTATCCGCAATTCTACCATGGGCGATGTTTCAACACCTTCATTCAACTCTGGGAGTGTGACTTTGGCCCAACTAATATCCAGCGGCCTCGCACATGATGGGCCACTCGCCGCGGAGTATCTCGATATTCTTAAATTGGCGTCCTCTAGTGCAAGCTGCCAGACTACCACCGTGGACACAACTAATTGGGAAGGACTATATATCTTATTTCGAATCCTGGCGTTGATTATATTGGTACAGGCGCGTAAAGACTTATGTTCTCCGATTTGCTTGCTGTCCAGTCGTTTGACCCAGATGACAACTACATGGGCCGCTCGTCTTACCAACAGAAGTATGTAATCGGACCTTGGTCCATTATTGCTGGTTCGGTTAGTCCGCCTTGTGCCTCGTGGTGACCCCCGAGGAGTTGTGGGGCGCCAGGCGGCCCAGTTCAGTAAATTACTCCAGCCAGGGCCCTCGCGATGTGATCGAAGTTTTAAGACGGAGGATGATACGTGGACTCGAAATTCAGAGTTCCGGAGGGCATGGCATACCAAGTAATTTAGGCTGAACACCCATTTGTGAAACGCAAGATGCTCTCTCAAACACGGCTGTGAACCTCCGCCCCTGTTCTCTTAAAAATTTCCTGTGTACGACGTGAGGGTCAAGTAAGCCGGTGGGGGTGTTTGGGGCTTAATCTTTTTGGGGCCTACGAGAACGGGGCAAGCTAAACGACGATGAATGTCGCCGCCCGCGGTGTCATCGTGGAGGCTTCAGCATTTCATATTATGAGGACAAAGGACCAGTCGCCCCGACCCAACCTCTGGTATGATGACCCTGTGTGACTCATCTAGATTTAAATGGCATGCAGACATAGGAGCAATACAGTGCTATATGATCTTTGCACCTCTCTTAGGAGGTGGTTGTGGTATTGAGGTTACCGTAACTGGTTGACGCCTCTTGGGATAAAACTGTGCTCTAAGTCTTCTTTCAGTGGACAACTATCGAGCCGGAGTCTACGCGCAGAAGCGGTATCCACGGATTGATTGGCCCTAAACGGAGGCCCATATTTCCTTAACCGGTTTGTGAGGGTTTTACCTAAACCTGCATTCTCCCCGTTATCTTCTTGTTAGATAGCGCGTCCCAAGGGTACAGTCTCGGTCCTAATGATAACCCTGATGTTAATGGTCTCGGGTTTGCACCTAGGCCTATAACAATCGATGGCTATCGGTTGGTACCGTGATGTTTCCGTCTTAGCGAAATTCGACTGGCAGGCGTACTCCGTCACGGTACGACGACGATACCGAAACAATGAGAAGTAAGTATCCAGCGTCTTTGGGACAACCGTGCCTATTTTTCGATTCCGTTTTCTGGCTATTATCGTTTATCTGCTAGAGGCTGTAAACGTCTTAATAAGGGGCGGTCGAGTCGTCGCTGTAGGGGGACCAACCCGATGCTACTTTTAAGCAATAATACGTAAAAAACGCCACTTTCTACCCTTCCTACTCGAAGTTCGGATGTCTCATAAACCATGAATGACAATACTGGCGCCCACTTAATAATGAGGACTAGTCCTCGCTCCGATGTTGAACGGAGAAGATCATGCTCCAGAGTCAGGCTCGGGTTCAGATCTTTTAACTTTCATTGACCGGGGCTATTGAGCGGTTCCTGCGGTTCCAGCTCGGATTTACACTGTCAGAAGTGTTCAATGCGCTTCATACGTAACGTGGGCTTTTTCTCCAGCACTCGGTTCTGTGACGATATTAACGAAGAAAACGTTGGCATACGACGTCGTTATTACAACCAAGAGACATCTTGAAGCAGCAACACATACGAGCGCTGACACGTTAGATAAATGCAAGAAGGATCTCAGGCCTGTCAAGAACCCGACTCCGTTGTTTTCCTTCACGTAGTAAGGGTCGTGCATACATGTGAGGTAACCTTACCATGATTGACCCTTCTTCTTTGGAGCATATGTCCTGAACAATTTCACAACATGGTTCTGGCACCGGTTTAGGGTCCTCTCCTTACACCAAAGACTCGCAAGGGCGCCGACGCATATCGGTCTAATCGTCACGTTTACCGTTTCCTGCGGCAGCGAGTTCTAAGGACGTGGCTAACTTGGCCGGCGCAAGCGCTAGCAGCCGTACAGTAGCTACGTGTTTCGGACGCAGCGAATCCAATTGAACGAACCGCCTAGGTACATATATATCACTCTGCCCCACTGTGGTAGGAGTTTTCCTCTTCGTAAATTTGCAAAAGCCCGCTACAGGGTGCAGGCCAATTAGCAATGTTTAGCATAACCCTGAGTGAAGCTTTAGAACTCGCGTCTTACCGCTACAGAAAGTACCCAAGGCGGGCTCATTTAGATCCAGCGCAGTTGAGCCCGTAAACGTGCTGTCCGGAGGAGGCGCCGCCGACCTTGCTATTATTACCCGTCATCAACCCTTCTCTTCTATCCGACGTTTTGGAATCAAAATGCAGAGGGGGCTGGGTGAAATTTCCATACGTGGGCGGTCTGCCAAGCTTCCTTTCTGGCTTCCTAAACGTTAGGGTGGCTCAAGGACATATCAGTGACAGACTGCTGGTCCGCTCAATGTGATGTTGGTGCCGCATTCATTTCCATTGTTCAAACTCACCCCACGCCGTACGAGCTGTGCAACGTCGCCACTGATACCCTGGATCTTTACGCGGCATTAACCTGGGGCGTTTGGGTCCGATCCTCGACGAGAAAACGAAAGATAGTCCCAGACAAACCGTTCAAATCTAGTCCTCTTTCACGGCAGTTGGGTGAGTGCGAGGACCCGGAGGAACGAGTGAAAGATTAATCATCATTTTGAACCGTCGTCCCAACTGTAAAAATCCACTGCAGTATTCGCATTTGAGCTCACCAGGTGCGGCGCAACTGACAGATGGAACGGCAGAACGTTACCTTTATGGGTCCGACTATATAAGATACGCAAGGTCGCTACTCGATGACTCGTTGCCTCGCGGCGGGGCTCATGTCTAGTTTTACCGTGGAAAGTATCCTAACGGGGATAAAACCGTTATTTATGGCTGTAGCCTCTGATCACCCTGAGTGTATTATCAGAGGAGAGTCACTAGGAACAATGAAAAGAGTCGGATAGCCGCGTGTTCGATACGGTGCAGAGGGTTTGTGATGCTAGGCGCCGATGGCCTCAATACGCATGGGGCTCTTCCCCGAAGACATTTCTGTTAAGTCGAAACGGATATATTGAACCCCGGCTAAGTGCACGAAGCTAAGCTTTATGTGTCGGAAGAGCCCGAGTCGGCTGCAGAAACCGAAGGATCCATATAGTGCAAGTAGGGTATAAAGTGTCGAGCGATATGGAAGGCATAAACTCTATTCGGATAGTACTGCAGGTAATGTAAGTGTCTCAGTGTGATACTTACTCGGCTTGGGCGAAATTTTGCCTTATGGCGCTTGTCTTGAAATGTAAAGATCATATAAAACTTTGCTAAATTAGTCGTGCATACAGTATCCTCGCGCGTCCACAAGATGCTCATCAACAACACGCGTAGTATCTCACATGGGCCCGGGTATCATATCGCGAAGAACAACCCCAGCTTTCGCCAGCTCAAAGAGCCCCATACTATCGTGGCATATCTCGAATTGCTAATGAATTAAACGAGAGTGGCCTGGTCAGAGACGGTCACCTTTACCTTTGAGATTGCCTGGGTGCTTCGTGATCCACGGGTAAATATCGCAAGTCCCAAGTCGAGTACGCCTCTGGGATTTCGACTCTCACGTGGTTTTCCTTATAGGGCGAGGGAGATACACGCCGCCACCAGCGCTCGGGAGCCGGTTTAGGCGCCTGACTACTCTTGACACTGTGAATGGATATCTTGGACCCGTGATGATCTCTCAAGTACACTCATCTACGGGGGGGCTTAGCGAGTCCCTTGGTATTGCTCAAGAGATACCCTAAATCGATTCATATAATGGAGCTCCCGTTATGCACTTCTATTCGCATCTCCAACCTAGCACAGGTAGTACGTAACGCCCTTGGGGAACCCAATCCACGAATGCTAACTAGTATTGGGACTTCCGAGCTGTTGAACGTAAATGGTACTGATCTCGATTAGACCGGCATCAATACCGATAAGGTTGAAGTTGAGCCGAATCCGGATGTCCGTAAGCGCGAGCGACCCCGGACGTCAGATAACGCAAGCGAGATGAATCCCTTCAGATTTATCTTTGCTTTACAGGGGTAGTCGGTTCTCGCGGCGCAACGAGACAATACGATCCCCAATAAAGCGAAGCGAGGCAGCGTAGTCCACCTCGCTATGTGTTAAATTAACGAGTGCGGCCGTACATCACGAAGGAGGACGCACTGCCTTCAGTACCTCGATTTCCGTCGCCAGCGCCTCTGACCGTGCGATGCCAGCCACGTAATACAGCCTCCATCGCCATGGATCGAGGGCCATTCAGAACTTCTAAACGTAGTACTAAATACATATTCTAACGGCGAGGTAACGATCCCGGTCGCAGAAACCGGTTTTCTCCCCCTCAATAGCCAGCACGAACTGTACCTTGCGTTAGTTTCTTGGACCGGCCGTCTTGAAGCTGGATCCCTAAAAATGGGACAGGCTGCAAATACTGTTGTCTTCAACGATATCGGTATCTTAGTGTATTGTGATGCGAGTGGCTCCGTTATGACTAACTCCAGCGTATAGATGGCTCAGAGCAATTTACTCTGTTAAGGTGCTATTTTCTAAAACTTAATGCCTATTAGGGAGAGCCTAGGCGGACCAATTCTCTAGTTGGAGCTAAAGCAGGCCTCAGGTGGAAGGCGGATTCGTCAGTTTTAATAGACGGGTTGATGATAGATGACTTGCATAAAGATGTTACTGTTCTTTCGCTCGTTACGTACGAAAGCGCTCGAGTCACCAAGTTAACAAAGGGCGATGGCCCGGCTTACTGTAAACGCCTATTGGATCAAAGGGGACCGCGTGTGCCGTGATATTTCTCAGGGATAGCTAGGACACATGCCTTTAATGGAAACTGACAAACGTCTCGCCCCTACGATGACGATCGTGAACAACTGCGGGCAAATAGCTATCGAGAATACCCTGCGACAAATTGCGGCTAAACGGTCCTCCTACTGATTAGATCAAGTTGAATATCTTTTTATTCGGCGCGGCTGTGCTCTGGTATCTAGTACCGTGGCAAGCGGAATACTTCTGGCTTCCTGTATCATTATGCAGTAGAGTGTCTAAAAGATAGTCTCTACGGTATTCGGGGACCAGCGTTATTCCTATTAGTGGGAACGTACTATCGGATGTGTGTAAATAGGCTAGGGCCGTCTGGTCCTTGCTATAATTGATCACGGTGGCCCATCGTGTGGTTTGACCGGCCTTGGGTGTGGCGCCTAGCTGTGTAAACCAAGACGTGACCATGACGCTGGGCCATACACGATTAAGCAGCAGCCTGAGTATCAGCTGAGGGTTGCCTTGGCTTAGAATCGTCTGTGTAAAGGAAAGAATAGTTTGAGCCCTTCGGTCGCCCAGCAGATTTGAAACATGTACAGTTTATCAGCATCGCTAGACCATGGATAAGCCGCCTGCTAGAACGCACATGAGTTGGGATTTGCCAAATCTTTCTGCAACGTGGGTTACACGAGTACGTGGGAATACATGGGTCCTGGGCGGACAACCCGTAGCCATAATTTGCCAAGTCCCCGTAAGGCCGACAACCCGCCCGATTTGCCAGCGAGTCGCACCTTGTGACGAAAAAATGCCCTTGTCACAGGAGGGGAAACTATAGACCGGATGCCCTAAAGTCGGACCGCATACCTCTCGCATGACCTACAGGGTATGGACCATACTGTGGCACGATTTAGGACGGTCGCACTAGACGGAATGCCTAAGGTAGCCACATTTTCGGACTCTGGTATGCGTCCCCGCTTAATCATTGATAACGGTCTGGTCTACCCACCTTTCATGCCTACAGGTATGCGATGCTCCGTCTACGTGCCTTGGATCCGCAACGCCACGGAAAACCGCCGAAATATCAACCTTGCCACTCCACTTCTCTTGCGGTGCCCCCTCCCAAGCGGATTGATAATCAGAGGTCTATGGTATGTGAATCGAACGGACGCGTAAAAAAACAATGACTATGTTTCCTTAGGGTCAAGGACCCACTCGTTTTGGTGTAAGTTGGAGTCTGGAGAGTTATCACATCAAAACTTTCGTCACATAGCTATGCCTCGGATACTTATATGAAAGACTTGGCTGTGCAAACGCTGATTCGCGACCCTCTGGGGGCATATGATACTGAAATTGCGAATCTATATTCCTTGATGGGACAGCTCGGTAAGGGGTCTACTGCACGTTCTTTAACTTTGGTGGATGCCGACACAGTGTAATATATCAAAGTTGGCAACCTCTTGGGCTAAAAGCTGACCCGATTAGGAGAGAGTCTTAAGATCCGTTGTATGTTTACTCGAAAGCCGTAATCTCCCCGAGCGAACACTCAGCCTACGTGAAAGTCATGACACTTGCCGCTCTCGAGTCGGCGTAGGCGTCTCATGCCACAGTTAGAGCTAAGGCACGCAGGTCTATTCCGACTATTGGCTTTGTCCTTGATTTTGAGTCTAGCCATTACTGCGGCATTCTTAGTTATGCAACAATACTGGGTGCGAACATGTACTCTGAAACCAGCCGCTTGGCCGAGCTCGTATCCGGGACGGCAAGACAAACGATCGCATCGAGAATAATGAAAAATAACAACTCTGATAACGGATTCTTAGTTCGTGCTCGGCAGTTTAGGTGTGTCGCTGTGAGAGTAGTCCCCCCTCTTTACCCGGTCGGATGCCCAGTCCCCCGACATTATCGGATGATTTATGAATATCACAGGGGAGTTTCAGTGCTGTGCGTGTACTGCCGGGGCGAGGTGTATCATAGATGCCCGGTGTAGATAGCTTACAGTGGGATGCGTATGAGGAAGGATGATTGAAATAGTGATAGCTCGAAGTGTCAGGCATTCTGCGATCAGAGACAGGAGGTTCGGTTAATGATGGCACTTACTTTTATCGCCCTTGCTAGTTTGTAGGTGACTGTCAAAACTGACCGACATAGCCTGGTCCTGTGGCTCCCAGGTCTAACATTAAACTCTTCCTCGATTGACAGGAAACCTTCTTATACAGTCGAGTTAGCTCGTGAAGAGGCCTTGAGGAGAACAGAAACCGATGCCTCAGCGAAACTCCTTAAGTGCTAAAGGCGTCAGCACATTATTGGCCACATGGTCGTCGCCAGTAGGTCTCATGGCAGATCCATGGTAACACGATCGAGTCGATCCACTTCACCCACAAACGTCTAAGCGCCCTTGGGCGGATTGGAGCGGCATAGAGAGCATTTATCACGGCTTGAAAAACTAGTCTATGGACCGGCTCAATCCAGGCGCTAGTATATGACAGCCCACCCCTAGTAGAACGCTTAACAGTTGGATGGAAGGTTTTTCTAGATGGGCCCAGAGCCGCAAATGCTTGATTAATGCGGGGTGGTAGGTCCACGTGTGAAGTAGATAATTTATAATAAGGCCAAAAGCGTGCTATCTGGTCGAAAATGCACGCCCTAAGTAGTCTATACGACACGAGCGAAACCCTGTTGCGAGAAATAGTGGCTGTACGTTACGGGTATCAAACAATGTGGTGCACACCCACACTGTACCAGTCCTTGCGTTGTTCTCGTGCCAACTTTGCTGATTCGGAATATACAAACGCACCCGGTGTGGCCCCGACAACTGTTGGTGCGTAGGCTCTACTTTTACAAAGCTGATTTTGACCGTTACCACATGTTACAAGGCTCCGCCGTTTCGCTGCCACCCGTATAGAAGAAGGGTCAGGGTTGAACGGACTAGGTAACAAATGAGTAAATGGTATTGAGCAAGCGATGAAAGTATTTCCCCGCTGCCTGCCGTTTCCATCGGTTACCGCTGAGACGGTAACGAGCTATCGGCTAAAGCGTCTTTGTCAGAGGTAATGTGCTACGTTTTATGTTAGAGATTCGGATCCATCTCTTGCTCACAGTATTGTCAGCATTTACGACGTCGCATGTCAGAGTCGTACTATTGCTCTTGTTTATATTGTTTGGCTACGAATTACTCAGATCATGCTCCAATGAGGCATTTCTGTCGATGCGTGACGACCCCTTCCTGGACCTATGATTGTGGGAGTGGTTTCGAGGGCTTCTGGATGACTTCAGTTTGTAGGAAGTTTGAGACGCTGGATTGAGGTTCGTTCCAATGCTCTAGCTCGGATATCCAGGGCCGTGGCCCGACACAAGATGCCTTCCATTCAATGGCTACTTCCCTCCGTCCCTTTTACAGCGATTGTTGTCTGATGCCCTCTAGGTCCGTCCGGACGCAACATCCTCGTTGTTCCTCAATCCGTACCCACAGCTCCAGTACGCTTCCTGAGACGGAGGCGACCAGGCTGCATAAGTGACGGAGCGCGATACCTGGTCTGGCGGGCGCCCACTCCGCAGCGCGTCATACGGCCATCGTCCGGGAATCTTTACATCCATTCATGGCCGGTCACGACGTCTTAACGCGGAGTCTATCGTCGTTATGCGATGTTTGGCGAAAGTATCAGTCGGTAGAAATGTAAGTCTTCAGTGATTACCTCGTAATTGGCTGAAGTCTCATATCTTCATTGGTCAGAACGCTCTTGGTTTCTCGCTGAATAATAGGTTTTTCAGTCAAGAAACGGCATCAGTGCTAATGTTATGCGAATCGCCATAGGCCGCCGTGCACCTGTTTATGTTAACTAACATCATTGGGGACTACCAGGATAAGCGGGACTCTGCGTTTTCATGCGCACGGTATCATCGACAGGCAGCTGACTGAAATATTGGTGCAACACGCGACATTCAGTGCCCACTTAGCCGCTAACACGTTCTATTCTCACCTCCCACATCCCTAGTAGTGGGTTCGGATCACCCACCTCAGCATCTGCCTCGACATGGAAAGATACATAGGACCTTCTCCGTAGGCCACCACATAAGAGTGCATCGCTGGCTCAAGACGCGAGTTGAGCCTCAACGAACATCTGTCAATCGCTTGTGACGAGAGCTATCCAGTACTGATCATTAGACCTGATTGTGCGTTCCTCTAGATTTCGTCGCTACGAGGATCTAAACGGTGCTCCGGGCCCACCCTTCCGCGTTTGTATCTCAATATTTGTACTACGCTGGTTGTCCCCTGAACTAGCCATCGTTCTAATTGAGATGATCGGGAGATGCTCAAAGCTCATGACATTCGATCCGGCACCCCTGGTCTCTAATCAGGAGCTCGGCGAAATCCGCCCTAGAACCTCTGCATGGAGGGACATGCAATGCTCGGTTCCCCAGGTGGCGAGGCTGGAGGGGCGATTTTCAGGTATCGTGCGCGTGTTTAAAGTACTGTATATTCCTCGTTGAGGCTCGTGATTCAAGGTGCGCCGCTACATTTGTAAGGTGAGCCGAACATGCCAAACAAGTACTTCAACTTTATCACTATTAGGCTTAGGGAAAGGTTGGAGTATCTTGGTACGACCCGCACGACCACCGACGGTAACAGGTGCCAGCAGTGCCCTTATTTTTCCCAGTACAACCCACATATACCAGCCTTAGCGCGCCATCAGGTGTTGTAGGGCAACTTACAGGTTACAAGCAAGGAGGAAAAGATTTATGTTAAGATCGAACAGGTTCTGTGGAACAAGGCATATTTGTGTATGAAGAGGTGCTGGAGGTTCACGCCTTAGTGGCCTAGCTGTGTTGAAATGCGTTCTAATATGAACTCTTTCTGAAAACATCCTGATGCCCTCCAGCGGGTATGAATATATAAATCGACGTAACGATCAGTCTGCACTGACTACTCATAAATAGTGTACCGTGATTGTTACAGGCTGAGAAGTACTCTAGATTGCAAATAATGTTACCAACTACTTGTGGTGCACGGCTAATGGCCTTAGTTATACCACTACTAACCATATGCAGGCTAGTTCGTCCGTCGATGTAAAACCTTCGTCATGACTCTCGGTTGGTGTGTTAGATCGACAGGGTCCTCTACACTGTAATGTTGATGTAAAACAGGGACGGTCGGCAGCTGATCCTCTCCCAACAGCCACGTGATTAGGCACGGCACTCTGTAGATGAACGTTAAGCTGGCCACTCGCAGGACTGTTCATCCGTTCAGTGCCCGATGTAGGTCCGTACAATTACTGGCTGGGAAATAATCGTCTGAATTGGCCGGGGCAACCCTAGGGTAATGTCGGTTACATGTACTCTTATGGGTTTACCCCCTTCGGACGTATCGACAGTAACCCTAGGCGCGCAGGACCATTTACACATACCCGCTCAGGGATAATGCAGAATACGGGTGGAGTTAATTTAGAGACCTTCGGGCATTACGAAGCCTGTTCGTCTCTCGATAGTTCGGGTGTCGATGGGACGTCAACTCCACGATGTATCGTCCCCCTATAATCCACGCAGGCTTCGCCTCAGTTGCTAAGCAGCGGGTCCTATTTCTTAGACAACGTTTGACAGGACTGAAGATCAATGGAGCAAAGTCAACTTAGCACCGTAATTACTGAGACGGAACGATTAAAACTGCAGGGCTGGAACTCAACCGGGACGAGCTGCACCATCTAGGTGTTGCCTGTCAGGATCATTGCATAACATCCTCCACTGAACTAAGAGAAAAGCTTCCTGGACCCGTGCGAAAACGAACCCACTCCGAGTTCCTCAGAAGGAGGCTCCTGTTCCACGATAGCTTTTTTCAGTCAACTTTCGACATTTACCATCTTAATATTCTCACTACGGCAAACGAACCTTATTAAGATGTAATTACCTTCTTCGGGTTGATATCTCTGAGACTATTCCTATTACCCGGAGAGTCAAAGAAAGGGCATCGTAGAGACCACTAGGAGCAACGACGGAAACTCTGACTAGCGCGTAGGCCGCTAGCTATTCCTTAACAAGAATTCCTCTAAATGGCGTGCTACAACTCGCTTCTCGCTTTCATTAGTAGAACGCTTAGAGTCCGGCAAATCTGTTTTCCGAAAGTCTTGTGCACTCCCTGGTCTCCTCTGTGTTTGGTGGAGCTGTGGATTCTGACTCTACAGACCTGTAGTTCAGCCCACTGTAAGACGTACCATCCGTACCCCAACCCGAGGATCGGATGGAGCCATGTTGGTCAAGGCTAAGCAACTAATCGCGCTTGAGCGCACGAAAGCAAACCAAGCTGAGCCGAGTGAGATTCGCATCTGACTTGTGTACCGTAGCGGCGGTATTTACCATCCTTCCCGCGGTCAGCCATGCACGAACGCCCAATAGGCGAATATAGTTCACGGTGCGTCCCGGCTATTCGGGCAATACGCGCTACGCCTAGCAAAGAATGGCTGGTAAGTGCACAGCGCGACGTAGCAAGATCAAACTTGGATTGTACAAGAATTATACTAGGCCCCCCGCACACACCCCGAGACAAACCACAGGTGCTTAAAGATCGGTGTCATGTAGCGAAGCTGGGCTTATACACCGCCTCGCATAGGTCCCCTCCGCGATCTAAACCCCGAATTAGGGCTACGCCCCATCTCTCCGTAAAACTACATTGGGCTTTATAAGATGTGTACGGTCAACAGGAGAGCCGACATGGTGACAGGCGCCTCGGCGTACGTGTTTTTTAGCGTAGGACGCAGCAGCGCGCTGCCTTATCTTCACATTGGACGCGGGTATTACATGGGCTTTATACGTTCTAAGGAAGGTGAGTCACAAGCAAACACAGTTCGAGGTCGCGAGAGCCCCAGTTCTTCGAAAATCTGTGTCTGCACAACACTCCTCCCGGAGTACCACAGCCGGGGCAAAAATTGCTAGAGATACGGGCCGACCAACGACGCAGTGTTACGAGTAGCCACGCTTGCATTACTTCTTGACACCATAGCACAATGAATATCTCACCAGAGTGACATTACCTTACAAATAAGACTGGCTTACACATGTTCACGACCCCAAGGAGGGGTTGAGATACGAATGGGGAGCTGTAACGGCAGGGGCTTAGAGCCTCGACCCCCTGTACCTCCCATTCATTTTTACCGGATGAACCTCCTTATCCTCCTTAACGACATAAGCTTAAGTTGAATTGACGGCGGGTTCGTTGTTCATTGTGATCTGCCACCCCCCCAGTGATGGATGACGCCAAAACTATGTTAAAGCAACTCTACACTGTGTATGCTGTTTAAACCATGGGTTCCGATGGATGCCGTTTTCTGGGCGCCCCTCGGCAGCTCAGGCACTCGCTGTCGCCACGACCGTTGGCATGTAGCCTGTGAATTCAGGCATGTATCTAATGTCAATATTAGTGTACGGGTGTAGCGTAGTAAGCGCCGCTGAGGCGACCCCAATTGCACGTGTTAGGCTAGAGGAATCCCATTATAGCAAGATCTCTGAGAGCTAAAGTCAGTGGGAGATCAGTGTGACTTTAGCGCGCTCGTCGAAAAAGTGCACCCATCGCTTTGTTCTTCCTTCTTAGTATATGTGTCTGGCTAGACGTATATCCGGCCGGAATAACCGTCACCTCCGGGTAATGCAGTTAAAAATCAAGCTGGCTTCGCGGCTCTACAGCTTCTTAAGTGTGTTGAAGTCGCCGCCCGAGACTGAGTTACGACTTCCCAGTCGTCTTTGGATATGTCTCAACTAGGTTCGGGTAAACTTTAAATCCAACAGTTCAGGTTGTGAGACTAATTCCTTTGGCCTAACTCCTCTAAAGTCACTAGCACCCCTAGTGCTAATCCTGTTCGCACCATAACTTAGGTCAATCCTTATTCCGATTTTCGCGTCGGATCTCGCTAGAGGTATTTGGTGCAAGCATTTCATCAGATAAGGATGATGGAGAAGTTGTCCCTGTTAGTAAGTCTCGTGACGGGTCAGACCGACGGGGGGCCATCCGAATGTCTAACATACACAGAAGAGATGTCCGACCCTGGGATACCGGCTATGACTACGAGATTCAGCCGAATCAATCTGGCCAACTTCATTATCGTGAGCTTCCATTCGCAAAGCATGGGTGACTTAGGTAAGTCTAGATTTGCGGGATAAGTTGTCTCCAATGGCGACCACATCAGGTCACGTTCCCATTTCTAGTGCAATTTTATTGCCGTATGTATCTATGTTGTTACGTGCCAAGCAGGCTTTTCTTGTATCTTACACAACTAAAAAAGATATCACTCTCGTTCAGAAAAGAGCAACAGGGTTGGGAGAATATGGCCACGTGCGAGCTTCGGAGAAGCAGCCGTTATAGCAATGCCTAGACGAATTTACAGTATTCGCCGTTAGTTCCTTCTGCGATGGAGGAGACAAGCAACTTGTCAGCCACTATCTGCAAGGCCTCGTAACATTTCTGTCATGACTATTGCCGGGGCGGCTGGTATTGGTCTTTCGAGGCTTGTTGGACCAAGATGACCAGCCGTCTTCGGACGCCATGCACTGGACTTTTCCACACACAAACGAGCCTCGTTTCTAGGATCGAGGTCTTGTATGTTATTGATGATCCCGAACTCGGGTAAACAGATCACGGACGAGGCCCTTGGAAGACGCCCGGGAGCTCGGCGCGGGTTCACCACGATGAACCATCAGTACCTGGCACTGGCCTGTTGTGTATCAGTTAAAATTCTCTGCGCGAATGACTGGTGCTATACCGGGATACTAGACTGTCGACGGTCCTGAATGGATAACGACATGGTCGTCAACAGGCTCTAACTGGTTATTACCAGTCACCCAAACATTTTCTTGAGTCGCGCTCTACGTGTACGGCTTACTCCAATACCATGGATCATACGTTAGTCACTGTGCATAGTGTTAAGTATACTCGAGCTATTTTCGAGGTACGTCCGCACCCGTTCTACCGCCGTAGGATTGACCGTGGTTGGCTCGCAACCCTAGCAATCAAAGTAGGAAGGATTGGGCAGTCACTTATCTAATTGGACTAAAGGGAATACGCTAGTCAGCAACTTATTGCGTACGCTGACTCTGAATCGCGGCTCGAAATACCGCGACCCAACGTCGGGGCCACAATGACACGGCGTGTGGGAAATCTCATAACATGCAAAAGTGCCACAGGTGCCCAAAGCCATAAGGCTCTGCTTGAGACATTGGGCAAATCGGACATACCATTCATCCCACTTTCCGGTTTTGGCGGGGGTATATGCTCTTGTGCCGTCCTCTTACGCAGATGGGACAGAGCCGCCGGCACGTCTTGTATCAATTTAAGTTCATGCCGCGTATGCGTAATTGTAGGAAGAGGGGGTTCAAAAAGCCGCTGGACCTTGACGGTCGACTCATATAAAGGCACGGCTCCGAATGGGCTGTCTACCGCAGATTCTCAATCGCGAAGTTGGACGCATTGGGTAAGGTTCTAATTCGCCTCGTAGAGCGATCAAGGTTGTCTTGTACAAATTGTGAGCTTGGCACATCGCCTGAAGAAAGGCATGAGTGTAACACGAATACTAACTGTTAGGTGGTGCTTGCGCTCATACGATAAAGCTGCAACCTAAACGTTCCACGTGGCTAGTCTAAGAATACGGTAACCCCCTGCGCTCATGAACCCGCTGCCAACATACTGCACTTCCTATGTTGTCACGTTGGGGTTACACAGATACAACAAGTCTAGCAGAGCCGAGACAACTCACAAACCGATACGTAATGGGGACCCGCTTATTTTTCCCGAACAAGACAGGAAATTACTGAGGATTAAACAATGCCCAATCACAAAGAACTAGCAGGGGCAACGACGGCCTTTGAAAACTGATCCAGGGTTTAACGTTATTTCCTGCGAAGACTGTACTCGGAGTCTATATGGGAGACAAGTCGCTCCCAGTCTGCCTCGAAGTAGTGCATTCGACCAAGGAGATCTCGGATGCGGTTGACGCTCTGAAAGTGCTCGGAGAATAACTCTCGCGTAACTGAAGGATCCCCACACCTCTACGATAGAAGGCCCTGGGTACACTGAAGCCAGTACTTTGCGCGTAAAACCACGAAATTAGGAAGTTGCAATCAGATTTCTCCTCGGGGTGGCTTACGCGATCCGATTGTAAATTTGCCTGCCGATAGATTCACAGAACGATTCGTTGATTCACCGTATGGCGGATTCCCATAAATCCCGACTCCCTTGCATATGCCCGAGGGGGAACGATGCTGCCTGGATTTAAGCGTTTTCATTTTAAAGCGCCGGCCTAACCCCTTATCGAAGTATCAACGCAGTACGCTTATAATCTTAAAAAACTGGTTGGTCTGCCTGTAACGGCAATACACCATGACCGGGGGCGAATATTTGCGACCAGTTTAAATAACGTACAAAATAACTTTCACCCGTTGCCATGAGAGCAAAGTCTAGAGTTCTAATCAGACGTGCCAAGAATTTACCTGAAGCTTAGTCCATCCCTCTTCCTTGCAGATTGGTACGGTACTACAAGACGAGTCTCTAAGTTTCTCGGGAGTATCACCAGCCCCTCGGCCACTTTATTGCGATATCGTTGCAGTATGACTGCAACACTGTTCCGACAAAGCGTTGAATTGGCTGTTGATAGTTCGGCTCACAAACTCTGCCACAGTCCTGTTTGACGAATCGCTGTTGAGCTGGCTCCTCTTATGACGCAGCGCCAACACCAGACTGTTAGCGTGACAGACTCTTTTCCCTCGACCTAAACTCAGCCACCTATGTCGTCGTGCGATTTCTGCAGGCAGACCGAGTCGGAATTTAAGCGTACGGTGATTTCAATAACGCGCCCAAACCGGCATGTACTCACCGGAAACTCTCCCTGTCACTCATTACGGGGGTGTCCGTGTGGACCCGGCCATCCGTGTCTTAGCAGGGCCCACTGGATACGGAAGAGCCGTGATAGTCGTGATTTTTTGTAGCAACGGGAATTCAATATGCGGCAAATAACCTCATGCCTACATATCCCAGAGGAAGACGCGCGCACGACTGGTTCGATCCGCCGACCTGATTAGTACCCTCCGAATGTGGTAGTAACCCTTTGCGGTCCCACCTCTAACTTTGCTACTCGTTGACCTCAATATGACGTTCACGGGCCATTTGCGGTCCATCCCACTAGTGGCGTTCCTTCTGCCATCTTGGTGGCCAGCCTAGTGCCAGGCACCCTCGTGGCAAGTTGATATGTATGTTTCGTGGGCTAGAACAGGGGGTCGGCCCACCTCGACTACTAACGTAGTTTTGCAGACTAAGCTTCCTGCGCACTGACCTTGATAATATCAAGTCATCGGCCGAGGAATCCGTAAGGGGTTCCCAGTTATTTACTAAGTCTCATCGCCATGCCCGCTTGCTCAGTTGCAGGGCTGAGTTCACCATTGTTATCGGTCACAACATGCCGACCGAGATGAATGCGTTGTAGCGCCTTTTAACTGTTATTCTACTGCGGTTGGGACGTCGCCACCTTGGTGGGGCTCTTGATAATAGACCTAGTATGGAAGGATTTCTCAGCTGACACTCACCTATCACAACAGAGGCCCTAAAGACAAATGTCCCAGAGTCAGTCCTATAGGCTGTACCTCAGCCATGCGTCGTACCATCGTCAATGTTCCAATCTGCGTAAGCGTTTTAGGTACATGGGACATGCAACAGTCCGCCAACAATGGAGTTGGCTTTCTTGGCCGAACAAAGTGGAGGTTTTCACTAGGATCTTAAGTATTATCTCACTCTGAAACAGTATGCCAGCGGTACGACCCTACGGTGGTTGCCGTATTCGCCGTTCACTGCCATTCGTCTTCTGAAGAGATGGAGTGCTCGAGCCACAAGTATTACAAACGTCGTTAAAGCCTTATGGGACTAGGCCGTACCCTGCCGAGTAGCGATGTTTGTCTCGCGCGTGTCCGGCCAACGATGAGATCAAAAGCGGTATTCTCTACTCAGCGGTACGGCCGTACATTCTGGCACCTGAATGCTTTTTCTCACCGGAATTACGACCATTGAAACCACTCCTCGCAAGGAGGACGCATGCTCCGACGATTGTGAAGCGTCCAACCACTTCGTTAGTTACGGGGTCTGGACATCCGCTGATTTATCGGTATATGATTGCTCGTAAACTGGAGAACTATTGTTCTAGAGCCGTTTTTATCCGATAACCGGCAAGACGGGGCAAGGGTAATTTACCGGCCTCTGAGTCAGCGATCTCAATGTTGCAGGTCATCACCTCATGATTTTACAAGGATCTTCCAACTATTATTCGCGCCGCAACAAGCCATAATAGAAAAGTCAGTATTCGAACTATCGCGCTAGGGTGATCCAGAAATCTACCCACCGGTGCTTAGACGTCCAAGTACCCGCTCTTTCCGTGTCGCAGAAGTTCAGCGCACGCACACTACGCCGTTAAAGTTCTCCTGCCGCGGCGTGCACAAACATGGCGGCGAACGCTGGGATTCTCGCCAGTTGGTGAAAATTCTCACTTCGTCTACGCAATCTGACGTTCTCCGCCTAAAGCTCATCTATTTCTCCTCCTCTGAAAGTGACCGGAGACGGAAACAGACATCGGGAGGATTCCTTGCATCAAATCTTCGCTAATTTAGCGAAGGATGCAACTAATAATCGAATTATTAAGATAGTCCACGTCGAGTGTAGCCGATGTTACCCACATTATACCCTAATCCTCATCTGCGCAGGTGTATAGATGTTTACCGGCTACTACTTTGATGCGGCCCTGTTTACCTATGGGAATCAAAAAATGCATCCCCGGGGGCCAATTTTCATCGCATCCCTTCAGGTAGGCGACGCGATCCGTTTTTGACGATATCCGCAGATCACGGGCCGTGGATCTCGCAAAACATCATCCCTGCAGCGACTAGCCTACAAGCGATCTCGGGTAGCTTCTCATTTGATCAGTCTGCAACGGGTACAAATTTCCCACGAACATTTCACATCGTTCCTAAGACTATGAGCCACCTGTGCATATCCGCACTATCAGTGTACAATCCTATGGGGGATTTTACTCAAAAGACCTAATCTAAAGTAAGCTATATTAGATCTGTAACAGTTGAAATTTTGGATCGACGCTCCCGGAACAGAAGCGCGGAACGACATGTAGGAATTGTATGTACTGGGTACCCAGATCTATCTGACGGCTACTCCAGCACTTTATAGGGCTTGGCTGACCCCACTGGACTTGGTAGCTCAGTTACGTCGGCATAGTTTCTCTTGCAGCATAGATCACCACCTTCTATCGCAGTGTAAGCTCTGTTCATATCGCACTCCTTGAATGCGCGGCTGGTCAGGCTATAGCACTCTACACCGGTCGACTCAATTTACATAAACTTGTTTAAACATAGCATACAAGGGGGCTGCAGTTAAAAGGCTGTAAATCGGTATGCAGGCCACTTGTCTCTGATTGTGTACACGCTTTCATGATTCAGCCCGACGGGCAAAGATACAGAGTTCGGAATCCCACATGGGGTACGCTTCTTCGCATAGGCTCACCCGCTAGATTCTGAGTATCCAGAGTCCTTACCCGATACTCGTCATCTGTCGACGAGACGTTCCGTCTCCTCCCCTCTGGGATTCCATGTTTAATTACTGAAGTGCCAACACATTCACGGGTATGAAAGAGCCTCAGTCCCTAGACATACTAGGGGTGACAATCATGGGCGGCCGCACCACTATATGATGCTAGGGACCCGGTTTGATCGTTCGTTCTTTGATCGACCACCGGTTCGAGCGGCATAAATATCCGTGCGTTCTGTCATGTCCGCAACGTGGTGACCTGGAGGCTATCACCCGAACTTCGGTCTATAGACTTGGTGAGCTCTCACGATACGGCGCTCGCTGTGCACTAGAGCTAGAACGCAGGCGTCTAACGCTTTACTATGGTTAACGAGGCGTGCACCGATTTGTGGTCCCAAAGCGTAGTAGGCCATGCGCGGTCTGGTATATTCGACGTGGTTTGCCCGTCGCAATATTCGGAGAGCTTCAGCACGATGCACTTCCCTGGCAACGCACCATATCGAGACTCCTCTTCTCATACTGTTGAGTGGCTCCCTGAGACTTTCATCGTGATGCAGGAATTGCAATATGCCGGCGAATCCCAAGTGACTGCAGGCTAATGAAACAACTCCAACGCTTCGATTGCATGCGTTGCACCGTTCCTTACCCGTAGCGTGCCTGTAACAAGTGGCTACAGTTTAAACAGGGATCCTGACTTTTCTGAAATATGTATGTACAAAGCCTGCCGTGAGTGGCCGCATCCTAAGTAACGCATGTCTTCCTCGGCACTCGTGCAGCGTCTATCATCCCTTGGGTAATCAACTGACGCGTTAAGTGGGCTCGTCCGAAAACGGGGGGCGCGCGGACTTCTTCACGGTCGTCGCACTCTCCCAAGAGACCGCAACCCAGTTAGCTGACCTGACAACCGACGCCCCCACTGCCGATTGCAAGTCACACCGGGTTCCATCTATCATGAGTGAAAGGTCGCATCAGGGCAATGGGAGCTACGAGTGCGTGGACCGAACGAGGCCATATTGGTAAGCTAGACCTGGCGGCAACCTATAGGGGCGAACCTGATTATTTGTCAGTATGTGGATAAGAGTCGCGTTCTCGAGGCAGGCCCCGCAACGGGCCGCCCTCGACATTAACTTCCACAGCTAGAGCATTGAACTTCCCGTGATAACCCGATAATAGACAGCTCGACTGCTCTTTAGCACACATTCACCTCAGAGCAACGATCAGGTTTGGTATATAAGGGGAAAGTTTTGCAGATGTTGTAAAAATGCCCGTCCGATCCTTACATAGCCAAGGTTGCGAGGTGGTGCCAAGTAGATAAGCGGCCGCGGGGTAGACGTCGCCAATTAACGGGAATAGTTCGAACGTCGTCAAATGTCGGCAAATATTTTTTTTGAACACCCTCTATATAGTTTATCGACGCCTGATAAATCCGCTGTATCGCTTACTAGTATCATGACAGATACTCGCCAGGCGCCCCTTTATGTCGATCACCTACGCGAGTGCGAATTCGGAACTTAAATGATGGGCAGCGTGGCATCCTCTAGTGGACCATAGGGCGCTTCCCGGAGACAGTACAATGACCGGCTGATTAGCCACCACAGCCTCTCGATGAAAGTGCAATATGCTGGATCTTGCCGCACACGCAAACACTTTGAACTTTAACGTGGGGTAGTCAGAATATAGGATAGAACACGACGATAGACGACGACCTGGGTGCCACTCACCTCTATATGTCTGGCGCGAGACAGCCGAACTCTACGGTGCTCGGAAAGGACCCGTTAAAATGGATTGGTGACACGTACACCCCGGTCGCTCACGTCAAGTGTATCGCCTTTTTCCCAAATCTGTTCGAATCACAAGCTATCCTTACCGTCCATATGATTGTAAACCAGTAATATGCGAGGACGAACGTGTGATAAGCCAGATTCTGGAAGTTGGACTAGTGCCAACGTCGGGCATGGTAATCAGGCACAATTGCACCACAGGCTCCCCTGCCCATTACATGAGGTTTTTCGTGTTTTCTCCAAGAAGGGTCAATGCCGAATACAAGCAAGACTCCTGTAACAGCTTGTATGAGTTAATGTCACATCTTGGATCGTGAGCAACTACCACCACACATCAATGACTCTTCCCCGGTGGGTCGATTCTCAGTCCGGCCTGAATATATATCCGAACCGCTCTCCGGAGATCGTACATGCGGCGCCGGAAGACGTGTCCGTAAACCCGGTATAGGCCAGACGAAGCTTTAGTTCTCTGCCTGCACCCAACGCGCTCGATGTTTATGCCATGCAACGTAGATCCCGGTTAAACCACATGTGGTTGCTTACTTCTGTAGCCTCACGCGATTTTACGCACGACGGCCCTATAAGTCGGTGGTATCAGTCTTCGTGACCAAAGTATAGTTTCCCCTACCTCGCCGGGGATCATAGAACCTTGTGCTGTCATATATCCCCATCACTTAGGGACGCACTTGCAGCGCAGACCCCGCCAGTTCATTCAAGCCCCAAACCGCTATAATTACTCAGGTCGCTTCTTAGAGCTCGTGACCAACATAACAGCGTAGTAATAACACTTGGGAATTCAAACTATACTCCCCCCTTGCGTACAGCCCTTCTAAACGTTATTCTATTAATGGTCGGACGCCACGAGTACAAGCAGTAAGAAGAGCCGAGACGCCGCCCGACAGGGTCTAGTTACTGGCCTCCAGATGTTAATACGTGCATTTCCAATACCTCAAAGGGCCAGGCAGCGGTTTTTCGACGTCTCTACCTTCAGCTCTGGTGAACGCCTTTGCGAATCCGGGTCGCCCGGTCGACGTTTAAACCAGTACGACCCGCGATCTCCTTGTACCTTGCGAGGCTTCTTCACTGCGTTCACGCTACGTTCGGTTTTCGCAGTCGCTATGTTGCACAGCAGGTTATATTTTGTCCCCAGTAGATAGGGCTCGGCCGATGCCATACACCTTCTGAATGTCGTTAACTCTGTACTCACCCGCCGACTCGAAGATTTGCGATGCTCCTTGCAAACAGTCCCGGACATAAATTTAGGTCGAGGTAAGGGCCTGAGAGGTGGTTAGACAAGCAAAGGCGGCTTCGAACATTCCCTGTAGCTAAATCCGACACTAAGATGGAGGTGCTTGGTTGACAGTTTCAACAGGATTAGGAGGCTATGCCCGACTCCCCACCCATCCTCGTTCTTACCCCAGGTGGCCGCAGTAAATCGAACAATAGGCTCCCGAGTACTAGCTGAAGGAACCTTCGCGCTCCATAATGGCTGGACTATAGTCCTCACGCATGAATACTATGTCGAACCAGGGTAGTAAAGTGCAGTGGTAGCAGTAGATCTCAATATCACACATGCAATTCAAAAAGGCATATTCGTGCAAGGAGACACTTTGATAGTGACGGGAGAGAAAATCTAAATGTGAGCCCGATATTGGTATTTAGATCTGAGCCCCTTAAGAGATCTAATCGGCAGAGTCCCTCAAAGCGGGAACACTAAAAAAATCTGCAAATCAAGTGCGTGGCCAGTACGCCATAGAAACCATGTAGCATAAGGACGTCAAAGTACGGTGCAAAGTGGAATTGTAACCCATGCTTGACGCCTTGATACCCTACGCATGTTCACCTCTCGAGGTGCTCGACACCAACAAGCCATAATGAGGCACGATCCGTCGGTAGATCGCGCGTTGTAGACGGGGGGGGCGTTGATCACGGCACGGATATACGTTTGCGGTGGCTCGCTTGCTGGAGCTCCGCTTCCACATGGGGGTGGTGTTTCCTATGTCCTAGGGTCGCGGCCGTCTCGTTACCCTTTTTCGCACTAAACCTTGGAGGGCGCCGTCCGCACTGAGAAGCTCGATGTCTCCTGCGTGTTCTACCGTGAATACGGTCTGGTCTATCCCCTGACCCTGTTAGAAAAGCAGTTGGGGGGATCAGTCAGGATTAGGGCGAGAACTGAAGGGAATTAGTCTCAACGAATGTCCGGCCTCCGATGGAGCAGTCGGGATGAGTAAACTTCTCGAATGATTCTCGCCTACTGGAGCGCTACACACTGCCTGGAGCATGGACCTTGCATCCCGGTCCAGTTTCTGTTGCGGCATCGAGTACTTCCATAATAGTATGCTCGGAAGGAACGCTAGGAGCGACGCCTGTTTTTCTACCTTGCCGGTAGACCGGGTTGAAATTATTTCAGATGGGTTACACGACATTGATTCGGCTTACTTGTCAATAAAGAGTGATTGGCTGTGTGAGCCCGGGATATCGTCTATGAACTCATATGTTGCGAATACGGAGTATCCTATGGATACGACGAGTGAAGGAATATTATTCGTCAGTATTTGCGTTTACCTGAAACATAGGGTATACCCCGCACTGCAAGAATGGCCTACGCCCATGGCTCAACGGAGCACCTCCACTCGACTAAAACAACAACGCTTGGGGCGATACGAACGTGTCCTACTACCGGAAAATTATTCCCACCGGACAGAATGTTTCCTACGCACTATAGCGCCGAAAGCATCAATGTTTCCGCCGTATTGCTGTCCATCACGCAGAGTCCCGGGCGAGCCTACAGCCAGGTCAGAGACGCAGTCTATAGCTACAGCGACACCAGGGATGGGGTCTAAAAAAACAACCCAAGTGAAAAGGACCAACTTACTTGCTTCTACCGTCGTGTAGGCTATGACACGGATGCTCATCATTTGTGGAGTGTTACTAGGTAGTAGCTCAGGCTCTACGGAGGTGCACGAAGCGGATCGAAAGTTTTCACACAGTAGGAAAGGACCCTCTGAATCTTTAGATCAGGACTTTCGCGAATGAAGAGAAATGGACTATCCATTCGTAATGGTGCAAATTAAGATAGTAGTCCACTGTACGCTATCATATTGCGGGGTGCTCAGGCGTTTAGTCACAGTCTCACAGGACCGTCTGTGTCAGAGAAGGTAAGGATCTCGTGTCCGACGTCCAGCTGCGTCGGACGGATGTACGCCTCTGGCATTCATGGGATCCCGGGCTTATTAAAGAACGCGCCATAATCTTGAGCACTATCCATAGATTGTGTATCGGACAGTCTAGACATTCGGCCTTGAGGCCTCGGCGAACGTGTTACTAACAACCGGTGGCAGAGACCGACACAGGAGCTATTGACTTGCTGCCACCGCGGACAGCCCTTGATCGGCGTACCATGTACGCCCTTATTTTCTTACTCACAACTCGGAGTTTGAAGGCATGATGCATTACTACCACTTGAAGGGTATTGTTGGTGGCGCTGTTTTGGCAGTACAGATATAAGCCCATGAAAGCATCACAAAGTTCACGGGTTGCCACCGCGGCTAGGTTGAGGTGGCAGTGCCTTCTCTCCTAAGGCCATTCTCCGAGTACTGGGACGAATATTGCAAAGGGTCAAAATTTATTGTACCCATAGACATACGAGACTAGCGTATTATTCCGACAACGACGGGTTCCGTGACGCTACGTGACTAAAGAGAGGAGAGATGGCAAGGTGTACGCGATGTGAAAGGTAACTTACTCCGGTCCATGTGGCAAATGTGTGAGGATCTGTAGTAGAAAACCATATAGTGTAGATGTATCTCTCACAGGCTCACGCACAACTTAGCGTATCAGTCTACAATCACGCTCTTTCGTGCGCCAATATCCGTCACGGGCCCCCTACCTCCTCATAATGATCATCTACGTAACCCGCGTACTTGACGCGTCTGGATACTCCGAGAGCAATAGCGGACGGGATAGGATCCCAGTACAGGTGGCAAACCCCGTCGGCTAAGGGCTTCAGCATACACGTGTCGACCCTGAATCTTCAATTTTCTGGAAGTAGGTATGTATCCTAAATATGGACGTGCACGAGGGAGAAAAAGCTGGGTCAAACAACACAGCCTCCCAGTATACATAATCCGTCCCAAAAACAAAAGGCTTTGGAACAATGGTAAGGTCGTATTCAGCGTTACTATGCATCAGTGGGACGTATTGTAAACCTTGGGTACTTAGAGCGCTGCATAAATCCGCGGTCAATTTCGGCAGCTCGCTTCTCGCTCCCCATGTGGCAATCACCAAAGCCAGGAGCAGTCCATCTGTAACGTTAGCACCCAGCGGGTGGTAGCTCACCGTGATACAACCCGAGTTGAGATTCTCGACTTGATAACCAGGAGAGCTCCTGGGATAGCGGGGACATCTCCTAGTGCCTGAGTTACAAAACTGATGGGTTAATCCGTCGTCTCGGTAAGCATAACCCCCGCTTGTCCCCGGAATATTTTCTTGCTTGTTCATTCCTCACTTGACCACAGTCTGTAGTTGGCTGATGCGAGTCAATGTCACATTGCACATGAATCTGAGACTGCTTATTAGTAGTAGAATGGGTGAGATTGATATACCTCTGGACTTCCGTGCTTGCCGAAGAAGGTGTTCATGACGGACGCCTGGCAAACCCTTAGCCGTACTTTCGCGTTATAGGGACCACTGCACAGTTGCCCGGCACCAGGTCTGCCCCGAAGTGCCAGCTAGTCTACTGTCTCACCGCCGGATAGCCGTCGTAGTATGATAATAAAAAGTAGTCGCCACTAGATATATCCCATTTTTTCATCGAACAACCGGTATTGCCTTGCAGTTCGTTTTATGAGCTCTCCATCGAGCTCTCCCGCATTTTGTCCCCTAATAACACAGCTTTACAATATGTGCGTTGACAGACCTAGCTCTTATGCCTGCTGGCCTCCGGTGAGATAAGTGGCCGGACCCAAACTCGTGCAGAGCCTGTAATTGCACGACAGCGTTGAGACGGACGAGTAACGCGGCAAGCATGGGTACCACGCAATCCGGACACCGTACCGATGTCACCCGCACCCGCAATTACTCCGATCGAGCGGAAGGGAAACGGGTCTCTTTCACTGGGGAAAGTTACCCGATAAGTGCGTATAGAAACCAATAACCTCACGACCTATTCTCTTTCCGGCCACATCCGGGGGATAGTCTTGCTTGCAGCCGCGGTGGACCTGTGGGCTAATATTTAAGAGACTCGTACACGTATGGGGCTAAACCGCAGTCTGGACGAGAGTTCGCAACGATCCGACGCAAGGTAGGAGGAATCGGTCAATGACACGATCAACCCCACTACGGGCTGAATCCGAATGCCTGGAATTTGCGGCGCTGGCTTCGACTACCTTATGAGCCGTGGTGGTGTCATGCGAAGACGGCATCCCGCTCACGACGATTACTTAATGTATTGGGGGGTGTGACTAAGCGAACGCACGATCGACGTCTATCCAGATGGATCCTTTCTCAGCCCTGGTGTTGGAATAAGACACCAGTACGATAACTAGCAGGAGACGTCGATAACAATATTTTATGGAACGACTCTAGAGAGCGGGACAAGCAAATGGGGTGACGCACGTTTACTAGGCGCGGGGGGAACGATCGTCCAGTCTGGCGCACCGAGGTAAATAACCGGCGCAGCTGGCCGGGGACATGAAACCGCCTAATGCTAACTCCTGTCACGAGAGAAATTGGGATGAGTACTGGTAGTTCTCTGGCGACCAACGCTGTGGAATCGCCAGAGTATTCTTTGAAACGGCAATTAGGTCAAGAGTCGCCGCCCGCGCTAAAAGCAGTTTGCGGAACACGCGCGGAAACAAGTACGGGACATATACTTGCGAGCAGTGGTGTTCCCCATCAACAGATCAGCGCGGAGACGGGAAGCCTCGACTTGTAGCAAAATTGGACCGCCGGGACGGCACTCGTTTGTGGCACAACTACATCCGTCATGGATTATCGGGGCGCACTCCTGTGTACCGATGGGGACCGTTACTTTGTCGTGCTGGAGTACCGCTTCGTGCCTCCCTTGCCGAATGTGAGCGCTCAACCACGAAAATGGGTTTTCACCCGCATTCGTCTCCTCTTAGCGTAGTGTGGCCACATGCTACGTATTGCAGCAGTGCATATACACGCATATCGGCCCCATATCTCGGTGAGATTGAAAACAGTCAATCCGCTTTTCTCTAGCTTAGATAACCTGCGATCTACGTTTCACAACTGGCGATTTAGAGACAGTGTAGAAGTGTAAGGCGTACGGCGCCACCCTCCTCCTCGAAGATAAATTCGGGTACACAAGTTCAAACTCAATCCAACACCCAAAGCGCTTACGGGAACGAAGTTCTCTCTGGGGGTTCTCTGAAGGTCCCTACCTTTTCGAAAAAGTCAGGGCTCCGTATAATGGAGTATCACCGGAGAGGCCTCTGGCTTGCTTTTTAGATAACATATCCAAGCCAGCGTATCCGGACAAGGCGGCTACACCCCAGATTGTATAATTCACCGGCCCACATCACGTGTGGCCTGCCAACCCGTAGCCGTGTTGAAGCACCCTCTATATGGACGTACACCCCTCGCCAGGTATAAGCGTTGAAATAGCACCACTATTCGTTCCCCTATGGAGCAGAACGTAATTTTACCAGCCCACGCACTTCATGCTACCCAGACTACTTGGTGATAGGCACTATTTACCAGTCCAGATGTGTATCAACCACGTTTATAGAGCATTGTACCTGTTGGGTATCGTCCTATCTCCCGTGGACGCGCCTGCGGTTGCGATTGGCTTCACGAACGTCTCCGATGGGATACTACCAAAACTCTTAATCAGAGGGTACAAGGTTTGAAAAGGAGCAAACTAAATGAGTTAGGGCCCTAATTCAACGGAGTAGTAGCACATGCGCGTTCCGGAATTTTTATGCCCGGCTGTCATTATACCTGACTATTGTTGTCAACAAGCGTATTCCAAGGAAATACCTAACGGCTTCCTCCGACTCCGTTGACAGTGTCCTCCTCGGTACATGGTCGCTGTCAATGGAGATCTTCGCTAATATTTTATCTTCTCCTGTATTTCGACCGTAGTATATAGCACCATTCAGGCACACCATGGAAGAAGGGCCACTTGGTCGCTGGGGAGTGCCGAGCTAACCCTCGTCTTCACAGTGGTCCCCAGATTGTCTCCAAGGGCGTGTCCACGGACACCACCTAAATCTTAGCTGTAGGGAATGAGTAGACATCCAACCTTAGGGCCGAGTCTACGCTGGCTTGCAACCCATTGTAATTCTGGTTAGATTCTTAGCAACCAATGTAGGATTTCCCTGCCATGTTCGCATGCACGTCATCCAGTCCTGTAGTCAGGCCCGGTGTACGCCTCTTACTGCCCCTCCATTAATGACTGGGTACATAAAAAAAGACGTTTCCGGCAATCGCCAGTGTGCTATCCACTAATATAACTTTCGTAACAATTTCCCCATTCAAGCTAGGGGGGTGCCGCCCACTCTGGTCACCGTTCTCGGGATGTAGAGGCGCCCCCATGTAGCCCGGGCTCTTTATAATCATCCCGATTGATCGGAATGGCGTCGAGAGCAAAGTTGCTGGACCTCGGTTTGAGGCCGAACTTTAGTCAATTCTACTCACTACAACTCCTAATGACTTTTACACTGTTACTAGTCACCCCTAAACGGCAGCCAGTGCCGTCTGGTATTGCGGGGCTTTAAGTCGGCAAAATTCGCTTAGTGTGAGGACGTTTTCCTGGTTAATTCCATCTCGCCTAAAACAGTCACACGTACCACCCAACGGCCACGCATGCGTAGAGACTCATTACCTGTGAGGTAAGTGAACAAGATGTGCGAGTTAATAGCGGAAAGCGAGGTGACTAAGGAATCGCTCAGTCATGCTCATCTTATTAGTGCTCAGTAATGAACAATAGGCAACGGGGGATTAAGTGCGGTATGTTCGGCTCCTAGCTGGAACGCTGGAACAGTACTCATATTTGCGACCGGCAATCATCGGGACACGCCAAAGGAAGTAGACCCGTAGCCGATTATCCCGTACGGCCTTCTAGCGAATTCTACAACGTGATGCATAGTAAAGTTGCATCTACGCCCTTGAGAGCAGTCTAGGCAAAACCGGTGCGGGTCCGAAGAGGGTCTGTGAGGACCGATATTGCGTTAGAACTTATGCCATTAGTGCGAATCATGTTGCTCAGTAGTCGTCTTGTGATCTTAACCGCTTTCTGATCGGGCATCGCAGCTATAAACGCATCGTGCCCAGTCGCGCAAACCGTCCGATACTTTTACCTCTGAGGAGGGAAGGTCTGGTCCCCACGGAAACAGGCCAATGCGATACTGCAGCAACACTCATCAGTATAGATCTAAGAGCCGCACAGCGAGAACGGGTGAACTCCGGTAGCCGTAGGGATCAGTGTTAACCAACTCGAGAGGAGGTGTAGCGTACTAGTTTGAAAGATTTTATCCTATACTGATAACCATTGGTATCGTTCCTCAGCGTGCTTGGCAATCGACTGTATTGCCCGACACTGTATGAACCCTTCGTCTCCCATAATCTCCTCAAAGTGTATCGCCACTACTATCACTTTAAGTCTGGCAATAGCATGAGTTCTATGGCCCCAAATTGCGCTCCCCAAGATCTGATCGTCGAGTAGACTGTCCAATCTCCAGTCGGTTGGCGGTACGTACCTGGGTTTAGGAATGATGATGAGGACGCAGGCCCGGCCCCACTGTGTAGCTCCAGGTAAGCCGGTGAGGACGTATCGGCGGTTCGAAGTGCTCTCTCAAAACAGGGCGTCTCAAACATTACATCCCATGACTCTAGGATGCGTCTCCTATTGATCCTCACCGCAGGCTGGTTTCTATCGCCTTTCGCTACTCTCCTCTATCTGTCTCGCCGTGGGCGTCCGGATAACCCCAGTTATATAGTCTTGTACTTGAAAAGTGACCACCGCTTGGGTACCTCCTCCGGTCTTCGCTTCGCGGAGAACCCGTTATGCATCTGAAGTACGCAACTAACATAACAGAGTAACAGGGGATCGGGAGAGTTTGCTCAGCGTCTTACGCTCCTGATTACTTCTCCGACCCGCTGTAGTGTAAGTCGTACCGGTCGACGAAACGCCAGACCCTGTATCCTGTACTTATCGCTGAAATGTAACTAACAGTAGCGGGCTCAGAAGGCGGCGGTGCACACGCCCGATTGAATTTACTCGACTCAAATGTCGGCAACCCTACGCTTGGCGTGCTCCAAACGTGCTCGCCGGGTTCTTCGACGCCTCTTCGCGAACTCCTGGATTGTTAGTCGAGTTGAGCTTACCTGGGACGCTGGAGTAGAGCCGTGAAGCGGGGTGTCAGGTTATATTGCGATCTCCTTGAATAGAAGGGCTGTACTGTATTCCAGCCGAATCTCAACCGCGATGGACGTACGGTTAGCGGAGATACACGAGTTTGCACAGTCTGGGGTGTACCGTGATAGGGTCACTTTGGCGCAACATTTTCACCGTGATGTTCAATGGCAGTGGCTCCTATTACAGGCCCGCACTTTGTGCAGAGCTAGGGGGCCAGCTAGTGCCGAATCATAAGCAGATTCACTGTTGGTGCCCACGACAGGTTGGTCACTTGCAGAACCTTCCCACATACCTAGCACACGGGAGTATAGCTGCACGGTTGTGGGGGTGGATCCAGCTTGTGATGCTCTAAAACCATATACGGCCCCAGACAATAACGTTAATTCCGGTTTAGACTCTCGTCCTATCTCGAGCACCCATACGTATACTTATAGCCAGAGGAGTAGCCTACCACCTAATCAACGACAAACCCCCATGGGCTGGAAGGACAGCATAATATATTCAGCATTCAATTGGTACTAAGTCTCTAAATCTGCGAACCTGGTCGAGCCAAGCTTAGTATAATTGCACCCCATATAAAGCTAGGGCATAGCAGAACCTGGGTCATTTTCCGCCCTGGTGATCAGCTCGGTCTGGGGTGGCGAAGCACACGATGTATGGTAGTTCCGCTTCGAAGCTTATCGTTAGTCCGCAGGCCTCTACTGACCTCCCACGACATCCCCCGGCCAAGCTACGAGGCACCTGTCATTGTATGTAGGCCGGCCCTTATTATGCACTATCGGTTGCGGACTTGCATTTCGCTATAGTGAGCAAAACGCAGGCTGACTCAGGTCATAGATTCATTGGGCAAGTTTCCTATATCCTCCTCAGCATCCAATGTAACGGGAGAGAAGTCTTCAAAGCTCAAACTCGGGGAGATGGCGGATAAGCCCCGCACAAGGTACCTTTCAGGTCCAAACATCTAACGATATGCCAATGAATCAACTCGGAGCGCGAGTGTATTAGCAGCGATAAAAAGTTACTGTAACATCTGAGTACTCTATGCTTTGCCTCACAGTCCCGTCGCAATACTAGTCGAATCTAGGAATCCGCACACATGTTGGGGAAGACTTCGTATGTGCATGAGAAGTAGGTAGACTGACAGCTCGGCCGCGACTGGTCCCAACATTCCCTTGTCTACACAGCTGCCAGTCTGAGCATCACCATAACGATGGAAAAACCAATTTTCTGCCAATAGTATCCACACTTACGTGTCCTATGGATCTACCGCCGAGTCTGATGGGCGTCGACGCTCCATATGTATCGGGTAGACATTCGAGAGACCGGGGGGCCCGTTTCCTTGCCTACGTGATAAGCCGCGTATCGTTAGACTTTCACCTAGAATCACATCAATGGCCAAAACGAGCCGCGCGTACGCGTAAACCTACCCCTAAAGCTACAACCTGAACCTCCGAATGCTAAGTGTCGTTCAGCCGATCAGTCGCCCACGTCTCAAACGATATATGGTGGGACCTCTGCCTATAAATGGGCTTTACAGACCCGCGGTCTTTCTCAGAAGATTATCGGACCAGTCTTAAAAGACTCTGGTGAAACAACCGCCGTTTCGTTGAGACCCTGAATCGTCGCGCGATGTGTAGAGTACCAAACTGAGCACGAACCAATGACCCAGCACGGAACAGTAGGCGGCAATGATACCAGACCACTTTTGGTTTCCGAGCCCTAGTCGCAGCAGAGTTGTGGCATTAATCCTAGGAAGCCTGGGATCTCGGGTATCAGCTTCGGTGTTAAGACTATACCAGTCTCTTGGTTCCGTGAACCGTTCACCCCTCCTTTGAGAAGGTTGGCCCATTCTAGGGTGCTTTTTGAGGAATCTGTCAAAGGATTGCTAAGGAAATGCGGGGGGCGAAGGTACAAAACACGAATTGCTACTACGATGGTAAATCGGTGTCCTTCCTTGTAGAGTCATTGCCCAGACGTCAGATCACTTTTCTTACGAGCTGGCCTGCATTGACGATGTTAGCGTAGAAGGCGCGCCCAGACTTCCGGTCCGAAGGAGGAGTTTTTGTAGACCCGCTCGGGAATCTAGCAGACAGATTATGAATACCCGAAGACTACCTGGGGAATGACATACGGCGCGACACCTCTTGCGCCTATTCGGGGGCCTGTTACAGTGCGCCTGGGGCCATTGTCGAACGAGACTTTCTCGGATATAACCAAATCCGGTGCTTATTGATTCTAATAACCGGGTCCAAAATCGAAAGATATGAGAGTTTACTCACTATTGTACTCAGTACGGGTCCGCCACAAGCCATGCGATAGGCCTTACCTGCAGCTTGACAAGACACCGCAACCATGTATACCCGGGAAGGTTATCTGCTCTCCTCAAGCAGTTGCCATACCAGGGTCGCGAAACGTCCGAAGCCGAGATGGCCTGTCATCCTTATATTAGGTAGATTAGTATGTACTTAACTCGTGTCATCGTGTCCATCGTAGTCAGGAAAAAGAAACACGTCAAGGCGGATTTAGGGCGATGAGATTCCCAGCCCACAGTCATAGGCGTATTAGGCGAGAGGTTCGAAATCACCAGGCACCGTGTTTCATTTCACCGCCGATGTTCCGGCGAGTCGGTTATAACAGGGAGAATACGCAGTCCTAGCGCTGCCTCCACAAATTGAGTGAGCCACCGCTTCCTTTAATACCAGAGCTGGATACCAAGTACTCCTATGCTGTTCCTGTTACACACTTGCTGTCACATTCCAGCATTAGAGCCACTCAAATCGTATGGTATCCTGTCCAGTTGGCTAAGTCGCACAAGACGAAAGACGTACGACCCTACCGCCCTGGCGTTTCCTAAGTAAGTGCTAGGCCAGCGACGTAAAGACCCATAAAGGTAAATTATCTCCCTTGAACTATCTGGGATATCATGTGCTCTAAAGCGTTCCACGCGGCCTACCCGCCATATTGGTCTCGAATATTTTACAATGTCTGGGAAGTGGCAGTGTTGGTGGTATTGACCAAGATGTACGGACGCCGTCCGGTTGTGAATGGTTTGTTCTAAATGACGCCTGCCCTACCTCATCCAATTCCCTGACCATGCATAACACAATCCGGCCCTCGAGATACGAGGTATCATTCAATTCAGTGAACACCTTGGAAGGTGGACGTTAGCATGAGGCGTTAGGCCACTAACCACCTAGCGATCTCGAAGGAAGAAGGAGGAAAATTACGCGGTGAATATCCTGTCTGCGATTGCTGTTCGGAAATAAGTCTAACTTAGGAGACGTGATGAAGTTAGAGCTCACTTAACTTTTTTGCACGGGATAGCGGTGTTGTTTATCTGCAACTCCTCCCGTTTGTAGGTGGTAGGAGGATTAGCGCTGGTCCGTTTAGTGTAACACCTTGCGGACACTAGGGCTCTGGCGAGCCGGCTTTTAAAGATGTCCTCCAAGCCCGCCTGTGCGCATGGTACCCTTCTCGGTCGACTTGCTGCATGCGGTCGTTAGCCAACACACGACGCCGTCTGAAACAAGTGAGCGCTCAGGAGAGTATCGCATGTGGCGAGTCTGGGGAGAAAACACGGCGAGGTCGCTGGCGAAGTGCACACGTCCGAGAATTGTGTGAGGGAAGGCCAGAGTCTGCTGCCATTTCGTGCCGTTTCAAATTACAATTGTTCGCATTTCTAGTTTAGGGTGATTCAGCAGTACACGAACGCGTCCAACTCTTGGCATTCCCCACCCGACCACGCCCCCGACTCTTCTTCACTGAGGTACATGCCTGACGCTGAGGCATGCTTTACCAGGGCAAAGACTGGACGTGAAAGACGTATCTTCTAACCATTGAAATCGTGATAGACTGGGAAGCGAATGGGACACCGACAGGGCCATTACCTCAGTGGTTGACGATGCGCCACTTGCCTGTCGCGATCTTGCCCGCTGGCCCATAATAGGCGAATCGTCTGCACCATGGACCCGAATGTACGTGCAACTAGTAAGGCGAGCCAACGTTGACATTGTGATTAGCCGTTAGATCCTTCAAGTCCAATTAATGCCTTACTGACTCACCCCCTGGATACTTAAACTTAGGCTCACGCGAAGCTTTCCCCCGTGGGCATCGCAGGCTTCGTGAACTACATCACATTAGTGAGCGTCCCCAAGACCACTACCTCCCCAGTCATTATGGTTACGCGTGGAAAGGGCGACCAGAGCACGCCGCCGTCTCTTTCATGTAGTCACTCAGCAATATAAAATAATCGTACCAAAGATAAATTACCCTTTTTAACATGCTTAATACTAGTATGCTAAACTGAGTTATGCGTGGCTAGTGGCCTTTTAACCATAACCACCACATGTGCACGCCTAACCTGACCGCCAGTTACTCCTACCTGGGTAAGCGTCGAGGAAGATAGGAGTGCACGGTTTACTTCCTAGTCATAACTTGGGAGCCTTCTCACGGTACCTGTTTAACCTCCAGCATTGTAGCGTGATTAAGTAATGGATGCCGGGAACCCATGGTCCTAGCGTACCCTAATCACTCATGCCCCCAATGCAGTGTTGGTCGCATTTGGCCCTTCCTCGATAGTCAAAATAGCTCTGCATCACTCCTAATTCATGTCGCAGATGGCGTAATGTTGAAATCAAGTGTTCCCCCTTGACATAGACGCGGGCTTCCGCCGGCACAAAAACGGTCCGGTACCAGTCAATGCCGTAAGTGCACTGCTGTCCGTTCAAAGTGACGCGATATGAGGAATCTCAGGTCACACCTGCGCGTAGACTGTGTCCGCTTCTCGCTACTCATTGACACCTATCATGTGCGGGGCCCACGCGTGTTACGTTACGTAATGAATACAGTATCGCCTTACCATTAATTACCTCGAGTACCGTCCGCTTTAGAGAAGAAATAGCTACTGACTTTCTCGCGGCAACTGTATATGACATATAGGGTAATTAAAACCGATCGATCCTTTGTAGGTCTATCTCATCGACAGGCCGCGCTTGGTTCAGCCGTCTAACACGCGTCCCTTATTTGTGCCTCACTGAGCAAGCCACGAAAAGGACCCAATCAAGGCCATGTATACATCTACCAAAATCTGGTATGACGAAGGTACAATAGCGTCACTGGATATTTGACCACCAGCAGGAAGGAAAGACCCGTATTCTATCTAGTCGACAAGGACAGTGAAGTTACATGCCTGGGAATGTGCGCGGACTGTGTACACGGCAGTAAGACGCTATATTGTAAACTTAACGCCCCTATCAGGCGCACAAACTAGTATGAGTGCGAGTGCCTCGGTTGATGCGGCCTAAGGTTAAGACTAGCTGCTTTCGAACTATGGTTGTAGCCATATAGGAACGCGCCGTACCGTCCTAGTCCCTCCGGTTTGAACTAGGTACTGCTCCGCATTACACCCCGACCACACGCCACTTGTGGGCGGGAAGAGGAGGGCAGAATGAGACGCGACATTGGCGTTGTGCATATGTCACACCAACATATATCAAGACGGCCGGCTTTCCGCCTCATGTGCCCGCGTGGGTACTCTTGATCGGTCGCTTACCCTGTCCAGGAAGCGTGCGGTCCGATCGATTTTAAGCCCGTTAATAGGCAACGTGAGGTACCAGCCATTACAGTTTCTTATGACAACATCACGGTAGTGCTCTGTATTCCGGTGCTGAGAACCGGCCAAGTTACTACAGAGAGTAACTAGGCCCCATTTGATCCGAACCAGCATGCGCATGTAAGTTGGCAATGATTGCTTGAGTCCGGTTCACGATTCCGAAAAGCAGGCGTGGTGTGATCAAAGTTTGCGGTGTGCTCCATTTGCACAGAGAATCATCCCCCGAAATAGTTGACATGGCCTTTTCCACAAATTTGCACGGCAACGTATATACGAACGCCGAATAATCTAGGGAGGGCGGCAAAACCATGCTGCTAAGTAATGCGGACCAGCGATATCAACGGCTGAGCGCGAAAGCCACCGCGATTCAAGTCCCGGGACGTAGGAATAGGTGAACCTCCACACAAATAGCTGGCAGTGACCGAGTAAGTCTACTTCCTAGCTGTTCAAATTGGAGTCTAAAAATAGAAACTGGTTCTAATTGGACCGCAGAACCGCTGGTAGTGTGCAAGTGCGTGGGTCTATTGGCTGACGTTGATAGAAAAGAGCAGTGCTACTAGCACCATGGCGCGAGCGCAACACCTGGGCGAAGAGGTCGTACAGAAACGTCCCGGTTCAGTACCGCAAATTCAGACTTGCCACTTTTGGGATCTAACCTGATCATCCGGCGAACTCGCAGGAACGGCGTGTGTGGACCAGACTTTCCACCGCTAATTTTGTTCCGGCGCCAATTTTTTTAATAAGGCTTGACGCACAGAAATGTTTCCGATAAGCTACGTGCCCGCAGCCTGAACGGCTGTAGGCTGAGTGCAGTAGTCCCATGCGCTCAAAAGAGCGACGTACTGCATGCAGTGTTCAATCGTTCTAAAAAATGCCCGATTTTAAGTGAACATGTTACTGAGTTACGAGTAAAACCTAGATAGAGCTTGCAAGGTTACCTTTTGATAAGCACACTGTGACATTTGGTCCCGTGCACGTTCACGCGATGGTTCTCGCTTTCAATCGCCCATCAAGCCTCCCATTAAAATTCTCTTATGCATGGTAAGTGGCCCGTTCTTCATAGCGATCGGCAAAGAACGCTTGGCAACAGAACTTCTCCCTCGTGTGATTTTGAAAACAATAATGAGTACGGAAAGGCGGTTTAAATCTGTAGCGTGTTAAGTTTTGTACTAGTAGTGCGCTCATAACTGTAATCCAATCACCGCATTCTAGGGCCGAAGGCGCATTGGATACCAATACTCCGCCAAATACCTTGACCCAATATTCGTGCTCTATAAATTTTCGGTGCCATGCTTGCATGACATGAATGAAGACATACAGCTAAGTACGCCTCAGGTTCGGTGTGTTCGCAGCTTACGCCACCAAGGCGGTGAGAAGCGTCTTTCGTTGTGACCTTTGATTAGCACTGACCGTTCAGTACACAGGTACCACAATCGGGACTCACTCCCATCAAGAGTGATAAGCGGCATTATACCTCCTCCCAGCGTAGGAGTGTCGCGGTATAGTGAACCATAATCCCAAGTTGCCAGGCCCATTGTACTTTTTAACATCGCGCCGGCGACAACAGCTCCCTTTCGGGTGGACTGTGATTCCATTCCTTTGGGAGGAGGATAAGCTCCCGCATTTATCCTCATGCAGCTACCGTAGCTACTCTAGTTAAAGTGACACCGATTCAGTCACCGTCGCTAAAGAAGAGCTGGAGGGGCTTCGAGGATATCCGATGGCGGAGTGTAGGTGTAGGTCCCTAGAATTCCTATTGACATTGCCCTATTCATAAGGTGAGCGAACACAGCATCAATTCTAAACTTATTGGGAGACCTATCCTTTAGGAATGCGTGGGCAGGACGTTGCAGAATGTCCAGCGTACCGCGACGAATCTAAAAGCTGTAAGGTCTAACATGGAGAGTGCATAGTGAACCTAGCCACTGTGTTAGTGCGCCGTCATTTCTCGGTACTTAAAGCGCCCCCACATCTTCTCCGTAACTTGCGAGACAATAGTACCGACTCACACAGAAAGCTACGGAGTTATGTTGGCACTAATGATGTTGGGCTGGGCAGCTTGGGGGTTAACTTCCATTCTCCAGGTTTGCAACACAGTCAGGGCTGTAGAGCATAGGTGTATGGCGCAGCATCGCTACGGATCACCACATTTAAGACACAACGAGATACTAATAGGATGATCCCGCGACTCTAAGGTTTGTAAGACATAGATGCGTCACTAGCCTCCCGACTGCCGGTCTCTGTCCTGCCGTACCAGTAAGGCCTTATTTGCATCGTTCTGCAGTTAGGGTGGATAACCGCGATTGGGTTCGCTAAGGGCCTGTCGTGAACTCCTCGACCAAATATCTCCTCCGGTTTTCCCCACGTTCTGGAGTAACAAAATTTTTCATTATACTATGGTTTCAATGGTGTTCTGGCGGGGTATGAGCCCCCCGGAGAATTCGTGGGGTAATTGCCGCGTCCTACGGGCGTTGCCAGGCTATGAGAGTTTATGGGTTAGCAGGGAACCTCGTTCTACTTTCTGCCTCCTCGTTATAGCGTCCTCAGATTTCCATCCCGTACACCCTCACAGGTGAGGTTGGGAACCTTTGATATAGAGCGTCAACTATGTACTGACTTTTCTCTCGACCCGTCTCATGGAATTCAGTGCTGCTTCTACTTTACACTGCTGGAGTTTCGATCTTCTAGCCCTCTAGAAGTTGTAGACTGTCAGAGCGTCGACTACCTACCCTAGAAGATTGTAGTTGCGACGCCTATCACTACTCAAAGTCTCCTCATTGCCCGCCGGTTTCCGGAGAAATTTACATTTGTTGAGCGCCCCATCTCGCAGCCGGTAGCATGTTTCGGTGCGGAGCGGCCTAGTGGAAAGCCTACGTCAACGTAGCGAAGTCCGAGGGAGACACTACGCTACACGAGGGATTTACAATGTGGTTCAATGTAAGTGGTTAAGGCGTCCTTATGTACATCAGGACAAGTTCACGGACTCCATAATGACACTGGTTCAATTATGCCAGCCGCAAGACAATCTCCCCCAACAATCGAAGGTACTAGGGATCGCCCTGCTATCGCTGGAGACTGGTCGTGCCAGATAGCATCTGGTTTTTTTAAATGTAGCTCTGTAGGCCTGCGAGCAGAGTCGGTCTATTCCGCTCCCTCGACGTACTAGGCCTGTACAAAGAGCGCAACGACGTTGCCTCCTTTGTATGATTTAAATACTGTCACTCTGGGCTTCACACAGCTTCATCTCTCCTGAGATCTGGCGTACCTCTCCGCATCGCCATCACGGTCAGAAGGATTAGCACGGGTTCTACCCATTTCACAACGAAATGATGATACCCTTGCAGTGTCGTCGTTAGGCGCCCCACTCACTCCTATGTTACCAACGGACGTGGCCCATAAATTTCTCACTAGATTCCGCGGGCTCCCTTAAGGTAGCGACTCCTCCAGTCAAGATATTGCAAGGGAATCACTTATCTTCTACCGCACGTGGAGTGGCGGAATGCGTTAATGACACTATGAATAACCCATAATTGGCGCTTGATGCGGAATATAAAGCAAGCAGATGGATATCAACATCTGTATTTGCTTTGGAATCTATCTACGTGGGGCTTCGCCCCGACAAGTTACAAACTTCTTCTTGGAGGCAAAGTCCTTTCCCGCATCATATTCCGGACAGGGCGGTGTGGCGGCCGGTGGTAAACAGCTGTTACCCGGAAGGAGCCTCTCTACACTCACCCCACCGCAGGCGGGCCAGCGCATGCCAGAAAAAGGTCGTAATCGCAGAGCTTTAATAGTGGCTATCCTTCATCGCCAAAACACTGCCTCTTGATACAGTGGCCGAAAGCGCCACCATACTCGACGTGCGACTCCTTACGTTGTCGGGTTCTCCAGACTACGGAACGCAAAAGACTTATCCGTCGTTTTAGTGGTCTAGCCAGCCAAGTCTAACCTGTCGTAGACCCTACTACCCTAATGAGATTCGCCATGTGCCTGAATAGTAGGACTGATCGACCTCTAGAAATTCCAGAACCCAGGAATATGTCTTGAAAATCGACGGCGCTACGGATATAGTGCCCTGCGGTCCATCGCGCAATTTTCGCTTATATCCCAGTAGGTTCGCTTCCTGTCTCGGTTAGTCCGTGACAACTAGCAGGTAACTTCATGCACTAAGGTCCCGATCCGCAACCGACAACTATGGTAGACTTAAGGCTTACTTACCTGGCCGGCAGTGTGCTGCCGGTAGCTACAACGTGGATAACAGAGCTCGGACAGTCCGCGTACTTACAACTGTCCATGTGGTCAGACCAATTGCGATCGTGTGACAGGAATCTAGGCCAGGTTGTGCTGATTCTGGAGCTGCGTCTCTCTGCAATAACACCGAGCGTGTTGAGATTTTACCACTGGTTCATGGTTTTGAGACTACGGGTCAGTCCACAGACTCCCTCATGAGGCGACGAATAATCTGTTCAATTGCCCTGCAAATTGCGCCCAAATAGTACGCCCTGCGCAAGCTCTGACTGAAGGAACAACGTTTACCCCTGCTACTTCCTGCTTGCGGACCTCGCAAAGGTCCAGTTTCGGTCCACGACAATGTGGCTGCCTAGGGCGTGGATGATTGCTCGTTATGAAGACAAAACCTAACCATTCTCTGTAGGGTCGGGGCGCTAACAAACCGGTGGACCGTGAAGTCGATTAGCTGCGTTGACCATGGCAACGGCCGTGCAATAACCATTGCGTCAACCGTCCTATTTGAGGCCTCTGTTTACTGTGAAAACTGACTAAGCACATAAAATTTTGGTGTGTAGGACTGCAGTGTATAGAAGCACAGGGAGTCGCCCACCGAGAGGGTAACTCGGTACAAGCGAACTGTGACCCTGCTAGTGATGTCTTCGATGGGAACACGTCAGCACCGAGTTCGGGCAAAGCCGGGGGCGTAGTGCGCCAATGCCAAGCGTGTGTACAGTGTCAGCGATTTCTGTTGACACTTCATGTAGGTCACGGACTTCAGTACTCCTCCCAAGTGACTTCGCTGTGGCTACCAACTAATGTGGGCCTCTATGTATTGCATGTAGAGACAGTTAGCATGACGCACTCAAGCAGGGGCATGACCCCATATTTCCGTGTCGACACCACACTATTCCACGAGTGCCCTCCATCTATAGCTGCCCGACGTTGGGGGCCTACTCGTGCGAAAGCGCTGTGATTGTATTCTTTTGTGATCACCATCGTGTTACAACACCGCCATCGGCTAGCCCCGAGGCGCACTGAATTGGGCCACCTTTCGTTGCCCCGGTGTCTAGCCGACCGCCGACAGGATGAAACTCTAAACCAGCGTCAACACCTGGGATCCAGCTTATTAAGCCGAGTAGGGAAGGCAGCGATCGACAGCGCTGTGAACCTATAGAGTGTGTGTTAGGCTCTGCGTCGTCCTGAGGCCCTAGGACCCGGCCACAATAAGGTATGTAAGGAGCTTAAGGCATCATGCTAATCCCACCTAACTTGAACCTACATGTGTTGCCGACGATGTAATACTCGTGTGTCCCCAGCGCCTGATGGACACTTTGGTTTTATGAGGTCGGTTATTCATGCCTGGGCGACTACCCTGGCTAAAAGGGGTCATACTGACATTTGTCTAGCTGGTTATGAACCTGAGCCTTCTTCTAAAAGACATGCAGAGCGCGACCACGATCCAATGTCCCGTTCCCTGCGGGGTGGGTAATGACCGCAGAACATTTGGCAACTTAACAGGGTTATATAGTAGAATAACAGCTGCAGGTAATGTGTGCCTCACAGGTTCCGTTCTCCACACAGCGGTTTTCCAATTATGTTGGCACCACATATTGCGGATCAGCCCGATCTTATTTGGAATTGGCGTATTAGTTCGCTTACTTGTGGCGTAGAAGACTCAGGGAGGTAACATCTGCGGCACATTATGATGTGGAATGCCTCGATATGCACATAAACTAGCGACCAAGATCATCAACGACGGATCGCCACACCTACATTCTACCGGTGCCTCCCCGGACCTACAATTGTTCGCTCTCATGAGTCAGTCGACGCAGTATTTGTTCTAGCACTTGAAATCATCCCGCGGCCGTGCTAAGTGGCGTCCCCGTTGGTCCTAACTCAAGCGAGTAGATACTACCCTGCTCATGCCTGAACGATATAGATGAGTAGCAATCGCGAAAAGTGTTATCGGCTCTTGGTTAACTTGGGTGAAAAGTCGTCCGACTCCTTCCCTTGTAGCACCTCAAATCTCCATCATTGCGACCAGGTGAGTCTGCTTGCCACTCACTAGTCGAAAAGCGTTTCGTTGGGAAGTCACATGACTCACACCTGGATAGAAGTTGGTAGGAAGTCCAAGGACAAGTTTATGTTCACTTCCACCCCGGGGTCACTTCCCGACCTTCGGTCGAAGCTGGGAGGAGTTGGACAGGTAGGGGTCGAAAGCTTCTCTCTTAACACCTCTTGTTCCGACCTTGTAGACTTAATCTAGACCTTTATTGATCCTAAGACACCATCGCATAGCCTTTTCGATCTGACCGACAGGTCAGACACGCCAGTTCCAATAACTGTGGGAGATATTTTAGGCCACCCGGGAGTGATAGTCTCGGGGTGCCTTTCTTCGGAACCCGTCCCAGGAGGCACTCACGACCAAACTGATCCGCTGGCTATGATAAACAATCTAGTTATCCTATTGGTTATAACACGGTGCTAGTGAAAACGCTCCCCACATGTGGGCCTCTTCTTTTACATGCATTCTCGTAACACTACGGGTTTACTAGATGTAATTTGAGATTCGTATAGACCCGTGATGTTTTAAAATAGTGTTATCTAGAAGGATGAAGACCCGACCGCGGGGGTGTCACGAGAGTACACCGGAGACTGGGGCGGGAATCGGAGGCGGGAAGTGAAATTCCACTGTTTGAGTATCAAGTAGGTTGTCTCATTGGACGATACCCACTGATGGAAGGACTCGGAATACCGTTTCACTGAGAACAGACTATCCTGATTTGCAGCCTACGCACTTAGTCTCAAACGTAATTCGTAACACCCGGCATGAAAAGTATCCGTACCGAATAGAACTGACGAGGCGTAGGGGCCGGTTACAGCTACGCGTGTCATCCTGTTGAGATTTCGCTATTTCACCGTCTTAAGATCGTGGGAGCGGACTGTTCCGGGGCCAGACGAACTTTCGAGGGAAACTGGGAGGAGTCAAATTGTTCCTCCCTAAATACGAGCTAGGAACGCAAGCGGAGATTCTTTACTTGCATGATGCTTGACGCCTATCAATCGCTGCCCGGCCACTAATTGGTCTTGGTAGCCTGTTGAAGGTGCGGTCGCGCCAACATGATAACGCAAATGGCGTGCTAGAGTCCGGGAGTGTGTCGATGTCCTCAGAAAGCATCGATGCGCACTAACCGCGGTCGTTATCTAGAACGCAGTCGTCACAACTTGCTCGTTGGACAGTGGTGGGTGGCGTGTGTCCTGCGGAACGGTTGCACGGACTAGCGGGTTCGGAAGGTCTCGTACTACGCGGTAGTAGTCCACACACCAGTAAAGTTACGTTGCGGCATTATTGTAAATTCCCATCGTAATAGGTTGTGTCGGTTCGCATCTCAGATAGTCTTTCTTTGAGTTCAGACGGACGGTATGGGCTATGACGTCGCCCCGAGCACTGTAGTATTTACTCGTCTCTGGACGGTTTGGGACGACCCCGCTTTCTGGATGCGGTGAAGTGGGTATTGCAATTTGTAGCCAATCTTTTAGTGCGACAACCCGCGCTGTGATCTTTGGTAAAGCAGCCTTGCATATATGACCATGGGACAAGTGTCACCTCTTACCATAATAAGTTCTGTCGTTCCAGATGAGGTACTGTCGCGCGGTTACTATTATAATTTGTGTTAAACTGCTGCAGTTGCTTTGCAACCGCGATTCTCCGAGCCTCGACGTCAAGGCGTAGCTCCATCCTAACTGGCGTTTTCTTCCACTTCGACTAGTTTGGAAACTTAAATCCAGCAGTTTATGGTGTAAGCTACCCAGTGTCGGTGCTTAGATACTATACACCATGCGTATACTTGCGCCGCGAAACGACTCTAATTAGATTTAGCGTGGGCGGTCAGGGCACGATCACAGATATTTACAAGACGGGACTTCACTACTCTCAGTAGAATCTTGTGAATTCCCGTCTGATAGTTATAAATGACCGGGTCTGGAGTGCCTATTCACGATACCGATTTAAGAAGTAATGCAATCGCCCGGGCATTGCTTGGACCGCCCAGACTGAAAGATACAAGGAGGGGTCAGAAATGCTCATGGAGAAGTAGAAGAACTATTGAGAGGGGGCGAGTACCTGCGAGTATGGCGTGCACACCAGGTAATTGTCGGTAACGGCACCTCGGTGCAAGCCCGAGCTTAGGTCCCACGGCTACAACCGACCAACCACCTAACGGAAAACCATCTTTCAAGTCTCCTCGTCATATCGTCGGCTACAAGCTACACCTTCATTAGGCCAATAAGGAATCTAATTCGGGGAGACTAATGCAAGGCCGCGTCGTCATGAGCGGCTCAGACCTTAGCAGCGCGGCATGGCCACCCTTAATAATCATGGCCGACTTGTGACCCCGAGGTAAACCTTGAGTCGCTATTACGCGCCTCTAGTTCCCCCTCGGAGGAGGGTCGCTAGAAGTACTTCGACAGGGTATCTGCCTCTTAAACGAGTCCACTTTTTTCCTCCGCGTGCCTTATTCTTGCTGACGCGGAGCACAAGCCAGTGTCCTTCCCCGGCGCTATTAGCCTGGCGTGTATTAAGGAACGGAGCTGTAAAGTGTCAAATTCCAACAGGACTACGGATACGCCCGCATGTCCCGCGCCGAGATTTCGGTATGCCAACGGGCGCGGTTGAGGAAGTCTGAAACACTATTAGCAGGTATTGTTTGCCTGCTCACAGGCGGGGTTGGGGTGGTGTAACCCGCAGGTACGTCTATGCCAAAAATGTAGGCATCGTATACAACAACCATGACGTCGGACACGTTCTCTAGATCTCACTCGGTTACTATAGCACAACGGGCATCCAGGCTGTCCTTAGATCCATGGCCCATTAAGTCTGGTAGGGGAACGGAATTATCTAGCGTTGCCACGGGTAAAATGCTACTGGCGGCCATGATGTCCGAGTGCACCGAGTAGGTATATCTAATGCACACTGGATCCAATTGTTGGGTCCTCGCCGTAATGCATCAGACATTGCTGGCTTGCGCCTAGCGCAGACACCATGAAGACAAGTTAACTCCGGCCATGTAGTGTGATGGCATATTAGAGAGACCCCAGCCAAATCGGTATATGACATCCACGATCGTTTTCCAGCAAGAACTCTTTTGCGCAGCAACCACTGATTCGCGTCCTATACATAAGTAACTTGGGGGATTTTACATCAGCTGGTCATGAATAAAGGTGTGCCCTAAGCCCTCTGATGCTATTATTGGGCTACCTGTGTATAAGATGTTTTCAACAAGAGGTACACAGCTGATGTACGTTCCGGTTTTTGCCGGTGCAGAGAATCCGTGAAACACCTCAGTTTCTCTCCTTGCAAACGGATTCCGAAAGTTGGAGGAACACCTCCTTACGTATGAAAAAATCCGTGTTGGGTGTCGGTGCTTTTTTTGCCACGGTCTCTACACAATCGTAAACGATTGCACCCCAGTGACTACTTAATGTTGACGATCCCCTATGGGTTGCACCGAAAACATTTACTTGGTTCTTTACCATAGGCTTTGCCAAACGTTCCACAGTAGATTCAGGCTATAACTCCGCCAATCCCACACGCCTGAACGGGTCATGACGGGTAATGCGCCCAGATGCTGCCTGCTCGGCTGAAAGTAAAACTGCTTCGTAACCGGGACAAGCAAATCGGGACTGGGGACGGGCCTATTCCGTATAGCTCAGATCGATGTAGGGTCCTAATGGAAGCGTCCGCACCCGCCCGCGGGACTGGATAACAGGGTTAGGCATCTTTCTTGTTAACAAATCTAGGTGCAGAGCCTCACTCCGCTGTCGCTTTAGCTCTCAGTCAAGGGGCCGTTCAGCGGTCTACCCGCACCCCAGTCACAGTGTATAATTACCCACTGATAAGCGTGGGGAAGGCAGTAATTCCACTCCTTACCGGGTGCGGTAACATGATATATGTAACCACGCTCGCTTGTTAATTGCTTTTACTGGGATGACTGGCAGGCTGGCTGATCGTTACGCTGGCGGTTCACCCTTAACAGGAACATACTAAAGAGAGCTCGATCGGTATGACGACTGCAGATTGAGGCCTTCTCGACTGACTGTATGGACAGTTTCAAAACACGAAGATGACTCATTGTACGATATACCCTTGAGGAAGGGTCCCTCATTGGGAGATTTAGAGCATTGAGCATTGTTCTCCGGCCCGCTTGCTGCACCATCAACTGGATCTCACCCGCCCTTCAACTTGAGATGTGTGAATAGACACGATTCTTAATGCCCGGGTGAGGATTCTACCCCACAGCTACTTAACTCCAAAAGGTCTATTCCCAGAAGCTCAGCAGCCGATACAATCGAGCGGCTCAGGTAGAGCTACAGTTGAGTATGTCGGCGCGTCCATCCCCCAAAAGACCTAGTCGAGCGTTCAAAGGCGTTTACGCGAGCTCCCAACCCGTAAGTAACTGTAAACCGCCTGGGCTAACCGCGTTAGTGTTCTCTACGTCACGCTGTGAGTTGGACAGAAATCACCTGACTTTAGCTCGATGCGAACTTGAGGTGGACTCGCTCTGAATGTATTGGAGGTATGGCTTATTTGCGCGCTGTAGACGATATATGTAACGTTGGCTGCCTGTGATGCTGGCAAAGTCGTTCAAACATCCTTTGCGCGAGACAGGTAGTGAGATTTACGCTATGGTCCTGTTGTCATTTTGCTACTCTCCTCCATCGTGTACGAATCCTAGTCTTGGGTTTACTCTGCTTGCTTCAGTACGCGTAAGCACAACGCCTTATTGGGACACATGAGTTGTAACTCACCTATGAGCCCGATGTCGCCAGGCAGCGTATCAGCAGCTCTCCCTATCCAAGGGTCTATGGTGGAAATGGGGGGCGGTTCCTACCACGATAAGATCCGGGGGGAGGTGTTCCTTGTCCAGATGCCCAAGAGATTTACGCATAGGCGCGCGAGGCCCGTAGTCACCCGTAGGAAATTTTCGGAATTATCTTAACCATAACGGCTTGCGGATATGGGCTCCATCGTGCTTGTAATTCCATCCCACAGGCAGTGTCACACTGCCAACACGGGCTAGCGCCGACAAATGTCACCATCTGATGTTACCTATACGGTCCCGGACCAGAAGCTACGCCTAGCCCCAACGAATGTTGAGCTTTGTTGCTTCAATGACTCTGAGTCTTGGGTGCCTACCTCTCCAAGTAATCGACGACGGCCGCAAGGTCGTCTCAATCGGGCTCGCTGACTAAGGCGTGAGCTATAGTACTGGAGAGCTCGCAAGACATGGTAAAAAGTCGAAGGAGGAGGCACACTGAGTAATCCAGAATCTCGCATACAATCATTAGCGCTAGGCTAGTTATTAGACTTAGCGTTGCTCCAAATCTCTAGAATATAAGTTCAGAGACGAGCACTCTTTAGACATACCCCGCAGACCAACATAAGGAGTATCAGCCACGAAGCTCTCCCGGAATTTGCCTGTGGTCTTGGTTGAATGAAACCCTTCGTCCCCAGCGTGAGCTGCAAGGAGAACAGCAAAAGCCGCGCGTACGCGGGAAAAGCGAATCTGTGCCTGTCGGCGTACTAATCGCAATCCTTAGTCGTATTTTGTCGTTCCCGACTTGTATTACCAATATACTTCGTGGAGCGGACACCCCGGGACAACAGCTTCCGGGCAGCGTATGAAAAGAACTCATCACGGTACATAAAACCTTGAACTAGTGCGTGGCATTTCAGGGGTATGATTGCTCCATGTAATCAGAGAAGATGCAACGCTCTAGTCACATTTCATATAGGCCCCCAATTGACAATCCGGATCACGCGGTTTGTACCGGTCAAATTGGCCAAGTAACACAGTTTAAGGTTCGGCTGTCCCCCACGCGAGACGGCTTTATCTAATCCCGAGACACCGTCGACTGTGCCCCAACCTTTGGGTTTCATATCCGATAGTTTGCGTTTATGAGATTATGATTTAGGGCTTAGTAGCTCAGATCACATGTTCTGGCGGGTTATTTCGTTCTCATGATGGAAGTTGGATTGGAAAGCGATCCAGCGATTCTGCAGAGGACGCCTGAAGTGTTACTGCTAGGAACTCGTCGCGGTTACAGAATCACGATCTGAATTTACTGTCTCGACGGGTAGAAGGACTAGTTATTTAGCACCTCAATCGCGGTGAGCAGATTGCCGATTCCCGGTCCGCCGCTCGCGTACTTTTGTTATCGGAGGTGCGTCACCCTTGCCTACCATGCCCGACCCCACAACTTGTTGACTCTCCTATGACACCAGCTGATCAGATGTGTGTCGGAGAGAACCAACCTCCTTCGTAGGCTGGGTCGTCCGCGTGCGGAAGCGGTAGTCGCTTTAGCCTACGGATGTTGAGGCTATTCAAAAGCAGGCCACAAGCCTGGAGCGAAAGCAGTCACTCCTGTGGAGGGTATGACCTAGGGCTATTCTAACCGCATGCTCTTATTTTACGTCCAGTGCAACTGCGTCATACTGTCTGCCGTTGCGTGGCCTCAGATCGCGATCCGGATAGATACCTGCTGACGTAGCCCCCGAATCACCAAGCTGGAGTGGTTCGTAAACTTCCGGCACACAGCGTTTAGAATCTCTGGAGATGTTGCGACGAAATTCGTCGAAAGGCAGTCTCCACGTTTGTTACTCCATCGACCGCCGTACTTGTAGTAATTGACAAGCATCAGTGAAACGTCAGACCAATACGCTTGGGGCTTTGCCCGCGAGAAAATTAGTACTCATTTCATTTTTGATTACGGATATTGGTTTTGGATGTGTTGGACGCCCCCTGTGTCTCTCGCCAACTGTGTACTGGGGGCTACGCGAGTGCGCTTTCCACGTTGGCCGTCGGGAATGAGTATATAAACTGGATATGTCCTCTCGTGTTCCCGTAAAAGTACGCTTCCATCAACCTCGGACGGCGGACCCGTAGGTTTCTGACTTTCCCAGTCATTTATTTGCTTACGACAGGTCCCTTCATATCCGTCCCGTGTTGACGGGTGGCTCAAGTGCAATTTATACATTCGCCAGCCGCTAGTACAGAGCCCGTGTTCTTAGTGTTTAACGAGAAGGTGTATAGTTGTTTCGCAATGCAATGTATGGCTGATAGTTCACGTAATTGGAGATGCCTTTACATGCCCGATGCGATAGCGGCATGAACGATTCTTTAGCGGCAGATACATCCAACTAGGCGCATGGTCAATAATAGTGGGCGTGGACGAATGACGCAACCGTTCTCCGTCCATGCAAGCCTATACTACGAGTATGTATTTAAAGTCGCATTCCCGCCACCTTGCCAGGCCATGATATTTAGCACACCCTCTCATAACCGATCACGTGGTGAAGCCTTATAAGATTATGCAACGGTCCATAGCTTCCGTAGCCGGTAACGGTTTGTACGCGCCAGTCCAATTCCGTCAAGAGATCAGACCGGATGAGTCATGTGGTCCGGAACGCTACAGAGGGTTTAGCTTGTCATCCTCGTGCCGCTCCATTTTCTCCGGAAAAATGCTGGAGGTCCGCTGAGAAGTAAATTACGACGCCTAGGGAACTAGCGATCAACTTGATCGTTTTCATGCCCACCACGCATAGTCACAAATGCGATTAACGCATCGATATCCCATCAAACTCCCAATTACATACTTTTGAAATCAAGGGAGAGGGAACTAAGTGGTCTTTCAAACTCTGATCAGATGGTACAGGGGCCGCTCGCTAATATAAGTACTTGGTGTCTGACCCCCATGTGGGTAGCGATAGGGGCAGTTGTTGACCCCGAAAAAGCGGGCAATGCCATCTATGAAACCACACATAGTTTACGACACTGATCCGCCAAACTCGAAAACTTTCGCAGGCGTTATTTTTCTTAACCTGGGTTATGCTCGGGCACAAGATACCCTAATGTGTCACATGTACATGCAAGTTATTCCAAGCATAGCATTTTGAAGGGGACCGTGAGCGCGGGCCCTGAATATCCCCAATTCAGTTCGTTAACTGCCAGTGCGCTAGATTCGGGTGCAAACCGTATGGACTATTGGGGATATGAGCGAGAAAGTACGTCCCCCAGTATTGATACGAAATTTACACCGAGTAGAAGCTACCGGGACGTTAACTTTGGTCTGGTCCGTAACGCCAGGCACGAGGCTTCTAGCGGATCGTAGGTCTTAGTTGCGGACAATTGGTTCCGTCACCATAGATGGCACGGGTTGGCGTGTGTATCACCGACGCCATTAGTATTAGGAGATGCGCGTAGCATAGGGGGTCATTAGGTGTGACCACTTTCCATGTCTCTGCTGACGTCGAAGTGCTCTTTAACTGACGTTACTCGGGGCCTATCTCTCGGTTGTCGCTGCTGAAATTGGTCTCCGGCCGTAATTATGGCTTGAGCAGAATATGACTTTACTGCGGCCTCTAACGTCGGTACGAGTCTCTTAACGTTTGCTGGCTCCTCATATATTCAGACACAATTGATCTACTGAAGTGAGAGACCCTAAGGAAAGAGGACCAGAATCTTATTTCGACTTAGACAGAAAACTGTAAGTGAAAAGTACCCTCTGAACTTCAAAAAGTTGAGTGATTACATCTTTTTCCCCATCGGGAGTCGTGGTAGGATTTCAAGCACCTACAGGTGTACCGGTACATAACGGCTTCCAGGCTGGTGAAGAGATTAACTCCTGTCGGTCTTCGCGTCCTTCTTGACTTCGCACTTACAACGTTGCAGAATTAAAGTGGCCTCTGATACTCTCCCCCGAAAACGGGACTCTTCAGTACTGGGTGAGCGACAGGCATCGTTAAGCATATTTTCTGAAACATATGTAAGCAATCTACCGACGATCCAAAACACTTGGTAAGATACGAGTTCGGTATTGACCGCACCTACTGGGTCGCCGGGAGTGGAAAAGAACGGTATAACGAGGCGCGTTATTTAACGCGGGCGCCCCGGCTGTGGCGGGACCAACATTACTCCATTGTTAGTTTTAAGGGCTGTTCGTGGGACACACAAAGTCAAGCAAAAAAAGGACTTGATCTCCTTGTCATTGCCATATCTTAATTCGCCGAGGGGCTAGGCAGACTTGGTCCATCCTAAAGATAGTGCCAATCCGATGCTGTACGCAGTCCGCGTGGATCATCCGAGCACCGATTACTTACAGAGCTGAGCAAAAAGATGGAATACCCGGAAAATAACTTAGATGGTCGAGATCACCTTCATCGTAAACTGCTTGACACAAGATGACTCGTACTTTCTAGGGAGACAACTTTCGCAACGCAGCGACCGCTCAGATTTGTGTCTTACAATATCCACTATTGGCTCTTTGATGGACAGCATAGCGGCCAGATACGTACTGTGACCCACGTAATATCAACGCTGGCATCACACCGTCTCCGTGGTTCTCTCCGTCGCGAGTGGCGTGCTTTCGTCAAGGCGGGCACCTAACACAGCGTTCGCGCAAGATAGCAGTCGACCCTAGCCTATCGTACACCCGGCGCTTACTAGTTAGTTTGTGAGTCCCTACAAAGGACGGGCTGGGATCTATCACAACTCTTCCATGAGATACATGGTTTGGACAGGGCTCTTACTTCAGACCACTTTCGCTTTGAGGCGGATCTACATGTCCTCATCTTAACTAGAGCATGATCGTCGCCCTCTGCGGAGCCAGGATCCGCACAGGCGAGTTGGATGGCGAAGTACAGTGAGTAGACAGGGGACCTCACTACAGAGAGCCCACCGGGATATCTCCAGAACTGATTTGTGCGTAGACATGATTGTGAGTACCGCTAGTACGGATAATGGGTGAGTGTGCCCATTGAGCCCCCGCTCGAGGATTCCAACCGTCGCCACGATCCAGCTGCGGATGACCAGCTGGTGTTGTACACAAGGAGCCCGGATTTCATTCCGTGGGTTAGAACTCACGCTCGAAACGCAAACTTATTTGGACGCTCGTAGCAACCTTGGCATCATGATCGGATCTATTGTCCCTGCCCCACCGTCAGGCGCACGACCCTCAGTACGTCTACACGCTGTACCCCCCCTAATCCAAGCTCGACCGCGAATTCGGCCTACGTAGGAGTCTCCCACGCTCCTTGTTAATTTTCATTTGTGAGGAGAATGCTGTGTGAAGTTGAGTAGCAGCTAGAGGGCGCACCCAGGTGCCTTGAAGAAAACACAATGCCAGGGTGATGGGAACTTTTACCAGCAAAACTGTGATGTACTTAATTCGGACTGCTCCGAGTAGTTAATCGGAAACGCCTGGGAGACCTCGGTCAGGGGTGGGATGAGAAAGATCGAGGGACGCTTCTATTACGGATCTATTATTCATCATCTCGTATGTTGGGCCAGTCGTACATTCATGGCCCGTAGACCAAAAATGAGTTGATCTGCGGCGGCCGTTGAATTCCCTCGTGTTATAGCCATCTCGGCAGCCTGAGTTTTAGTGTTATCGGGCGAACGGAAGACTCCTTAACATGCGCGCCTAAGAAGAGCCGTAGGGCCTGTAAAGGATGCCGTATATTATTGGTTGCGGCTGCGGTGCTCCCGTGACAGGCGCTAGCGGCTTCTTGGGACGGCGATATCGTCCCCGTCACAATGGTACCACAACCTTGAAAGAAATGCAAGGCTTTAGTCCGGTGCCGCCGAATACGGGGCTGCAGAAGAAGTGAAATGAGTAATTAATTAGACCTGAATAGTAGCCAGGTACTGGATCTTAACCAGCGTCCGACAAACACATCTCACCTAATCGAAATGTACCGGCTGTAGTCCTCGTGGAGACTTACCCCTTACTCTATTGCGCCTCGTTTGGGTGTAAACAGTTCTATCTACTCGGCCGGTCAGGGGTACATAATTCGTAAGGAGGGTTTAAGCGATAGTTTCTAATGCGCAAGTGCTCAAGAGAAACACAAGTGTCAAGGGCGACTATCCAAGGGGTGCGGACGGGTAGTTTAGACAGTCACTAGCTGTAGGTCTTGCCCTTTCTCACGATACCAACCGAGGGCGTACCGCTTTAGAAGTGTATTGGTTATTCCTTGCCAGTTTGTGGTCATTGTAATAAATCTAACACGCGTTAGAGGTAGTTATTCGCACATGTTTCTAACGGGTAGCTCGCATCACAGCGCATGTCGCCGCATGAGGGGTTAACAAACAACTATCTAGGTTACGTACCTCAATCGCTCCTGAGCATATTTATAATAGCTACCAGTGGCAGAACTTACTTGAGGGTAGTGGGAACTAGCGATTGGCTACCCAGCCTTATTTATTGCCCCGACGGGTGAGGGGTCCAAGAAGCTAAGACTTAGTCGGGGTTATGATAGGAACTTAACAAGTCCTCAATGGAGTGCGATAGTGTAGGTGCCTTACCTGATTTCCATTGAGTCGCGCACGGCAGGACGCAGCGAGGGGACGTGGTCGAGGCCCCTGGGGCGTAGCTCCATAGCGGGATCGGGGCATTCTTTCCGATACTCTGATGGTCTTTAATGTCCGGGATTACTGCCTAGCGCCGGCCATCACTATCCCGCATCAGATCGTTCGTGGCAGTTCGAGAGCGGCTGCTCGCTATTTTCTTTTGTTGGCTTAGTACCATGGGTGTATAGCCAGGTGCAAATTAGCCAGATTCATCACTACACAATAGTGAATGGGGTGTTGGAGGCGCGACCGCCTGCCGTCCCCTGGCGACTACTACCTGTGGCGTGATAATCTTCCAAAGAGCCACCATAGAACGGAATAAGCCACCATTCTTATAGTGTTCCACATCTCCCTCTTCAGAGCGACGGCCTCACCGTAACAACTCGGAATAATGAAGGAGTGTAAACAACATCTCTATCACCGCATTGCATTGTCCTAGTACGGCCTAAGAGTTTTCATAGGCAATGATTCGGTAGCTGCATCCGATTGAGGTACGACGGTACCCCCTCAAAGAGTAGCTCCCACAACATAGGCGGACATACCGCTGATCGCCTCTCTTTAGTATTGTGCGCATCTCGCCCTAGCGAAAAACAGGTGATTGGAGCTGCCTCGAGACTACCTGATCCACGCCCTCAGCGGTTGAGGGGATCGTACGAGTAGACGACTAGCCCATTGACTGGAGTTGACGTATGGTGAACACCGACAGGCTGTCGAACACGCAGAGGGTCCCTATACCGTGTGATAGAGCGCTATAAGTGCGTTGACAATCGATAAAAAGCGCTCAGTGCAAATACTGAGACCTTACCTTCGACTCATTTTCGCGCTATAGGGCGGATCGTTGGGCTAATATGGGACAGGTCCAGTACTTTCATATGTGGGGCTCAACACGCTGCTAGACAAACCAGGATGTGCGGGATACGACGAAGTTTTATCCATTCGTTCGAACGACGATGGAAAATGCACTTTATTGGGAGTCGTTTGGTCACGCTCTAAGGTCGGTGGTACCGGGCAAAACATAGCTGTTCCTATTGCTAACGTTGACCGTACGACATTCGGGAGTTAGCTGATCGGTCAATCTTAGTGCCTCTTTTCCATCTACAAAGGCGATTCCCCTTAAGGCAAACTGTTGCCGTTTTGTATTGGATCTTATCTGGTCGCAATCTACGAGTTAGGGTAGCATATCGACTGTTGAATGTCAGTAGAGCCTTTACTTTGTTTTTATTCAGTAAATCCGTCCACCGCCAATTCGTTCCTTTATTATCTCACGTCACTTAAGGAAGGAACTAAATTGAACCTCGCACCTTCTCCATTCCACCCGATGGGCTGGGGGCACCACAGCTTGAATAACCACCCGAAGCACAAGGAGAGAAAGTGGTCCGCCCGCTCGCCGCTTTTACCAGTGGGTGAGGCACTCACAAACAGGATCTTGCGGGTGGTGAGTGCTCGCATAGCCATAAGGTTATGTCGTAAGGCATGGTTGTGTCTCGGGCCTAAACGATACGGAGCCTCTGGGGATGCTTAGCTGGGCGGACACAGGATACTCCTGTCGTCGTCTGAACAAATGTTGGATTGACTTACAGATCGCCGATAACGGCGTTCATACCTGGCAAAATCCTACGTAATTATGAGGATCTGCCACCGTGGAGGGATGTGCGAGCCTTGGTATTTATGCCGATTGATTCCCCTTACATCAGTGATGCGAGTATTTGCGTATCACATTTCCTTCTCGTCATTTGGAGGGCGTGAGTGATGGCTCAACCAGACTTATTCTCTAAACTTCGACATTTTGGTTACTACCCTCGCTCTAGTATATGCTCAATTCCCCCTGGCGGATCGTGTCCCAGTCCTCCATTAAAACCGAACGAGGCGGCAGCAGGCATTGAGAGCAGAGTGTCAGGAAAGACACACGTGTGATCGCTGACGGCATTGTTTTTGCTCCTGCTCATATTGGTCCTAACCGTACCAGTAGTCGGCACCTGGTTTGTACACGCCCCCCGAGCTCAGTCAGTCAGCAAACATACAACGTTCGGGGAGCTCAACTAGTTCTCACTACGCAGATTAACGTACAAGAAGCGTGTAGAGGTTGGCAGATTCATACGTCTCAGGCCATAAGGCCTCAGTTGTCCAGAATCTGCGCTACCCAAATGGCGCCGTTGGACCTGAGGCGTGTTGGCGTTTTACACGCTGTCCGAGGTGTCGGTACCGCTCAGGGCATAATGGACGCATGACTACGACTAATCGATGTTTGCAACACAAGGGCGCCCTCGGCTGTGTACCCTTATCCTCGGGTAGCGCTATTATGGAAGACAAATTGTATATAACGGTGGTGACTGTTCCGACTGTCCATGTCGAGCAGTCATGTGGCGTCTCTGGGCCGCAAACATTTCAGTCATTGGATCATATAACGCGTCAAAGTGATCCACCGTGGATAACGCCTACGCCCGGGGTTGATGTCAAGAGTCTACAGACCTCTACGCGTGGAGAATCAAGAGGCTATCCTTAACGTCATCGAACCTCCTCCACGGGTAGTTGGTCTGTTTTAGATAAACTCTTTCAAATTTACTGTCTCATGGTATCTTAGAGTGTGTGAACCATACTCTAGTCCTATCCGGAGCGAAGGGTCGGCGCAAGGGTAACGGCACCAAATTTCTGATGTAGTACTCAAGAGCACACCAAAGCCCGTGCGTAAATACATCGCTTTGCTTTACGACATCTCACCAATACTTGGCCGGATTATTGGCATTAGCCCTAAATACATAAGGTCTATGCGGTTAAGAAGTTGTTCGTCTGAGTTAGGCTGCGGTTACACTCCATCAGGCTAGTAGGTGGAAATACATAGGGCAGAACTGCATGTTTGACGAGGGGACTCATTCGAAAGGTCTGCCCCAGGTGCTCAGCACGGCGTCTGCCAAACCGGTCAAGGACTAGAATTTGCCACCGCTAAGAAGAATGAATACTTCCCTTCGATCCTAGGAATCACACTCAGGTCGTGTTATAGAGCCACCACGCCCGAAGGCGGATGTGGATTTAAGGGAACCATAAATGGAGCTATCTGTCACATTAGCATCTCAGTTAGAGCTGGAATACGGGGCCTCGAGCTATTGCAATCAACTGGTCGGAGATATCAAACCCTTATACCTTCCCAGTTGTAGGTAGGAAGATCTACTTGAAAGCAAACTCACGAAACTGGTAATCGCAAGCGCTTTTATCTACTCAAATACCCGTTTTTAAGACACTCGGCGAGCAACGCGGGGCGACGGTGAAGTGCAGCGGAGCGGGACTGACCTACCGAATCAGTTTATGGTTGTGCTCAGAATTGATCGTGACCTTGTTTGTGCTGTGTATATGTTTATAGTCCATATTAAGGCTTTAGTTATGGGAGCATACCGGTATTAAGAAGACGCCTGCTTAGATCCTCCAGAGTAATGACATTTACGGAGCTGAAGAGCAGATCTTGATATCGCTCCGTCTCCTCTGACCCTCGTCACACCGCCCCATTATTAAGTGAGCGCTTCAAACCCGACCACAGTGCGGAAGCACCCGGCGGTGATATTCGGTCCGCGTAACCCGTAAACGAAGGTCAAAACTCGGGCTCGCTTCGCTCGATAATTTAATCATCAATCTGTGGTAGCCCTAGAGACAGCAGTCCCGTCGAAAGCGTATAATCACCACGTATTCGTTACTGCGTGACGAGCTGGTAATATACTCAAGGCGGGCAAGACAAGACGAATTACGGACTGTGGACTGGTTGATCGAAGTTCACAAGGAACACAGCATCGCCATACCCAATCAGCCTCAAGACACCTCCTTCTGTCCTAATCGAAAAAGAGCGTCGAGCAACCATGACAGGCGCACTTTCCTCACAAAGCAAAATGTTAAAAGGGTAGCCCCTGACTCAAATCCCTCGCGCCGAGCGGTGCACACAGTGCGGGCGAGAGTCCTTTCCTAAGGCTTAAGCTTCGGAATGGGGCCATCCACTCCTTAATTTACGTGAGTGTTGAAATCGTCGGTCGACGTGCGGCTTCCAGAAGGCAGGAGACTGCACCACTTGCATGTATACTTCTCTACTGCGCTCATCAATGCCATGGGAGACGAACAGTTATCCGAGAGGTATGTCTGGCAATACGTTCCTTTGACAAGAGCGCAACTGGCAGTGAGAACGAAATCAGTGTTTTGATCGACCACGACAACAATGAAGAGAGGGTAGTGAAACCGACAGTGGAGGGAAGCCCTATCCAAACTGATGGGATGGCGAAAACACGTGGGCCGTGATCAACATAAGCGTATAAAACAATCCATTTAACAGAATCACGTCCCTCCCATTACTAAAGAGTTCCATTTTGGGAAGGTTGCTTATACACGTCGCATCATGGTTTACGGAAGGAAGGTTCGCCCCAGGGGATCGTTCCTTAACAGGCGCAGACACCGGCCCGGGCGCGCTCAAGCATACCGTTCCTCTATTAATTACTCCCCTTTACTCTAATCCTGAGAGGAATCGGTTCATAGCCTCCCGCCCCGGTCCCGGCGTGATTATCCTCTGTGCCCCAAACAAATAGAGGGTAAGCCGTACTAGGATGAGTCCTCGTCTCAACTGAGATCCTATGCGGAAGCACGCATGGCTAATTCCTGTGGAAATCCGTGACGCTTCATCGGTTGTAATAAAGAAAGCAGACTATATTATTGACACCTCAGAAACGTTTCTTGAAGTCCCCCCGCTTTGTGGTTGAAGTAGATGGAGTTCTCTTGATTCTCGCACTATCGGAGGCGGCCAGTCGTAGTGGAAGGTGGCCGTCTCCCGGGATGAACGCATACTGTTGTCACCTTTCCGTAAACTGATGACCTGCCTGGTCCCAAACGGTAGTGCTATCCCGGGTTTTCACGGATTTCATAGCGTAAGTAATCTTCGATTCAGTTATAGATTTAGAAGGCGCGACTAGATGGAGCGCTGACGTGGGAATTTACCATTAGTCCATTCATATCGCCAAATTGATGCCATCCGTACTTATGGTCTGCAACTCCTCGTTAGCGCTTGTGCGCATCGATCGAACAATGCAGAGCGGGAAGACGCGCCTTCTAAAAGGATCATCAGAATCAGATGGACGTATAACTCAACATGTGTGTGCAGGGGCCTTCTCCAGGGTATGCATGGGAAGAGATGAGTGAACCCCGCAATCCCAAGGTCTGCGCTCAACGCAATGTGGACGAGTCGCGTGTTCGGGCCGATAGCGACGGATCTATGTTTCAGCGAGGATGGCTCCATTGTGTCTCGATCGAAAGAGGTTACAGGAGATGATCATCCACCTACTTTAACCTGGCACGTACCTATCTGCTGGTCCCTCGTGAGACTGTAGCTAGCCCCATTGGGTCGCGGTCTTTAGTCGGGTCGCCTCTGCAGTCGATCCCCAGAGCGAGTTATTACTAGAAGTTACCCGAACGCGTTAAACTTGTGGGTCTACCGACCTCACCCATTAAGCGGGAGATAATAGCGCCACAAGGCATGCTGCTAAGGACGCACTCACCATGGCTGTAAGAATGGTGGAAAATCACGAGTGCATTTCCCCTAATACGGCGAACCTCGGCAGAGCGACGTATAGTCCCCCTAAGAATAAGATATGAACATTGGTCTTACTACCACCAAGTCGCATGCCAGTAGTACATAAATGAATAATTGCTGTGTTTGTCACTCACACCGAAATTTAGGGTTTAACCCGTCCTGGCATCCAATATTCACGGTTTCCTTAGATACG'
MinimumSkewProblem(Text)
'''

def getAllWordWithOneMismatch(word):
	words, letters = set([]), ['A', 'C', 'T', 'G']
	for i in range(len(word)):
		for letter in letters:
			if letter != word[i]:
				words.add(word[:i] + letter + word[i+1:])
	return words

def FrequentWordswithMismatchesProblem(Text, k, d):
	counts = {}
	for i in range(len(Text) - k + 1):
		kmer = Text[i:i+k]
		allwords = [kmer]
		curwords = [kmer]
		for j in range(1, d+1):
			temp = []
			for word in curwords:
				temp += list(getAllWordWithOneMismatch(word))
			curwords = list(set(temp))
			allwords += curwords
			allwords = list(set(allwords))
		for word in allwords:
			counts[word] = counts.get(word, 0) + 1
	maxcount = max([counts[kmer] for kmer in counts])
	print ' '.join([kmer for kmer in counts if counts[kmer] == maxcount])

'''	
#Text = 'ACGTTGCATGTCGCATGATGCATGAGAGCT'
#k, d = 4, 1
Text = 'CTGACTTTCAGTTCCGAACGCGAAGGACGCTGACTTTCTTGCCGAGGTTGCCGAGGTTGCCGAGGGCGAAGGACGTCACGGAACTGACTTTCTCACGGAACTGACTTTCAGTTCCGAACTCACGGAATCACGGAAAGTTCCGAACCTGACTTTCGCGAAGGACGGCGAAGGACGTTGCCGAGGGCGAAGGACGAGTTCCGAACTTGCCGAGGTCACGGAATTGCCGAGGTTGCCGAGGTTGCCGAGGTTGCCGAGGTCACGGAATTGCCGAGGTCACGGAATTGCCGAGGTTGCCGAGGCTGACTTTCGCGAAGGACGGCGAAGGACGAGTTCCGAACTCACGGAATCACGGAATTGCCGAGGGCGAAGGACGAGTTCCGAACTCACGGAATCACGGAACTGACTTTCGCGAAGGACGTCACGGAACTGACTTTCCTGACTTTCTCACGGAATCACGGAATCACGGAAAGTTCCGAACTTGCCGAGGTCACGGAATCACGGAAGCGAAGGACGGCGAAGGACGCTGACTTTCAGTTCCGAACAGTTCCGAACTCACGGAAAGTTCCGAACAGTTCCGAACTTGCCGAGGAGTTCCGAACGCGAAGGACGTTGCCGAGGAGTTCCGAACCTGACTTTCAGTTCCGAACAGTTCCGAACAGTTCCGAACCTGACTTTCGCGAAGGACGAGTTCCGAACTTGCCGAGGAGTTCCGAACTTGCCGAGGCTGACTTTCCTGACTTTCTCACGGAAGCGAAGGACGTTGCCGAGGTTGCCGAGGTCACGGAAAGTTCCGAACTCACGGAAGCGAAGGACGAGTTCCGAACAGTTCCGAACAGTTCCGAACCTGACTTTCTCACGGAACTGACTTTCGCGAAGGACGTCACGGAATTGCCGAGGCTGACTTTC'
k, d = 6, 2
FrequentWordswithMismatchesProblem(Text, k, d)	
'''

def getAllWordsUptodMismatches(curwords, d):
	allwords = curwords
	for j in range(1, d+1):
		temp = []
		for word in curwords:
			temp += list(getAllWordWithOneMismatch(word))
		curwords = list(set(temp))
		allwords += curwords
		allwords = list(set(allwords))
	return allwords	

def FrequentWordswithMismatchesReverseComplementProblem(Text, k, d):
	counts = {}
	for i in range(len(Text) - k + 1):
		kmer = Text[i:i+k]
		allwords = getAllWordsUptodMismatches([kmer], d)
		for word in allwords:
			counts[word] = counts.get(word, 0) + 1		
	maxcount = max([counts.get(kmer, 0) + counts.get(ReverseComplementProblem(kmer), 0) for kmer in counts])
	#print maxcount
	print ' '.join([kmer for kmer in counts if counts.get(kmer, 0) + counts.get(ReverseComplementProblem(kmer), 0) == maxcount])

'''
Text = 'ACGTTGCATGTCGCATGATGCATGAGAGCT'
k, d = 4, 1
Text = 'AAGACAGCAAAAAAGAGAAAGACAGCAAGTGGATAGCGCGCGGAATGTGGATAGCGTGGATAGCAAAAGAGAGCGCGGAATTGCGCTCCAAAAGAGAGCGCGGAATGCGCGGAATGCGCGGAATGCGCGGAATTGCGCTCCTGCGCTCCAAAAGAGAAAAAGAGAAAAAGAGAAAAAGAGAAAGACAGCAAAAAAGAGAGTGGATAGCTGCGCTCCGCGCGGAATTGCGCTCCTGCGCTCCAAAAGAGAAAAAGAGATGCGCTCCAAGACAGCAAGCGCGGAATTGCGCTCCGCGCGGAATTGCGCTCCAAGACAGCAAGTGGATAGCAAAAGAGAAAGACAGCAAGCGCGGAATGTGGATAGCAAGACAGCAAAAGACAGCAAGCGCGGAATTGCGCTCCGTGGATAGCTGCGCTCCAAGACAGCAAGCGCGGAATTGCGCTCCGTGGATAGCAAAAGAGAAAAAGAGAGCGCGGAATGTGGATAGCAAGACAGCAATGCGCTCCAAAAGAGAGTGGATAGCGTGGATAGCAAAAGAGAGTGGATAGCAAGACAGCAAAAGACAGCAAGTGGATAGCTGCGCTCCAAAAGAGAGCGCGGAATGTGGATAGCTGCGCTCCTGCGCTCCAAAAGAGAAAAAGAGAGTGGATAGCAAGACAGCAAGCGCGGAATGTGGATAGCAAGACAGCAAAAAAGAGAAAGACAGCAAGTGGATAGCGCGCGGAATGCGCGGAATTGCGCTCCAAGACAGCAAAAGACAGCAAGTGGATAGCGCGCGGAATAAGACAGCAAAAGACAGCAAAAAAGAGAGTGGATAGCGTGGATAGCAAGACAGCAAAAGACAGCAAGCGCGGAATAAGACAGCAATGCGCTCCGCGCGGAATGTGGATAGCGTGGATAGCTGCGCTCCAAAAGAGATGCGCTCC'
k, d = 6, 3
FrequentWordswithMismatchesReverseComplementProblem(Text, k, d)	
'''

import itertools
def FrequencyArray(Text, k):
	A = {kmer:0 for kmer in ["".join(seq) for seq in itertools.product("ACTG", repeat=k)]}
	#print A
	for i in range(len(Text)-k+1):
		A[Text[i:i+k]] = A[Text[i:i+k]] + 1
	print ' '.join(map(str, [A[k] for k in sorted(A)]))	

'''	
lines = read_file('inpros68.txt')
lines = read_file('rosalind_1kba.txt')
FrequencyArray(lines[0], int(lines[1]))
'''

def PatterntoNumber(Text):
	#print sorted(["".join(seq) for seq in itertools.product("ACTG", repeat=len(Text))]).index(Text)
	num, n = 0, len(Text)
	i, pow4, gap = n - 1, 1, {'A':0, 'C':1, 'G':2, 'T':3} # ACTG
	while i >= 0:
		#print pow4 * gap[Text[i]]
		num += pow4 * gap[Text[i]]
		pow4 *= 4
		i -= 1
	print num	

'''
Text = 'CAAGTACACTAACGTTGGACGCCTGGG' #'AGT'	
PatterntoNumber(Text)
'''

def NumbertoPattern(index, k):
	i, pow4, base = 0, 4**(k - 1), {0:'A', 1:'C', 2:'G', 3:'T'} # ACTG
	pat = ''
	while i < k:
		pat += base[index / pow4]
		index = index % pow4			
		pow4 /= 4
		i += 1
	print pat	

'''
index, k = 5427, 9 #45, 4
NumbertoPattern(index, k)
'''

def Generated1NeighborhoodString(Text):
	strings = set([])
	for i in range(len(Text)):
		for base in ['A', 'C', 'T', 'G']:
			strings.add(Text[:i] + base + Text[i+1:])
	return strings
	
def GeneratedNeighborhoodString(Text, d):
	inp = out = set([Text])
	for i in range(d):
		out = set([])
		for Text in inp:
			out = out.union(Generated1NeighborhoodString(Text))
		inp = out
	#for string in sorted(out):
	#	print string
	return out

'''
Text, d = 'GCACTACT', 3 #'ACG', 1
GeneratedNeighborhoodString(Text, d)
'''

def MotifEnumeration(strings, k, d):
	motifs = set([])
	for i in range(len(strings[0])-k+1):
		motifs = motifs.union(GeneratedNeighborhoodString(strings[0][i:i+k], d))
	common_motifs = motifs
	for string in strings[1:]:
		motifs = set([])
		for i in range(len(string)-k+1):
			motifs = motifs.union(GeneratedNeighborhoodString(string[i:i+k], d))
		common_motifs = common_motifs.intersection(motifs)
	#print ' '.join(common_motifs)
	return common_motifs

'''	
#lines = read_file('inpros69.txt')	
lines = read_file('rosalind_2aba.txt')	
k, d = map(int, lines[0].split())
MotifEnumeration(lines[1:], k, d)
'''

def Hamming(s1, s2):
	return sum([1 if s1[i] != s2[i] else 0 for i in range(len(s1))])

def DistTextPattern(Text, Pat):
	k = len(Pat)
	return min([Hamming(Text[i:i+k], Pat) for i in range(len(Text)-k+1)])

def DistTextsPattern(Texts, Pat):
	return sum([DistTextPattern(Text, Pat) for Text in Texts])

'''	
#lines = read_file('inpros70.txt')	
lines = read_file('rosalind_2bba.txt')	
k, strings = int(lines[0]), lines[1:]
d = 0
while True:
	motifs = MotifEnumeration(strings, k, d)
	if len(motifs) > 0:
		print min([(DistTextsPattern(strings, motif), motif) for motif in motifs])				
		break
	d += 1
'''

'''
#lines = read_file('inpros74.txt')	
lines = read_file('rosalind_2hba.txt')	
print DistTextsPattern(lines[1].split(), lines[0])
'''
	
def ErrorCorrectioninReads(sequences):
	counts = {}
	for sequence in sequences:
		comp_sequence = ReverseComplementProblem(sequence)
		counts[sequence] = counts.get(sequence, 0) + 1
		if comp_sequence in sequences:
			counts[comp_sequence] = counts.get(comp_sequence, 0) + 1
		#sequence_pair = sorted((sequence, comp_sequence))
		#sequence_pair = (sequence_pair[0], sequence_pair[1])
		#counts[sequence_pair] = counts.get(sequence_pair, 0) + 1
	sequences = set(sequences)	
	correct_reads, incorrect_reads = [], []
	for sequence in sequences:
		if counts[sequence] == 1:
			incorrect_reads += [sequence]
		else:
			correct_reads += [sequence]
	#print incorrect_reads
	for sequence in incorrect_reads:
		for sequence1 in correct_reads:
			if Hamming(sequence, sequence1) == 1:
				print sequence + '->' + sequence1
				break
			rsequence1 = ReverseComplementProblem(sequence1)
			if Hamming(sequence, rsequence1) == 1:
				print sequence + '->' + rsequence1
				break
'''	
#sequences, qualities = get_seq_fasta(read_file('inpros71.txt'))
sequences, qualities = get_seq_fasta(read_file('rosalind_corr.txt'))
ErrorCorrectioninReads(sequences)
'''
	
def ProteinTranslationProblem(RNAstr):
	lines = read_file('RNA_PROT.txt')
	map = {}
	for line in lines:
		rna, prot = str.split(line)
		map[rna] = prot
	i, prot = 0, ''
	while i < len(RNAstr):
		prot += map[RNAstr[i:i+3]] if map[RNAstr[i:i+3]] != 'STOP' else ''
		i += 3
	return prot 

#print ProteinTranslationProblem('AUGGUAGUCAUUCUGGGCACACCGUCUCCACCUGACGGAACCAUACUCUUUUGUGUGCUGCCGGGCUCCUGUGGAUUUCUUCGUAGAAACGUGGCCGUGCUGUCUCCGGUCGCAUAUCGAACGGUGGACCGACACGUUGUUAUUCAAAUGGCGGCGCACGUCCGGAUCGUUUUGUGGGUUAUCUGCAUCUCCAUGCCACCAGACGCCUCUGGGGAUCGUCGGGGGUGUCGGAGGAGACCCCAAGAACUGCGGCUUCCGCGCAGAGGGGCAGGGGGUCUCGUAGCACGGGCCUCGGGUUGUCCAGUAAAGCACCACGAAGACAGGUACCGGUGGGUGAUGGAGAUGUCAAUUAGAAUAGUGGGGACUUCUUGGAUUUUAUUUAUUUGCGAUCAAGUCGCACCCUCCCGGACGUGUAUGACUAUGCCCGGUAGGUGCCAGAGAGCGCUCUCUCAACCAGGCAUAUCGAUCGCUGACUGCGAACAGGUCGGAGGGUGUGAUACAAUUUUACCGAACCAACAAUCCCUGGAACGAUCAUUAACUUCACUCGAAAUGGGCCAACCUCGGCACCAGGAGCAGGGCCAGUGUGUUCCCCGGCGGCCAGAGGUAUGCCAACAGGGUACGGUCCUCACUUCAUGCAGUGUUGCCGCCGUUCUGCACGCCGUCCCGCGUCAUUCAAGACCGAAGGUAGUAAUUCUUGAUAGGACAUUCCGGCACGGUUUGGGCCAAGGAGGACAACCCUACCCGUACGUCUCCGGAGACAAAACAGAGGGGACAGCUACGAAAUAUCAUGGAACCAAGGCGGCAGACGCGAGCCGCUGUGCUGGAUUUGUUCAUCUCUAUUGGGAGACGAUUCGUGCCUUAGACGGCUCCCCAAUGCUACUGCAAGAGUCGGACGACUGCGAGGCGGCUACUCGGAGCGACAGUAAUCCGAGUCUUUACGUCGUCAGUCUUUACCGACCUCUUGAUGCUUGCAUUGCGCUCAGGGUACAAUUAUUGCGUUGCCGGGUGCGUAGGUCAAACGCUCGCCAAUGUAACCACUCUUUAUAUGCUAUAAUUGGGAGUUCAACGAGUAAGUCCAUCAUCGAUGGACCCUACUCUACCCCCGCCUCCCGUAUGGUUUUUCCCGCGGUCAUCAUAGUGCGGAACGCUCCUGAGAAUAGCCAGGACCCUUUAUACUCCUCACUGACGAUUUUCAGUGACGAAGACUUCCUAUUCAGCCCGGUAAGCGAAUUGAUUUUGUAUACUAUAACUGCCGUUGCCACUACCUGUUUGUGGGGACAACCGACGGUCGUACAUAUUCGAUUCCCUUUUGGAAAAUCAACGCCGGGGUGUUACCGGGAAAGGGUCUGCGAACGCGUCCUCGGCGUUAAUCGUGUCCCUGGACGGAUUUUCGUCCUUAAUUGUUUGGGGUCUGACACGUGCACCGGGAUCGUCUACAUUGGCUACACAUGCGGCACCUCUCCUCACCACUGUGCGAUAUAUAUUCGAAUACCGUUAAGGGUUGCAGUUCAUCUCAAGCAUGACGCUGGAAUCCGUGUAGUAAAACCCGGCUUAGGAGAGGAUUUUGACUUUCACAUCCGUCGAACGAUAGAGUCCGGAAUCAUGGAACCCGCAUCACGGUCCUCCAGAAUUAGUCUUGUCGUCCUUACGUUUCGAGUUCAUACAGGAGCGAAAUCUCCGCCCCCCGAUGAAAUGCGGCUAUUGGAUCAGAUAAACAAUCGGGUAGGGCUCUGUCUUUCUUUCGCUAUGCAGCGGGGUGUAGUAGUGAUGUCUGUCCGGGCCCGAUCCGAAUCUCGAUCCCCUGGGUCCACAUUGUUACGACUCCGCAUGAAAACCCCGAGUAGGGGGAUAAUCACGUCGAUCACGCGUUGUUAUGUGAAAGUUGACGCGAAUGAGAACGGAGCGGAAGUCACUUGGCGUCAUAUUACGACAGCAACCGAGGCUCCUUGCUCUCUGCCCGAUCACCUCCGCAUAGCUUGGGGUGGCCUCAAACACGGAGAUCCACACUGGGAGUCUGUCAGUACACUCCCUGAUGAGGUUCGGGCCAGUAAUGUAUCACAGGGAAUUGCGUCGGGUGAAACGCAGAUAGUUCUCCCGCCAGCGAACUCGCUCAUCGCCUCUAACAACGAUCACGCCUGCAGAGUAAAAACCUUGGUGUGCGCCGAUAGGCCAGUAAUGUCUAAAGCUAUUACCUUCGCCAGGCACCUCACUCUCGAUGGCCUUGCUCCCGGUCGUCUAUGCCAAAAAGUGUGGAAAUGGCUUAUGCUGGGUGUAACUGUUUCCGCAAAGUUUCUUCAGCAUCCUUCCGUCGUGCGUGUCACACCAAGAAGAGCCAGGUGUGUCGUCCGGAGUGGUAAUGCGCCGAUCGGAGACCUGAUAAAUAACCGCGUCCACAACCGCGACGCAGAGAAUGGAUGUAGGCUGAGAAGCGCGAGCACCAUGAGUGGGGAUUUGGUACCGCCUUCACCUAAGGACAAACACUCCUUAACUGCGCUCGCAGCGCUUAGGCUCAACAUGCUGCUGAGGACUGGAGCUAUCGAUUUCUGUGUAGCGUUGUCGGCCUUGCAGUCGUGGGGCAAAGCACUCGAGCGUUCGAGCGAUAUCCAUACCAUACAUCCACGAACCGUAGGAAAUGGAGUCCCAACGGCCACAGGGUUAUAUUGUCUCUUAGAAAUACUCGCCCGGGAGAAGAGUACGGAACGCUAUACGCUGACCGUCACGGCUUGCACCUGUUGUAAAUUGUCUGUGGUCGCUCCACAUUCUAGUUACAUCGGUUCGCGCGAUUUCUUAGUAGUAAAUGCAAUCCAUGACGACUGUUAUUGCUUUCAUGAAUCUAACUGCUCAUGUCCCUAUCUCCAGACUCUUAAUCCAAUCUCACCUUCUACCACCAGAAGAAUUAUGAGGCCGGGCGUAUUUAGGUUCGACCGCCACGGUGCGAUAUACGUAGAGUUGUGGACCUUAGCCUGCAUCGGCCUUAUUCAUCCCGGAAAUUGCAUAAAGCUUCCUACCAGACGUCUCCAGGUAUACCUGAACACCCGUUCCAUAAAACGGCGUAGAUCGACGGCAGUGACUGUGGUACGUAAUGCGGCUCCUAAGCCCGACAGUAGUAUGUCAGUGCCUCCAUGUUUUUCCUCCGGGCCAUCAGUGCAGCAACUAACCGAACCGAAGACGAGGGUCCACCGGCGCCAAGAGCGAAAAGUUUCCGGCAGCUCAAGGAGUACGCUAUCACUCAGUGAGCAACGACCCCCACUGGCAUUUGCGCUCGGGACCUCUAACGGGUAUGGGGCGAUCAUUAACAAGGCAGAAAUAUUCGGCUUGUCUUACUCACGCAAGGUCAGCGCGUGGAAAAUUAACGACUCGUUCCACAUCCCUUUAAUGGGCAUCAGAUCGCUUCCUUAUUCGCGCAACGAAGACACAAUGGGAAGUGAUUACCCCCACCCGCGUUAUAAUCAAUCAUCGUCAUCAAAUCGACUGCGAACACCGUUCCUUGUUAAUACACGAUGGCCCGGAGGGUGUAGCAACAAGGAGGAGUUUGUGUUGGGUAGCGCAGGUAUUUGGAUGUUUAUACAUUUGUCUGAUGAUUCUGACAUACGAAGUUGCGAAUUCUGUUGGAAGAUGGCAUCCCAGCGGUGUCACUGGUACAUUCUAUUAGCAGUGGCGCGGCAAGGGUGCUGCGUGAGGUUCCUCCCAGAUAGAACUUCAUGUAUCCUUAGCGAUGCACCGAUAGUAUGCGAGGAGGGACGUCUCCGUGCACCAACAGCGUGCUUGUUUAGUCCCAUAUGUGGGCAGCUACCCAUCCGGCAUCGAUUAAGGAGUCAGUGUGAGAGUACAGAUGCCUACCAAAGUCGAGAAAUCAUUGACUUAUUACCGCAACCCGAUCAGUGGAUAUCAGGAGAAACAGGCUUAGGUGAUACGGCUGGGAAGCCGUCCACGCUCGCAGCUGGCGCUUGUGAUCCUCCACUCAUGCGCUAUAGACUCACGGGUAUUCUCCGUUGUUGUGCGGUGUUAAGGCUCCACGGUGCCGCGAACGUUAGUGGUAUUUCGGAUGUAUGGUCCCGAUGCGACCCCAUCGAGUUGCGACGGAUACUAUAUAGCGUAUCGAGUAAAACCUUGAUUACGUGGAGCAGUAGCUGUAUGUCCGUACGACUCUGGAUUCUAUUAUACUGGGUCACACACCUCCAAGGUUUAUAUACGAAUUCUCGCCAGGGCGGUUGCCUGAACCGUUCUCGCGGUAUUCUUACCGGGCGGAAGUUGCUGUGCUCCCGAGACACGAUUUUGUUCCCCGUAGUCGGCUCUAUUAAAGCACCCCUUGGUAGAGAGCUGGUCUCACCUCAGAGGAAUGAGGGCAUCCGAUCUCAGGGCAUCAAGCCCGGCGUCAGGGUGUCAACUCUACUUGGGAAUCUUACGUUCCUAAUAUUCAGACACUUCUUUACCAUAUACAGGCCUACUACGCGUUACCUCUUUGUUCCAAUUUCCGAAACAAAAUGGGCGCAAGUGACGGAGACCAGUCCUAUCGUCCAGCUCCACUACACCGGAAUUAUCUCGGGCAUGCCGACAAGAUCUAAUAAUAACCAACGUCUAUCUGCUGGUGGCACUCAUGUCCCCUCCGAUCUGUAUGCAUCUGCCCUCAUAAUAGUCCAUCUUUAUGCCCCGGGUCUGCGCUCCCACUCCGCCUUCGCCAUGUCGAUUAACACGAUACUUGUAAAGGAAAUACCAGUCGCGUCCAUCGCGAUAUUAUCCCUUACCGGUUUGAAUAGUUCAUCCUCAGCUGGCACCGGCAUCUCCAGGGUCGUAUGUAAGUCAAUGGCUGAACAAAACGGCAUAUGUUCGCGAGGUGAUAAUCCUACAGUACCUAGGCCUAGAACGUCCCUAGUCGAGCAAUCGACUGUUCCUGACACGCCUCACUGCCACCGCCGCGGUCCCAGGAACGGGCGCUGGCCUAAACAUACGCCGUCGUGCAGUUCCCCCGGGGAAGAAGAUGUCUCGUCAUAUUCGUCCACGCCCGGCUCGGGGCAUGCCAACCAUCAUGGUACCGUUAGAGUGCUAUGUAAUCAAGUGGAAGCUUUAUUAAAGCGUACGCCCCUGGUCCUUGGCACAUCCGCACGUCUAACUUUCACGGGCUGCAUGACCGGCACCAUACUGCAUACAGGCUUGCCGCAUUUGCAUCGCGUGACGGGGCCCAGCAUAUCACACCUGGCAUUAAUACCUGUCAGGUUUUGUAAAGCAGCAUGCGACAUCACCAUCCAUGUUAGGAAUACCAGUCUCCUUUUUUCGGCUCGGAAUCAGCAGUCAGCAGCGAUAAUAUUGUUUAGAAUGACGGAACUGCCACAACCAGAGGCGCGAACCCAGAACGUGUUAGAGGCUUCUGAGUUGGAGGCCAAGACGCAGACCUUUUUGUUAAAGCAGUUAUGCCCCCAGAGAAAGUUAAUGACGGUUUGUGUGCUCCAGAGGUUCUGCGAUCUGCUACCUUUUCUACCGCACAGAUCCCUAAUUUUUGAGUUGGGCCAAGCCUCGGUGCUGGGAUCGGUAUAUCCGCACAGCCGAUAUGCGGUCGAAGAUAAGCGCUAUCCGGACCGAGAAUCACCUGGUAUGGAGCCCGAACUCAGAGUACACAUGAGAAGCGGUCUCCUUAAAAAGUUACUCAGCGGGUCCAGGUACAUUAAAAUUUGGUUACAAGAACUGUUGGCGAGCCUGAUUGGCGACGAAAGAAGGCGACCAGACGCAAGGUCGCAGCAUAUAAUCAGUCUUCGUCUCUACACAUGGAAGGCUUGCGCAUCGGGUCGCCAUAGACCAGGAGCUGUGGUUCGGGCCCGUGUUCAGAGACGCAGUUGUAUUUCCGUACCGCUAUGCAUAUGGGUGAUAGCAUAUUUUCUCGCAAGAUACCACCGUGAUGACAGACCUCAUCUCAUCCGGCGCUAUGACUCUCGGUGUCUCGGCGAAUGCAUAAAUCCGGAUACUGAACAAGCGCAUUUCUGCGGCGUUCUGGCCGCUCAGCGACCCGUUUUGCCGGGAGCCGUAUGUCGUAGUCCGUGCCCAAUCCCUUAUAGCUGUAGGCGAAAAAUACCGGCGAGCUGCUACCACUGUGUACUUUUCUGCCUAGCCAUUGCAAAAAGGAUAGCAAUCCUAAAGCAAUAUGCGCAGCCGCGAUCAGGCCGUAAACCGGCCCGUGUAUCUUCAAUCGGCUCUUAUACAGUGUCCGGUUCAAACUGCGGUUCCUGGAUUGACGUUUCGGUCAGCAAGCGAGACGCGGCCCCUGUUCUUCUCUUCAAGGUGCUAAGGCUCAUUAUUGUCUCGCGUAGGACGAAACUGUACGUACCGUGCGUGAGAUGUAUCCUUAGGUAUUUUAAUAAGGAGGUUUUACAGUUAGAGCAGCAAUCGUCUGGGCUGUCCAUUAGGUCUACAGUUGAGUCGGAUGCGGAAAUGGGCGGCACAACCAUAACGGGAGCCCACGUGAGGGAGAUUCCAGAAAAUGUAUGGUCGGUCUUAUCGCAACAUAGUGUGAGUCUGGCGACUGCCCGACUUUGUAUCUGGGUGAAUUCUGUUUCGGAUAGCAAAGGGCUGUACUCAUUUUGUCAGGACGAUCGGUUUAUCUGUGGUUUACCGCGGUGUCGCGGGCCCUUAGCGUACCCCCAAUCAUCAGCAAUUGCGGAAGCCCGACGAGGGGGCCGCGCUAUCCCAGAGCCCUGUACCUUCAUCCACUUUCCAGGGGUGAUAGCGGAGCGUAUGUUACAGUGCACUCACGUUCAGACGUCAGACUCCGAUGGGCAAGAUUCGCUUCUGGGUUAUCCAUCGACAAUUUUGGUACGUCGAGCAGGCAGAAGUGAUCUCCUAUAUUAUGAACUCCUGAUGCUAACAGUGGCUUUGGACGCUGGCUGUAACGCAUCUAUAUCACAGGUGCCCAACGCGGUAAAUAGUUCCACGAACCCAGGAGCUAGUCCUUCUGCUAUAAAAUGUAGGUGCGUUAUAAGUGCCCAGAAUCCUGAACUGUACACUGACGCAGUAAACGAGGCCCAUUCGCAAGGAAUAACAUAUCUGACACCAGUCUCAAGAAAACAUUUCUGGGCGCCCUUAUGCAACGGAGGGCCGAGGAAGCACUGCGCCCUGAUAGACUACGGCGUCUCCCAGAGUAUGCCAACUAGCAACGCCUGCCUAUCGCGACUCAGACUGAGUAGUCACAGUGCGACUUGUUGUGGGUCCGUAAAAGAAUUUAGACAAUAUAAUACCCAAUAUUUUUUUUGCCUAACUCCACCAAGGCCGAGCCCACGACAAAAUGAACCACGGAGGAUCAUGUCUAUUCAGGCCUUUACAAGACACGGGGGUCACUCUUGUUGGAGCCGUAAGGGCAUCUUUCCCUACGACAAAUCAUUAUGUGCGCCUUGCAUCUGCAGUCUAAUCGAUCACAAAGGUGAGCGGUCCUGCUCCUACAGCCCAACAACAGGUUUUGAAAAACUAAUUUCGACCGCGGUUGUCAUCUUCCCCGUUAGUGGGAUUGCGACAAAUUUCAGAGGAGGAACGGAUUCACACAUAAGUCUGAAUGCUGUAUUGUCUGGGACUUGGCGACAGCUAGAGACAUUAGACGUUCGCUCCAUCGGACACGCUCACUUUGUUGCCUCGGGGCCCUCAACGGGCAACCUCAGUAACCCGCCACGCCGGCAAUCAGCUAGUCCAUUGGUUUCUAGAAGGCGGGAGUCACAAUUUCCGAGCUUUAACCAAGUACACGGAGGUUAUCGAUUAUCUAAAGGUUAUUCCGUGAGAGAAGACCUGUUAUCGCCUUCUUUCCGUCAUCUUGUCUUCUCUUUAUGUGAACUGUUCGCUUUAGUUACCGGACAUACGCUUACCGCCGUGUACUCGCACUUGAAGCCCAAAGUCAGAUUCACUGAGCGUAAUAUCUCGUCUCUCCGGCCACCGCGGGGGGAGAGUCGCCGAUCUGAGAACUCAAGGCAUGACUGGUUCGCAUUAAGUGAGCAGGUCGGCCGCCUACUAACUAACCCCAUUGCCUUGAUGUGGGGCAAUAUGAUUUACACACUACCGGCGUUCGAGCGAUCCCCGGUUAAAAGAAGACUGACGUACGAAAUACGUUUCAACCAUAAGUGUGCGAAUGCUAGUGUCUGCGGUAUAUUGUUUUACUCUCACGAAGCACCGGACGCAGCUAAACGGUACGUCAUUUCGAUCGCUAACGAGUUCGGUCCAGGGGCUCCGUGCCGCAAUGUAACGGUAACGGCAUUUCUUGUGUGCAGUUUCAUAUUCCUCAGUUCGAAGGCAUGGGACUCACUACCUCAAUACACAAUGGGCUGGGUGGUUGGUUUGGAGAGAAAAUUUAAGUGUGCCUUACCCUCAGCCGCAACCAGAGUCUAUCCAGGUAAUUGGCGCUUGUACCCCGGCCAAGCAUGUCCUUAUGCGUGCUCAGGAAUCCUCAAUCCGGUGUCCAACCGGCGGGAUGUCGGUGAAUUAACCCCCGUUCUCUCGCAAGUUAAGGUGCUCCUUUACGCUCUAAGGCAAUCAGAUCACAUGAUCAUAGAGGCGCCCCCUAUACCCUUGCCUAAUGCCGCAUCAGGCUACUAUAUUUUUAGCUUCGAGUUACUUGUGGCGUUAAGCGGAGAAAGUGCCCAAGCAUUACCUGUGUUUAAUGCAACAUCCGUCGAUCUGAUUACCACGCUUUACCCAAUCAGUGGUAGGGUAAUAGUACGUGUUUGGGCAGCGCGGUCUACUGGUAGGGCAUCGCGACAUGUUACGGAGACCUUAGAGCAGCAAAACCGGCCCACCCAGCACCGGCGCGCUCACCUCGUCUCCUGGGCGCUGUAUCCGUGCAAGGUUUUUGACCUCGUAAGUUUGGAGCGGGAAGUAGAUCUUGUCGUCCAAGAACCACAGGUGAUUUCACCUCGCUUGUGUGCCGGAAUGUCCUGCUGCACCGCUGGGAGACGGACGAUGACCAUUCCCGCUAUGUCACAUUGCGGCGCAGACCUGAGAACUAUCUUUCAGCUCGUGUUUCAUCAUCGGCCCCAACUCACUCGAGACCAGGCCGGAACCCUAUAUGUCUCAUCUCCGAGCACGCAUACUACUGUCGCGCAGCAAAUGACCAAGAUCCAUCGGGAUUCGACAUUCUCCGAUCUAGUUAACUAUAACAUCGGGCGUACAAUGCUGACUACAAAUACCUUGGGACCGGAGGACGCACUUAUCCGUUCGAUCCUUAAUGCAGGCGCGAAAAUUGGGCUCAGCGGGACACCCAAAUUAUCGACGAGGGAGCCCAGGACAAAUAGAGCUUCUACGCCCUUCUCCGAAGCGAUAUGUGCGACACGAGGGUACGGGAAUCCUAACAGGCAACCGUCACUGAGAAAAUGUCGCCGCCGAUGUAGCAGAAGAAAGACUUGGGCACAAAUCCUCUGCAAUAGAAAUGCCCGUUUUUCGCACAUUAUGGUCGCAAAGGCCGAGGGACAACUAUACGCCUCGAGUCCUCCCGAGUCGAAGUUGGAUGCAGAUACUAGCACGUAUUUGCCGCUGUACUAUUUACACACUAUAUCGUCUCCUACGGAUCUGACAAUAUGA')
#print ProteinTranslationProblem('AUGGCCCGAGGCAUCGACCCAGCACACGAACCUGGGUUUGUACCUUGCACAAUAAAGCAACGUUGCGGUUGUGAUCCCGGCCAGAAUGUCAUUGCGUAUCUGGUCAAUAACCACACAAUUCAACGAAGAUGGGUUAGGCCCUUGUGCGACCGAGCUAGAGCCUCAAGGCCCAAAACGGGUAGCAUUCGGCCUCCGGUACAUACUAUGCUCAGACUGUGUUUGAUAUUAUUAGCGCUCUGCACAGCAACCGAUGCGUGGGAUGGGCAAUUGCUAAGACUAGCCCCUCUACUACAAGCAGUUACUUCAACUCCAAAAAGCCAUAAAAGCGUUAUCUCUCUAACGGUGCGAGGUAUCUAUCUUUCUGUGCCGCCCUCCUCAAGAGACCGCUCCUCAAGGGUAGCGAUAAUGUACGCAGAGGUUCAUUCACAAGAACCAGCUCUCGUUCUGGCCCAUGAAUUAACCAGACACGGCUCGGCUUUGCUAUUAGGGAAUGGCAGCGAGAGGCUAGCGACGGAAGCCGCAAACCUACCUAUUACUUCCCCCGAGAUCCGCGCGGCGAAUAACUCAUUCAGUCUUUCCGAGGGUGCGGCGCGAUCUACCUACGUAGUGUUACAUACUAGGGUUCAUUCCUCCCCCAGGAAUUCCCGCAGAUCCCACGGCUAUAUGGCCACCGCUCAUGCACCCCACCACUCACAACCUGAGCGUUGGAGUUUUCCUUUUCGGGAGUCAACGUUCCUUAUUUUAGAAGAUGAGUCGCUGGCGGUCCUUUAUUCCAGUUUAUUUAACGGGAAACCUAUCAUGGGAACGGGCGUGGGCAACACCCGAGUAAACAUCCCCCACGGCGUCUUGUACACUGAUUUUAGAGCGAAGGAUAAUGAGCAAUACGUUUACCAAACGAUUCCCGAGCGACUCUGGCGUGUACUAGGAGAAUUGCUAACCGUGAACUCCACUACAGCCGUUUGGAGUUUAUUACAGUCUAACGCAGAACAAUCAGCGGUCAGGUGGCCUACAUCCCUGUUGGCGCGCAUAGCGUGCACAAACAAGCCCUAUGCGACACCGUGCAUAUCAUCCGAAGGCGGAACAAUAACAAGUUUAUUACUGGGUAAAGUGAGAAGUUAUCAACCCAAGAUAUCGUCUCCAAUCGCAAACCUAGGGCGGGAGUGCCAAACAGUGCGAACAAUCUUGAGGUGCGUCACCUUGUACCACAGAUGGGUGAAGCUACCAUCUACUACCCCCGGCAACGAACACGGCUUUCGACGCUCUCGGCGAAAUCUUUCUGGGCCUGGUAUUGCACUCCUUGUGCUGUUAAUCCAACAUGGUCUAGGCGUACGACCAGUAACGUGCGAAUGCUCUGAGACUGCACGAGUGCAGCUGCCACGUGCCAAAGCAUGGAAAAGAGAUCUUCUCGGAAGAAAGGGUAUACGGCGGAAUGGGCGUGUGCAUAAAAAAAACUCUGACAUGUCAAUGAGCCUUGUCCACAAGCAAUCCGAGGCCCGGCUUGGGGGGACCAGAGAGUCUAGAUUAUACGGGUUACACCCGGAGACUGAAUACACUCUGCUAACCCCACCCGCGACAUAUAGAGCCUCAGGGAUUUGUGAAGGUACGGUUGAGCGCCUUGAUCGAUCUCAUCGUGCAGUUCUGAGCAGACAGGAGUGCCCAUUCUUUGUUGAAAUCUCGUUGUUCGCCCAGGCUCGCAAUGGAGGGGACACCGGCCAAUGCCAAUGGGAGGGUGCCUCACCAGAAAUGGACCGUCGGCAUAGGCCGAUUUCUGGCUUCGGACUACUACAUCCCGAACUCGACUCGGUUCUGAGAGCAUGGACUGUGUUUUUUAGAUCCGGGGCAUCGAUAUACAGAUGGUGCUUCUACCUGACAUAUAAUUGCGUCUUAUUCACCGUCACCCGCCAGACCCUUCGUCCCCAGUGUCAAUCAGCAUGGGAUGCCGGGGCAAGGUUGAUUGAGCGUAGAUCCGCGCGAGUCCCAGUAAAUAUUGUAUUAAUUGUACUAAAGGACAAUAAGGAAUAUUUAGGCUUCAAAGACUCAUUUAAGCAAAUUGUGGUCUGUGCUAGCGAUGAGCAAGUAUGUGAUACGACCGUACCACGAGGGAAGAUGGCUUACCUGAGCCCACUGCCCAACUUGCGAGUCGGAGGCUCCGAUCGUUGUGGAGCGUGCUUGCCUCAUGUACUGGAGGAUAGCAGCCUACAGUCACGAGCGAUGGGUCGGAACCAUCGUGACUGUACUUUUGACUAUCCUAGUCUCGUCUUGUUAAACCUUACACCAUUGAACAUUUCCAUCAACGACCCUAUGUGGGCCGACCGCGUGCCCUGCAAGCCUAUAUGUGCAAGCAGCACUAAUCUAGUAAUGGCAAUGUUGUUCCCUUUUUUUCCGUGUGUGAAAGUCGCAGUUUUUUGUUUACCCCUGCGCACCCGUCAACACUCAAUCUUACUUGGCACUUGUCAGCCCAAUAUGUUCACGUAUGACAACAGAUUUCUCCCGGCCUGUACUGUGCUGGAAAUUCGACAGUACAUGGAACCGCCGUCGUUACACCCAUAUACCUGUCUGUCGGGUAAAUCAAUGCCUCUUACGCAACAAUUCGAUCCCUGCGCGUCAAGCCUAAAUUGGCGUCGUAACCAUCCAGCCCGUCGAGUGCAGUGCCUGCGGUAUUCGACCUCUAUGCAGAGGCAAGUUACGUUCCCGCUCUGCACCCUUAGUAAUAAUUGCUCCGGGUCCGCUAGCAGGUCCCGUUGCGAAAUGUACUACCUUGUUACGCUGCUCCCUAUUACUACCCGACUUAUAGGGGGAACUCGGACUCAAAAUGCCGUUGUUUUUGAGUAUGCAGCGUCCUCAUGCGACACUGAACGCCUCAACAUUAAAGAAGUUCGCAGGGGACGUGUCAUCCUGCUAAUCCCAAGCUCCUCGGACCAACAGUUUGGAUACCUAUGGUCUCGAAUUCAGUUUUUUUUACGGAGCCAGAAGAAUAAAUGCGAAGAACAUCUGGCACUGGUCUCGGGCAGAGUAAGAGCUCUACCGUCCCUGGUAUCAAGGAGUUGCUUCAGACCCUUUGGUCCUGUUGAUAAGUUAAUAUCCCAGACGGGGCCCGCUAUUGCGUUUGGAACCAUAAUCUCCUCGGUCUACGGUAUGCCAGACAGUGUGCAAAGCAAAGUACAAUACGCUUCCCGGGGGUUGCCCAUAUGUCGCGGCAAUUUCCCGCUUCCCCUGUUGGUUAACAGGAGCAUUCUCCAGGCUAAAGGUGUAUUAAAAUCAACCUUUUGCCAAUUAACUGUAAGUUGCCUCUGUAGUGUAUGCUUGAGGUCUCUACUUCCGCCAACGAAGGUCUACACACCACACUCCCCGGGAUGCAAACUCCCCUAUGAACUACUGGCUGUCCGGAGUGUCUUCAUUUCGUCCGCAGGUUGGUCAGGCGUUCCGUUCCAACUGUUAGCCAUCCGGAGAAUAGUAUUUACGAUCAAGCCAUCUGCUAAAAUACCUGCGGAUUAUCACAAGAACGGGGCUAACGACAAGAUUACGAAGGGAAAGCUGGUACCUAUAAGUUCAAAGCCAGAUGCAGAGAAUCCUUCUUGUGUGCAACCUGGGGCGUGUAUAAUACGAGAUUGGAGAAUAUCGGAGAAAACUGCCGACCCUGGCGCGACACCAACCCCCUCCAUAAGGACUCCUGGAUGCUGCCUCAUCCGAAGGAUCCCAGGAGUUCACGCCCUACCGGCCUACGUAGGUAAUGAAGCAGAUCCCCUCACAGUUCGCCACUCUCCUUUCUUAAUUAUUCCACCUACGGGUGAGCGCGAGAAGUGUAUAACACCGAACGUCCCUGGCGCGACGCGAUGUAAGUGUCGUCCAAGUUUAGAACCAAACACUCCAGGUUCUGCAGACAGAAAGGGUUGUCCAUCUACCCAAGCUUAUCGAGUCGCUAUGCGCUCGACCAUGCCAUACUCGGACAGAAUAAAAAGAUCUGUCACUCCAUAUAUUAUUCCCCCACGCUUACACAUAAGGUGGCCGCUAAAUGAAUCUUCUAAGGAGGAUAAGACGAAUUUCAAAAGGACGCGAGGUCUAACGCAACAAUUAAAACAAGCCACGGGCAGUAGGAGUGGCACUUUUCAGUCGCAAAUAGACCACACAGCUUCUAGCAUUAGCGGAGAGGAAAAUGGGAUGGUCGGGGUUCCGGGAGAUAGGGAGGUCCCCUUGGUCUAUAACACAACUCUGAAUAAUCGCCGGUUCAGCAAACACUGCACUCAGACUAAGUAUGGUGGUUUGAUUAAACCCGUGGAGUCUAACCUAGCACAAUUUCAUAGAUUAGGCCUAAUACUCGUCAGACAUUGCUACGGGGGCAACCUCGUCGUAGACCAGCAAGGCGAAGGUUGGAGGCCACCCGGUGUGCAAUCUCGGCAGAUCGCGGCAUCAAAUUAUCACAGAUCCAUAUUGCACGUUGAAUCGGUUGAGGUAGGCCGUUUACCUCGUGCUACAUAUUUCGCAGAGUCUAUAACACGCCGUUCCCGUCACCCUACUCCAAGUCACCCCCUUCCUCCGCACCGCCCGACCCGAGACCGAGUACUCGACUGCACGGGUACUGUUCAAGCUAAUGACAAUGGAGCUCCUGACGUUCGACGUCACGCCCCGAAUGCUGGCGUAACGGUAGGGACGAGUGACUGUGUAUCUAUUGCGUUCCCAAGCGUUCCAAGACAAUAUGCCGCGGUAUGUAUACGAUUAAUAAUGAAGUUGGCGUCACUCCGCUGGGAUCGGAACGGUGGCGAGAUCUGCACUCGCUUUUCAAAGUGGUGUUCAUCUAUCCGUGUGACUCUUUACUCGAUACCAUGUGGGGUGCGCCAAUGGGCUUAUGUUGCGUCCGUCGAACAUCUGAUACCGGUAUGCAGAUCGGAUUUGCAUUUAGUCUCCUAUAAGCUAUUGUGUCUGCACGCACGGGGUUGGGGUGAUGCUCCGAUGGUACAUCGGGGGCUGAAACUUGCGGUGCCGAUGUCAUUAGGCGGAGCAAGUGACAAGGACUUAUCAACAUGGGGGACUUUGGCGGUGCUGGCCCUAGAACAAAUGACCCUCGGUAAUACCACCCAACUAGUCGCGAAUCUUGCAGUGAACUCCCCCUUCGUGAAUAUAUGGCAUCAGUAUCGAGGAGGCUUGCCAGCAUGCAAAACUGCGCCCCGCUAUUACUCAGCCGCUAGAACCUCACGCCCUACCCAGAGACGCAGAUGGUCGUCGCUAAUCCGUGUUCCCUGGAAGGCUACCGCGCUCCCUGCAUGGGUAUCCUUGAACGAGUUUAUUCAACGAAAGAACUUCCGCUCAGGUAUUUGCGGAAACGUCAUUGGUAGAUGUUGCCUAAGAACGGCAUGUUCGCAAUGUGAGAUGAGUGUAGAGUCUGCGGCAAGGUUUGCCACAUCGGUCUUACAGAAGAAACCUGUUUUUAUUGUCACGGCUUUUUUCCGGACGUUUCGCUUCUGUGCCGAAUUAAGAUGGCGCGGGAUGUAUUUGCACUCUUCGAGACCAAAGACAGUGCCAUACUGGUGGCGGGUGUAUUGCCUACCAUGGGACGGGAUCGAGAAAAGACGACGUCGAAUUACGGUAAGUUUGAGGAGCAGGUUUUAUAAUCUAGCUCCAAGGGGGAUCUCGCCUGUGUGUCACGAAUUCUCGACUCCCGUGAAGAGUACAGUGCGCCGCCACGCAGGGGGUCCUCUCGACAAGUAUCUCAGUCUACACUCAGGGGUUAACCUUGACCCGAAGGGCAUGGGAAUCAGCAAGGGAAUCGGUACACGGUCAUCGGCCCACUCCGAAAAUUACUUCGCAGAUAUUUCGAAAGAGUUAGGCACGAACAGAAGAGUUCUGGGUAGAUCACACCGCUGCGUUGGAGCCCGGUUUUUGCAGCAGCUAUGUCUCCUAAGCGCACCUCGAUUGAAUCUAUCCAUAAAUCCCUUUCGCAGCUUGACUGACUCAAAGACGGACCGGACGCUCAGGGGGCAGAGUAGAAGACUCCCCAGCCUGAGAGUUUCGGGAGUUGAUCAGUCCAAAACCGAUCGCCAGAUACUGGGGCUUCGGUAUGAAGCUGAAAGUUACAGGGGUGCGUACAAUGGCAGGAAACACAAACCACUCGUUAUGCGUCGGUACCGAUUAAAACGUACAGCGCUAGUCUGGCUCCAUUCCAUUGUAAACAUUGUACCACCUUCGUACAGAAGUAACCGUACAGGGCUACCUGCCCACGAACUGCGACAAGAUGCGCUCAGCAGGCGCCACUUGCACUGCACAGAUUCUCUAUCCCUCGCCGGACAACAGUAUUUUGGCAUUUACGAGCCGUGGGUGUAUUCUGAAGGGGGCUUGUCGAAACCUGCAUCCUGGCCGUCGUACUACAUUAGCGGAACUCGUACACUGGAAACGCGCUCGCUCUGCGUCCAAGGGGAGCUACCCAGGGGCCGACCCCCAGUCGUAAAUGGUGAUCAGGCCACGUUGUCGACCCUCGUCCCUCAUAUGUCCGAAGGUUGGGCUUUGAAGGUAGUGUCCUCUACUUCCCUGCAGGUACAUGCAAUGACCAGUUUCGACUUCGAAAUACCUGAUGAAGAAGCUGCAGUACUGAUAGCAAGGCCUGUGGUAACCGCACUGGCUGAUACCUUCGAAAAAAAGGGGGCCGUGGUAAAAUUCAGUGUCAGGGAUAAACGCACAGUUUGUUUCAUCGGUCAAUCAACUUACAAGCUGGCUUGCACUUCAGAACUUUUUCCGAGUACCGGGAUUGACACGUAUAUACUAACAUGGGUUUUGAAUAUAACAACCCACUGCUGUCGACACUGCAGCCUUCGUAUGAUGUAUCGCCUGGCUCUGUCCCUAUCAAACCCAGCGUUAGGUAAAACCACAAGCCGCCAUGUCAAAGGUCUUAGGUCAGCUACACACGUAACUCCGGGAGAUGGUAGUGAGGAUUAUCAAUCGUCAUACGCUCCAGCUACUACAUUCAUGACAGUAAACGAAAGUCCCGGUCUGACGAGAAGACUUGUACAUAAGAAGAGGGUGAAAGCUGCAUUAAUACGAUCAUGUAAAAGUAUGAAGGGAGUACGUCCCAAUGGUACAAACCCAUGCUGCUGCACAAAGAGUUCCGAGUCGUCCUUGGGGCCGCGAGUGACGCACUACGGCCCGCACUUAACCGUUAGGCACAAUGGGGUAAGUAGCCCAUAUAGGCAUCCCCGCAGUGCACUGCCGCUUAGAACCACGUUAGUUGUCAGAACGCCCUGGGAAUGGAUCUUAGCCCCGAGACUAUCCGGCGACGGCUUCCUCCUCUCAGCAGUUGACUGGUUCAAAGUCACGUCCGGACAAUACCGCGUCAGUACUCGACAACACGACGCGAGAUUCAACCCACCACGUAAUACGUACGGUUGUCCGGCAAAAAAGCCUCGGGUUCGGACUCGUCUGGAAAGAUCCGGUCUCUACAGGGACAUUCAUCCCAACAGCAAGACCAUUUCGACCAAAAGCCGUUUGUUAUCCGGCGGACGUGUCCAGGAUCUCAAUCCAACGGCGACGGCGCUCGCAGCGGAUAGUCAUAACAGCUCAGAGUGUGUGCUCUUUAACUUUGACCCCAAAGAUGGCUUCUUUUCGAUCGGCGAUGCGAUAGGCUGGACUUUCCUGCUCUCAAACGCGCCAGCACAAAUUCGAGCCACUCUCUACACCCUGCCUGACCGCUUUCGAAACAGGGUGUGGCGUGCGGGUCUGGCUCCACAACGUUGCUGCCUACAUGACUACCGGAAACGGGUAACAAGUCGGGUCAGACCCAGUUCGGCCCGCAGUAUCAGUUUUGUGAUAUCCACUACAGGGACGUACGCCGCAGGAAAAACCCCGUGGAUUAGUCCAAUACCCCUGCAAUGGCUCUACCAAGCGACGGGUGGGUCCUCGGCAUGCAGGAUUUUAUUCUCAACGCUUAAUAUUAUAUGCAUUGCCAAGGAUGAUCCCCCUCAAGGCUUUAUAGGUUUCAGUAUAGACUGUGAAGUCCAAUACAAAACCUCAUCCUGGAAGACGAUGAUUGCUAACGUUCGGAUUGUGUCCGUUGUUGGCCGUAAACCGGAUCAGAAAAACCAUCGCGGAAUUCUGCGAGCCGGGAUCACACUCCUUCGCGCAUGUUUGCGCUAUCGGAUGGUCAGGGCCGACUUGUGGGAGAUGACAGUUGGUAUUGGUGACAAUACGAACAAGCUGACUUGGGUUUUGAAACAAAACGGACAUGAUCGGUGGCGCCGGGAGUGUGCAGGCGGAGCGACACUAGCCGUCAUCGCGUACAGGCCUAUUAAGAAAAAGAGGUGGCAAGAUGCGUGA')

def GenerateConvolutionSpectrum(spectrum):
	n, freq = len(spectrum), {}
	for i in range(n):
		for j in range(i+1, n):
			diff = abs(spectrum[i] - spectrum[j])
			freq[diff] = freq.get(diff, 0) + 1
	freq = sorted([(v, k) for (k,v) in freq.items()], reverse=True)
	out = ''
	for (v, k) in freq: 
		out += ' '.join(map(str, [k]*v)) + ' '
	print out

'''	
#lines = read_file('inpros89.txt')
lines = read_file('rosalind_newba4h.txt')
GenerateConvolutionSpectrum(map(int, lines[1].split()))	
'''
		
def ReverseComplementProblem1(Text):
	complement = {'A':'U', 'U':'A', 'C':'G', 'G':'C'}
	return ''.join([complement[x] for x in Text])[::-1] 

def PeptideEncodingProblem(D, Peptide):
	RNAstr = ''.join([x if x != 'T' else 'U' for x in DNAstr])
	#print RNAstr
	k = 3 * len(Peptide)
	for i in range(len(RNAstr) - k + 1):
		kmer = RNAstr[i:i+k]
		if ProteinTranslationProblem(kmer) == Peptide or ProteinTranslationProblem(ReverseComplementProblem1(kmer)) == Peptide:
			print ''.join([x if x != 'U' else 'T' for x in kmer])

'''			
DNAstr = 'GTGCCCAAGGCTGAGTCACACCATTTGTAGGACCCGCCTACCATAGAAGAGCAGAGGATCCTACTAGAGCTTTGCCTTCTCCTCTCCCGGTTGCCACATGCGGGGCAGACCCAACCGTCCAGACCGGTCTCAGTGCGTATACAACGTCTGGCCTAGAATAGCACATCAAGTCTCGTTGTGCGATGCAATACCTTATTGGCAAAAAGCAGGGGAGCCAATATTAGCCGTCAGCTGCCGGCTGATGTGACTTTCCCCGGAACTCCCCGCTGGGTATACAACTGTAAATGTGTGAAGGCTGGAGGGCGCTTTAGGTCGCTGAGCCTCTAGGAGCCCAATTAAGTTCAGTCCACTTCTAGATTAGGTTTAGTTGGTGACAAGCTGCTATAAATATAACGTACACATCTGGCCGCGGAGCCCTCCGTCGTCGTGTACTAGTAGGAATGTGTACAGTTACTCGGATGAGAATACTGTTATCTATTCTTTCAAGCTGCGTACGCCCAATGTGGCAGGTCACCCTTAGTACACTTCCCTCAAATTACGTCCTCCCCGTTAGGCGTCGTTGGATCGAGGAAGCAACCCTTGCGATACCGCCAGGAGCCTCTAAGGTCAGCTTCATGCCGTAGATGTTGAGATGATCCTAGATGAATCCGAAAAGGATTCCGGTAGCGGCCGGAGTATAGTGCTCACGCCGCCGCCGCAGGAAGCGGGTGGAGTCAGGTGGGGTAGATCGACGCGGTCTGCTGATTCTAGGGCTCAAGTGATAACTAAGGCTCAGGGCCGTCGAACCTGGCAGGGATACTGTACCTGGCAGTACCTTGTGCACATATCTTCCCCCCACTTACTTCTGGAAATCCTGTCGCCGTGATGGCACCTGTAATTCTCCAAGTTACTGCGTTAGACCGAGCAATCTTCGAGAGATCGTGGGACGGATGCACATCGTATCGGAAGTCGGTCACAACCTGCTACGATTTCTTATCCCAGTAGGGCTGCGCTGACGTTCACCACACCGGTTGTTACTTAGTATGTAAAAAAATCTTACGGCAGACGGAACGGTGAACGCCATAGGCCTATTAATACGTAGTCTTTTGTTGCGTGCTAGTAACTGCGCTATGGAGAGCTATCGGCTTAGTTGGCGAAGTGCCGTGTGTCCACCTGGCTGGCCATAGTCCCCTTCTGGAAGAACCCATTTGTCCGCCTGCTACTTCACCATGTACCCGTGCCGTGCAGGATATCCTAAGATTGCATGTTGTCCGATTGTCTGGGACTTTACGAGTTTGAGTCTGTATTCTTGATCAACGTCTAGTTGCATCGCTTTCAGTTGTCAATTTGCCCCTGAGAAGCTGACGACCACGAAGGTCCGAAATTGGTTTAGGCGTGACGCCTGTTCGCGGGGATTGTTGCAATCTAAAAGCACTTCGCGGGCTGCTAATCTCTGTTCCCATGTTTGACGTTATATCCGTCCGAAACTTCCAGAACGGTACTATAGCTAGCCAAGACGTCCGGATGAGTCGATTACGCTACCAGAGCTACTAAGGCACATATATTATTGATTTGGCCGTATCTACAACAACACGAATTTGAGGCTGTCTGGGGTCTTATCAGCGCAATGCCAGCATCCTAATGATAACCTCCTCGTGGTTGCATTTTCGATTTACGCGGAATTCGCGATTTCCAGAAGGGGACGATTGCGAGCCACCCCGTTATCTAACTACACAGCGTTTGGTTCTCTTTCTTTTCCTACGGCATAGCGAGGACCCTGATTTCGTAAGTTCTGTGGCTTGCGATTGTTCCCTTCTGGAAATGTTTACGGAAATCCTACGAGGCTCTGACGAGTGCGGAGCGCCAACTCCTCACGTCAGGCCTGTTTCCAAAACGGCACGATAGCTAACCAGTCGACTATCGACTCTAGCGCTCTCTACTTGAGCCAATCCACGGGGGCGCGGGGCGTTTCGGCACCTCCGAAAACCCACGTAACAGGTATTGCCTCAGATGACATTCGTCAGTTCCGTATCGACGGGCTACTCGACGTTTTCTGCTCAGTTATTTCGTCGAGGGCGTTTCGACACTGTCAACTTGCTTCGCGGATGCTGGGTCTACCGGTAGTAGAGCCGAAGGGTTTCGCAATCAGCGCTATTTGGCCCCTCGGGTCTGGTTGGCAATAGTGCCGTTTTGGAAGGGACCTTACTAGGGACGGGACAAATACCGTAGTAGCTCGCCCATCACTTAGCAAATACTACACTAATTAACCCGTAAGCAGTTCATTGCTCTGGAAAATCCGTAAACGTGCGCAGATATTAAGTTCGGAAGTACAGCACTAAATGTCACGGTCAGAATGAGACGCCGGAACACAGAACCGTGAACAGATTTAAAGTACCTCTCGCGCTTTATTCCGGAGAGTACTTCTCACGACAGCGCTTACTTCAGACATATAAGTCGTTCTGTTTGAAGGCTCCACGTGCACGGCATTCGAACCTTGGAGTTTAGTTAATCAAGTGGGTTCAACAGATAGGGATTTAAGGAAGCGGGTCCCCATGTAATCAAGGATGTGGCTATCCTATTACTGAAATATAGCATGACTCTCTAAATTTATTTCCAAAACGGTACTATAGCAAGCCAACAAGCCTTTGGATTCTTAGCCTTCAGGTTCCATCCGAGCGTCCTCACCAGTCGGTATAGTAAATGCTATCCTGTAACCAATTTGCTTCTTTCGATACATTCCCACGAACACCGGCTTCCAGGAAGCATGGTGCAACATAAATGATAATGGTGACAATAGCACGACGACCCCAAACGTAACTTCACTCTAAGGAGCCTAGCGGGACATGTAAGACAGTACCTCGAGTTATACAGTTCTGTTTGTATCCACTCTAACACCGGTGGTCACACCTTCCCCATCACCGAACAGCCTGGCGCGTCGCAAAGGGAGCGGTTGCTTCCTTAACATAGTTCGAAGCTAGTCGCGTGAAAATCGACGACCTACCGTGCCTATGGCTTTTCGGCGAGTTCTTATGCGCTACGTCTGCAACTTGTCTAGGGGCGCTCAATGAGTCGAATTCTTAACGCTAGCTGGGTTCGCCTCATACCAATTAACATTGATCTCCCGGAGTAGAAGTACACAGTAAGTCGAAATCGGGTTGGCATGTGGAGCTTGGCGAGGAGGTACATATTAACGTTTACCCACATAGGTTTCGTGATGTTGTCAGCACAGCTGCCCCAAGCGTGACTCTATGAGTTTGAGTCATCATGGACTTAGTTTTCCGTTCCCGACCACAATCGCACGTTAAAGGTAGAATGCTGAGATCCCCGGCTTCGCAGGAGCCCTCGCGCCCTGATGGATGAGACAAATTGGTCATGTCCATCTTCTACTTGATCACTGGAATTAATAGAGGTGGTACCTCACCAACAGGTTTATTAAGCGCTAACATGCATCCTTCTAACAGTTTTAACGTATCCCTACCATTTCGGGTGCGTCCAGGTTTTCTCCGAGTGCAGGTTGAGGATCAGTCCGCTTAACTTCAGGGTCCCCAGCAGCAGTGGGGGGCCTCGCAAGTAAACTGATGAGAGCGTCAAAATGCGGTGCCTCGTATTGCACCCAATGACCAGATAACGCCCCTTCAGAGCTATTCGACAGCTTATGGGACCCATTTAGGGGCGTGCAAGCCCGAGATAGTTCTTAGGCGGGGGTCTGGCTCGTCACTATTCAGGAACGAACGCTGCTCTGTACTTACGCGAGCATATTCAACCCTCTAGTTCAATGTCCCTTCGCTTTCGAGGAGGACGCATAGTGACAACCTCAAACCCAAATCGCGTTCCCATTAGACAGGTTTGAGGTCCTGATGCAGCATATCGATAATTGACTTAGCTGCAGCTTCTAGTTTCTGTGTAATTGGATAGACTCTGTTGAGCGTAACAAAACGGGCCCCGACGCTGCGAAGTCCCTTATCGCCATCAGGCCAATCTTACGTTTTGAATCTAGCTCAGATTCCAGTACACGTGGCTGGCTATCGTCCCATTCTGGAAAATACGCTGCGAAAGCGTTCTCCGGGGATCCCCGTAACCCCACAAAGGCGCCATTTACAACCTTACAATTATGACAATCACCGATTTGCCGTGACGGCCATAGCATGCGAGCTAGGCAACCAAGCGACACTAAAATATGTCGGTGGAGTGTCGGAGTGCATATACATAACAAAGATAGTCAGATACTCTATTGTTCTATACGAACTCCTCTGTTACGTGCAAGACAGAACCTCTCCCTAATGGAGTTGCGGGAAATTATGTATGTCGGCCGAAAATGATCACTAGAGAAGGAAATTTAAATTCACGCCGAGTTATCGTCGACAGCGTGATGGAACAATGACCAATGATTGCTGGTTAGCTATTGTTCCTTTTTGGAAAGTATCCCTAGCGTGGATTTGTGGCGTTAAGAATTGGAGGATCACGTTAGGAGACTTAGAACTCCAATAACTGCCCTTTCCGTACAACACACTAGGATGCCATTGCGTTGGCAATGTTCGCCCCTGCCACGCCTTGATATTGTCTTGTTACGGACGGGGACCATCAACCTAATAGACGAGTAATATCGTGCTAAAGACTCTCCGTCATCTACACCGAAGTCTTATCGCCTATGCCCTGTACACGTTGCATGTGGATTCTGCGGAGGGACATGACGGTACTCCAGTTAAGGAATAGGTTCATGAGGTACCCTTTACGGGAATGAGAAGAAACCTCCTGGGCGCTGTTATCCGATGCAGTGTTCTTCTACGGAATTTGGTAAGCATGTGCTAGACAGCGGATCAAGTGATAGACTTTGGCTGGCTAGCCATCGTGCCGTTCTGGAAATTTACAAGGCTGGCTAGTACGTACTGTTAGTACGGGTGGCTAGCGATAGTACCCTTCTGGAAAAATGGGTTAGCTTGCAAAAGCCTCAGCTTTTCCCGGGTCTCCGTGCTGGCTTGCAATAGTACCGTTTTGGAAGTTCCCTGCACCTGTGATGGTCGCTCTGCCCGGACAATAGATGACCCGGAGCGACCATATCTGCATTTCCAGAAGGGTACAATTGCAAGCCATTTACTGAGACACAAGTGAACTTCAACGACCCACACACCTGTCATCTTGGGACTGCATTAGAATTTCCAAAATGGGACAATCGCAAGCCACAACAATCGCTCCCGTGTTTCTGACTGATAGTCGGACCCGAGGTGATGAGACAGAGGTATACGGATTCATGACCGGTCTAACTCCTATTCAATTCTGCCAGTTATCCCTCCGGAGGTGAACTACCTATCGATGTCGGCCCCTGTTGGCAAAGTTTATCAAATAGCGAGATCCTGTGCGCACAAAGACCTCGAAAGAAGAGTCACACCCTTAGAGAAAAGAACTGTATGAGAGAATCTGGTTGGCGATTGTACCCTTCTGGAAAATTTCCCATCTGGTGCTATCCCCTGATGATCCTCAGCCATGATAGAAGCGTAACCGACGTTTGTAGGTGCACCGAAGTAGAAACGGGCCTTTGAATATACTCGATATACCCGCGGTAGCACCAACCACTCCCCTTTCTCCCGGAGCTTGCCGGACAGACGGGTCAGCCTGAAGCTGGATACTCTGTTTAATAGGCGACGATAAACCAATGGCGCAGCGACACCGCGGGATGTAAGTTTGCGTTTAGGAGAATCAGATGTTATATATGTTATCCAGAGGAATGTCTATCACGTGTTTGGGTAATTGTGGCTGTCCAACCCAAGCTGCTGTTTGGCTTCAGAACGAATGCCCCTCCGGCGCTCCATAATGAAAATAACGTAAAGCGTGGAGTGACATCGGCCTACCCACCACCTTATTGTCAATAAGCGCTTGGTGCTAGTTTTCGGGTACTGATCCGGCGATCTTGCGCAGTTAACCGTTCTTATCACCAAACCGCCATCTGAGCCCGGGAACGTGGATTTCCGATTGAATGCCGTCACTATATTGGAATAAAGGGTAGGCGCAACAAACAGAGATGGCAGCTCATTAGTCAACTGCAGCGCTTACAATGAGGCTGGACTAGGCGCGCCCAGCTCTGGTTGAAGGCGCAACTGAGACCCAGCCTTTGGCAACGTTCGGCCACTATGCCGCCGGGCTGACATAACCTCTGAAATGACGCAACTTCTTCCGGAGGATTAGGTCAGGTTTGTGCGTCATAAGCCCTATTCCCCTTCACATCCCTCAGAACGCATAATTTGTGTCTAGGTTGTGACTTCAACAGCCCAAATAACATTTATGGTACTGTAAGGTGGTGGGACTATATGGAAGGCCCTAGCCAAAGAAACGCTGAAGTTTAACGCTCTCTCACTCAGAAGCTACGCTACGGACTGCATCGGGAGCGACGTATGACACCTGGAAGCTAGGGTCGACGGCACTATCTCTCCACCCCAACACAAATCGGGGGAAATATCCCGCGGTTATTAGCGTGTGTGGTTACCCTACGGCAGACTCGTTTATAAGAAGCGCACGCGAAGAGCAGTGAGTTATGTAAGTTTTAGTGCAATGTCGTTCTCCGTACCAAATTAGGTAATCCTATCGGACGTATTGCAACGCCCAAACAAGGGAGCGGCCTTGTTTTCGATGGTTAGCAATAGTCCCCTTTTGGAAAATGGTGAACCTGACACTTAGTAAGAACGCATTCTACTTCCAAAAAGGCACAATCGCCAACCACTTGTATGGGGATCCGACCATTTTTCAAAGGGCCCTGCACTAGCCAAGGGTTTACGGCCCTAGTGCATTCATGCTTTCACACCATCAAAAAATAAGAGAAGCCTAGAGGACCAGTCAGAAACGGGATGACTACTACGTCCACAGTTAAAGAAGTCCCATGGCATTCTCTCGTCCTTGATACTGTAAACACGTGTACGTTTCCAAAACGGTACGATGGCCAGCCACTTCAGTCGGTACTAACGTCTCAGCCCTTAGTTCCCATTTGTGGACTCTACGCATTTGAGCTAGGACTCAAAAGCAGTGTGATAGGAGCTCTCCACGTATTTGGCCGTACACTGCGGGGTCCCTGTTTACTGTACCTTATACGTGAAGGGAATCCCCCTAGAGAGCATAACCCAATGGGCTGTCTGGTGAGGGTTCTTATGCTGGGGGGTGCTCGAACACCATACTCTACTGTTAGTGCCCGTGATCCTGTGGTCAAATTTCAGTTGACTGAGAAGTCGTCTGACTCACGCTGTGGTCTTCAAACACTGGAGATTTTTTCTTGCGAGAGTAAGCACTCAGACCCTTAGAAGACTGGCTGGCTATTGTACCTTTCTGGAAAAAAGGACAAGATGACCAGTTAACTATAATGTACTCATGGAGCCTAACCTCCGCACTCCCCTGGTCAGGGCCTAGAATGAGAGAAGTTCGACATTCGTTTAGAGGACGAGACTACTGGGCGACACCAATTTGCTGACGGACAACCGCCGGCTAATAATGACCCACGCTTTTATTACCGAGACATTGAAGTCTTGTGTCTCCTTCAGAGCGATTGGGCGAACGGCCGCGACACACCAGACGAATGCCTTGAGGCGGAGGATAAAGGAGGGTTAATCGAGTTATAAAGATCACCTGCCTAGGTGCCCATATCTATACCCGACGCTGGGGTTCATGACAGTTTCGGAAATACAATGGAACCAATGTAAGTGAAATCTGTTAGATCCCTACACCGCTTTGGACAGGGTTTGTGTAATTGAGCCTATATCTGTATAATCTATCAGTTCACCAGGCATTATGTCCTCACGCTATTATCACCATGCACCGTGACCTGAAAGTTAAAACAGGGGATCTGAGATTGCCCATTCTGTTCCTGTGTCGTGGACTTGCAATATACTGTTCAGGAATCCCGGCTACATCACTCGTTACGTCGTAGCTGACCACTCTAGCCTGTGAATACCTAGATAGGCGGATAAGGTCCTTGCGTACTCCATAGAGTTGAGAGGCTCAAGATATCATATAAGCCATTTGTGCTGGCTTCAGCGTCCGCTCTCGAGCCCGACGATCCCCAGGTGCAAGACGACGGAAGGTCGCGGGCAAGCACATGCTCCTCATATTCTGTAAAAGGGGTCGGAACGAGTGATGCATGCTCCCAGTTCGACAAACGGAGGAGAATCTTGCGGTTGTTTGAGACTGCGAAATAGATCCTCAACTTTTCCAAAACGGTACAATAGCGAGCCAAGAATGTGAGACATTAGTTACCTAGCCTATACCATGCGACTGACGTAGCCGAGTTTAGAGGTAGAGTGGTCTACCGTAGCGACGAATCATGACTGGGGGAACATGAAATTAATTGCGCAAACGGCTCAATCAGAGTGGGACAAGCAGTACGCCTCGCGACACCCGTTGTACGCCAAGATACACCAAGCGGCTCGCGTAGGATACTGGTATTGCAGCGATCCATAAGGATATCATTACTTGGAGGGAACTTAAAAATTACTGATTGAAGCGGCATCAAGCCAATAGTTCCGTCTATTACGCAAACTATGCTGGGTCGAGTGTCTGTAACGCAACCCGCGTACCACACATACATTTGAGAACTACCAAAAGGTCGAGTTGTCGTACCGTCGGTCGCAGTTAGGTTGAGACGCGCATAAATAGTTACAGTTCAACTCTCAGGT'
Peptide = 'WLAIVPFWK'
PeptideEncodingProblem(DNAstr, Peptide)
'''

def ConstructGraphSpectrum(spec):
	lines = read_file('mass.txt')
	map = {}
	for line in lines:
		pep, mass = str.split(line)
		mass = int(mass)
		if not mass in map:
			map[mass] = pep
	map[113] = 'L'
	map[4] = 'X'
	map[5] = 'Z'
	spec = [0] + spec
	n = len(spec)
	for i in range(n):
		for j in range(i+1, n):
			m = spec[j] - spec[i]
			if m in map:
				print str(spec[i]) + '->' + str(spec[j]) + ':' + str(map[m])

'''				
lines = read_file('inpros101.txt')
lines = read_file('rosalind_ba11a.txt')
spec = map(int, str.split(lines[0]))	
#print spec
ConstructGraphSpectrum(spec)
'''

def ReconstructStringFromGenomePath(kmers):
	text, n = kmers[0], len(kmers[0])
	for i in range(1, len(kmers)):
		text += kmers[i][n-1]
	print text

'''
lines = read_file('inpros102.txt')
lines = read_file('rosalind_ba3b.txt')
ReconstructStringFromGenomePath(lines)
'''	
				
def getAllSubsets(x):
	return map(set, powerset(set(x)))

def getAllSubStrings(x):
	#return [''.join(x[i:j]) for i in range(len(x)) for j in range(i+1, len(x)+1)]
	strings = ['']
	y = x + x
	for k in range(1, len(x)):
		for i in range(len(x)):
			strings += [y[i:i+k]]
	strings += [x]
	return strings
	
def GeneratingTheoreticalSpectrumProblem(peptide):
	lines = read_file('mass.txt')
	map = {}
	for line in lines:
		pep, mass = str.split(line)
		map[pep] = int(mass)
	strings = getAllSubStrings(peptide)
	#print strings
	masses = []
	for string in strings:
		masses += [sum([map[x] for x in string])]
	#masses += [sum([map[x] for x in peptide])]
	return sorted(masses)

#print GeneratingTheoreticalSpectrumProblem('NQEL')	
#print ' '.join(map(str, GeneratingTheoreticalSpectrumProblem('FECCFYDHGQKR')))
'''
peptide = 'VLWWHFIQYETN' #'LEQN'	
GeneratingTheoreticalSpectrumProblem(peptide)	
'''

def LinearSpectrum(Peptide):
	n = len(Peptide)
	lines = read_file('mass.txt')
	map = {}
	for line in lines:
		pep, mass = str.split(line)
		map[pep] = int(mass)
	PrefixMass = [0]
	for i in range(1, n + 1):
		PrefixMass += [PrefixMass[i - 1] + map[Peptide[i - 1]]]
	LinearSpectrum = [0]
	for i in range(n + 1):
		for j in range(i + 1, n + 1):
			LinearSpectrum += [PrefixMass[j] - PrefixMass[i]]
	return sorted(LinearSpectrum)

#print LinearSpectrum('NQEL')
#print ' '.join(map(str, LinearSpectrum('MSCRGEIWSPCIEFNELEFTKKGRCSRHTSAWIPQEYEEPTAV')))

import collections	
def LinearpeptideScoringProblem(peptide, exp_spec):
	theo_spec = LinearSpectrum(peptide)
	theo_spec_counter=collections.Counter(theo_spec)
	exp_spec_counter=collections.Counter(exp_spec)
	score = 0
	for m in exp_spec_counter:
		score += min(exp_spec_counter[m], theo_spec_counter.get(m, 0))
	print score	

'''
lines = read_file('inpros90.txt')	
lines = read_file('rosalind_ba4k.txt')	
peptide, exp_spec = lines[0], lines[1]
LinearpeptideScoringProblem(peptide, map(int, exp_spec.split()))
'''
	
def CyclopeptideScoringProblem(peptide, exp_spec):
	theo_spec = set(GeneratingTheoreticalSpectrumProblem(peptide))
	print len(theo_spec.intersection(exp_spec))

	
def CountingPeptideswithGivenMassProblem(mass):
	lines = read_file('mass.txt')
	minpep, maxpep = float('inf'), -float('inf')
	map = {}
	for line in lines:
		pep, m = str.split(line)
		m = int(m)
		map[pep] = m
		if m > maxpep:
			maxpep = m
		if m < minpep:
			minpep = m
	peps = list(map.iterkeys())
	x, genx, total = 1, {}, 0
	print maxpep, minpep, mass / maxpep, mass / minpep
	for pep in peps: 
		genx[pep, map[pep]] = genx.get((pep, map[pep]), 0) + 1
	total += sum([genx[p, m] for p, m in genx if m == mass])
	while True:
		nextgen = {}
		for pep, m in genx:
			for p in peps:
				if m + map[p] <= mass:
					nextgen[pep + p, m + map[p]] = nextgen.get((pep + p, m + map[p]), 0) #+ genx[pep, m] #* (x + 1)
		genx = nextgen
		#print genx
		x += 1
		total += sum([genx[p, m] for p, m in genx if m == mass])
		print x, total
		if all([True if genx[p, m] >= mass else False for p, m in genx]):
			break
'''
mass = 1024
CountingPeptideswithGivenMassProblem(mass)			
'''
		
def SuffixArrayConstructionProblem(Text):
	suffixes = []
	for i in range(len(Text)):
		suffixes.append(Text[i:])
	print sorted([(suffixes[i], i) for i in range(len(suffixes))])
	return map(lambda(x): x[1], sorted([(suffixes[i], i) for i in range(len(suffixes))]))

#print SuffixArrayConstructionProblem('AATCGGGTTCAATCGGGGT')
#print SuffixArrayConstructionProblem('AATTGACGTGATAAGCATCGTGGCGGGTTTCCAATCTGCCTTGCCGCTTAGAGGGTGCAGAGGGACTGCGTTCAGATTTTGCGGTCGTTGGTTTAATTGGCCGACCCTGAACATTCCTGTCCATAGTTCAGCACCAACCATACTATTAGTCATGCTACTCAAACGCGTTCGTAGAACCATACTTCCGCTATCGTGTCTATAAGACCCAGCTAGGGGCGTTTCAAACATTTCACCAGCCCATGGCTACTACGAGAAAAAGGCATTTGACCACTACCGCAATGGAACGGCTGTTGTCTGCTCGGAGGCTATTTTAACTGAAGATCAGCAGGTATGTCTCGCGGATGGAACAGTGTATTTCAATTGCAACTGACTACGTGTGAGGTTCGGCTTGGAAGAGTTGCACAAAAAGGTTCTCCCAACAAGCCAAAAGGAAGCTCTGCCGTAGCACGTTGCTCGGACACACTGGTACAGTGTGGGCATTTTATGTTACCAACATCGGGGACGGGATAGATTAATGTACAATATAGTGGATATAGCAGGTTCCGCTTCCGGTTCTGTTGTCCCCGGTGGTGACGGCCTGACAGTGCGAACTACATGGTCCACACGAGATAATTCAGCGAACCACTCTTAGTTTCGGAATTGTTACTGCTGCCGTCGGATCAATGAAGTAATCGCGGTATGGACTCACCGTGCATGTTTCATCGCCCGTTCCTAGTACCACAAACTATAGTGCTGAATCCTCACCGCTAAGTCTGGCGTGTAACGTTAAGTACGAGCCGTACACCTGGGTCGGCGCTCCCTGGTGTTTGATCGGGCTGAATATGAGCGTATGGTTCACGATCCGAGTTGAGGCTCAAGGTCGGGTGCAGGCGGCCAGATCCTCTCCAGCTGTTGTGTCACATGCAGCAATAAGGGGAAATCGATGCTTTTGCAGGCCCCTTCAACAAAGATTTCTGACATTGGCGTTATTAATCAAGATCCAAACTGGACCGAGTAGTAATTCTCGTATTTTGGCCGGTAAGCAGCTTCTGCTAGTCCCATGTACAGCGGACAGTGTAGGCCCCTATATTTTTCCTCAGGGGTACTGTGTCTTACTGACGCCCCGTGGCGTGATTTAGGGCTGTCGGAGGATGCGTATTACAAGGTGCGCTACGGCCCCTTGAGCCAGCCAGTCCTGCGGTTTGATGTTGGATGAGGGCTATCGGCCGCAATTAACCTCCTCCATTATCAGACAAACATTCACGAACAACATATATGCCGGCTGATAGGTGTGCGCCACATCGTCTGGGGGAGTGAAGATAACAGTTATACTGGGCACTGTATCGGTACGCTGTATTTCTCGCCATCACATTGCTCCCCGACCGCTGTCACGATTTAACCAACCGGGTAAGGACGTCAGGTCCCGCTACCTTTTACGGGAATCCGCAGCTAGGCTATGGGCGTAGCACCGCTCCGTCCCTTAGCGGTCGGAGATACGTGAGCAATGTGGGCATTTATTCCCAAGTCGATCGGTAGCAAGGAACGTTGCTGCGAGTGCTGATTTACGAGTACTTGACCGAGGGGCAACCAGCCCCACTGTCACGATACTGGGCCACCGAGATAGGGCCGTCATCACGCCGTGCAAAGTAACTCTCGTAACTGTACTCGGGATCGCATGTTAATAATTCACAGACTCTAGTACCTATTCTGCACTCTCCACAGCGTGGCGGCCGGGACCATTGCTCGTCCCAGACGATTAACCTCATAGAGCTCCGTGCCAGAATGCCGTGGGACCGGTTTCTACGGGCGGTGAGGACTCAATTCCCAAGCCGGAAGTATCACACTCTTTACGCACAGGTGCAGGCACCCAGTAATAGGACAGTGCGTACGTGAACCAGGCCCAAGTACGCTACCGCGTTCTGTGTTGTGGCACCGAGACTCCTCTTCCTAAGTCAGATAGTAGCCTTGGCAGTAGCATCGGCTATGTTCGTGTGGTAACTCTTAGCTGACATGTACAAACACATCTCAGACACAAGTGACTAGATAGACGCAAAGAAAGTCTAAGACTGTCATTTACCCTAAACAGTCCCTAATTCTTCTGTTAGGTTAGAGTACATGAATAGATCTATTAGCCTAGCCCCATCGACAGAATTGAAGATCGCATCGCCGAATTGACGACATGCTTTCGGTATGGACCATTCTTCGCAGCCGAGCCAAGCTTCATCGGGGAGAAGGAGGGTTAGATACACTTGTCAGGCGAGAACTGGTGGTTGAAGAGGCGCTTGACGCTTGCTATCGGAAGGGGTGCGCTGGAGCAGGCACCAAGTGCATGTTATCTAGTAGGAGCTCTATGACACCGGCGTAGTCGACCAGCGATAAGCGGCCGATCGCTAACGATAATCTCCTGAATACGCCTGGAGGTTCCAAGTACTACTCTAAAGACTACGCTGTCGCAATTCTCTTCTCTTTCTGTGTAGTAGTAGGGGGTAGTTCAACCCACATTACGTTAGCCATTAGACAGGCGGGAAGTTTCGCATATTTCGGAGGGTCTCAGGATGTTTCTTCGTCTTTCAATATCATCCAGACCGCCTTACACCATGGGGCCCCCCTAGCATGCCGTCGGTCAATCATAAACGGGAACCCAAAGCCCTTCCCTGCGCGATCGCAGCCACGCTTTAACCCCGCCGCGTCGAGCGCTACACAAGGTGTGGGTCTATCGAAATGTGCGGACCTTTCCATTGAGCACAGGATCTACATTAGATGGAGGAACCGGTATCGATACGGGAATGTAAAGATCGCCAAAATGAACGAACCGACGCGACGTTTTACTTGTGACAGCATCGTTCAGCCTTTTGGCCGTGAACTATGCCTCATCAACAACCCGATTGCTGATTCGCACTGGATAACAAACACTGTTCAAGAACATCGGCGTAAAAGCCTAGCTCACGTAGATATGACGCACTAATATTAACGCCACAGCTCGTTGCCGTTGTGCTTCTCCAGCCCTGCGCCGGAGCGCGAGACCAAGGTCCTGAAGAGACTATACGAAGAACTGCCGCTCCGAAATCGGATCTCTTTCGCTCGAGTGCAACTGAATCCTATGCACCGTAATTGAGCATTCCGTCTAATAAACGCTTCATTACGGACGTCATCGAACCCCGCCTATCATGGGAAACATTAATACACAACGGGCATTATATGTACTGCGAGGGGACGGAGATCTACTCTGAAAAACATTCAGGTTAAAGTGGCAGGAAGGTATGAAGAAGTGCCCGGGGGTTGATAGTGTGGCGTAACCCTAGAATGTTGGCTTTGTAGCATGCCGTATCATGGAAGACAGGCGTTCAAAATAAAGTCGTGTAGATGCCAATTCCTGGGGAAGTAGAATCCCCACGTACGCCTGATTTCGACGCCCGAATGCTACAATTTCGGCGTAGATGGCAACCTTAATTTATTCAGCCGAATAGTGCATTTTACAGAAGTTACTTGGAGTTGATGCACTGTCGAGCCAGAGTAGGTGCGGACGAAACCCAGGTGAAAAGATGTTTAGAGGCTTGCGGTCATAGGCTACTGGTTCGGGAGACCTTCCCAGTAAAAAAACAGGAAAAGACGAAGTAGCAATCGCCATAATATCTGCGTCAGAAGTAACGCACATAAGCGGGGAATATATCTTTCTCATCTGCCAAGTGACACATCGTATGAAAGAGAATGGTATCGGCATACGCCTACACTTACGAAAGTATCTCGGACATGCGGAGCTTGCTTCCGATCCTCGTTAGCGCGATGGGATTTTAAACGTGCCAGCGTTACCCAGCCGAGCCCCTTCAGCTTCTGTGGCAAGCTAATAAACCTCGCAGTATCTCAAATCACAGAATCCTTCATTCGCCAGAGTTGGTCGGATAGACCGGTTACAGAGACGGTGCACATGGCCACCCGGAATAGCAAGAATAGCTCAAAGTCTTCTTACCCGCGATCCTCTTTAGCTTCACTTCCTGCGAACACTCTAACTTGCCCGGGGTAAGTACTTTCTATGTCTGTATTCCTTTCAGGATGCCGCGCCCCCTCGTTCCCGATGCCGGAAATCATACTCCCTCATACATACCTTTGGGATACGAATCGCCAATGCTACGAATATATGGCGCAGAGCAATCAAGGGGTTAACCACAAAGGTTACAGGTTCCTACTTCGTCATAATCTGCGAGTACACATAGCAACTGAGGCGGTCAACCCCGGCATTCCAAGGCGGTTACATGATAAACACGCGAGATAGCCATTGTGGTAGCACCTAAGGTGTGCTCAATTTGATAAAACAGGTGTAATCAGCGCAACAACTGCAGCACCTCAGAACAGTTTAACATCAGCTAAACTCTCCGCCTCCGGATACAACACACCACGACCGTCGCTCATGTCTATGATCGCTGGCGGTGGGGGTCAAAGTTACCTAAGCCTGAATCCATGAGGAATGAGACATAACTGCGGTTCATCTGTTAATGCGGATGGAGCCCAACGTACAGCAGGGTGATTCACCATGCAAAGGCTTGAGACCATGCCCCCCCGAATCGCCGCAAGGGATTCGATGGATGTGAAGTGCAGCGCATTCCAGGCCCGCCGTCGCCAGGACTTGGTTAGAGCCGTGTTCTAATAGTCTGCCATCGAGTCGAGTAACAAGTTGTTGTAGGCCGCCTGCACAGCGTCGTCCGGAAGCGACAATCCCCATACAGGAGGGGTGCTGCAGGTACTGCCTAAGGCGGAGGAATTCCTCTATTTCGCATGAAGTTGCACAAGGATATCGAGATCGCGTATACTAAATGCCATCCAAAGTTCTACTAACATTGAGTGTTCTCAATGTCGTTGTAGCCGACGGAACTCCGCCCGATTGTATTTTCGGTAAGAAGGAGCGGGAAGTCGTCATCTAGTTTGCTCATTTCGGCGCTCGGTGCCGTGTTTGTTAGTTCTTCCGGAAATCGTTTCAATCGCGTGCGTTACGGGTTGAATGATAGTCCCTTCACGGGTTCCAAAGGGAAGATTATGAATAGGTCTCTATCAGCGGTACCAGAGTGCACGGCGTCCAAACCGTTTGAGACTCCCCCTGTATTCGTCACGTATAAGGTGGCTGCATAACGCCTACGGTCCGAGCGGTAGAATGCATGCCCGACCCACTGCCCTGTGTGGTGCGGCGGGAAATGGGTTTAATACCTTGATGTACCAATACAAGGACGTGAGGTCTCGGGTGCCCCTCCAGTCTCGGTTTGGCTTTTAACGCGATAACAACGGTAATAATGACCGTCTGTGGCGCTCCCCCTGAGACCTCCGATTCAGACGGACCATCAGTTCTTGAGTTAGAGGCTGCGCCGCAGCGAGTGCATTCCCGCCGTTCCCAATCACTCTACCAAACGGACGTGCCCAAGCTAGCCTATTTAACAGGCAAAAGAATTTTGGGAACCGATTCTGCATCTCTCGGTCTACTTCTCTTCCGCCCAAGTCCCTGCTGGCTGCCACGGTCACAGACTTATGGATTGCTGTAACTAATCGGCTAAGCCCGCGAATCTGCTTAATCGGTTCCCAAAACTCCGAAAACGGGAGGAGGCCGTGACTAGCTGGTTTAGCGCATTACCTGCCGGGACGACGGGTATGGGGCCACCCCAACGTCCACTCAGAAAAGTAGTCAGCAACCCCCTGCATGCAAGCATGCTCTATTGCCTTACTTTGTCCTTATGTTACATAAATCTACTCCTCCTTACTCTTGGCTTGATCCCTGCGAAAAGGATGACCATGGTACACGGCACCCCAGTGGTATGTTTCTATAAGTGAACCCTACCATGATACACCTAGGCAGGCAGGGACCATCAGCTCATTAATTCGTGAGGAACACTAGTGTTTCCCCCTCGACTTAACCTTGGTGGCTACGAAGGTCGGTATGATCAAAATTAACTCATTATCAGCAGAGAAATAGGGCCGGGGCTGCCGCGAAATGCCGGAGCCCGGGTGGTAAAAACGCAGTCCATTGCAGTTGTCAAGAACGCAAACGGTTGCTCGCGCCGAAGATCCAAGCTTTCATAGTTTCAGGCCCGACCGTACTCGGTAAATCTCGATTTCGAGGTGCTTAGTTTGGGTAGCTCTGTCTACATGACGGCCTCGTAATGTACCTTGATGGTTCCAGGAGAGGTAAATGTAGGCTTCGCTAACAACTCCAGGTCGGTTTATTACATTGAGACCACACGCATCACGAACGGATAGTTTCTCAAACAAACCTAAGCTTCGACGCGGATGATCATGTGTGCGCCTTGTCACTAGAAGCGACGCGAAGATCTATAACGGTTACGAGTCCCACCTTTGTAGTAGCAGGATACTCGGATGACTCGACATCTCCTCCGTCTGCGGTACAGGCCCCCTAGCCAACGACGGTAGCGTTCTAGTCTTGCCAGTCGGGGTCGCCGCGTTTGAGTGAAAGCTCAAATGCGTCCAGCTTCAATCGATACCTTGACAACTTCCTTCCGGGTAAAACACTCATTATCTCTCACCAGTCTTCCATGCGAAGGTCTGTGCTCATGCACTCACCACTCGGGAGGCAATGCCGCCCCGAATGGTCGAATGGGCAATGGGCCAGCATGTCTTTTCAGAGAACCACAATATTGCTCCAGCATGATAGAGGACTAGATAACCGTACTTATGCAATGGCAGGAACCATAAATGTCATATTCTGTCGGTGCCAGAAGAAAGATTTATATCCTGCCGGTCTGATATGTACTTCATCTGGGGTCTCGCAGAGGGACCTCCATTGTCATTACTTTCAAGGGAAAACATGGGTTATCCCCACGGAACATCTAGGCTGAGATCCTGGCATCCTTGACAGTGAGGCAGTCCGCGGGTCATGCTGCCGTGCTTTGGGACTCCAATATATAATCCATGCAGCCTTATTGCGTTGCCTAGGGCGCCTCTGACAATTAGACTTGTCATGTGTCACTGACTAACCGCATGGCTGTTAGCATCCCTGTAATGCCTAGACCCATAACGTTGCTACGGCGTTTCTTGCCTGAATCTGTAGTGTCAAGGCACCGAGCTCAATAAGCTCGGGCGCTTGCCGTTAGGAGTCAACAGGCTTAGAGATCAAGAAATAGGTTTGCGCTGCATACCTCACTATGACCGCAAATCACGATGTATAGGCCCATCGAAGCGGAGAGGCCAGGTATATAGATCCTACTTACGCTTTTGAAATCCCTCTGCTTTCTAGTGAATGAATGGCCGTTACTAGAGACAGTCGAGTAGTTCGACGCAGGCAAGTAACCTGACTCGCCACCCCAAGCTTTCCGTTGGCTGAGCTATAGAAACAACACTAATAGCGGTGCAGGGCCTTGTTAAAATAAAGTATTTCACGCCGCCGGTCTAAGCTGCGGCCACTTATACGGAGGTCCCCCGGTACCTGTTACACGATGTTAGGCAACCATTAGAGGGTAGCCTCGTCTGGTTGTTTAAGATTCTTGGCGCCCAGTACGTCTGCACATGTAAGAACGCAAATTATATCCATCCCCTCTGCCCGCCTGCGAAAGAGCTACCCATCCTTTGCATAAAGTACTTCTGAATTTTCAATCTGAAAATGGCGTTGATGATAGGCATCGCATGTGCCATCACGTTAATCTTGTTGGGCCCGGACGACCATCCTACTGGTGATTTTGACTGGTCAGAGACTATCACTTGTCTGTGGACAGCGTATGTAGGCCAACCGGTACCAGCGAGGAACATTCCATATGGTCAACGGTTTCTGCACGCCCGCCCCTAAGATGACCAGTGATGAGCCCATACCATTCGCAACAGGGATGCTCCGGACCATCTCCCTTCTCCTAGAGGTGGGGCTTTTCGCTACGCTGGGCAGTCGGCGGCATGTACCCGATCACAAGTTATATGTACAATCAGGACGAGCCTCGCTTTTAGCTCGTCGAGAGCGGACCGCCCATTCCAGCCTAAAACCGGTCAAAGCAAGGATCCCCGTAAGTGGGGGAAAATTCAATCTACAATACAAAACGAGGCTACGCGAGAAAGGTTCGTAAGACGCCACTCCACCTGGCCCTTGTGGCGGAGCAGATGTGCGGGGCGATTACGCCTCATGGACGTACCTTTCTGAGAAATGCTCGTGCCTTGATTGTCTCTAGTAGCTTAGGAACAACAACTTGATCTACTACACATGTTCCCGTTAAACCCAGGAAGGCTGGTGAGTACGCATACCCCGCCATAGACTCGCAATACTCGGGGGGCATAGTTTGGGCCCCTACTCAACCTGGCGAGAAAAGGTCTTCCAGCTTCTACCAGCTAAAAGAAAGCCTATGGAACTCTTTAGGAAACGAGCAGCAGCGAGAACAGGAGACCAGCCAGGAGACCCGAGGTTCGCACAATTTTAGAGTGTTGCATCATAACCTCAGCATGTAAGCTTGCGAAAAACGCCAGCCCTTCCCGTATGCCGGTCGAAACGAAGGCGGGAAAAAATGAAGGTTTACTTAGTTACAGTGAGTCATCGCCTTGAGTCACGATCAAAGGCAAGGGCTAAGTAAAGGGCACAACAACACTTTATCGATCTTTGACTCTCGAACTCCGCGAAGGAGCCCCACTAGCGCACGGTTCACACGGAAGAATGCCAAGACGGAGGCCGGGTGTACTAAGAAACTGCTGGATGATTAGGATAGAACAGGATAGCCATGCATCAGGTTGAGTGACTGATGGAGCCGGGGCGTTTCTTAATCAAACCTAGCGTGAGTTGGCAATCTGAGAGGTCGCGTCTTCAGGGAGAAAGTCGGTGACTCAACCTCGCGGTTATAACAAGCAAAAAGCTTAGTATACACGACTCCGACAGTGGTGGCACTCGCCAGTCGAACAACAGATGCTTTGGGAGATAAGGCTTATACTGGGAGAGAGGCGCCTGGAGCGGCAGACGTTAGGGGAAGTCGTCGTCTAACTGGGTCGAGGTTTAAACCCGTTTATCTAAAAATAGCAGGCTAGTTCGGCAGTAAACACTTGATAAAGGGCGTACTGAGCATAGGCTTCGGCCATTGTGAATAGGGAAACTGTGGGGGGGTCAGACGTAGCCAAGAAATCCTGAGATCGCTTGCCGGTCCGTGAGGAGTCCCGACGGCTTTTGATTTTAGGGGTTCGCTGCAGCTCATTTCATGGAAAATACAACACCGGCAGAGACTCTCCGTTCTACCGAAAACTGGCAGTCGACGGGCCCTAGCGTCGAAGCCGTTCGGACCTTGTTAAAAAATTGATCGTAGTGCGCGTCGAACATTTATAGCAGTCGTGCACAACGAGCTACCAGAAAGGTGCTAGACCCCCACCAATCCGGTGATGTACCCGCTCAGACGGAGATTGCCATCCTTCCCCACCTTTATCTACTCCTCTGGGCGACACCCCGGACGCAATTAGCGAATCCCCAGTCTAGAATTTCAAGGAGGCACAATCTTTCTTGGCGGGCTTGACGGCATTATCAGTCAAAGATTGAAAACCAAGCTTCCATGAAGTCCCCCACACGATACTCCTCCCGCTGAGCAATAGTATTATCCGATTCTATAACGGCTTACGAGCATACTACGCGACGGAGTGGGACTAGACTCTGACATAGGGGTAGTCCGAAAATTGTGCATGGCGTTCCGGCGGCCATTTGGAATGAAAGACCCGATGTAGTGGGGGTAATAGTACCAGAGGTGAGACCACGCAGGCGCTCTCAGACTCATCCGTAGCGACCCGCTTGGGTCGCCTTCCTACCCCATATATCTCCTAGAATAAGGGACGGTTGTAGTCTGGGAGGAGACAGGTAGCTGAATGTGCGTGACAACTCCGAGCAGGTCTTCTGGGCTCCGAGGTCGTTACCGTACGATCTCCCCTGTGCCTGGGTGACTTGGTAAAGACTGCCCGTTCGTGAAATTCATGAGATGTACCATGTTGGCGTTGGTCACTTTTGATTCCAGGAATACCGTAAGTTCCACCCAGCAATCGGACGTTATGGAAGCACTCTCTCCCGGCTGTTAGGATGAAA$')	

def PatternMatchingWithSuffixArray(Text, patterns):
	print SuffixArrayConstructionProblem(Text)
'''''
lines = read_file('inpros103.txt')	
PatternMatchingWithSuffixArray(lines[0], lines[1:])
'''

def PartialSuffixArrayConstructionProblem(Text, k):
	suffixes = []
	for i in range(len(Text)):
		suffixes.append(Text[i:])
	suffixarray = map(lambda(x): x[1], sorted([(suffixes[i], i) for i in range(len(suffixes))]))
	for i in range(len(suffixarray)):
		if suffixarray[i] % k == 0:
			print str(i) + ',' + str(suffixarray[i])

'''
Text = 'PANAMABANANAS$' #'banana$' #'PANAMABANANAS$'
k = 5
Text = 'GCCGATGCCACGCCTCGCTAATTAACAAATCCTGAATTCTTCTGGAATTTTAGGCCTATGCTACCGAACAGCATATCAGTCCAACTGCAGTTCTCTTTGTAATTAATCCGGTGCAAGGCTGAGGCAACCAAGTGAATGTAGCGAGAAATGCAGGTGACACTTATGAAACTGCGAGCGGTTATGATGTATGGATATGACAATGCGTTAAGTTAGTGTTATCATATCGTACTCTTCTTGCGTTGTTAACTCTACAGAGGACATGTTCACTATGCGTGATATACGTTTGTTCGGTTAATGTGCAGCTAGGTAGACCTGCGTGAAACTGGTGCTGCGTTCGGTTATGGCGTAGACACGCTCGAAAGGCATATGGGTGCACCACGACACTTTATCACTTTACAGGCTGAACTCTATCGTAAGAGGCCGATGAGCCCAATATTCGTCCATCCAATATTGAAGAACATCTGCTCAGACGAGCAACGCAATATGTTTACAGCCCCTAACCAGACGTTACTGTCCGTCTGAGGGCGAGCCACCTATCTTCCACTGGTCGACGCCCTCACAAGACAGTCATCACCTCACCGGCTCACGATGTAAAAACGCGGAAGCTCGTGGTTTGCATAATTGTCCTAACTAAGAAGGTCGACTACTATGTACTCAAATGGTTCATCTGTCAGATGCAACCCTATCGCATCCAGACATTTCGGCAGCAATGTGGCCCATTTATTGTGCTCGGCAGACGATACTGTGGGGCACTGAATGAGTAACCCCCATGAGCTAGGTCATCCCTATAGATAGAGTACGAACTTAGGAGCGTTGCCATGGGTTTGGTATTGCTGCGCGTACTCTAGACTGAATCACCTAGTGGCCGTGATGTGCGTCTATTGAGCGACGGACTGCAGCGGCGGTCATTAGAACCCCCCACGCGAAACTGACGACTACCGCGAGCGGAGATGGATTCCGAACCATCTTATAACCCTCTCGGCTAACTCTTCAGTGAACCTGTACATTATCACTCTCAGAGACCTCACAGATAGCCGCCTGCTAGGTGAAATCCGCCAGCCCTCCGAGCAACATTGCCTACGAAGATATTTTGCTTGGTGACCTACGAGAAGGTCGCCGATTGGATTACCGTTGTGTGCCATGCTAGATCTAAAAACGAACGCGTCATGCAATAGGCCCCACCAGGACGAGCTCTCCAAGAGCCGTATTCCTTCAGTCCTCGACATGTCCACGTGTGCCAGTTCAGATTAACAATTGAACCGCCGGCCGGTTGTAAGAAGTTGTCTGGCTAGAGGCGCAAGCGGATCCGACATACAACACTCTCCGCGAAGATAGAGCGCTTGTCGATTTCTGATACACGAAGCCCCCGCTCAGTCACCACCCAAGTGCTGTGCCTGGTAGAATTCGTCGAGCCTATATCGGTGAGTCAACCAGTGGTTTCATCGGGTCAATTCACCTGCCCTTCTCTCCCGACTGTGCAGGAGAGCATAAACGGAGGTGCGAAGAATGCAATCTTCGAAGCCTAGAATAGCTTAGTGACATATTGTCCGTATCCACAAACCTCACGGTTACAATAAAACAGGCAATGTGCAGAGTGAAGTGTGGAAGGGCTTACTTTAATGTCTGTTCACGCCGGGTCGCCCTAGAGCCGAGCCGGTAAAGCTTTACATGCCGGCCAGCCAAAGTATCGGAAGCGGTACACATATACGATATCGCTGATTCGGAGCCCCCGTTGTGGTTTATCGCACGGGCGAGAGCAAAGTATATCGCCAGGGATGTACAGGCTCGTTGAACGAACGCGACGGGCGAGAGTTGAGGGAGAGCATCAAGGGTGCACCGCGGCCCGCATCGCCACCTCCGTCGACACAAGGTCCCAGTTCACGTAGACAACGTAAGCCTCGCCTTGTAGTTGATGGAAGTTTGAGACACGCGAGATCTGAATCCAACTGCCACGTGGCCTTATCGCAGCGAAACGGCTTCTGGCATCCATACCGGCTGCTCATAAACCAGAGAGTTGGCTCCTCAGTGGCACCTCGCGACACAAGCGTCGACTAGAAGTCATCAGGTTTCTCGGTTGCCCTTTATCCGGCTTAGGTGTTGATTGCCGTGTAAGCAATCGAAGCCATAGCTAGAACACACATCTTCCTGTTAGAACTGATCTGCAGTGGGATGATATCGGCGTCATGGACGGGCCGAAATCGTCATGTAGTGCTAAGATGTCAAACCCCGCATGTTCTGCCATGGACAGTTATACCGTACGTTGTCACACCGACGCAGTGTCCTAAACTGTCTTTGCCTAAGTAACCTTGGTTGTAACCTGCGCGGGTCCTTCGCCACCAACATTGCAAGACTAGACATAGGATAGTGATCATAGCGGGGGAGCGGAGATCTGCATGGTCGACAGATCTGGGCACACTACATAACGGCGAGTGTCTATTCGAATAGTCTGACTGCGCAATCTGTCCGGTCTTTTAAGAGGTAGTTTACCAGCTACGATTGGAGTATAGTATGCGTAATGTTATTTCGCCCCCTCCAATATTTAAAGAGCCCTGTACTTCCTTAAGTCAGCCAACAGCCGTTTCTGACACATTACTTAAACAGGTCGCCCACTAGAAGGGTAAGTCATCGCCTCCCACCTATCCCGCGGCTAGCAAGTAAGGGCCTTTCCTCGCGCTTGTGCGTTGCGAACGTTGAAGTGGACAAGGCCCACCAAGCGTCTCCGCCCGTTTATCCGACAGTGATGACGGCTGCTTTTTCGTCAATGAAGTTAAGGCTATATGTTTGGGTCACCGCCGAACTCTATGAAAGCCAATGAGCAGGTGTATGTAATGAATCTGCCAACATGGGCTTAAGGCCCTGCCTGATGTGTCTTTGCGCAAACCTGGTGTCGGACATATTGGTTGGATTGAAAAGGTAAGTTAGTTGGGAGAGCTGGTGATAGCCGCCTCATGTGAGGTCGTGAACCTACGCCCCGTTAGTTCTCCGGAGTCTGGGGGGGTTATACAGAGACGCGTTCACGTGATGAAACCTTCGGATATGGGGTTGACCCAACTGCCGGCCGACCGAATAGTTGACAGGTGAAGTCACGAACAGCAATTATAGGGGAACGCGACATTGCTGCAGTCTTCCCACTCAGGACAGCGTCTTTACGTATAGTATAACCTTTTTGTCGTGATTATGAGTCGCGATAAAGAGCCGCGGCCAAAGAGAATTGAAGGCCGATGAGGTTATGGTAGAAGGATGGCGATGGAGGGTCTTTTTGCGTACATAGCCCGGCATTAATGTTGTCCTTCTACGACTAAGTACGGTCCTCGACGACTCAGTCGCGTTTTCGTGCACCCGAGTGGTTTATTTGACGGAATTGCTTCCCTTTTTGAGGTAAAGAGTCTATTTGCATATACAATTGGGTACCTTATTACTTGAATCCGGCTATTCTTTATGGCTCGACGTAATAAGGAGCACTCGCTAACCGCTCAGGTTGGCCCATTTCGATAATCCTTATAAGAATCGAGGCCATCGCGGTGCGGGGCCGCGGCACAAATTGAATTGCGCGCTTACCAGCACGCTCTATGGCCCCTACCCCGGCCCTTCCCGGTCAGATTGTACTTGGTATGGTGCAATTCTCCAGAAGGGACGGACTGGCAAACCAGGAATAGCCCCTACCTAAGTCCCCAAAACTCTCATGCCACGACTTTTGGCTTCTGCTATACAAACGGTGTTCGGACAAACTGCACTGAGGACTATTAGCCAACCTACAGATGACTCTTGTCTAGCGGCTAATAGGTCGGATCCTGGCGTGACGACTCCCCTTTATTTGACTTATCATACAATCCGGACATAGTTCTGTCTGCGTGAGTTTGTAGGATGGGATTCTCTAAGCTTTGCGCAATTGTCATGTTGGTTTTTTAAATCTCATATTGCGGTAGCATGGTCGACCAGCTTCCCATACTTCGCATTTGGATATTCGTCGTTCCTGACAAGACAGGGCGGACATCCGCTCCTCTTTCCCCATCGGGGGTGTCCTATTTGAGACTCAGAACAATGCACACTACAGGTAGGCCTCGAGCACGAGGGTTTGTTCAAGCCGGAGGGATGATGGTCCACCATGATGATCACACAGCCTAAACCGCGCTGCAAACTGACGGGGGTCCGGTACACATCAAATCTCCGATAACTCCTACGAGCGCAGCGAGTACGGCTACTTGGGTGTACTCGAGAAAAAGGTCCGGCCTTGTCCTTGACTGCTGGGATATCTCGGCAAGAGGTTGGAAGTTAAGCTAGTATGGAACATCCTACATTAGGCCGACGATAACGAGCAGAGTGTGAGAGTCAAAATCAGGAATTCCTCTCACAGAGCCAGGACAGTGCGCATCACGACTTACGGAATCTATTAATTTATCCATCAATAGTGTGCGCGCGGTTTAAACGCACACCTACAATCTAGTGGTTGACTATAAAGAACCTCGTAGGGTCGAGGCAGGTCCTAAACGGACTTGGGGACAGCATACGTCGGATAGACCCCGATAGCTTGGAGTGCAAAGCTTTCTCATGCCAATCCGGCAAATACAACCATCCGAAAGAACCCTCCGAAGTAATCGTCACGGTGAGCCTCGCTTGACGCACAAACTTCGATTACAAGACGGAAGTACCATCGCCATTCGGCATACGATTGATTACACAATGTCACGGATTAAGCGCCGGTCGTCCGCGCCGAACAAGTTGGTATTGGCCCCCAGAGAGGCCGGTCACGTAGGATGTTGGTCAATACAACTATAGTGTGTTGAATTTACCGGGGGGGTCGGCGGGTGCCGGGCCCGAAAACGCACTACGAGGTTGACCCCGTCGCTATTGCTATGCGGAGATAGTATTGGGAAGTCTAGAGCCTGTCACTGGGGACAGCTGTGGAACAGCGAGGATCGGAGGGCCACCAAGCGGGTGGTAGACTTACATAATCTACGACTTTCCGCTGTGGGGTACCGGTTGCCACCATCATCGACCTGACACGAGAAAGGGTTTACCAAACTACCGTTAACTGCTTTGCAAAGATCCGGCTGCTATAGGGATCGTGGGGGACAGCGGGCTTTTTAGATCAGGCGAGCACGTAGGACTCAAGTGAAGATCAGCGCTTGTTTTCCGCCGTATTCAATATGACAAATTAAAGGCTCCGGAAGTCTTCCCTACCTTCCTGATGGTCCAAGCAAAGCGATTGCCGACCAGGTACTGCGACGATATTCTCGTGAACATGCTGATCGGGCCTAAAAAATCTTGGTGCTAGAAACGGGAATGGGAGCTTATGATCTCTGTTAGTCAGGAAACCTCTAATCGGCGCGACTTTGAAATGTGATGGATTTTTTATCGATCTGGTCCGTAGCTCGCGGAACGTGAGCACTGTTATTGATGCCGTTTAGAAAAGTATACCACGGCCGAATATTGTGCCATAGATTTATTCGACATAATGCTTTCCACTAAAGCGGGTCCCACAGGAATTAGCGTATATTAAGTCTTCGGCCGACCTGTTCGATGTTGTGCTCTAAAGCCAGGAGGTAAGACGTACGCTAGCGCTGGATGGTGGTGAGCACATAGTTGTTTAAATTACTGCGGCCGTCTTCCTGCGACTAGTTCGCAGTATTGGTAACGGACCATTTCGGAATGCCGACCGATCTGGACGTCGAACATATGGTCCAGTCAATTGGTCGCAGCACACGAGCCCTCCTACAATGGACTGGTAGCAGAAATGTACACCCTGCCTGCTGCAGACGGCGTCAGAAATGTGGCCGAACATAAGGATCTCCGATTAGTACTTGTTTGTTGATCAAGCATCAGTCGAAGACACAGGCATCACGGATTCTGGGACAAACGGCGGCCCGCTCGTATCGTCTTTATCTTCGACGACGTTCAGGCCCGTTCATAACGCGTAGGCGGTCAAAGGGTGTCCTAGGGTTACCAACGGGGTCCAAGCTTCGGGCATCGTTGGGGTTAATGTTCCCAAATGCCGAAAGACTATCTACAATTATACCGAAAATCATTCGCTGGTTAACTACACGGGGAGACAACTCCAAGTAAGAGCTCTCCCTCGCGTATATCCCATAAGGGAGGTAACACATATGTTTAAGAGCCGGACGCTAAAACTGTGGGCCTAACAGTCATCTCCAAGTCGAGCCCATGTGCATAGGTTTCCAACTACGTATTTGACTAGACACTTTTATCTGCTGCGCCATAACGATTCTGACGAGTTCTCGTCGCGTAATCCAATCATGTCCGCGTCAGGGAGCCCCATAGAGAGAGTTAATAAACTGGCTGTGTTTCTGCTGACACGTCGGAGATGCATACCGCCTATTCCACCCTTTATTTTCGTAATTGCTGGATACGTTAAAACTCAGGCAGAGCGGCAGTCGGCATAATAACTGAAGCTGTCGCGCTGGGAGCCCTGTCCTGACCGAGGACTCCACCTGAGCGATACTGCAAGACCTATTCTTCACCAACTCGGTGAGACGCACCCGCGCAGGCGAAAGGGCTGTGACGCGGCCAGGGGAGACAGTCCCGGCGAAGAGAATCTGGCCTTAAACGCGCAGGGTCAACACTGCGGACAACTGGGAGTTCGAGAGTCGTACCTGGTATTCAGGTGAGGTTTCGTCAGGCAGCGTTCAAGACCCGCAGGACTACCACCTACCGCGGTCAGATAGCAAATTATTTCTACTGAGTGCGAAGGAACACCCGTGGGTCCAAGGGCTGCCGACGCGGCGTTGCTCGCGGCAGTAAGCCCCCAATTTGATTTTCGACATCAGACTCGGTTGACTGGGTTCCACATGTCCGCGCTAGGAGCGTACTCGGGTAAAGTACGTGCAGGTCCGAGCCCATTCATTCTCGGCAAGATGTCTCACAAATTCGACGCTTTACTCGAACCCGACTTCCCATTTTTATTACCTAATCAAACCTCTCGACTGGGTGTGACATTACAGGATCATGAAACGATATCAATGCAGGGGCCCAAAGGGGGGGAGCCCACGGGGCTACGTGATTAGAGGTGGGTATTAGCACCGATTTTAATATAATGTTCCCTGGCTATCAATTCCAACTGTAACTCACCGGTTGTGCGTCGTCGGTCGAACCGGGTCATGTTCGGTTGTGAGAACGCAACTTATGCCTAGTCCTGCTATCGTTGTCTCTGCACTGAAGTTACCGAAACTGTAATAACGAAACGAACGTAAGGATTGCACGATCCTAGTTTCGCTTGAAACGGATGCTCGCCAGTGCACCCTAAGTAGGTAAGCTGACCACTGTGGGGATCCTAGGTCTGGCTGTTAAGAAGAGTTCAGGCAATAGTTAACAATACACATCAACGATGTTGTATCGATGTATGGCCAAAGCTGTATTAAAAGTATGGTAGCCTTGACAACAAGATACTCATCCCATTTCAATCTTCCTATCCAGAATAAAGATACGGCCTGAACCCAAATTTCACTGCCATTTCTGGCAATCACGTAGTGGGCAATGCCCGTTCGGAGCCCAGATGTAAGTGCCTCGTATACGGAAACTAGCAGACTTCGTACGGATTGGTTGCCGAGTTTTTTGGCTCTTGCGCGACGTTATGATGATTAGACTCTAAATGAAGGTAAATCTTGACACTGATATCGAGAGAACACTATTTTGCATATTTCTCTCGCATGCATCCTTATATTTGGACGTTTTTTGGGCGTCCCAGCGGAGGCCTTCCAAATTGTTAGCAAGGATTAAACTGCAATCATGGGTATTAAAAGCATAGTTGTGTGCTATATAAAAGTAGCTAACGACACGAGGTACATTTGTCCTGATGAGAGAAAGAGTGACGATGAGCTAATTTAAGGCCCCCCGAGGGCGAGCATATAAAGATCCAGGAGTGCTTCTCATTTGGAGAAAAATAAAGTTATCTACGAGTTCGTATAAGGTCTTGGGAGGCAATGTACCACAGCACCAAGGGCAGCTTGTGTGCCCCTCGCGGGTGCTGTAGCGACACAAAACAGATTGCATTACTTGTGATGATCGATACACAAGGGCTGGACCCGCATACGAAAGAACAGCAGGACATAAACGAGGCGAAAACGATGTGGCTAAACTAAGTAGGGCCTCGAGATAGGTTCTATCCCGCGCGTTCTCCGCCTTATCCTAACTCCAACAATCTCCCCCGTTTTTGCACCCCCTCACTTCTTTCGGGTAGCCCGGACACTAGTATCCTGGAAGCCAGGCCGGCAGGACCCCAAATATTCTATATAGCAGCCGGACTTCAATTCACTTCTATTGTCTTCCACAGGAGTAATCGGTGGGAATACCTGGGACGAGACGTAAACGGTAGAACTGTCATTGAGACGCCTTACTAGCTACAGGACGGCGACCCGGTTAATACCCCGCGTCGCTGGTGTATTCTAAGAGCGATTTACTGTAGGTGGTAGGAACGGAGATTTTGATGCTTCACATTGTCGATGTTCGACCGGATTACATATTGTTACAATCGCAGACACGGGCATCTATGGCAAAAGGTCCTACTACTGGATCTTGCTGAGCTATTCACTAGTTGACTAGGCCCTCCGACACGGAGCAGACGAATCAGAGAGTAACTGACAGCCGCGGTGCAAGATAACGATGGTCGTCATGACCCATCTCAATTCGAGATGTGTACGCGTTACGTAACCGGTACCGTAGCACTATTAGCTGTTAATCCTCCGCAATCCATGGCAAGCTCAATACGGATAGTTTCGTGCAGTTCTGAGCGGTATGAGCGTCTGCCATTTCTGCCGATGCGTTAGCCCTGACGTCCTCCTTGCTTTCCACAAACTCGATGGCTGATACTGACTATAGGTTCAATGCATAATTCCATATACCGTGCAAGCAAGTACCTCGACGTGCCCTCGGCAGGAAGCGTTCGAGGTTTTATGCGGTGTAGATTAATTAACGGAGTATGCTTATATAACGGCCCCTAAACTCGCAGAACTCTGCGCCCGCGTTTATCGTTTCTATAAACTAGTCGAATTGCGGAGTAGCCTAGGTTGTCTGGGCCCGTCGAGAATAATTCCCCCGCAAGTAACTGCTTTCGGTTGTGTAGTCCGACCATCTAACATTAAGTCTGCCCCTCGCGCTTGCTCGTGAGTAACAAAATGTGCCGACCGACATGCAGGTGGTTTTATAGACGTCGCCTTCAGGGTTCTCGCATGTAGGTTTATATCATTTCCTGCATGGCTGGCGGACTAGTCGAACATAGAAGACATGAGTAGTTATTTGCGGCCCGGCGCGTCGGGAAGCAACGAGTAATCCAACCCCTACTATGGTGGCGTTCGCTTCTTGTATACGAAAGGCGAAGCTGATGGACTGTTCGGTCCAATGTCTCGTAAATCAGTCTGAGTGAGACAAATCACCAACCGAAATATCAGCTACATTGTAAAAAAGGGTTTGTCCGACCGCCTCCCCGCACACACTATTGAGATAAAACGGATGCTCGACAGGGAAGCAAGCTGCTTTAGAATCAATGCTGACTCCACCTTACACGTGCGCCGGGTCGCCGGCCAATTCTAGACCTATTGCGCACGTACTCCTTTTACGGTAAGCTTGGTGCGCTGGGGTTGCGACTGTAACTACACCAGAGTTTATACCCTATTGCATCTGTGATATGCCGAGGCATATTTGCTGCCACCTCAGTCGATGTACCCTAAAGTTCCCTCAAACTGGCTAGCTCCAGGCCAGGTCTCGAGCCCCTCATCTTTCGACAGAAATGTGACTTCACGAGTCTTCTGTCCCAGCTGACATCTTTGGAAGGTGTACCCAGGTTTTCTTATCCAATCCAGTCTCACCCAGATGTGCAACCTCATACTTGAGTTCTGCAACTGCGGATCATCGCCTTATTGTTGCAAGGAGAGGCAGACATGTTCTGGACTCAGACTTTTTCAGGATCCCGGGTCCCCCGCCCGCAACTACATAACTTGCACGGCCCGGGCACGGGTCACCCAGCCGATGGGCCTACGTTTTAGGGTGTTCGGAGGCCATGTATAGTCGCTAGCACACTATCATACACCACGGTTCAGCTCATGCGGTATAGAGATATATAAATACGGAACTAAGCTCTCGACAGGGGACCATTCTTCCACACGGAGAGAATCACTGCTAGTGCTCTTTTCCTAATCTAGCTTGGTCTGTCGCGGTCTCAGTTAGACCGAGTAAATATCAAGGCTTGACCATCACCATTCGTGTACATGCTAGGTACAGCATACGTCACTCGCAAACAGGTGCGTGCAGGATATTGATTTAAACTCGATATAGCCAAATTAACGAACCATGTTTTCGGCCAGCGAGTGACTGGTGATCTTGCAAGGAGGGTATGTTCCAGTGCCGTAAGAGCTAACGGCCAACTAACGACCTGGCTTGTGAATGAGGGCTACGATACCTCGGGTGGACTCTCACTGTGATATTACCGACTCCTACCATACGTGAATGAACCTTGTAGCCCTTAGATTAACTGACGTAACCCGGAGTTCTACCAGAGATACCCATTGTACATGAGACCCCTAGCGTTACTCATTGTAGTTAAAACGATGGCTATAGGCGCTCTTGAAGCTGGGGAGCACATCGTGGTGTCCTTGCTAATAGGAAAGGGTCGAATTTCCATTGGGGGTTACTAAGAGCATAAGCGCATCGAATTCTACGCAAATAGCCCCCTAGGCTTGACCACGACTGGGACATCGACAGCGGACGCTTGTCCCAAAGCATCCAGCTACAACTGCGGGGAGAGAAAGCAAGACAATCCACCTTTGATACTGATATAGCTATGGTTTTGACTAAGTCACTCCTACAGGCTGTTAGTCCATCAATGCGCCCTCTCATTCTCCATTCGATATGCGCAGTTTACCCACGACTGCATCGAACGTTACCTGGGATACTCGATAAATCTGGCGTGTGTCGCGTACTGGGACAATTTACGTCCTCCGCTCGTACTAACAAGAGTCTGTCCTATTCCGTCTTTCCGCTTTGCCGATGGCCGTACTCGGGTCATTTTTCAGAATACTGACGCGTTAATTTTACATCGCCGAGTCGGTAACCATCCTGTCGTCAGAGGGATAGCTGTCTCCGATAGATCTCAGGAAACGCTCAAACCATCAGCAACGCGTTCGCGTTTCAGCTATAAGTGCATAAGTGCTACGTCTGCCAGAGAGCGATATGACTTTCATCGAGAATCTTGAGCGTGCGGCCTCTATCCGATAATCAACAGGTTCTCACTCAGAGGACAAAGAGTGCAGATGAGACTGTGACTATCTCTGTAGAGCGGTGCGCCGGCAGCTAGTTTATCCCAGAGCGGTGCATATGCCCACCCCGGTGCTGGACTGACTCAATCGCGGCGGGATTTCGACCACAGGCGCCTTCGAAGCAGTCTGTCACATACTATACCGTGCAGATGTCAATACAGAGTGGCTACCCACCGATACTATGCGATGTTGGTGTCCTTCCATTGGGAGTCAGCGCCTGGCCATTAAGATACGGTCGACAATGAATACAGGGTCAAACTGAAGGTCCAATGAACTTTGTTAAGGTTCAGTTAATGCGACTCACTCCTATCTTCCAGGTAATCTGGAACAGTGCGCTTAACATACACTAGCTCGACCTTCGAGTTCTGAACCATAGTATAACCCCATCATGGATGTTATAGCGCGAGACCAGCATTGGATCTCTTCGCGGCATATCGGACATTGATCTCTGGACTTGTAGGGTAATGGCTAACTCAGTCTGCCTCCCGTCGGAAAGGGACCTACCGCCGGGGGCGGATCGAAACCTCCGAGCATGGCATTCCCAGCTCCAAATTTCAACAATTATAGAGTCAAAGTACGCAAAGGACTGCGGGATCGCTCGATGAATGGGATGAATTCTATTTGCAATCTAGGCGCCGTCTTAAGCACAGGTTGACCACAAATACGAAGACGGGCCGTAACCAGCCACGTATGCGCGGATCTGCTGACGCAATTCTTGACTCTCATAGAACATCTCGGTGACACATGCTCGGCCACAACATGGAGGTACATCGGGTATCTTGCAAAGACCCGGAGGTCTTGGGTGGATATGCGGGTATTCTACCCTAAATGGTTGCGCGGTGTTTTGCTTTTAGGGCCATAGGACCATAAAGCCGTGTATCATAGGGTTGTATATGGGAAGGTGCTCCCATGGCATAATTGGTACACTTCTGTTGCCGATTCATAACTTGTCACTCCATTTCAATATGCGCCATGTAATGAATGTCCGACTGCGTGCCTGCAACCCGCGCGAGTCTTAGGCGTCCCTCGATACGTCAAAAAGGGAGCTACTTCGTCGGTCCGCAGTCAAGCCGGCGATCCAAGTCATGGTTAGTGCATCCTAGTGCGCGAGATGCCACCGCCGGATGGTATTAAGTGCACTAAGATAGATAACCCACACAATCCCGACAAAGAGACAACAGCAAGCAGAGTTGGGGGACAATCGCCTCAGCAAAAGAGCGAACCCGCGCCAAATTAAGTCGCCAGCAATCGGACCGTGGCTAGATAGCAGACCAGACCGGCGTTCTAAGAGCTGTATGTTGGCAGAGAGTGTGCAAGCATGGAAGGGCGCTGTTATATAGGAGTAACTGAAATCTGTTAGCGTGTGCTGAGAGATTACGCTGAAAAGACATAGCATGGTTACTATAGCAGTCAGACGAGAAAAAAACGCGAATTGGCTATTAGATCATTGGTGGTGGAAGGAGAGGTACGCATCCTCTGCCCAGACGTTATCCGCGACAGACTAGTAATAACTGGTGTGCGAGCCGCAAGACAGGCGAGGGTGTTCCTCGAGATTAGCTAGGGACTACCTGGGATGGGCAAAATCTGGTCCGACGGTAGGTCTCTCGTACGATGGCGCTCCTTTCTCCGGCGCGGTAGGATGTTTCGATGCTGCAGCGTGTGAATGGATAACATCAATGCGTCACCCTCGCCCAGAGCGCCCTCACTAATCGTACGACTTGAGGGTTCAGGTTATATACTATGAGGTTAGGCTGACGATTAGTTACCAAATACTCGAACGCGTAATTTGCTTTGCGTTGATTCCCATTTACGTATACCACATATAGCCATATACGTTCACGCATCTACCAGTAAATACGGTTCTACTAGTGTCCCAGGGATAAATGTATGTGCCACCCGGCCCCTGACCTAAGCACAAAGATGATAACGTACTGCGGCGTCCGGTGTCACATGCGTGCCCTGTTTGAGTGCTCCGAGGAGCTTGCACAGAGTTCGCTAGTCGGCGCTTGTAATCATATTTAAACGGTCCGACTGTTCTACCGTATACCCGAGGGCTGGTTGTATTAACGCGTTCTCACCGGTATGTATAGGAGTGCCTGGCTTGATTAAGGTCGCCCTGATGGTCCCCAACGTAGGTCAGACTGTAGCAAGATTGTGTCGGTGATGACGCCATGGGGACGGACATCAGCCCGCAAGTTTTCAGCGACTCCTATCAGGATAAACGCTAGACCCAAGTTATGTATAGCGATATTAAACGTGCTGCTCCATGGCGTAATCGCGGTCACCAGATGCGGCGCGTTTTATTCGTAATTGACCTGAGGGATCAGAAATTCCTTAAGTGAAAGAATTTTCTTCAATCATTTGTACTAACCATGAAACAGATTCGGCCACGTTCATTTCTCGTGCCAATCTTAGTGTTTTATGCCTTGTCCGCCACAGTCGGCCTTTCATGCAGCGAGTCGTGTCTGCTCCGATAGCATGCATGGGCATCCTTCGTATGTGTAACTATGGAGCGAGGAATTCCTACTGCTTTATATGGTTTCATTCCGAGTGGGGCGGGTGGCTTTCTTCCAGTAAAGTACGACGCCAGTGTTCACGAGCTGGAGTTGTGTTACCGAGGTACCGTTCTTCGTAGATATTATCTTGATTAATAACACTAGTTACGTCATTTTCTTGATAGAATAAACGTGTGAACACATTTTTTAGGTTATCCCATCGTAGCGCTATAATGCGCCCGCCCATAAGGTAACAGAGTGTATCGTCGCTTTGTGAAGCTACGAGATTTCGGTAGGCGCGATAGACGGGGGTGGTATTCGCGGAGCTGGGTCAATAATGAACACACATTCCGAATCTAAGCATTATAACATATAGGCCTATAGGAGTGTCTGAGTTGGGCCGCCTGGAGGTGATGCTTTGCAGGTCTGACATCCTCGAAGGGGGTGCGGCAGACGCATAGCTCTCAATTCTCACGCATCAGGCGAGCGCTACATAGGGCCCTTGGAATCCTTGAGTACCGCGAAATCGCTGACCCACGATGAAATGAAATTAACCAGGCGCTATGGCCCAGTGCCCATGACAGCAGACGGTTGGATGGTTCTAGGCTCACACTCTTAAGGAGCGACCCGGTTGCGGCGTTACGTGCTATCATCGTGAGCCCGGCCCACCACGCCAGTCGCAGTACTCGCGAATTCGTGTGGAGTAAATTCGTCCAATTATCCTCTGTGGATGCTATGGTAAGTACACTGCACTTATCTCCTGGATTTGTCGTTGGGAGAACAGCCAGATAAGAGGGTTCCTAATTTCAGCGCAAGATTGACTGTGGCTCAAAGCGCCCTCTTCGTTTGCTTGGACGGGTCCCGCAGCGTTAGATGGGTTAACCTGGGGCCGCAAAATCCCGTTTTAAGTGGGTTTAATCAGTAGTTGAGTGTTGGACCTTGGCTTGTTATTTAGGAAAAGCCCGATCGACTTGACTTTTCCGTTCTCACTTGATACTATGAGGGCCCGTGCTTGTAGACCACGAAATAGTAGCCCCATGCACACCTCCACATAGCTTAAGAACGTCTGACAGACTGCTCCGTATTCAATGTCTAGGGACCGGTTCTTCCCAGCAGGTACATTGGACTGTATAGATTGATGGCGCCCGAAGGGACCCTACTCGTAGAGCAGATCACGGAATGTTCAGACGCTAATCACATCAGGTGACCAGTAAGCACCGTAGTCAGAATCAGAATGTTAGCCAGAGTCTTCACCACCGGACACATCCAATACTCCAGGGTACATCGAATGCTCACTTTTACGGGTAAGACGTAACCATACGCCCAATAGGTCTCTCTGGAACTCGAATTTACGCCTAGTAAATGACGGGCACTTACAGCAATCGTAGGAGGTTCGATTAGCTATAGGTCCTTCGGTGACGCTCATTGTATCATTGTAGGGGTTTACAAAGATTCTAGACGAACGTTCGGTCGGCAGGGATCTGGGTCCGTGCGCTATAGGATGGTGAATGTGTATTGCTTCACTTTGTTATCCTGCCCTGATGGGATGTTGCAATCGGAAATACGTCAATAGTTGTCACGGAGGGTCGAGCGTGTACGCCTCGAGATTGACAATCGCCTGATTTATGCTTTACCCGGGAAATGCGAATATCACCCCAGATCTGTGGCTGTACCCGAATAAGCCCATACCGGCCGAGGTTTCAGATTGTAAAGTTCCCAAGAAAGTTCCGTGGGACATAGCGTTACGTACCCTTAAAGTACTTGAGAGAACTACATTTGATTAATATGGCGATCGGCACATCCCGTTTTCAAAGCGACCATGTGGCTGTTCATGGCATTCTATTGCACTACGCGTCAGATCCCGAGTGTATGCTTGAGACGTTTACCCGGGGCTGCTACTTCACAACCGGGCGCCACGTTCCTTCTAGCATCCGCCAAAGCCGGTTTGCAGCGCGACGCTGGGCGAGGACTGGGGTCAGTGTACTGGGATTTGTGCGGCTTGGACTTTGGACGGATCACCTTGGTGGAGGATGAGGGCTTTCCGGTCGCAACGAAAAAATGTAACGCGGGTTCGCCTCACCCCCGCAGCAGGATTAGATAAAAACAAGGTGTTATGGGACTGGTACTCTAATTCACATCAAGAAGACGCTAGACTGGTTGACCATGAAGTCGGCTGCGTTATAGTCGGTCTGTTATATGCCCGGCACATGCACAATTTCTCTGATGGGTGGGCTATGCCGCATATCGAGAGCGCCTTTTAGTCCTAAAGTGGACCTCTACGTGTGTCAAGACCTTCCCATAGTTGTGAACGACAGCGGAACCGTTGCTTACAAGAGTCGAACGCCGTGGCTTTTTGCTTGACAAAAGCGGCCGGGCACTCTGCAGTCAAGTTAACGAAAGCTCTCGGCCACGCTCTTAAAGACCACTCGACCTTCGACAGGAAGTAGTGCACTTCCAGGGGCAGTGCTTGTTCTTGATTAGGCCGTTTCACCATCATGCGACCATCATCCAGCTTGTGCCAGAAGGGATGTCCCGACGCCCTGGAGGAACTCCGGAGGCATTTGATAACAAAATTAGGGACGCAGCTAGCTTATAGTTCAGCAGCGGACGCGCATACTCGTAGGATTGAAATATTTCCAATCTACCCTACGTATACGAGATAATTACAGGGGGTCCTTGCTTAAATACTATCCTCACAAAATTGCCGAGTAGTATAAGAGACATACCCCAAACGCTACCGCTGAACATTTCCAGCCAGGATGAGAGCTAATCAGCAGGGTAAGTTATAGCATTAGAGGTATTATCATTCACCTAAGGAGCCGCAGTGTTGTGCCATCACTATGCTGCAGTCCTCCGGAGACTAGAGTGAACTAGGCGTTCTAAGAGTTATTATAGGGTCTCGCCAGCCATTTTGCTCTAAGTTCATATAGGAATCAAAATCGGGCATTTTTCGCACGTCTTCTTACGAGTCCAAGGTCTCGTCGGTCGGCTTCCCTAAACCGTGAGCCTACACAGGAGGCATAAAACGTCCTGTCGACAATCTTCGGCATAGCTCACTTCTAAACGGTTACAGGGCTGTTCTGCAAAGTAAGACCCAAGTCCGGGCTGACAGCCCAGCGGGGACCAATCCGCGACCGGCATATAGCGAGATAAACCACATCGATGCGGCGTGTGATCATATAGAGCGCCTGCAGGGGGAACTCTATTCCGTTAGGTATGCCTGTGTACAGCGCTGCGTGAGCGATCTGGTGATCTCCTATTTGATCTTGGCGGACTGGCATAATTTGTTGTGTTCTAACTCTAGGAAGACGCCACTCTCAGCGAATAATCAAGCTATGGGTGCTCATCTCCATAAGCTCGCCCTCTAAATTTCGGGGCACTATTGTCTTCTAAGCTTCGCCTTACACATCTATCGGCGATAATCTAACATTTCGAAGCAAGTTACGGCCGTCCGGTGTGACGCCCTTAATTCGTGGGGAAGGACGCATTAGGGCACAAAGTCGTCCAGACCATTAACCACGGGTTCAGTTTCCCCCACAAGTACATAGCAAATTGTCCGCCCGATCGCAACAAGTACAGGCAGACCACACTGGTTGAGCGTCCGAAGACCATAGACCTTCACTTGACCTGAAATCTCCGGACTGCGGAGTAATCCGAGACAATGACCTATAGAAAGCGGGTCGCAGCTAATGATAACCTCTTAAATGCTCACGCGGGCGGTTTTAACTACACGATATGTCCTACCCTACAAGCGTCGTACAACTAATTACGGGAAATACAGCTTGTTAAGAGGGGAGGAGACAAAGGGCTCTTACTCGACATTGACGTTGCCCCTCGCATAGTACTGTAGAGACGCCACAGAACCTTTTGCACATGATAGGAGTATTCCCGTCGTGCACTACGGTGCTTGGCGAAACAGGGGAGACTTAATTCCTTAAACGGTATGCCAAGACGACATTGTAGCAGATCCACGCCTTCATTCAGATACTCGAAATCACCGTTCATATATCACAGGCTATTTACACAATACCTACGGTCCGCCATAGCACGGAGAATTTAGGTTGAATATGGATGTCACGACACCCCTAGGTCTACGCAGCTTCGTGCCGATGAAGTTTCGTCTTCCTGGCTGGGGGACAAGGGGCAACCTAACCCAGGTGACGATCGGCGGATACTCACCAGGATAGGACGAATACCATGCCTTTTTCTCGTGCCTGGGACTCGGGATGCTGCCATGTACCCGCGTGATGGGAATTGTGGAACGGATTCTTGTTCCCTATCCCAATGCACTGCGATAATGGGTAGTTGGCCTTTTCAAGTTAACTGAGGTTATTTGCCGGTCGACTGGAACATTCGTCCAGACTGACCACGTCCTCCAGTCCGGTGGTTAGGTACATTGGATGATCTGACCGGTCATTCGAGGAATAGCACGTTCACGTCAAGGGGATCGGACGGTCTGCCAACCAGTAGACACGAGATATTCCTCGACAGAGGATCTTAAAGCTCCGGGCCATCGTCCAATGGCAAACGGAGGCGCCATAAGTGTTTCCTTGATTACTAATCTCCCCAGGCTTGGCCCGGACGCCAGTGGGCAACGGTCTAGTCAACCCTACTCCTATATTAGTTATCCATCATCAGGAACAGTCAAAAAATTATTACATACCAGTCTAGTACCTGAACGTCCGACGACAACCGATCTTAGAGAACAATGCGTTGTAGCCAACTATCTGGCTCCTACACCACATAGAGCCGCGAGCGTTGGACCTGCCTACACAGCGGCCCTGTACTTAATTGCGAAACCAGCTGAACGGGTGAGAGCGCGTTTCAAACGTCAAACGCGGAGCGAAGTTCATTCGAATCTCGTATGTATGATAGATTGGTGGTGGAAGGTTCGGTGTGTGTAAGTTCGGTGGCGCCTAAGGACTAAGTCCAGCCAGTACTAGTGGCCCGGACCAACCTTACACGAAAGGGGACTAAGTTAATTTGTTGTACTCCACATGAACTCGTCAACGTATTTCGCAGCCATTGGTGGAGAACGTCGCACTCAGCTGTCACCGTACCCGAAGTTTTGTGGATGAGATAACGTCGTGATACTAGCCTGTGCGAGCATGCACTCGCGGGCAATCCCAATAACCGGAGAGCCGTACTTAGGCATTACACCGTAGACGGAATATAAAAGGGGAGTCGGACTCCGCCTAACAGTTAACATATTCGATGGTGCCTACTAGCGGCATAGCCTGTGTGCATTTTGCCGTAGGACGTCCGTTATTGCATAACATCGTCAACAAAAAATGTGGATTTCCCTCGGCCTAGTCCTGCCAGGATGGGGGATATCGCAACGTAAGTTACACGGTAAAGACCCAAATAAGCTCACTCCCTGGCTAACTAAGCGGATCAGCTCCTGTTATACACAGTGAGCATACTCCTCTCGCATCTGAATAGACAGTTTGATCTGCACTAACTGAGACCCTACCATTCTAATGTCTATTCGGTTGAATGATGTTAGTGTTATTCCCCCCTGCGATGTTATCAGACGGCCGAGTTGTTCGCCCGGACCCTCATGCGCGACACAAATACAACATAGCTCACCGATTTCACGGAACTTTCGTAACCCGGACACCTTAGTTATTGGTGGGCATCCTGGCCCCTCCGGTACGCAACGGTCTGTGCTAGACCCAGCGATCCAAGCTGAATTAAGTGGACCTCCTTCGTTGATCGACCGTGACTACTACGCTTCCAGTGTGTCGATATTTTGTGCGTGGGTGGCTCTGAGATAACCATTCCTCACGCCTGAACGGGGCTCTGACTTGTGACCCATAGCGGGCGTTCTCTGTTGATAAAAGACCAGCCTAAGGTGTTTTGTGTAAGAGAATCATTTCTAACAGGGAGCTGAACACAAGATTACTACGATCCCCGGGTCCTCAGCTTCAGCTGTATTCCGATCGTCACAGTTTTAATCGAGACTCTCGATCCATCATTCACAAGCACAGAGATTTCTAGCGGCATTATCCAGCAACTCTCAAAGGCTTTTCACAGTTTCCGACCTGCAGGCGCAACGATTACAGTTTCCAAAAGTCTGGCATCTTCACGCTTAATGCCCTACTTATGTGACGACCCTGACCGGCTGCAAAGTCGCTAAAGCTGCCTCGGGCCCTCGGACCCGCGCGCCCTGGGCGACGGCCATCACAAGGCACCTAACAATACAACCACTTGTTTCCATCCGATCTAGAGGAGAAGGCCC$'
k = 9
PartialSuffixArrayConstructionProblem(Text, k)
'''

import re

def MultipleApproximatePatternMatching(Text, Patterns, d):
	
	#print Text
	n, np = len(Text), len(Patterns)
	#print n, np
	#lens = {}
	#for p in Patterns:	lens[len(p)] = lens.get(len(p), 0) + 1
	#print lens
	cache = {}
	patternLocs = {}
	for i in range(np):
		#if i % 1000 == 0: print i, len(cache)
		p = Patterns[i]
		m = len(p)
		k = m / (d + 1)
		allmatches = set([])
		for j in range(m - k + 1):
			pj = p[j:j+k][:8]  # only cache first 8 chars
			poss = cache.get(pj, None)
			if poss == None: cache[pj] = poss = [m.start() for m in re.finditer(pj, Text)]
			for pos in poss: allmatches.add(pos - j)
			#pi, index = p[i:i+k], 0
			#while index < n:
				#found = Text[index:].find(pi)
				#if found == -1: break
				#index += found
				#print index, pi, Text[index:]
				#allmatches.add(index - i)
				#index += 1
		#print len(allmatches)
		patternLocs[p] = allmatches
	
	indices = []
	for ip in range(np):
		#if i % 1000 == 0: print i
		p = Patterns[ip]
		m = len(p)
		for i in patternLocs[p]:
			k, mismatch = 0, 0
			for j in range(m):
				mismatch += ((i + k < 0 or i + k >= n) or (p[j] != Text[i + k]))
				if mismatch > d: break
				k += 1
			if mismatch <= d:
				#print p, Text[i:i + m], i, mismatch
				indices += [i]
				
	print ' '.join(map(str, sorted(indices)))
	#print ' '.join(map(str, indices))

'''
#Patterns, Text, d = ["ATT", "GCC", "GCTA", "TATT"], "ACATGCTACTTT", 1
lines = read_file('inpros47.txt')
Text = lines[0]
Patterns = str.split(lines[1])
d = int(lines[2])
MultipleApproximatePatternMatching(Text, Patterns, d)
'''

def hamming(s1, s2):
	return sum([1 for i in range(len(s1)) if s1[i] != s2[i]])

def ApproximatePatternMatchingProblem(Pat, Text, d):
	MultipleApproximatePatternMatching(Text, [Pat], d)

'''
lines = read_file('inpros48.txt')
lines = read_file('rosalind_1hba.txt')
ApproximatePatternMatchingProblem(lines[0], lines[1], int(lines[2]))
'''
	
def edit_distance(s1, s2):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = {}, {}
	for i in range(m): tbl[i,0]=i
	for j in range(n): tbl[0,j]=j
	for i in range(1, m):
		for j in range(1, n):
			cost = 0 if s1[i-1] == s2[j-1] else 1
			tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
			if tbl[i,j] == tbl[i-1, j-1] + cost: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + 1: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + 1: 
				path[i,j] = 'U'
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
	while i > 0:
		s1_, i = s1[i-1] + s1_, i - 1
	while j > 0:
		s2_, j = s2[j-1] + s2_, j - 1
		
	return tbl[m-1,n-1], s1_, s2_

'''
#print(edit_distance("Helloworld", "HalloWorld"))
lines = read_file('inpros34.txt')	
#lines = read_file('rosalind_5g.txt')	
print edit_distance(lines[0], lines[1])
'''

def FindingAllSimilarMotifs(s, t, k):
	
	s1 = s
	m=len(s1)+1
	pos = []
	
	for start in range(len(t)-len(s1)-k+1):
		
		s2 = t[start:start+len(s1)+k]	
		n=len(s2)+1

		#print s1, s2, m, n
		tbl = [[0 for _ in range(n)] for _ in range(m)]
		for i in range(m): tbl[i][0]=i
		for j in range(n): tbl[0][j]=j
		for i in range(1, m):
			for j in range(1, n):
				tbl[i][j] = min(tbl[i-1][j-1]+(s1[i-1]!=s2[j-1]), tbl[i][j-1]+1, tbl[i-1][j]+1)
		
		end = n - 1
		while end >= n - 1 - 2*k:
			i, j = m - 1, end
			#for i in range(len(tbl)):	print ' '.join(map(str, tbl[i]))
			if tbl[i][j] <= k:
				print start, start+end
				pos += [(start, start+end)]
				'''
				s1_, s2_ = '', ''
				while i > 0 and j > 0:
					if tbl[i][j] == tbl[i-1][j-1] + (s1[i-1] != s2[j-1]): #if path[i, j] == 'D':
						s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
						i, j = i - 1, j - 1
					elif tbl[i][j] == tbl[i-1][j] + 1: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
						s1_, s2_ = s1[i-1] + s1_, '-' + s2_
						i = i - 1
					elif tbl[i][j] == tbl[i][j-1] + 1:  #elif path[i, j] == 'L':
						s1_, s2_ = '-' + s1_, s2[j-1] + s2_
						j = j - 1
					else:
						print i, j, tbl[i][j], 'Error'
						break
				while i > 0:
					s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
				while j > 0:
					s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
				pos += [(start+1, start+end, s1_, s2_)]
				'''
				
			end -= 1
	for p in sorted(pos):
		#print p
		print p[0], p[1]
'''		
#lines = read_file('inpros81.txt')
lines = read_file('rosalind_ksim.txt')
k, s, t = int(lines[0]), lines[1], lines[2]
FindingAllSimilarMotifs(s, t, k)
'''

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

'''
lines = read_file('inpros35.txt')	
lines = read_file('rosalind_5h.txt')	
score, s1_, s2_ = FittingAlignment(lines[0], lines[1], 1, -1, -1)
print score
print s1_
print s2_
'''

def OverlapAlignment(s1, s2, match, mismatch, indel):
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
	maxscore, imax, jmax = max([(tbl[i,j], i, j) for i,j in tbl if i == m - 1 or j == n - 1])
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

'''
lines = read_file('inpros36.txt')	
lines = read_file('rosalind_5i.txt')	
score, s1_, s2_ = OverlapAlignment(lines[0], lines[1], 1, -2, -2)
print score
print s1_
print s2_
'''

def GlobalAlignmentProblem(s1, s2, matchmat, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = [[0 for _ in range(n)] for _ in range(m)], {}
	for i in range(m): tbl[i][0]=i*indel
	for j in range(n): tbl[0][j]=j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = matchmat[s1[i-1], s2[j-1]]
			tbl[i][j] = max(tbl[i-1][j-1]+score, tbl[i][j-1]+indel, tbl[i-1][j]+indel)
			'''
			if tbl[i,j] == tbl[i-1, j-1] + score: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + indel: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + indel: 
				path[i,j] = 'U'
			'''
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
		
	return tbl[m-1][n-1], s1_, s2_

'''
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

#lines = read_file('inpros34.txt')	
#lines = read_file('rosalind_5e.txt')	
lines = read_file('rosalind_5l.txt')	
score, s1_, s2_ = GlobalAlignmentProblem(lines[0], lines[1], matchmat, -5)
print score
print s1_
print s2_
'''

from copy import deepcopy
def GlobalAlignmentLinearSpace(s1, s2, matchmat, indel, k):
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
	mid_col1 = GlobalAlignmentLinearSpace(s1, s2, matchmat, indel, middle)
	mid_col2 = GlobalAlignmentLinearSpace(s1[::-1], s2[::-1], matchmat, indel, m - middle - 1)
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

'''
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
#lines = read_file('inpros82.txt')	
lines = read_file('rosalind_5k.txt')	
#GlobalAlignment(lines[0], lines[1], matchmat, -5, len(lines[1]))
#print GlobalAlignment1(lines[0], lines[1], matchmat, -5)
#print MiddleEdgeinLinearSpaceProblem(lines[0], lines[1], matchmat, -5)
'''

def GlobalAlignmentWithAffineGapPenaltyProblem(s1, s2, matchmat, opening, extention):
	m=len(s1)+1
	n=len(s2)+1

	tbl, tbli, tbld = {}, {}, {}
	for i in range(m): tbl[i,0]=tbli[i,0]=tbld[i,0]=i*opening
	for j in range(n): tbl[0,j]=tbli[0,j]=tbld[0,j]=j*opening
	for i in range(1, m):
		for j in range(1, n):
			score = matchmat[s1[i-1], s2[j-1]]
			tbli[i,j] = max(tbl[i-1, j]+opening, tbli[i-1, j]+extention)
			tbld[i,j] = max(tbl[i, j-1]+opening, tbld[i, j-1]+extention) 
			tbl[i,j] = max(tbl[i-1, j-1]+score, tbli[i,j], tbld[i,j])
			'''
			if tbl[i,j] == tbl[i-1, j-1] + score: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + indel: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + indel: 
				path[i,j] = 'U'
			'''
	i, j = m - 1, n - 1
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if tbl[i,j] == tbl[i-1,j-1] + matchmat[s1[i-1], s2[j-1]]: #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i,j] ==  tbli[i,j]: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		else: #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
	while i > 0:
		s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
	while j > 0:
		s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
		
	return tbl[m-1, n-1], s1_, s2_

'''
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

#lines = read_file('inpros59.txt')
#lines = read_file('rosalind_5j.txt')	
lines, junk = get_seq_fasta(read_file('inpros67.txt'))
lines, junk = get_seq_fasta(read_file('rosalind_gaff.txt'))
score, s1_, s2_ = GlobalAlignmentWithAffineGapPenaltyProblem(lines[0], lines[1], matchmat, -11, -1)
print score
print s1_
print s2_
'''

def GlobalAlignmentWithConstantGapPenalty(s1, s2, matchmat, indel):
	return GlobalAlignmentWithAffineGapPenaltyProblem(s1, s2, matchmat, indel, 0)

'''	
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

#sequences, qualities = get_seq_fasta(read_file('inpros46.txt'))	
sequences, qualities = get_seq_fasta(read_file('rosalind_gcon.txt'))	
#print sequences
score, s1_, s2_ = GlobalAlignmentWithConstantGapPenalty(sequences[0], sequences[1], matchmat, -5)
print score
#print s1_
#print s2_
'''

def CountingOptimalAlignments(s1, s2):
	m=len(s1)+1
	n=len(s2)+1

	tbl, opt = {}, {}
	for i in range(m): tbl[i,0], opt[i,0] = i,1
	for j in range(n): tbl[0,j], opt[0,j] = j,1
	for i in range(1, m):
		for j in range(1, n):
			score = 0 if s1[i-1] == s2[j-1] else 1
			tbl[i,j] = min(tbl[i-1, j-1]+score, tbl[i, j-1]+1, tbl[i-1, j]+1)
			opt[i,j] = (tbl[i,j] == tbl[i-1, j-1]+score)*opt[i-1,j-1] + (tbl[i,j] == tbl[i, j-1]+1)*opt[i,j-1] + (tbl[i,j] == tbl[i-1, j]+1)*opt[i-1,j]
	print opt[m-1, n-1] % 134217727

'''	
#sequences, qualities = get_seq_fasta(read_file('inpros72.txt'))	
sequences, qualities = get_seq_fasta(read_file('rosalind_ctea.txt'))	
CountingOptimalAlignments(sequences[0], sequences[1])
'''
	
def LocalAlignmentProblem(s1, s2, matchmat, indel):
	m=len(s1)+1
	n=len(s2)+1

	tbl, path = {}, {}
	for i in range(m): tbl[i,0]=i*indel #0 #i*indel
	for j in range(n): tbl[0,j]=j*indel #0 #j*indel
	for i in range(1, m):
		for j in range(1, n):
			score = matchmat[s1[i-1], s2[j-1]]
			tbl[i,j] = max(0, tbl[i-1, j-1]+score, tbl[i, j-1]+indel, tbl[i-1, j]+indel)
			'''
			if tbl[i,j] == tbl[i-1, j-1] + score: 
				path[i,j] = 'D'
			elif tbl[i,j] == tbl[i, j-1] + indel: 
				path[i,j] = 'L'
			elif tbl[i,j] == tbl[i-1, j] + indel: 
				path[i,j] = 'U'
			'''
	maxscore, imax, jmax = max([(tbl[i,j], i, j) for i,j in tbl])
	i, j = imax, jmax
	s1_, s2_ = '', ''
	while i > 0 and j > 0:
		if tbl[i, j] == 0:
			break
		elif tbl[i,j] == tbl[i-1,j-1] + matchmat[s1[i-1], s2[j-1]]: #if path[i, j] == 'D':
			s1_, s2_ = s1[i-1] + s1_, s2[j-1] + s2_ 
			i, j = i - 1, j - 1
		elif tbl[i,j] == tbl[i-1,j] + indel: #tbl[i-1, j] > tbl[i, j-1]: #path[i, j] == 'U':
			s1_, s2_ = s1[i-1] + s1_, '-' + s2_
			i = i - 1
		elif tbl[i,j] == tbl[i,j-1] + indel:
		#else: #elif path[i, j] == 'L':
			s1_, s2_ = '-' + s1_, s2[j-1] + s2_
			j = j - 1
		else:
			print 'Error'
	#while i > 0:
	#	s1_, i, s2_, j = s1[i-1] + s1_, i - 1, '-' + s2_, j - 1
	#while j > 0:
	#	s1_, i, s2_, j = '-' + s1_, i - 1, s2[j-1] + s2_, j - 1
		
	return maxscore, s1_, s2_

'''	
lines = read_file('PAM250.txt')
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

lines = read_file('inpros44.txt')	
lines = read_file('rosalind_5f.txt')	
#lines = ['TCCCAGTTATGTCAGGGGACACGAGCATGCAGAGAC', 'AATTGCCGCCGTCGTTTTCAGCAGTTATGTCAGATC']
score, s1_, s2_ = LocalAlignmentProblem(lines[0], lines[1], matchmat, -5)
print score
print s1_
print s2_
'''

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

'''
#sequences, qualities = get_seq_fasta(read_file('inpros57.txt'))	
sequences, qualities = get_seq_fasta(read_file('rosalind_smgb.txt'))	
#print sequences
score, s1_, s2_ = SemiglobalAlignment(sequences[0], sequences[1], 1, -1, -1)
print score
print s1_
print s2_
'''

def OverlapAlignment (s1, s2, match, mismatch, indel):
	
	m=len(s1)+1
	n=len(s2)+1

	#tbl, path = {}, {}
	tbl = [[0 for _ in range(n)] for _ in range(m)]
	#prev_row, cur_row, last_col = [0]*n, [0]*n, [0]*m
	#for i in range(m): tbl[i,0]=0 #i*indel
	for j in range(n): tbl[0][j]=j*indel #0
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

'''
#sequences, qualities = get_seq_fasta(read_file('inpros58.txt'))	
sequences, qualities = get_seq_fasta(read_file('rosalind_oap.txt'))	
#print sequences
score, s1_, s2_ = OverlapAlignment(sequences[0], sequences[1], 1, -2, -2)
print score
print s1_
print s2_
'''

def TrieConstructionProblem(patterns):
	root, id = 0, 0
	trie = {}
	for pat in patterns:
		node = root
		for ch in pat:
			next = trie.get((node, ch), None)
			if not next:
				id += 1
				trie[node, ch] = id
				next = id
			#print node, ch, next
			node = next
	#for node, ch in sorted(trie):
		#print str(node) + '->' + str(trie[node, ch]) + ':' + ch
		
	return trie

'''
lines = read_file('inpros51.txt')
lines = read_file('rosalind_7a.txt')
TrieConstructionProblem(lines)
'''

def MultiplePatternMatchingProblem(text, patterns):
	trie, root = TrieConstructionProblem(patterns), 0
	nonleaves = [node for (node, ch) in trie]
	leaves = set([trie[node, ch] for (node, ch) in trie]) - set(nonleaves)
	indices = []
	#count = {}
	for i in range(len(text)):
		node = root
		#string = ''
		for ch in text[i:]:
			next = trie.get((node, ch), None)
			if not next:
				break
			#print node, ch, next
			#string += ch
			node = next
			if node in leaves:
				indices += [i]
				#count[string] = count.get(string, 0) + 1
				break
	#print count
	print ' '.join(map(str, indices))

'''
lines = read_file('inpros52.txt')
lines = read_file('rosalind_7n.txt')
MultiplePatternMatchingProblem(lines[0], lines[1:])
'''
import re
def SharedKmersProblem(k, str1, str2):
	m, n = len(str1), len(str2)
	kmers = set([str1[i:i+k] for i in range(m - k + 1)]).intersection(set([str2[i:i+k] for i in range(n - k + 1)]))
	#print kmers #, str1, str2
	#MultiplePatternMatchingProblem(str1, kmers)
	#MultiplePatternMatchingProblem(str2, kmers)
	i, j = 0, 0
	pos1, pos2 = {}, {}
	rkmers = {kmer:ReverseComplementProblem(kmer) for kmer in kmers}
	while i <= m - k or j <= n - k:
		for kmer in kmers:
			if str1[i:i+k] == kmer or str1[i:i+k] == rkmers[kmer]:
				pos1[kmer] = pos1.get(kmer, []) + [i]
			if str2[j:j+k] == kmer or str2[j:j+k] == rkmers[kmer]:
				pos2[kmer] = pos2.get(kmer, []) + [i]
		i, j = i + 1, j + 1
	print pos1
	print pos2
	pospairs = []
	for kmer in kmers:
		for p1 in pos1[kmer]:
			for p2 in pos2[kmer]:
				pospairs += [(p1, p2)]
	for p in sorted(pospairs):
		print p

'''		
lines = read_file('inp31.txt')
lines = read_file('rosalind_6d.txt')
k = int(lines[0])
SharedKmersProblem(k, lines[1], lines[2])
'''

def LongestRepeat1(text):
	MultiplePatternMatchingProblem(text, [text[i:] for i in range(len(text))])
	
def LongestRepeat(text):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	max_repeated_text = ''
	for suffix in suffixes:
		node, done = root, False
		repeated_text = ''
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						id += 1
						del tree[node][string]
						repeated_text += cp
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
						repeated_text += cp
					elif lcp == lstr and lcp == lsuffix:
						done = True
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		#print suffix, tree
		if len(max_repeated_text) < len(repeated_text):
			max_repeated_text = repeated_text
	
	#print tree
	#texts = sum([x.keys() for x in tree.values()], [])
	#for x in texts:
	#	print x
	print max_repeated_text

#LongestRepeat("ATATCGTTTTATCGTT$")
#LongestRepeat1("ATATCGTTTTATCGTT$")
#LongestRepeat("TCATAGGCGACTGACCTTGTATTTGATGATAGCGCGGCTCGAAAGCAACTAGTAGCTAAGCCCAGCGTGGGGTAACAACGTGGAGGAAATTCCTCACCGATTCGAGGGTGGAATACCGACCAATGTCATCGTCCTGGACCGCGGCCTTGACTGGCCTCTTCTCGAACCAGAAGGCCACGCGAACTATTACCTAGGAATTGAGCGCAACGTTGACTGCAATATGTTGATGTCGCGAACACGTTGTGCTGCACAAGGTCTGTAAGGATCAGAAAGGATGAGTGGTCAGTCCTTGGTTAGACTCACCTAGCCTATCCATACAGCTGCAGGTTGCTAAGTAAGAGACCTTCCGATCCGTGCGACCTTTTCGCTGACAATCCCTGACAACGCAACGGGACATCTATGTGTCGTGTAGCAATACGTAGTTTGGAAGGCGACTACCTACCAGATCAGAGATGATTGCGCGGGGGTTCAGCCGAGTTACGCTGTAGAATGCTCTCGACCAATACCAATTAATAGCGGTCGGATAAATTTGAACTCCAACCTTGTCCGGGCTAACAAGGATGGATGGATCGTACAAGGTGAATATTCACGGGTAGTTAAATTTGAACTCCAACCTTGTCCGGGCTAACAAGGATGGATGGATCGTACAAGGTGAATATTCACGGGTAGTAAAATGAAAATGTGCAAGTTGACAGCGTTTCACGATACAAGGCGTAATAGACCCTTGTCCCAGATAGATCTTTCTAAACCCTGAGTGGAGTGGTTCTAATTTTGTACGACAACCTTCGGGGGTGCTAGGCACGGTGCCACCGCCGTCTTGGTTCGCCATAGTAACGGTGGGCGTGCAGGGATATACCGGTGAGCGACCTCTCGGTGAAGCGCAACGGCTGCATAGATCACCCGTGTAACTTCCTTCCACCACAGTCCAAGCTGTTTGCTAAATTTGAACTCCAACCTTGTCCGGGCTAACAAGGATGGATGGATCGTACAAGGTGAATATTCACGGGTAGTAAAATGGCAGTAAGCCCGTTCGAGGACTCATGGATGCTTAACATGTCAACAATTTTCTGTCCAGGCTGTAGGGCAGGGTGACGATAGAGGTCGTTTAGACCCTGTCTTGCGCCACTCAGACATCGAGTGTAGCTATCTCTAAGACCAACCGCCCGTTCCAACTGTGAGCAGCGAAGTGGGACGACTATCGTCAGGTATGGCATATAAGGGGGGCTATGCTACTTCA$")
	
def SuffixTreeConstruction1(text): # correct version
	n = len(text)
	tree = {0:{}}
	root = id = 0
	for i in range(n - 1, -1, -1):
		suffix = (i, n - 1) #text[i:]
		node, done = root, False
		while not done:
			if node in tree:
				lcp = 0
				for string in tree[node]:
					isuffix, jsuffix = suffix[0], suffix[1]
					istring, jstring = string[0], string[1]
					cp = os.path.commonprefix([text[isuffix:jsuffix+ 1], text[istring:jstring + 1]])
					lcp, lsuffix, lstr = len(cp), jsuffix - isuffix + 1, jstring - istring + 1
					if lcp > 0:
						remsuff, remstr = (isuffix + lcp, jsuffix), (istring + lcp, jstring)
						if lcp < lstr:
							oid = tree[node][string]
							id += 1
							tree[node][(isuffix, isuffix + lcp - 1)] = id
							tree[id] = {remsuff:id + 1, remstr:oid}
							id += 1
							del tree[node][string]
							done = True
						elif lcp == lstr and lcp < lsuffix:
							node, suffix = tree[node][string], remsuff
						elif lcp == lstr and lcp == lsuffix:
							done = True
						break
				if lcp == 0:
					id += 1
					tree[node][suffix] = id
					done = True
			else:
				id += 1
				tree[node] = {suffix: id}
				done = True
		#print suffix, tree
	return tree	

def SuffixTreeConstruction(text):
	suffixes = []
	for i in range(len(text)):
		suffixes.append(text[i:])
	#print suffixes
	tree = {0:{}}
	root = id = 0
	for suffix in suffixes:
		node, done = root, False
		while not done:
			lcp = 0
			for string in tree[node]:
				cp = os.path.commonprefix([suffix, string])
				lcp, lsuffix, lstr = len(cp), len(suffix), len(string)
				if lcp > 0:
					remsuff, remstr = suffix[lcp:], string[lcp:]
					if lcp < lstr:
						oid = tree[node][string]
						id += 1
						tree[node][cp] = id
						tree[id] = {remsuff:id + 1, remstr:oid}
						id += 1
						del tree[node][string]
						done = True
					elif lcp == lstr and lcp < lsuffix:
						node, suffix = tree[node][string], remsuff
					elif lcp == lstr and lcp == lsuffix:
						done = True
					break
			if lcp == 0:
				id += 1
				tree[node][suffix] = id
				done = True
		#print suffix, tree
	#print tree
	texts = sum([x.keys() for x in tree.values()], [])
	for x in texts:
		print x
		
#SuffixTreeConstruction('GGATAGAACCAGTCAAGAGAACACGTATTATCTGGAAGCGACCGCTAACGTCGGTGGCGGCCTACGCTAGAAACTTAACGGCTGATCTACCCCTAGAGGCAAGGTGACGTATGGTAGCGTCTCGATCACTCGCTTACCCCAACAGGGAACCATGTGCTAACAATCCAGAATATATCCTCGTCATTGTCCCATAAGGTTTCTTCGGTACTATAAACCGGGGCCGCTTCACACACCTAAGGCGATTCACAGTGTCCGCGGTACGCTCACATGTGCCGGAGATCCCGTGCGTGGGGGCGCCATATCGAACGGAATTGCGACGTGCGTCATCCTGTCCTGGCTGAGCATTCCCCGAGGTAGCGTACGAATCTTACAGACAAGGTCAAATCGTGGACGGGTACCTTGAGAAGCCCGAAAAATACGACAACAGGTAATGCATTGTCGAAGTAAAAGACAACAACAAGAGTACCTTGATGGAATACAAGTTCCAACGACATTCCGGCGTATCCCGTGTAGTAATTAACCCACTCTGCGACGACATGCCCCATCTCCTTATTCGTGCCTAATGGTAGCAATCTGAAGACCGCTCCCTATGACTCAGTTTCACGGTGGTAGTATCTTGGCATCGCCTGGTCCACCTTTTTACAATTACGTGTTGTCGCCTCTCTGCCATTTGATGTAACGAACTCCGAGACCGTGATCACGGAGGGTAGAATGGAAAACAATCTATTCACCACAGCATGTTTGTCGCGGGTAGTTACATGGTCAGCCTTAGGGTTTAAACAATGGTGCTGAGTCTGTATGGGGACCGAGAATTTACCGAAACGTCGACACAATACCAGCCATGAAAGGGAGAGGAGAGGATGAAGCGCGGTTGCCGGCTAACCCAGAAATCGCAACAGACTCACC$')

def GetAllSubstrings(tree, node, lprefix, substrings):
	if node in tree:
		for (istr, nnode) in tree[node].iteritems():
			lstr = istr[1] - istr[0] + 1
			for i in range(lstr):
				lnstr = lprefix + i + 1
				substrings[lnstr] = substrings.get(lnstr, 0) + 1
			GetAllSubstrings(tree, nnode, lprefix + lstr, substrings)	
		
import math

def GettingRepetitive(s):
	
	n = len(s)
	print n
	pow4, log4n = [1], int(math.log(n) / math.log(4)) + 1
	for k in range(1, log4n + 1): pow4.append(4 * pow4[k - 1])
	tree = SuffixTreeConstruction(s)
	#print tree
	print 'done suffix'
	sub_k_ss = {}
	GetAllSubstrings(tree, 0, 0, sub_k_ss)
	#print sub_k_ss
	print 'done kmers'

	#kmers, sub_k_ss = set([s]), {n:1}
	#for k in range(n-1, 0, -1):
		#k_1_mers = set([])
		#for subs in kmers:
			#k_1_mers.add(subs[1:])
			#k_1_mers.add(subs[:-1])
		#kmers = k_1_mers
		#sub_k_ss[k] = len(kmers)
		#print k, kmers, sub_k_ss[k]
		#if k % 1000 == 0: print k, sub_k_ss[k]
		
	m_a_n, sub_s = 0, 0
	for k in range(1, n + 1):
		#sub_k_s = len(set([s[i:i+k] for i in range(n - k + 1)]))
		sub_k_s = sub_k_ss[k]
		m_a_k_n = n - k + 1 if k > log4n else min(n - k + 1, pow4[k])
		if k % 1000 == 0: print k, sub_k_s, m_a_k_n
		m_a_n += m_a_k_n
		sub_s += sub_k_s
	lc_s = (1.0 * sub_s) / m_a_n	
	print sub_s, m_a_n, lc_s

def GetAllSubstrings1(tree, node, prefix, substrings):
	if node in tree:
		for str in tree[node].iteritems():
			for i in range(len(str)):
				nstr = prefix + str[:i+1]
				lnstr = len(nstr) 
				#print nstr, lnstr
				substrings[lnstr] = substrings.get(lnstr, 0) + 1
			GetAllSubstrings(tree, nnode, prefix + str, substrings)	
			
'''
s = "ATTTGGATT"
#s = "CATACATAC"
s = "GTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATTAATTTGTCGTATTAGATTTCGCTTTTGAAAGACCCGATGCTGAGTACAGTTCGTGCCTTACACAACCGTGGCAGTCCTGTGGGAACGAAGTCCACGCCCATTACGTCATAGGATCATGAATTAGACCACCTGCAAGCGCCTTCCTAACGTTTCAATATCGATATCCTCTTAGGCCTGTGACACTACGTCTCAGCACGGATTTATTACGATATAAATCTTAGATTGGCTGGCCCAGTCCAAATCGAGTTCGGACATATCGTAGGTACGGTTCACACCTCATGCGAACACGGCTACATGCGCACCTTGTCGATAACTTTTTCATTACGAAGCGGGAGGAGGCTAATAAGGGTATACGTTTACCTTTTAGAAGGGAACAAAGGCCGCATATGGTTACAAAGGATATTCAGTAGGTATCAGGTTCAACAGATTCGTATCTTCCCGCCGTCCCGAAAAGCGTTCTTAGAGAGTGCATTGCTGAGCGACACATTGAAAACTCCTTCAGTGCGTCACTTCGGTGATGCAAATGTCTACACAATCAGGAGCGCAGTAGCTACTCACTTTAGGTCGACCTCTGGTGCGAGTGTGATGGACCTTATCATGATTTACCGACCACCCGTCCATTAGTCGGGTACCGATACCGGGTCAAACACGCCTGCGGAAATTCCTTCACTTACATTGAGGCAGTTAGATCGGGTATGTGATCGGCCTTCGATCAAGACTGGGGTGAAGTTTGCCCAGTCGAAGCGTCGCTCACGGTCCAAACCTGTCAGCCATATTTCGGGTGTGGCCCCTTTCACTTCAACTCTTAACATACTTCCTTTAGAGCCTGCCGTGTGACAGGATCATCCTGCGCTGCCGCAAGATTTGCTTTCCTACTGGACGATTGGTTTCCCTTGATGACTAATATTTACCCGTCTAACCTTCGAAGGTTTGCCTTCCAGTCATCGCCCACTCGATTACGGATGTTGGGTAGTCCATTGACACTTGTTTATGTACATTGGAAGTCCGGGACTACCCCTGGTATGGTCGGAAGCGACTACACGGATTTATTCACGGACTCGGCAAACGTTCACAGCCGCATGTTTAGTCATGGATTTTCGACAGTTGACGATAAGACATCGGAGGATAAGGAAGTGCGTTATGTCTTATGTCCCCGTCCGATGGACTGGACGAAGTATAACTGATAACGTTACTTTCTCCCAACAACTACTAGAAAACTTGTTTAGTCCGGGTGCGCACCTACACGCTGTAAGATCTTACATTTCCGTATAGGACGACTATCTACCGGGGTCTATGACACGCGACCAGGGGCCGCTTGGCAGCAGTGACTGCGCTTAAAGTCTAACCTGATGCGCGAGGGCGGGGAATCCAAGGTGCGACCACGAGACTCGCCCGTTGACCGGCTAATATTTAACCGGTTTATTAATGCCCGACCGTCATGTATACAAGCTAAATAAGGGGCCGGAGAAATGTCGTGGCCCTGCAGAAACCTCTAAAGCCGAGCTGATAGTTAGGTTGTGAATTTATTTATCTTTTATGGTCACTAGATCCACATTCTATATATAGAGCAGCACCGACATTAGCCAGTAGTTATACATGATGAACTCGGGCGTATTCGATGCATGGAATGAACCTTGCGCCAGCTCCTAAGAACGACTTCCGTCAGGCCTTAGCGAGGTGCCACAGGGGTGGGGGAGAATAATTTACATTGAAAAGGCTTAGGACATTCTGCTTCAACCCCGGGTTTTGTCTAGATTACACGCTGGTGTGAGGAGCTACCTGGCAACCAAGGTCTGTCAATTAATTTACGTGCACGATCTAGCAAGCGGTGTACAAGGGCTGTATGTCATGATACGATTTAAAGTTACGCTCGTTAAAGCGGGCTGTCTGCGGCCTGATAAAGATAATAGTTCAGAAGCCCTATGAAATAACAGAAATCGATCCTATTAGTGGGTGAGAAGGGACTAAGGCGTAAGGGCGTCCCCGGGACCTACATCTTTTTGAGCAGATAATATCCTTATACGCGTTCTTCTTTGACCGGGATACAGCGAGGTAAGTCCGCACGTAAGACTGCGGCAGGTCTATAAGGTGTAGGGAAACAGGCCTTGCCCACTAATTGATGTTGAGACAGCCACGTAGGGTGCGGCCTTTGGCTTCAGCGGACAAGAGGATGATGAGGCATCGCTCTAGGCACAGCATGTCTACAGCGAGATACACAACGACATCATGTAGAGGCAAAGATCCACCTAGCACGGGACGTTTGTCTGCCAGATAAGCGTCTTGCTGCCGTTCACAATACTCGTAGATCGCCTTTGTCGAATGGCAATTCCACCCACACCCTTGCATCTTCACGCTAATCAATTTCCCTATCCGGAGATACCGTTTTCTGTGACGATAGCGCCTTGAAAGAATCCTACAGCTAGCTATTCCCAGCAGGTCATGATATTACAAACTTCGCGGCCATCCGTACGGCACAAACTCTAACCTGGTGTTTGACAGTCGGTGATGTTTTGAGACATACTTGACATCTATCCATATTTACTATCTCGCCTGTCCAAATGGTGAACAAGGCATAGATCTTCAACGCTCGGGTGGAGCTTCTTTATATGGCACTGGGTGCAAGAGCGTGTTAAGTGCTCTAGAAGAACGCTGATAATCCACCTCTCCTGAGTTACTTCCCCTAACTTGCATCTTATACAAAGCGATCCTATACGGAACTATCGGCGCGAGTCGTCAAATCGCCCATTGTCGGATATGTGCACAGAACAGGAGCCTCTCCTTAATTTAAATGTTCGTCCATATGAGCGTATACGAGTACTAACAGGTACAATCACAAGTTAAACGTCCCACCGTCGGCTTGTCATTGGGCGGCATTACAGCAAAAAACTCGTACATAGTCTTCGTAAGGGTTCATTGTCCAGCTATGGCCGTAAGCTAATCGCGGTTCCGTTAATCGTATCGGGATGTCCTGACAGAATTTAGCGTTTCTATTGCGTGGCGGCAATGGCCCCGGAGCAAAACTTGCTTGGGTCTCGTGGTTTTCAGTGATCTATGAGAGTAAAGTACGAGACGCGCACAACATTACCCAGCGGAGTCAAGCATCAGAGTGACTGACCAAATTCAGGAGATGACTAGCACATCGGACGCTGGTATTTTGGGATGTTTTAGGTCACGCACGTTCGAGCGACCACATAGTCTTGACAATAAGCTAACGGAACGGGGAAATCATTCATAGATGATGTGGTTATGCGTGTGGCATCTGGCTGATCCAATCCGGCCTTTCGAGCTTTGCACGTACCTGAGAGCAATAAACTTAGAGACTCGGTTGAACCAAATGACATGCCAGGTTAATATTAACACGTCTTTATGTAATCCTACTATCCACGGATAGGGTGATTAATGCGGCACACTCCGATATCGCTTTGAGTCTATTGCATCCGTAATAAAAGCTCTCAGCGTGTCATTAGTAGATTGAACTGCTCGGAGCCGACCGGTGAGGGCATTTACCGACGTGTGCATTGCTGGCATTTCCCAAAAAGGAAGCGCACGCAAAGGCCTTTTTCCGTAATGGCATCCTATGGAGGACGTATTACTGGGCTGGCTGCTTTTAGAAGTCGATGCGGTCGCATGACCAGTGACACTGATGCCAGTCCCGGTGGGCTGGGCTCCTAAGTGCGCGTTAAACTTGCGCCCTGGATATGACACCGTAGCCGCACATGAGATTGGTTTATACTGGATACTATAGACGCCCACCTGAGCTGGAGCCCTCTCCCACCACGTAGATCCCAATGAAAGGTAGTGTCAGACGCCATGGCCCATGTATTCATTCAGAGGTCCCAGGGCTTGATACTATTAGCAACGACGTCGAAAGTAAAGCACAGTTATCATATCAGTTTGAAAGCGGCAAATCGTCTCTACCCAGCGCTCTTTTTGCCAACGAAGTTCGGTAGTTGTAAAGCGGAGAGTCAATCTTATGCCGCCCACAGCCATATTCTGCGCGGTCGCATAAGGTTAACTGCTATGTCATTTTTAACGTACTCTGGGTTGAAGTGATCCGGCCCTTGTAGGTGCTTGTAATAAAATGTGATAAGCGACTACTGTTGCGAGACAAATCGGGGAGTCGTTCAGCACCGCCATCTGGCTAGCTAATCGCGAAACCATTCCCGCTGGGACGAATCCCGGGCTGGTAAAGCCTCCCTCGCGGGAGCACATGGTACAAGAAGGGTATGTGTATGTGGCGTCCCCAGTGTGGATGTAATTTGAGCATTGTCCAATGAAAGTAGCTGGTTCCCGGTTAAGGCAGTGGGCCCCTGAAAGTGGGTAGACCCTTCTGCACCGAGTAGATGATATTTGAATAAACGTCGATTGAGGTGATTTTGGGGGCACTTATCTCAACAGAATAACTTAGACCTCGCATTTCATCAGCCTTATGACGGTTACTTCAGTGCCAACATGTTTAGAAGCCTTGCGCGATGGTGGCTCGAGCAAATTCTTGGATGAACGGTGTCAGGCTCCCCAAAAGCGTGACGGCGTCCACTGACTCGCTTCTGTTTTACAAGACCCCACTGGTAGACAAGTTGGTCGCGGTCACGACAAATAGTTAGAAAAGGTCTGCTCGTAACAATACTCCCGATTTCACGAGTATCACGTCGGCCTCTATTATCCTTAACTGGGGACCCAAGCCAATCGGAATCCGGCTTTGCGCATTAGTACACCGTGTTCATAGATACTAGGCCAGCATGGGGAAGTGGCTCTCATTTTGGACGCTCTTCCAGTTCCCCTAGTCCGAATTGAAGGAAGGGTTCTTCATACCCGTGTAAGCGCAGGTCCTGCCGATCGGCACTGAGTTCATCGTCCAACCGTGCTGCTATATTAGGCATGCACTCGCCAGGCTTGGTACGAGTGCACTCATACCAGCCCCCCCCTGACCGAGAATCACCGCTAATTTACGATGTTACACTCAAACCCCCATTGCTCTGCCCTTTGCTGATACCAGCAGGTTGATGTCCCATCTAGACAAGATGACTCAAATAGCGCCAAACTAACGGAGGCAGTAAATTCGCAACGTATTGCGTTTATTATAAACCGAACGAGTGAGAGGACGAGCTACCTTAATAGACTTCGCCGCCAGGCACTCTAGCCGCTCCATACCTCCTGCTCCCTAAGACACCGGTAGCCCGGTTTATGAAAGGGAAACCCGTTTGTATCTATTGCGCCCGTGTTGCCCCGCCTCAGGTCTTTTAGCCAGGTTGGTTACCCACAGGAGCTACGTTATCAATTAGTCTCGGCGAGCCCTGATACTTGCGAGAAGACGGACCAATAGGGTTTCATTGCGGCTCCATTACCTACGTGTTGCTTTAGGCCCCTCAATATTAACGTTTCCGTCGTGACGTACGATGTAAGCAGCTGATACTCTACAACCCGTCTCGCATAGGAGCTGTCTGCCGCCGCAAGACTTTACCTAGAAATGCAATACGTCCACTCTATAACATCATCGGGCGTCAAAAGGGGTACACTATCAAATGCCGCTGTCTGAAAGGTAAGAACCGCATCAATTCCGGGGCTGAAATACGGTGTGCATGGCATGGAGGCGCAACTACTTTGAGACAGGCTTTGTCGGGTGGATGCTTTGGAGCATGCATCCCGTCTAGTGGCGTGAGACCCAAGCGACGGCGTTATTAAGTGGGTTATTAAACCAAATAAAAAAGTGGAACGACTTGTTGCTTCTATATCTATGCTTTGAGAATGCCACATTTGGTAGGTAGAAGCTTGCATCATATTGATCACATCAGGGAGTCACACTAGACCGATACTTCAACCACTGTAATCTCTAGGTGCGCCGAACGAGGCAATCGTAGTATATTGGTGAGGCTTAGGTTGAAAGTTCACGTCATGGCCGGGTTAACTAGCTTATACTAATCCTTCTCTAGGATCGTTCCCTGTCAGCGGTCCACTCTTGCGCGAAGCTGGTAATTTATTGGCAAGCGGACACCGATGAACGGATAGGTCAGGAGCCATTCATAAAAGGGATGTCATACCGATACGTGTGTGTCTAACAAGTTTGAGAACGAGGTGTCAGTATCTCTTGTGTGCAAGCCGTAGCTCTGATCTGCATACCCTTAACGGAACGGCAGAGGATTACTTTATGTCTTCACTCATGTCTTGCGGGTCACGAGTTCTCAGCACTCTTAAGAAAAGGAAAATCTCCAGCCAAACGGAATCTTTGCCCGGGCTGTTCGGAAGCCGCTAGGAGTTATCAGTCTTATTGTTTCATTGCACCGCACTCGCCTCTTACTTAGCACAAACATGGCGTACTCGGAGCTACGCTGGACTCACAGTCTTTCTTGTTTTCGAGGGAAGCTCAGTGAAGTAGTTGTGGGCGACAGCGTTTGTGAGGATCGTTGGTGATTTGGACCTATCCCCTCCGAGCTCGCAAGCTGTACTCGATCGCCGCATCTACAGCGCACTCGAGCATTCAGCCCTCAAGTCCGTAGTGAGCGATATGCACCCAGATCTTAAAAGGACAGAGATACGTAGTTTTGACGTGTATACCATGCCGTGGCGAAATGGAAGCCCCGATTCGAATTCCTGGTAGAGAAGGCCGGAGGTCTATGCAACATACCCTACCCCGACACCCAGTACCCTGAGCCGATTGTGTTGTTTTGAAATTAGCTAATACCGTCCATAGGTTCTGACCAAATCAGGCGTTGTTTGTGGTTAGTTTAGTAACCCAATACGGGGCCCCTCTAATACGCAGCTACGCTATTCAAGACAGCATGGGGTTCTCACACAACTTATACGAGTGTAACGGTCCGCCGAGATGGAGGCTTTCAAATGGGTTGCAATATACAGCAGATAGGGGCGCCGAGCGTGGATAGTAGCTTAGTTCCACCGTGGCTTAAAGTGCATTATTTGCGGTTTGAAGCAACTGGTCTATGTTAAACCGTCAGTTTCCGTGAATGTTAGAGGTATAACGTGAGCGGACTGCCATAAGGTCATGTACAGTCTAATAGTGGTAATCCGTGGTCGCGAGAGCATAGAAAAATATGCTGTAATCGTCCAATGTCGTGACTACAAGGGCTTCGCTTTGGCTAATTTCTAAGCGACCCGGTGGGTCAGCCAGATTAAGTAGAGACGAGTTCACCGGCGCGTTATTGCGGTCTCAGACTTTATGGTAAACGAGGAGAGACAACTGAATACAGGGAAATCGCACGTAATGGATTATGTTACATTTTTATGAGTACAGCATCGTACGGATCATTCAAGCAGAGCGACTAGTATGTAGGGTGCATGCCGAGGTTTCGGTTGGGGTTAGCCGCTCGTTGCGCTACTCCTCGGAAGTTTAGATTATACTAACAAATTCTACACGGCATTCAACCAACATTTCCTCCTTAACCCGCTCCCGTCGGCAGGGGCGGACCAAGTCATCAGCTATTCCGTGATAGATAGATACTGGTAGTTCTTGTCGGGTCGACCCACTGACTCGATGGCAGCTGATGGGTATCTCTACATTTAAAGCATACCTTGGGACTTGCATTGGAATGAACGGTGTCGGTTCCTGAGGGGCCGTGCGCGTAGAGTAGGGACCGGACATCTTAGGGAGCTGTACATCAGCGTGGAGGGCTAACTCCAGGGGAACGAAACTCCCCATATTTTCGTTTCCAGATGCCCCGTTGCAACGGCTTCCACACATATGAAGACAGAACATTTACACCGGGTACCCGCTCTCGACGTCCTATCTTCGGCGAGAGGAAGGCCCTCACAGTGGATTGTCGAATTCGGGGCGTCGAGTTAAGTCAGCTTGAAGACACATTGGTCTCCAGGTACCCTGGAAGGTTCCCTCAGGCGGGTGACGTTTCTATATCTACTAAAGCCCAAAAGAGTACCGAACCACACCTTGCGGCTAGCAACGTCCACCTGTGGCCTCACTCTGATAAATTTATTGAGAGGACCATCCGTAAAGACTGTGAAGGGTCATAGGTCCGCTGGCACAGCGTAGTGACATCAGGGTCTGATAACCCACGGAACGAGAGTCCCCCCCGTACTCTGGACTATGGGAACGCATACTTCGTGACAATACATATCGTGCCAAGCTTAGCATCGTCCTCTAAACGAACCCAAACGGTGAGAAACCCATTTATGCCAGCACAAAAGGAAGCGGTGGCATTGAATCTTAACGGATCACATATACTAACCCACTTGCGAGGATGCCCCTAGGGGCAACCGCATAGTTTCCCATGAAAACATTGGTGCGCCGTTGCAGAGGAGCTCATTCGGTAGTACATAAGGCGTAGGGCCTTTGACGTTTCTAACATTTAAGATTCCTTTGAGACCATGACACTCTCATTATTGAGCGCTGTGCGTATTATTCCCCTTGATATATATCACGTTTCAGCCGGTGAATAAAACGATAAGCGGATCAACACAGGGTCGTTACAACGCCTGAGGTTGCTAGGAGGGGAGGCCAGAGCCCTGATATACTTGAGCTCGAAATGTGAACGTTAAGGGCTATCAGTCCGTAAGAACGTTTCTCTGAGAAACGTCCAGATCTACTACCGCTAATATTACTGCACTGCCGGATGATCAGACGCGCAGTTGGTTTGTAGTGTCTCAGTATCGCCAGTCTAGCGACGTGGGCCCCGCGATAGCGTCTTCCATTGTAAACAAATTCCATTACGCCTCACGTCGTCGCGCCAAACAGCGGCTCGAAATGTGACCGGAGTCGAGATATGGAAAGGTTAGTCTTACGAAGGCATGAACAAATACGCTTGCCGAGGTCCGATGATTAAATATGTCGCAAGACCATCTAGAGCAAACGCAACGTGGTCTCCCTTATCATAGACATGCTCTTACCGACATTCGTGGCGAACCCCGCTTCGCAAACATGTGGGTTTCAGTTGGGTAAGGTTCGATAAAAGCGGTTAGTCGAGAAATAGTTAGTCATAGCGGGCATCTCCCCGCTTCTCGGGGAGTCATTGACTGAAATTGATCCGGTTGGTAAACTAGATGTGCTTTTCAGTTTATCTGCGTTAACGCTTCAGCACGACTATCAGCTGTGCCACACCAAACCTGTGGAGGATTGAAGCGAACAGCCGTAGGACGATTCGGACAAGTACGAACCATACCTCTGTAATGCATTAACTGTACGTGTTTAGAAACGATTAGTTAGGGTAGCCAGATAACGAAGCTGTCTTGTATCCATCAAGTTCCGCAATGCTTTAAGCTTAGACCGGCAAAGAACCGGAAATGCCGCAAATAATTCAACTACTATTCTCTGGCTTGTAAGATCGGAAACTCTCGTTACGCCCGTCTCCTGGACGGGGGCGAATTTAATAGTGTGTGGCCGAGATAACCTTGAATTGCTAGGTGCAGCCTTCATGGACTATAATTAGCGCACGCGACTTATGATGTTGCTACGGCGAGCGGATGCGGCTTAGGGCAAACCATTCTAGCTTGCGGGGTTTGACGCTTCGAGTAACCATTTTGGCTGGTCAGCGGCTTACAGATACAGCAAAATATGCACGACAACCGCTAGTCATGGATGATCACTATCTAGTGTTAATTTCGTATTTAGCCCTGGAGGGGGCACGGTGGCATTGAGCTGAGACGGGCAGATCACGCGAAGTTTCCAGCCTCTCCACCCTCCGAGGAGAGTGTCTGAACAGTGCGAGGTTTAGTGAACGCCTAGTTTATCTGCTGGTCACTATCGCTACTTCTCTCAGACCCCATGATCCCATGAATCCAATATAGTCCCAACAACTTGACTTCTAAACTTTACCTCTGGTTATCTCGCCATTTCGGGTGTGCTTCATATGTAAATAGCAACTAGAGGGACGAGGAGTTATTCAGAGCGGGCGGAGCCCTCCAGGCTCGTCTTGTGCCAATACGCGCAACGCGTAGGTCTAGAACATCTTCGAATTAGCACGGTCGATACAGCTTGAAGGGTGGGATTGGCAAGTGGAACGAAGGGCGCATTACTAGCATGAGTGACAAGGACCGAGAGTCGAACGATCGCCCAAAAAGCCTAGATATCTACGGCGCCGGGCGAAGCTCTGGATAATCTCCAGTAGTCGGTTCTGAGAAAACTTACGTTGTAGATCATTAAAGATAGCAACTCATCTGTTATCACACCGCATTTGTTCCGGACACTAGTACCCTTGGCGAGAGCATTTAACATGAACGTCTCTTAACTCCGGTTACGCGACGCAATGTTAAACGGATTCCAGGAAACAGCTAATTTTTACTGTGGTTAGCCCCTGGAAGGTATAATCAATAATTTGCATAGGGATCCTTTTAAATTGCCAGGGGAGAGGGTAAGCCTTGAGTTCCTTATATACCTAAGTGAATGTAGTAGCCTCCTTGGAAGAGTACTGATGTGTTCTGGAAATAGTTAATCAGAAGCCGAATTGTCCGACAACGTCACGGGGGTTGGGAACGCACGAGAACCCAACGCCAATCCGCGCGCCATATGACCCCTTTTCGTTAGCGGGGACGATAGGTGTTGTCGCTCAGTACATGACCCTTCATCGTGCCCCGTGATATCGTGATGCAGCTAAATCACTTGCACGGTGGAGGAAGAAACATAAATCCCACGGAACCCTCATATCCCACACTCGGGTTCACCGAGTTTCTAATCTCATCTTCTCTGCCCAATCGGTTCTTGTAGACCACGTCCGGAACAATAGTAGCAAGTTTCGTATGTTCTGCTGTACTGCCTTATGTTTCCTGTCGCGCGGACCATCCCGATTTCAATATACTAGACTCTTGTCCTTGATGGGCTATTAAACCTTACAGCTCTTTTTGAGGTCGAACTAACCCTGCTACTGCAGGAGCGCCAACGGTGGCTAGATCTTGCCGCAATCGTCCGAGCGCAGCCCGTCAAATCGTATTATGTTGGTATTTCTAGAACGTGCTCTATACGCCGAGCTAATCTCAATCAGACATACGATAGGCACCTGCTGAATAAGTACTGTCTGAGCATCAAGGGCCAGGACAGGGCCCACGTTGTTACATGTACTACAACTCCCCAACCAACAGAGCTTTGTGATGAGCTCGAATTTCGGAATTCAAATCCACAGGAGCCATTTGGCCACATCCGGATTTCAGTTAAATGAGTATCACCAAATCCCCTCCTATGAGCCTCAGGTGTCGACCGGATCGGATTCGATTCTGGTCGCTCTTCAGCCTTACGTTCCTCGCCACACACCGGCGGGTGCATCCTGCAAAATTAAACAACGCCTCGAAATCGCGAAAGGCCTGCGCTTCCAGCCATATGTTGTCGCACAGGTCCGTCATAGGTGTGGAGCCTAGCCAAGAGCAGTCCGAGGGGAATTATGCATCCAGTTACCACTGCCGACCGGGTGCAAATTCACGGTCGCCAGATCGAGGAACGTATTCCGTGGTACTGATAACGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATTAATTTGTCGTATTAGATTTCGCTTTTGAAAGACCCGATGCTGAGTACAGTTCGTGCCTTACACAACCGTGGCAGTCCTGTGGGAACGAAGTCCACGCCCATTACGTCATAGGATCATGAATTAGACCACCTGCAAGCGCCTTCCTAACGTTTCAATATCGATATCCTCTTAGGCCTGTGACACTACGTCTCAGCACGGATTTATTACGATATAAATCTTAGATTGGCTGGCCCAGTCCAAATCGAGTTCGGACATATCGTAGGTACGGTTCACACCTCATGCGAACACGGCTACATGCGCACCTTGTCGATAACTTTTTCATTACGAAGCGGGAGGAGGCTAATAAGGGTATACGTTTACCTTTTAGAAGGGAACAAAGGCCGCATATGGTTACAAAGGATATTCAGTAGGTATCAGGTTCAACAGATTCGTATCTTCCCGCCGTCCCGAAAAGCGTTCTTAGAGAGTGCATTGCTGAGCGACACATTGAAAACTCCTTCAGTGCGTCACTTCGGTGATGCAAATGTCTACACAATCAGGAGCGCAGTAGCTACTCACTTTAGGTCGAGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATTAATTTGTCGTATTAGATTTCGCTTTTGAAAGACCCGATGCTGAGTACAGTTCGTGCCTTACACAACCGTGGCAGTCCTGTGGGAACGAAGTCCACGCCCATTACGTCATAGGATCATGAATTAGACCACCTGCAAGCGCCTTCCTAACGTTTCAATATCGATATCCTCTTAGGCCTGTGACACTACGTCTCAGCACGGATTTATTACGATATAAATCTTAGATTGGCTGGCCCAGTCCAAATCGAGTTCGGACATATCGTAGGTACGGTTCACACCTCATGCGAACACGGCTACATGCGCACCTTGTCGATAACTTTTTCATTACGAAGCGGGAGGAGGCTAATAAGGGTATACGTTTACCTTTTAGAAGGGAACAAAGGCCGCATATGGTTACAAAGGATATTCAGTAGGTATCAGGTTCAACAGATTCGTATCTTCCCGCCGTCCCGAAAAGCGTTCTTAGAGAGTGCATTGCTGAGCGACACATTGAAAACTCCTTCAGTGCGTCACTTCGGTGATGCAAATGTCTACACAATCAGGAGCGCAGTAGCTACTCACTTTAGGTCGACCTCTGGTGCGAGTGTGATGGACCTTATCATGATTTACCGACCACCCGTCCATTAGTCGGGTACCGATACCGGGTCAAACACGCCTGCGGAAATTCCTTCACTTACATTGAGGCAGTTAGATCGGGTATGTGATCGGCCTTCGATCAAGACTGGGGTGAAGTTTGCCCAGTCGAAGCGTCGCTCACGGTCCAAACCTGTCAGCCATATTTCGGGTGTGGCCCCTTTCACTTCAACTCTTAACATACTTCCTTTAGAGCCTGCCGTGTGACAGGATCATCCTGCGCTGCCGCAAGATTTGCTTTCCTACTGGACGATTGGTTTCCCTTGATGACTAATAAACCCTACCGCGTTCCACTTCGGCAGTTGAGGCAAGGGAGTTCCCCAGGGCAAGAGCGCGTTGCGACGTTTTCACTCAGGCGTGGTTCCTAATAACAGTGCGGATATGCTTCATTGTGAGTACGCGTAGAGGGTTGGCCGTCACGGGGAGTTCATCTATACTTCCTGGTCCATTACGTGTACGGCCAAGCTCGGTAGCAAAGTACGGGGGACGCACAACCCAATTGTAGACTAAACCAACTCATCAGCCTCCCAACTTGGGCCAATTTCTAAGCGTTATCACTGTGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATTAATTTGTCGTATTAGATTTCGCTTTTGAAAGACCCGATGCTGAGTACAGTTCGTGCCTTACACAACCGTGGCAGTCCTGTGGGAACGAAGTCCACGCCCATTACGTCATAGGATCATGAATTAGACCACCTGCAAGCGCCTTCCTAACGTTTCAATATCGATATCCTCTTAGGCCTGTGACACTACGTCTCAGCACGGATTTATTACGATATAAATCTTAGATTGGCTGGCCCAGTCCAAATCGAGTTCGGACATATCGTAGGTACGGTTCACACCTCATGCGAACACGGCTACATGCGCACCTTGTCGATAACTTTTTCATTACGAAGCGGGAGGAGGCTAATAAGGGTATACGTTTACCTTTTAGAAGGGAACAAAGGCCGCATATGGTTACAAAGGATATTCAGTAGGTATCAGGTTCAACAGATTCGTATCTTCCCGCCGTCCCGAAAAGCGTTCTTAGAGAGTGCATTGCTGAGCGACACATTGAAAACTCCTTCAGTGCGTCACTTCGGTGATGCAAATGTCTACACAATCAGGAGCGCAGTAGCTACTCACTTTAGGTCGACCTCTGGTGCGAGTGTGATGGACCTTATCATGATTTACCGACCACCCGTCCATTAGTCGGGTACCGATACCGGGTCAAACACGCCTGCGGAAATTCCTTCACTTACATTGAGGCAGTTAGATCGGGTATGTGATCGGCCTTCGATCAAGACTGGGGTGAAGTTTGCCCAGTCGAAGCGTCGCTCACGGTCCAAACCTGTCAGCCATATTTCGGGTGTGGCCCCTTTCACTTCAACTCTTAACATACTTCCTTTAGAGCCTGCCGTGTGACAGGATCATCCTGCGCTGCCGCAAGATTTGCTTTCCTACTGGACGATTGGTTTCCCTTGATGACTAATAAACCCTACCGCGTTCCACTTCGGCAGTTGAGGCAAGGGAGTTCCCCAGGGCAAGAGCGCGTTGCGACGTTTTCACTCAGGCGTGGTTCCTAATAACAGTGCGGATATGCTTCATTGTGAGTACGCGTAGAGGGTTGGCTTTACCCGTCTAACCTTCGAAGGTTTGCCTTCCAGTCATCGCCCACTCGATTACGGATGTTGGGTAGTCCATTGACACTTGTTTATGTACATTGGAAGTCCGGGACTACCCCTGGTATGGTCGGAAGCGACTACACGGATTTATTCACGGACTCGGCAAACGTTCACAGCCGCATGTTTAGTCATGGATTTTCGACAGTTGACGATAAGACATCGGAGGATAAGGAAGTGCGTTATGTCTTATGTCCCCGTCCGATGGACTGGACGAAGTATAACTGATAACGTTACTTTCTCCCAACAACTACTAGAAAACTTGTTTAGTCCGGGTGCGCACCTACACGCTGTAAGATCTTACATTTCCGTATAGGACGACTATCTACCGGGGTCTATGACACGCGACCAGGGGCCGCTTGGCAGCAGTGACTGCGCTTAAAGTCTAACCTGATGCGCGAGGGCGGGGAATCCAAGGTGCGACCACGAGACTCGCCCGTTGACCGGCTAATATTTAACCGGTTTATTAATGCCCGACCGTCATGTATACAAGCTAAATAAGGGGCCGGAGAAATGTCGTGGCCCTGCAGAAACCTCTAAAGCCGAGCTGATAGTTAGGTTGTGAATTTATTTATCTTTTATGGTCACTAGATCCACATTCTATATATAGAGCAGCACCGACATTAGCCAGTAGTTATACATGATGAACTCGGGCGTATTCGATGCATGGAATGAACCTTGCGCCAGCTCCTAAGAACGACTTCCGTCAGGCCTTAGCGAGGTGCCACAGGGGTGGGGGAGAATAATTTACATTGAAAAGGCTTAGGACATTCTGCTTCAACCCCGGGTTTTGTCTAGATTACACGCTGGTGTGAGGAGCTACCTGGCAACCAAGGTCTGTCAATTAATTTACGTGCACGATCTAGCAAGCGGTGTACAAGGGCTGTATGTCATGATACGATTTAAAGTTACGCTCGTTAAAGCGGGCTGTCTGCGGCCTGATAAAGATAATAGTTCAGAAGCCCTATGAAATAACAGAAATCGATCCTATTAGTGGGTGAGAAGGGACTAAGGCGTAAGGGCGTCCCCGGGACCTACATCTTTTTGAGCAGATAATATCCTTATACGCGTTCTTCTTTGACCGGGATACAGCGAGGTAAGTCCGCACGTAAGACTGCGGCAGGTCTATAAGGTGTAGGGAAACAGGCCTTGCCCACTAATTGATGTTGAGACAGCCACGTAGGGTGCGGCCTTTGGCTTCAGCGGACAAGAGGATGATGAGGCATCGCTCTAGGCACAGCATGTCTACAGCGAGATACACAACGACATCATGTAGAGGCAAAGATCCACCTAGCACGGGACGTTTGTCTGCCAGATAAGCGTCTTGCTGCCGTTCACAATACTCGTAGATCGCCTTTGTCGAATGGCAATTCCACCCACACCCTTGCATCTTCACGCTAATCAATTTCCCTATCCGGAGATACCGTTTTCTGTGACGATAGCGCCTTGAAAGAATCCTACAGCTAGCTATTCCCAGCAGGTCATGATATTACAAACTTCGCGGCCATCCGTACGGCACAAACTCTAACCTGGTGTTTGACAGTCGGTGATGTTTTGAGACATACTTGACATCTATCCATATTTACTATCTCGCCTGTCCAAATGGTGAACAAGGCATAGATCTTCAACGCTCGGGTGGAGCTTCTTTATATGGCACTGGGTGCAAGAGCGTGTTAAGTGCTCTAGAAGAACGCTGATAATCCACCTCTCCTGAGTTACTTCCCCTAACTTGCATCTTATACAAAGCGATCCTATACGGAACTATCGGCGCGAGTCGTCAAATCGCCCATTGTCGGATATGTGCACAGAACAGGAGCCTCTCCTTAATTTAAATGTTCGTCCATATGAGCGTATACGAGTACTAACAGGTACAATCACAAGTTAAACGTCCCACCGTCGGCTTGTCATTGGGCGGCATTACAGCAAAAAACTCGTACATAGTCTTCGTAAGGGTTCATTGTCCAGCTATGGCCGTAAGCTAATCGCGGTTCCGTTAATCGTATCGGGATGTCCTGACAGAATTTAGCGTTTCTATTGCGTGGCGGCAATGGCCCCGGAGCAAAACTTGCTTGGGTCTCGTGGTTTTCAGTGATCTATGAGAGTAAAGTACGAGACGCGCACAACATTACCCAGCGGAGTCAAGCATCAGAGTGACTGACCAAATTCAGGAGATGACTAGCACATCGGACGCTGGTATTTTGGGATGTTTTAGGTCACGCACGTTCGAGCGACCACATAGTCTTGACAATAAGCTAACGGAACGGGGAAATCATTCATAGATGATGTGGTTATGCGTGTGGCATCTGGCTGATCCAATCCGGCCTTTCGAGCTTTGCACGTACCTGAGAGCAATAAACTTAGAGACTCGGTTGAACCAAATGACATGCCAGGTTAATATTAACACGTCTTTATGTAATCCTACTATCCACGGATAGGGTGATTAATGCGGCACACTCCGATATCGCTTTGAGTCTATTGCATCCGTAATAAAAGCTCTCAGCGTGTCATTAGTAGATTGAACTGCTCGGAGCCGACCGGTGAGGGCATTTACCGACGTGTGCATTGCTGGCATTTCCCAAAAAGGAAGCGCACGCAAAGGCCTTTTTCCGTAATGGCATCCTATGGAGGACGTATTACTGGGCTGGCTGCTTTTAGAAGTCGATGCGGTCGCATGACCAGTGACACTGATGCCAGTCCCGGTGGGCTGGGCTCCTAAGTGCGCGTTAAACTTGCGCCCTGGATATGACACCGTAGCCGCACATGAGATTGGTTTATACTGGATACTATAGACGCCCACCTGAGCTGGAGCCCTCTCCCACCACGTAGATCCCAATGAAAGGTAGTGTCAGACGCCATGGCCCATGTATTCATTCAGAGGTCCCAGGGCTTGATACTATTAGCAACGACGTCGAAAGTAAAGCACAGTTATCATATCAGTTTGAAAGCGGCAAATCGTCTCTACCCAGCGCTCTTTTTGCCAACGAAGTTCGGTAGTTGTAAAGCGGAGAGTCAATCTTATGCCGCCCACAGCCATATTCTGCGCGGTCGCATAAGGTTAACTGCTATGTCATTTTTAACGTACTCTGGGTTGAAGTGATCCGGCCCTTGTAGGTGCTTGTAATAAAATGTGATAAGCGACTACTGTTGCGAGACAAATCGGGGAGTCGTTCAGCACCGCCATCTGGCTAGCTAATCGCGAAACCATTCCCGCTGGGACGAATCCCGGGCTGGTAAAGCCTCCCTCGCGGGAGCACATGGTACAAGAAGGGTATGTGTATGTGGCGTCCCCAGTGTGGATGTAATTTGAGCATTGTCCAATGAAAGTAGCTGGTTCCCGGTTAAGGCAGTGGGCCCCTGAAAGTGGGTAGACCCTTCTGCACCGAGTAGATGATATTTGAATAAACGTCGATTGAGGTGATTTTGGGGGCACTTATCTCAACAGAATAACTTAGACCTCGCATTTCATCAGCCTTATGACGGTTACTTCAGTGCCAACATGTTTAGAAGCCTTGCGCGATGGTGGCTCGAGCAAATTCTTGGATGAACGGTGTCAGGCTCCCCAAAAGCGTGACGGCGTCCACTGACTCGCTTCTGTTTTACAAGACCCCACTGGTAGACAAGTTGGTCGCGGTCACGACAAATAGTTAGAAAAGGTCTGCTCGTAACAATACTCCCGATTTCACGAGTATCACGTCGGCCTCTATTATCCTTAACTGGGGACCCAAGCCAATCGGAATCCGGCTTTGCGCATTAGTACACCGTGTTCATAGATACTAGGCCAGCATGGGGAAGTGGCTCTCATTTTGGACGCTCTTCCAGTTCCCCTAGTCCGAATTGAAGGAAGGGTTCTTCATACCCGTGTAAGCGCAGGTCCTGCCGATCGGCACTGAGTTCATCGTCCAACCGTGCTGCTATATTAGGCATGCACTCGCCAGGCTTGGTACGAGTGCACTCATACCAGCCCCCCCCTGACCGAGAATCACCGCTAATTTACGATGTTACACTCAAACCCCCATTGCTCTGCCCTTTGCTGATACCAGCAGGTTGATGTCCCATCTAGACAAGATGACTCAAATAGCGCCAAACTAACGGAGGCAGTAAATTCGCAACGTATTGCGTTTATTATAAACCGAACGAGTGAGAGGACGAGCTACCTTAATAGACTTCGCCGCCAGGCACTCTAGCCGCTCCATACCTCCTGCTCCCTAAGACACCGGTAGCCCGGTTTATGAAAGGGAAACCCGTTTGTATCTATTGCGCCCGTGTTGCCCCGCCTCAGGTCTTTTAGCCAGGTTGGTTACCCACAGGAGCTACGTTATCAATTAGTCTCGGCGAGCCCTGATACTTGCGAGAAGACGGACCAATAGGGTTTCATTGCGGCTCCATTACCTACGTGTTGCTTTAGGCCCCTCAATATTAACGTTTCCGTCGTGACGTACGATGTAAGCAGCTGATACTCTACAACCCGTCTCGCATAGGAGCTGTCTGCCGCCGCAAGACTTTACCTAGAAATGCAATACGTCCACTCTATAACATCATCGGGCGTCAAAAGGGGTACACTATCAAATGCCGCTGTCTGAAAGGTAAGAACCGCATCAATTCCGGGGCTGAAATACGGTGTGCATGGCATGGAGGCGCAACTACTTTGAGACAGGCTTTGTCGGGTGGATGCTTTGGAGCATGCATCCCGTCTAGTGGCGTGAGACCCAAGCGACGGCGTTATTAAGTGGGTTATTAAACCAAATAAAAAAGTGGAACGACTTGTTGCTTCTATATCTATGCTTTGAGAATGCCACATTTGGTAGGTAGAAGCTTGCATCATATTGATCACATCAGGGAGTCACACTAGACCGATACTTCAACCACTGTAATCTCTAGGTGCGCCGAACGAGGCAATCGTAGTATATTGGTGAGGCTTAGGTTGAAAGTTCACGTCATGGCCGGGTTAACTAGCTTATACTAATCCTTCTCTAGGATCGTTCCCTGTCAGCGGTCCACTCTTGCGCGAAGCTGGTAATTTATTGGCAAGCGGACACCGATGAACGGATAGGTCAGGAGCCATTCATAAAAGGGATGTCATACCGATACGTGTGTGTCTAACAAGTTTGAGAACGAGGTGTCAGTATCTCTTGTGTGCAAGCCGTAGCTCTGATCTGCATACCCTTAACGGAACGGCAGAGGATTACTTTATGTCTTCACTCATGTCTTGCGGGTCACGAGTTCTCAGCACTCTTAAGAAAAGGAAAATCTCCAGCCAAACGGAATCTTTGCCCGGGCTGTTCGGAAGCCGCTAGGAGTTATCAGTCTTATTGTTTCATTGCACCGCACTCGCCTCTTACTTAGCACAAACATGGCGTACTCGGAGCTACGCTGGACTCACAGTCTTTCTTGTTTTCGAGGGAAGCTCAGTGAAGTAGTTGTGGGCGACAGCGTTTGTGAGGATCGTTGGTGATTTGGACCTATCCCCTCCGAGCTCGCAAGCTGTACTCGATCGCCGCATCTACAGCGCACTCGAGCATTCAGCCCTCAAGTCCGTAGTGAGCGATATGCACCCAGATCTTAAAAGGACAGAGATACGTAGTTTTGACGTGTATACCATGCCGTGGCGAAATGGAAGCCCCGATTCGAATTCCTGGTAGAGAAGGCCGGAGGTCTATGCAACATACCCTACCCCGACACCCAGTACCCTGAGCCGATTGTGTTGTTTTGAAATTAGCTAATACCGTCCATAGGTTCTGACCAAATCAGGCGTTGTTTGTGGTTAGTTTAGTAACCCAATACGGGGCCCCTCTAATACGCAGCTACGCTATTCAAGACAGCATGGGGTTCTCACACAACTTATACGAGTGTAACGGTCCGCCGAGATGGAGGCTTTCAAATGGGTTGCAATATACAGCAGATAGGGGCGCCGAGCGTGGATAGTAGCTTAGTTCCACCGTGGCTTAAAGTGCATTATTTGCGGTTTGAAGCAACTGGTCTATGTTAAACCGTCAGTTTCCGTGAATGTTAGAGGTATAACGTGAGCGGACTGCCATAAGGTCATGTACAGTCTAATAGTGGTAATCCGTGGTCGCGAGAGCATAGAAAAATATGCTGTAATCGTCCAATGTCGTGACTACAAGGGCTTCGCTTTGGCTAATTTCTAAGCGACCCGGTGGGTCAGCCAGATTAAGTAGAGACGAGTTCACCGGCGCGTTATTGCGGTCTCAGACTTTATGGTAAACGAGGAGAGACAACTGAATACAGGGAAATCGCACGTAATGGATTATGTTACATTTTTATGAGTACAGCATCGTACGGATCATTCAAGCAGAGCGACTAGTATGTAGGGTGCATGCCGAGGTTTCGGTTGGGGTTAGCCGCTCGTTGCGCTACTCCTCGGAAGTTTAGATTATACTAACAAATTCTACACGGCATTCAACCAACATTTCCTCCTTAACCCGCTCCCGTCGGCAGGGGCGGACCAAGTCATCAGCTATTCCGTGATAGATAGATACTGGTAGTTCTTGTCGGGTCGACCCACTGACTCGATGGCAGCTGATGGGTATCTCTACATTTAAAGCATACCTTGGGACTTGCATTGGAATGAACGGTGTCGGTTCCTGAGGGGCCGTGCGCGTAGAGTAGGGACCGGACATCTTAGGGAGCTGTACATCAGCGTGGAGGGCTAACTCCAGGGGAACGAAACTCCCCATATTTTCGTTTCCAGATGCCCCGTTGCAACGGCTTCCACACATATGAAGACAGAACATTTACACCGGGTACCCGCTCTCGACGTCCTATCTTCGGCGAGAGGAAGGCCCTCACAGTGGATTGTCGAATTCGGGGCGTCGAGTTAAGTCAGCTTGAAGACACATTGGTCTCCAGGTACCCTGGAAGGTTCCCTCAGGCGGGTGACGTTTCTATATCTACTAAAGCCCAAAAGAGTACCGAACCACACCTTGCGGCTAGCAACGTCCACCTGTGGCCTCACTCTGATAAATTTATTGAGAGGACCATCCGTAAAGACTGTGAAGGGTCATAGGTCCGCTGGCACAGCGTAGTGACATCAGGGTCTGATAACCCACGGAACGAGAGTCCCCCCCGTACTCTGGACTATGGGAACGCATACTTCGTGACAATACATATCGTGCCAAGCTTAGCATCGTCCTCTAAACGAACCCAAACGGTGAGAAACCCATTTATGCCAGCACAAAAGGAAGCGGTGGCATTGAATCTTAACGGATCACATATACTAACCCACTTGCGAGGATGCCCCTAGGGGCAACCGCATAGTTTCCCATGAAAACATTGGTGCGCCGTTGCAGAGGAGCTCATTCGGTAGTACATAAGGCGTAGGGCCTTTGACGTTTCTAACATTTAAGATTCCTTTGAGACCATGACACTCTCATTATTGAGCGCTGTGCGTATTATTCCCCTTGATATATATCACGTTTCAGCCGGTGAATAAAACGATAAGCGGATCAACACAGGGTCGTTACAACGCCTGAGGTTGCTAGGAGGGGAGGCCAGAGCCCTGATATACTTGAGCTCGAAATGTGAACGTTAAGGGCTATCAGTCCGTAAGAACGTTTCTCTGAGAAACGTCCAGATCTACTACCGCTAATATTACTGCACTGCCGGATGATCAGACGCGCAGTTGGTTTGTAGTGTCTCAGTATCGCCAGTCTAGCGACGTGGGCCCCGCGATAGCGTCTTCCATTGTAAACAAATTCCATTACGCCTCACGTCGTCGCGCCAAACAGCGGCTCGAAATGTGACCGGAGTCGAGATATGGAAAGGTTAGTCTTACGAAGGCATGAACAAATACGCTTGCCGAGGTCCGATGATTAAATATGTCGCAAGACCATCTAGAGCAAACGCAACGTGGTCTCCCTTATCATAGACATGCTCTTACCGACATTCGTGGCGAACCCCGCTTCGCAAACATGTGGGTTTCAGTTGGGTAAGGTTCGATAAAAGCGGTTAGTCGAGAAATAGTTAGTCATAGCGGGCATCTCCCCGCTTCTCGGGGAGTCATTGACTGAAATTGATCCGGTTGGTAAACTAGATGTGCTTTTCAGTTTATCTGCGTTAACGCTTCAGCACGACTATCAGCTGTGCCACACCAAACCTGTGGAGGATTGAAGCGAACAGCCGTAGGACGATTCGGACAAGTACGAACCATACCTCTGTAATGCATTAACTGTACGTGTTTAGAAACGATTAGTTAGGGTAGCCAGATAACGAAGCTGTCTTGTATCCATCAAGTTCCGCAATGCTTTAAGCTTAGACCGGCAAAGAACCGGAAATGCCGCAAATAATTCAACTACTATTCTCTGGCTTGTAAGATCGGAAACTCTCGTTACGCCCGTCTCCTGGACGGGGGCGAATTTAATAGTGTGTGGCCGAGATAACCTTGAATTGCTAGGTGCAGCCTTCATGGACTATAATTAGCGCACGCGACTTATGATGTTGCTACGGCGAGCGGATGCGGCTTAGGGCAAACCATTCTAGCTTGCGGGGTTTGACGCTTCGAGTAACCATTTTGGCTGGTCAGCGGCTTACAGATACAGCAAAATATGCACGACAACCGCTAGTCATGGATGATCACTATCTAGTGTTAATTTCGTATTTAGCCCTGGAGGGGGCACGGTGGCATTGAGCTGAGACGGGCAGATCACGCGAAGTTTCCAGCCTCTCCACCCTCCGAGGAGAGTGTCTGAACAGTGCGAGGTTTAGTGAACGCCTAGTTTATCTGCTGGTCACTATCGCTACTTCTCTCAGACCCCATGATCCCATGAATCCAATATAGTCCCAACAACTTGACTTCTAAACTTTACCTCTGGTTATCTCGCCATTTCGGGTGTGCTTCATATGTAAATAGCAACTAGAGGGACGAGGAGTTATTCAGAGCGGGCGGAGCCCTCCAGGCTCGTCTTGTGCCAATACGCGCAACGCGTAGGTCTAGAACATCTTCGAATTAGCACGGTCGATACAGCTTGAAGGGTGGGATTGGCAAGTGGAACGAAGGGCGCATTACTAGCATGAGTGACAAGGACCGAGAGTCGAACGATCGCCCAAAAAGCCTAGATATCTACGGCGCCGGGCGAAGCTCTGGATAATCTCCAGTAGTCGGTTCTGAGAAAACTTACGTTGTAGATCATTAAAGATAGCAACTCATCTGTTATCACACCGCATTTGTTCCGGACACTAGTACCCTTGGCGAGAGCATTTAACATGAACGTCTCTTAACTCCGGTTACGCGACGCAATGTTAAACGGATTCCAGGAAACAGCTAATTTTTACTGTGGTTAGCCCCTGGAAGGTATAATCAATAATTTGCATAGGGATCCTTTTAAATTGCCAGGGGAGAGGGTAAGCCTTGAGTTCCTTATATACCTAAGTGAATGTAGTAGCCTCCTTGGAAGAGTACTGATGTGTTCTGGAAATAGTTAATCAGAAGCCGAATTGTCCGACAACGTCACGGGGGTTGGGAACGCACGAGAACCCAACGCCAATCCGCGCGCCATATGACCCCTTTTCGTTAGCGGGGACGATAGGTGTTGTCGCTCAGTACATGACCCTTCATCGTGCCCCGTGATATCGTGATGCAGCTAAATCACTTGCACGGTGGAGGAAGAAACATAAATCCCACGGAACCCTCATATCCCACACTCGGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAAGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATGTCATCTTAGCCTCTAGGCTAGCCCAAAATTAACAAGCCCACAGCGGAAGCAGGGCGCAGCACAATGACGGAAAGGTGTGGTTTCATAAGATAGTAAGGGGTGCAACACTCCTAAGGTATGGAAGGCTGGGCTGACCGCCTGGTTTAGAGACCTCAGCGCGGCTTCAGATTCGACTCTCTTCACTGATAGTATTCCGTTGGGGACGAGGACTTATTGCTGGCAGCCGAAAGAGCAACCGGAGGTGAGTCGTCCCATGTATCTATGATAAATAACACATTTCGCCGCCCCGCCTCCCTCCCTCGGCACTGTTACTACCGATGTCACCATAGGCAACTTGGTGCACACCTAACATAAATCATACTCCAAATGAAGTGAACTCGACACCCCACTTTCGTCCCGGTTCGAACGTATGATCACTAAATGTTGGGATTGGGGTATGATTATCAACCACACATCGTGTAGTGGCGTTTACGCGATAGCGTTACTCCCCACTAATCCATAGAGAGTGGATGAGTAGCCGTGATGTTACAATAGTTCAAATAACAAAGGGGCGCCAGGCCAAGCGAGATGTACCCATACTCAAACGCCAACTGTGGAGCTACGGGATGACCCAATTCGCCTACTAGCCTGCCGTCAATAGTATCGGCGGTAAGGGGTATTTTTATACTAGGCTGTTCGACTCTGGACTCTGCGTCTTTTGTAAAAATAGCAAGTAAAAACATCTATGCCGGGCTCACGAAGGGCTCAGGCTTACAGGACTCCAGGCGGAGCCTTTGGTAACATGACTATGAGTAGGATGTTAAAAGTAACACGGTTAATAGGGCCCCTCGCTACGCACATTAAAACCTACTTACTAGTTTGTGGAAGCGGGCTCGGCATACCCTTTCCACTTGCAAATCATCTCATACCATTCTCTACCCGGCTCCACCCGGATCACAGAGGTCCCCAATCATTTTCGCGGCAGTGAGGAGGAACACCGCTGGCATGATGCATAGTTGAAGTGATACCTGAACTTGAGTGACGCCGGCATTTGAGAATCTCAATTCCCATAAGTTCTCAATTGTTATCCTTTCCTATGTAGTACCGTAAAGTCCCTGCGGTGTTCTACATGTTGTTTGGTCCTGTAGACTCATCGAGAGATTTCGCAATTACCCAGCTGTTTGGTCCGGCTGCTCAGGTTTGTTGAAGAGTGCTGGTGGCCACTGGTGTAGACTTGAGACTAGTTGAGAACTTTTTGCACCTTCCCTCGCAATGGTGGGGTTTGTTTATCTTTGAGAGCGTTACGCGAACACCTTAACCGCCAATTGATGCGGGATTCCGTACTGGTCGGGGTCATATATATCTACATTGTATGGCAAACACGTCTCTAGGACCGGTCGCCCCTCTCCGCTTTAAAAGCATTCCAATTCCCTCCAACGTAGGATGTTACGAACTAGCGACCCTGACACTCACTGTGGCGAACTGCCAGTCTTATCGCGGTGTTAGATGCGATCTATCTAAGCCGTGGGTTCTAACGGACCGCTCAAGCTAGCGCCTCAAAGTGTAATATGCTGATCTCGAGCCGCCTGGACCACCCCTCCACGACACTATACGTCCAGTACCACGAGAGCTTAGCATCAACAAAATCACCACGTTACAGGCATACCGCATACGACGAGGTGACCCCTACTTCGGTCGCCCGCACTCATGCAGACAGCCCACAATCATCTAGACCCCCCCACCACTACAGGGCTAACGTACAAAGTATTAACTATCCTCCTACTAGGCGCCTGCCCAAGCACTAGCGGCTTCTCGTATATCATTGGGCGCTGTTGACCCGAGAAAAGGCCGCCTTGATGATCCCCGAGCTCAATCGGTAGACTGCATGGCCACACCTCCAAGCATCGTCAACGTACTTGACGGCCCGCGATAGCACCATCAGGGTACTGGCCCTTGCAATCAGACATGCCTATCCACCAAGCGACCCCAGGACGCGCATTCGGTGTGCCAGGCGCCCACTAGCGAGATAAGACTGGTTATAAGCTGAATGACTCCGTTACGGGTCTAGGAGGTTAACAGAATGAGGGCAATACTCAATGTGTTTGCACGAGGGATACGCAATAACAACTATAACAATGAAGGCAATAGACGAGGGCATAGGCAACTGCTTTCAGCTAGGTACTTCGCAGTCGTTCCTAAGTGTCGCTTCTCTTCCTGCACGGACGATATGGAATCTACACTCAGCACGCGTACGGGACAATTCACGTCTTGCACCAATGGGAGAGGACCATTCGAATGATCCGCTCCTAGTATACTATGGTCGCCCACCAGTGCCACTCCTTTGGATATGGTTGGCTTTCTAACACCCTGTGTATATCGAATTACGTGAAAGGGATAATATTTTCAAGAGAGCTTAAATTGGAAACTGGCCCACTCGATTTTATGGGAGTTGAATATCGCGGGTTGTACGAGCGTCGTCTTTAGAGACTAGCGAAACCATGCGGATATGAGATCCGTACGACTTGTATCCCCAAGAGTTCAACCAACAAGTGGAGACCCAAATCAAATTGAGCATTAAACGAGCAGATTATGTTAGAACACTCATCGTTTCCCCCTTTTGGGAAAATTTTTATCTCATTTCTGGGTATAAAATAAGTGGACCACCTCACAGTTATGGGTCATGAGGTCCCTGATAACGTGTCGCAAAGATAACTACAGCGGGTTAGCACCATAAGCGAACGATTTGCTAAAACGCTGGCCAGTTCAGGAACAGTTCTCAATGATAGGAAGCAATCTAACCCCAGGGCAGGGTACGAGTTTTGCTGGTCTTGTCTCAAGGCCACGATTAAGATGTTTCGGACACTCGAGACCACCTGACTACTGAGCATTCTCATTTTTAAACGTCCTGAATAGACGATGATGATTATGTAAATGATATATAGCGTTCCGCCCGTTACCGGGAGTAACACGCATCGGTCGCGATAGTTCTGAGTAGAGGCGATCAAACCTATGATGAATTGTTAACTACGGCCAAGTGTAGCTTTCGATAAGAACCCGTCCCTAGCGGGGATTACTGAAAGCAGCAATCACAGGCCCGGACTAGTTTTACTAATCGGGTTGAGACGACTCATTTAATGATTAGGAATCGTACTGCCTCTGATAATTCGGACCATCTAATGCCCGCGCGGCATAAAAAGTTATAATTCTACTTTTATGTCGATAGGCGAACGGAGTGTAATCTACCGTAATGAAATTCTACTTTGATTCTGAACAATTTAGAGAGGTGGTGATCGTGTGGCGCGGGTAATCGGTGCTTGTGTATAATTTGACGACAGCCGACAAGGGAATATTACGTTAGGCGATCATTCGCTAGCTTTTGTTATTATCGCTCATGACTGGCCTTGTCAGTTCTACTATCCCCGAGGCAGGGCCATCGACATCGCCGACCCCACATAGCGGTCTCCATAATGTTAATAACGGCTCGCCGAAACCGCCATGGCTCTTTACGATATTGACGCCAGACACCAGTAGATCATGGAAAATGCTGTGGCGTGCATAGGGCCTCCGACGTCTGGAACACCTCTACACGAGGGACCCGGTATCGACAAGTAAGAGGGCTCCGCGGTCAACGAAGGTTTCTTCCGAATCGGCCCACCTTATCCAAAGTAATGGCCGAGAAATTCCAAGTTGTTCTGCATTCATGGTAAACCTGCCCAAACAGGCGAATGGGCGGAGGTATTAGGATAGCCCATATACTGGAACTCTTGTTGGGTGTTCGAGGAGTGGGTGGAGTGTGGTGACGCGTAGACTGCGTGGTTGTCCCACCCAAATCTCCGCCTAGCTGTGAACTTTGGTCCCTTAGGTGCCGCATAGTATACCCTATTCTATTATTTAGAATAGTTATGTTAATGGTTAGTCCTAATCGCCGCATGCAGATCGACAGAATAACATTTCGGCTGATGGCAGACATAACAAGGAGGGCTTATATAACTCGGCAGGTATGAGGTTTATTCGCAACTATCCATGTCCCGAAGCGTTTTTTGCCAGCTAGATAAGGGGCATAGGATAGCTATGCCGCGGCCGTGGGTAAATATTGCCTCGACTACGATTATACAGCTAGAGATGGAACATACTTATAAACTATGGGCTACAGGGGGGTTTCCGGGTTTCGGGGCAGCTCTACCCAGAAGGTACGTTATGTTTATTCACCCTTATAACCGGCGTTCCTTACTGTGCCAACTGTGTCTAGTAGTCCTTAAAGTCGCCGTCCCACGCTATCACACTGTCGCATTGCCCGGAAAATAGGAGCAGTCCTAAAAAGACGAATAACATTTTAATCGTCGACCTCGAACCAGTAGTTTTTAGGAAAGTTCGTCTGTTAGACGACAGATCAAAGTACAGTAATCGTGCAATGTCAATGCGAGACTCGGCGCTTACCGAAGGCACGCGTTGAGCCGTGAGAGCACGATGAAGATACACGCCTGTGCTTGGCGGGATAGAGTCGAGGTGTTGGCCAACTGGAAAACGGGTTTTTTACCTCATTAATATTTTCCGTGACAACCCCCTGAGATAGGTTGGTATGCATGAGTTACAACCTAGATTAGACAAGACACGGTAATTACAACCAAGCCAGCAATGTTTAAAAAATCACATTATGAAGGTAGGAGAACAATTCCCCCGCGCGGGGAGGGGTGGTACTTTACACCTGGAATGTAACACCTTCGTATGATTCATGGTCCATTCATGTTAAAGATGTACTCGAGCGTCGACCTGGCCGGCGGCACGGCCTTCTCTATTGAGTTTATATGATCTGAGGGCTAACAGTCCATGGGTTTATCGACGAGAAGTACCCCGCTAAACTATAACACCCTAGCCGTCCCGGGTGGTAAAACACGTAAACCATCGGTGGACCGGAAGACGACAGCGTCCACAACCGAATCGGCCTACAGCTTAAGGGGACAGGAATTCATCGTGTTCGGTTCAAACTACTTCTTTACCGGGACCCTGATGTGAGGCGCGTACCGATACATTCGATGTGGCCCCGACTCGCTTAACCACCCTTCCTAATCCGGCCTTCGCGCCATTTTCGCTATGTCTCGGCATATGTCGACGTGTTTACAGACCCGTGAGGCTTGACCTACCAGGCCATCTGGGAAGTATGGAACAAGTGAAGAACCATGGTCCTGGCGAGTTGAACGTTAAAACTGACTTGCTCCGATGGCCTGCAGTGTTCTTTGGCGGTAGAACACCCCAGCGGAACATGCAGTTACTAATTCTTTCCTGACTGAAGGATCAGTCCTTATGCTCGCTACTCGAGACGTATGAATGGGCGCACTCCTGCGATAAGCGCCTTATTCAAGAGCCCTCTCTAGGTTGATAGAAGGGGATTTTTATATCTCAAATTGGACGAACTAAAGACGTCTTCAGCCGTAGTATATTTTTAGGGCCGATGCCCGTTAAGAGGAAATTCAGCCGAAGCGAATGCTCTAGCGAATTTCCGGAGGGAGCCACTTGGTCAGGATACAAGTTCGCCTCATGTAGACCACTCAGTCAACAATAAGAGCCTATCAGGACAGACATACGAACCATAGCCTCCGCTATCAGACGTGGTAATCAATCCTTGTTACCGGTAACCTGGACCACCATAGTGAATTACCTTATCGATTTAGAGCTGTCACACAGCCGTCAAGCGTGTCACAACAGGTATGTAGGGGAAGTCGCGAGACCTCTAGTTATCTTACATGATTTGGCATCCTTCGTGGCTAAGCACACGCAAAGGAACGAGGTGCGGACTTAACCTTACAAGACGGAATGCTATTAACTCTCCGAGCAGAAATTCTACCGCGTCCCGGGGTCATATGAACGAAAGCGCAGCCCGCAGCGCCTCTCGTTCAGCGCGTCATCAAGGAAAGTACCACTTGAAAGCAAGACGACCATGGGGGGCATTCGGGTTTGTGTGAGAGAGACACGAGAGTAGAGACAGGATTATTAAGACGGTGGATTTCATTCATACCTACACGGTCATGGGAGCTCTGGATCGATCCCAATACTAGCACTGTCAATGCCTTAGAATTACCACCAAGACGCTGTGTAAGACGCTGAGCGACGCGTATCCGGCCTCTTATGGTACACGTGGTGACAGCCCTTTAATAGCGAAGTAAGGGATTGGTTAAGCAGATCCCAGTATGCTGGGCAATCCCGGCCCGTGATTATGAAACGTGCCCAGGTTCAGGGGTAGTGAATTGCAGACTTTAATCGCTACTCGGTATTTGTACAGATGCGTGCAAGATAGATCTTTAGAATACCCTGCATCCCTGCAGTCAAGCGTACGATTCCAGATGCTTTGCCTGCTCGGGGGTAATGTCTGCGTACCCATATCGGTCTTGGAAGGTGGGGCCAGGTAATTCCCTTAAAGCGCATTGGAGTTGTACGGACGCGGGGATTAACCTAACGCCTGATTGGACGGTGGAGTGGCGCTGCGGCATATGACTCGGTGTATTTGGGTGAGCCTTAGTGCAACTCTGAGAGCTAGAAATTTACATGGTTCGTGCGCAAACCGAAAGGTTAAATCGTGTGGGAACTGGGGTGTACGCTTACCGTATAGGCGGATGATACGGCCTTTCGGTGTCCCCAGACACGATAGGCTAAGTGCGAGCTGCTAGTCTCCTGTTTGATTGGGGATAGGCCAACTGGAGACTTATCCCTGGGTACCCCTTTTCATCGCACGATAGACGTTCGTTGGAATCTCTAGGCAATCACTCTCATAGCTTGTCAGTAGACCCTCGCGGTACTACGCAAGCAAGCACCAGAGGGTGTTACCCAAGACGAATATTTCAATAAACCCCCACCTCATTCACCCTCGAAGACAGTATCAGCTCGTTTGTGTCTTGTAGGCCCATCGGCCCCGCGGTGGTTGTTTATAGATCAGATATACACGGCGTCCTGCTAGTTCGCTGTTACTCGGTACCTTAGGGATCGAAACGGTCAATCCCTTAGGGGCGACCGGGATTCAATCGTTGCCGCTGTAAAGTGAGATCAGGGAAGCGTGTTTACAACCTGGAAACCTACGGGTGGCATACTGTACGTGCGTCGTTGATTCCAACCCAGCGCCGGACATTAAGTTAACTGAAGCGAAAGGGGAGAGTCCACGGGATAATAGGGAGGGCTCACCGAAGTGTCTCTATAGCGAGAAGTACCAATCCACGCACCCCCAACCTGCATTGGATACGGTCAATGATTGGCATCCGATGGTTAGGGGGTATGTGGGTAATTGGACATGTTGGAGCAGTCCGAATTGCTCGGATTCTCTTTGCATATGTTGCTCACCACCTTCACAACGGTAAGGGCTTTCACGATTGCTGGGCCGGCATCTCGCCCGGGACGAAGTACCGGTTGCGATCCCATCAACACTGCTCGGCCTGAAGCACCGGCGGCGGAATCGATGATGGAAGCGTCATAAGTGCCGCAAGTGCGCACTATCACTCCTTGATTACCTCCGCCTGTTATGGTGAGCGCGATTATGTCGCCGCATACGTTATCCCTTACCACTCAAGTGCAATCGGTGAATCATATTGTGTTACAGCGCGTGTTTCAGGTTACTAAAGCGTTGCCACGGCAGTCAAGATATCGAAGCTATCCGAGCCGGTGTGCGAAAATAGAATCATTTTGGACTCCAAGGGGTGCGCTCCCTGCGGGGCAGCTCCGCACTTGTCTAACGGTTAAAGCGTGGAAGTCGTGGGCACAGTAAGCGCGGAGCTCACATCGCCCTCTAGCAATATCCATTTGGCGTCTTCGGCTATCATGTGCATCTAAATAGCGTTCTGCACATGAAAGAACCGTTAGGCAGAATCAGATCGCGCTAAAACCGGTCGCCTTTTTGGTAACGAAGTTATCAGAAACTTCGCTATCTCCCCGAATTAGGACCGGGGGGCAGCCGAGTCCAAGACGGGACAATCGAGCAGGTAAGACCCGACAGAGGACACATTACCCCGTGACATTTCGAGGCCCGGGGACGACGGGTCGCTGATAGAGTTTGAGCATTAGATTCCTCGGGTGTATACTCGTAGAGTTTATTGGACGTTGGCCACCCATAGGATCCAATTTCGCAAATGGATACTGCACTTTTGTGGTAAGCTGGCCTAAAGCACCAAGGATTTGGTCAGGGCTTCATGTACGGTCCTGACCGTAGTCGATTGGTATTTGGGTTGTTTAATGGTTGGGTTCTATCTTCCAAGTCGAAGACACGCGGATATCGAGCGCCCGTTGTGAATTCACTACGGCCAGACTCTCTCAGTCGAAGCCCTGTGCCGAGTATGTCAGGAGGAATACGACCTCTACGTACTGCCCTCCCCTGCGGTCACTATAACTTGCTGCTCGAGCTTTAAGCTACGGTAAGGTGAGGACCTTAGAGAGGGCTTTAGAGTCCAAAAATGCACGCCAGCAAACAATGAGCGCACGCAATTTTGTGGAACTAGATTAAGCCCCATCGTAAGTACTCAAGTTGGATTAGTATCTTAGCGTGGAGCATGCCTCTCAATCCGCTGCCATGTATCAGATTGCAAAAGGCACATAGGCCCACTACTCATCTGGTGCTCTCCACAGCTTTGCGGTGGCTAGACCCCAGGGTGAAATATTAACACGGTTCGCGGTCATAATACACCCTCCGGCGATCCCGACGCCAATCTGAGTTCCTTTGTTAGTCGACGACCTTACTCCGATGTGGCTTGTGCACTCGAGCACGGGTGTAGTCGGGATCTCTCATCATGGTGATAATGCACTTCCTAGCTATCGCATCCAACTGGACCCAGTAGAGCGGACCTCAAAACTCAGCACCATGTGCTCGCACATGTCGGGAAGGGGCCAACAAGTATTTACAGATTCTGAGTACATGCCCTGTGGTATAGATCATGTTCAACGGGAGCAGGATATCAAATATGATCCCCTAACGCAGAAGACCCACCCACCAAAACACAGACTCCACCGAGCAGCAATTTGGCGTGCGAGAATTGGATTAAACTGTGTGCAGTGACCATACGATGCATCCCCTTCGGGGTGCCTCAACCTAATCATCCTCGATTCAGTCATTCCAGGTCGAGGCAGACTCAGTGCTTAAGCCCGCTCGTAATGTGCGTTGTAGGAAATGAATTTGGTATACGATTATAGGAAGGTGCATCGCGTGCCACTACCTCCCGCAGTACAAGATCCTATTGGCGTGCCCCAATGTTTAGCTATCTCTACGGAAGGCCATGTGCTTACGTGAGCCTAGTAATCGTAGCCACGAGCCACTTCTGCCGCTTCGTGCTGGCCTCCTGACGGCTATGACACTATTAATTTGTCGTATTAGATTTCGCTTTTGAAAGACCCGATGCTGAGTACAGTTCGTGCCTTACACAACCGTGGCAGTCCTGTGGGAACGAAGTCCACGCCCATTACGTCATAGGATCATGAATTAGACCACCTGCAAGCGCCTTCCTAACGTTTCAATATCGATATCCTCTTAGGCCTGTGACACTACGTCTCAGCACGGATTTATTACGATATAAATCTTAGATTGGCTGGCCCAGTCCAAATCGAGTTCGGACATATCGTAGGTACGGTTCACACCTCATGCGAACACGGCTACATGCGCACCTTGTCGATAACTTTTTCATTACGAAGCGGGAGGAGGCTAATAAGGGTATACGTTTACCTTTTAGAAGGGAACAAAGGCCGCATATGGTTACAAAGGATATTCAGTAGGTATCAGGTTCAACAGATTCGTATCTTCCCGCCGTCCCGAAAAGCGTTCTTAGAGAGTGCATTGCTGAGCGACACATTGAAAACTCCTTCAGTGCGTCACTTCGGTGATGCAAATGTCTACACAATCAGGAGCGCAGTAGCTACTCACTTTAGGTCGACCTCTGGTGCGAGTGTGATGGACCTTATCATGATTTACCGACCACCCGTCCATTAGTCGGGTACCGATACCGGGTCAAACACGCCTGCGGAAATTCCTTCACTTACATTGAGGCAGTTAGATCGGGTATGTGATCGGCCTTCGATCAAGACTGGGGTGAAGTTTGCCCAGTCGAAGCGTCGCTCACGGTCCAAACCTGTCAGCCATATTTCGGGTGTGGCCCCTTTCACTTCAACTCTTAACATACTTCCTTTAGAGCCTGCCGTGTGACAGGATCATCCTGCGCTGCCGCAAGATTTGCTTTCCTACTGGACGATTGGTTTCCCTTGATGACTAATAAACCCTACCGCGTTCCACTTCGGCAGTTGAGGCAAGGGAGTTCCCCAGGGCAAGAGCGCGTTGCGACGTTTTCACTCAGGCGTGGTTCCTAATAACAGTGCGGATATGCTTCATTGTGAGTACGCGTAGAGGGTTGGCCGTCACGGGGAGTTCATCTATACTTCCTGGTCCATTACGTGTACGGCCAAGCTCGGTAGCAAAGTACGGGGGACGCACAACCCAATTGTAGACTAAACCAACTCATCAGCCTCCCAACTTGGGCCAATTTCTAAGCGTTATCACTGTTGGCCGCGCGATTGTACAAGTGCCTGCGTCGAGTGGCGTTGCAACATTACGGGTTTATGTGATCTCTGCTCTATATTGGGCTGGGACGCGCAGTTTTGAGTGGTTGCATCCCTGACCAGATTCCGAGATTGCCTTAATCGCTTCCTACTGTATTCTTTAGCCCGCTCCACGTCAAAAGGCCTTGCTACTATATATAGCCAGTCGAACTGCTAGAGCCCCAGTCTCGCATCTGTACCTAGTCCGGCTGTTATGTCGTGCTACAAAGCAGAGTTTGACCTAGGGCAAC"
#GettingRepetitive(s)
'''
	
def LinguisticComplexityOfGenome():
	print 

'''
	
def binary_search(intList, intValue, lowValue, highValue):
    if(highValue - lowValue) < 2:
        return intList[lowValue] == intValue or intList[highValue] == intValue
    middleValue = lowValue + ((highValue - lowValue)/2)
    if intList[middleValue] == intValue:
        return True
    if intList[middleValue] > intValue:
        return binary_search(intList, intValue, lowValue, middleValue - 1)
   return binary_search(intList, intValue, middleValue + 1, highValue)
   
 '''
 
def get_seq_fasta(lines):
	sequences, sequence, ids, id = [], '', {}, lines[0].split()[0][1:]
	ids[id] = 0
	for line in lines[1:]:
		if line[0] == '>':
			sequences.append(sequence)
			sequence, id = '',  line.split()[0][1:]
			ids[id] = len(sequences)
		else:
			sequence += line
	sequences.append(sequence)
	return sequences, ids

def overlap(a, b, min_length=3):
    """ Return length of longest suffix of 'a' matching
        a prefix of 'b' that is at least 'min_length'
        characters long.  If no such overlap exists,
        return 0. """
    start = 0  # start all the way at the left
    while True:
        start = a.find(b[:min_length], start)  # look for b's suffx in a
        if start == -1:  # no more occurrences to right
            return 0
        # found occurrence; check for full suffix/prefix match
        if b.startswith(a[start:]):
            return len(a)-start
        start += 1  # move just past previous match

def OverlapGraphProblem(sequences):
	sequences = list(set(sequences))
	n = len(sequences)
	edges = set([])
	for i in range(n):
		for j in range(i+1, n):
			if sequences[i][1:] == sequences[j][:-1]:
				edges.add((i, j))
			if sequences[j][1:] == sequences[i][:-1]:
				edges.add((j, i))	
	for edge in edges: #sorted(edges):
		print sequences[edge[0]] + ' -> ' + sequences[edge[1]]

'''
#lines = read_file('inpros61.txt')	
lines = read_file('rosalind_3bba.txt')	
OverlapGraphProblem(lines)
'''
	
def greedy_shortest_superstring(sequences, k = 30):

	#print(len(sequences))
	sequences = list(set(sequences)) #sorted(sequences)
	#print(len(sequences))
	
	kmers = {}
	for j in range(len(sequences)):
		sequence = sequences[j]
		for i in range(len(sequence) - k + 1):
			#kmers[sequence[i:i+k]] = kmers.get(sequence[i:i+k], set([]))
			if not sequence[i:i+k] in kmers:
				kmers[sequence[i:i+k]] = set([])
			kmers[sequence[i:i+k]].add(j)
	#print len(kmers)		

	overlaps = {}
	for i in range(len(sequences)):
		suffix = sequences[i][-k:]
		for j in kmers.get(suffix, set([])) - set([i]):
			overlap_len = overlap(sequences[i], sequences[j], k)
			if overlap_len > 0:
				overlaps[i, j] = max(overlaps.get((i, j), 0), overlap_len)

	sequences = {i:sequences[i] for i in range(len(sequences))}

	id = len(sequences)
	while len(overlaps) > 0:
		
		overlap_len, (i, j) = max([(overlaps[node_pair], node_pair) for node_pair in overlaps])
		#if sequences[i] in sequences[j]:
		#	sequences[id] = sequences[j]
		if sequences[j] in sequences[i]:
			sequences[id] = sequences[i]
		else:
			sequences[id] = sequences[i] + sequences[j][overlap_len:]	# seq i's k'-suffix = seq j's k'-prefix
		
		#print i, sequences[i], j, sequences[j], overlap_len, id
		#print i, j, overlap_len, id
		
		del sequences[i]
		del sequences[j]
		
		#del overlaps[(i, j)]
		#if (j, i) in overlaps:
		#	del overlaps[(j, i)]
		
		node_pairs = [node_pair for node_pair in overlaps if node_pair[0] == i or node_pair[0] == j or node_pair[1] == i or node_pair[1] == j]
		for node_pair in node_pairs:
			del overlaps[node_pair]
		
		for oid in sequences:
			if oid == id: 
				continue
			if sequences[oid] in sequences[id]:
				overlaps[id, oid] = len(sequences[oid])
			elif sequences[id] in sequences[oid]:
				overlaps[oid, id] = len(sequences[id])
			elif sequences[id][-k:] in sequences[oid]:
				overlaps[id, oid] = overlap(sequences[id], sequences[oid], k)
			elif sequences[oid][-k:] in sequences[id]:
				overlaps[oid, id] = overlap(sequences[oid], sequences[id], k)
				
		id += 1
		#print sequences, overlaps
		
	return ''.join(sequences.values())

'''	
lines = read_file('inp42.txt')
lines = read_file('rosalind_long.txt')
sequences, ids = get_seq_fasta(lines)
lens = [len(sequence) for sequence in sequences]
#print sum(lens) / len(lens)
print greedy_shortest_superstring(sequences, k = 200)
'''

def StringReconstructionProblem(sequences, k):
	print greedy_shortest_superstring(sequences, k / 3)

'''
lines = read_file('inpros66.txt')
lines = read_file('rosalind_3gba.txt')
k, sequences = int(lines[0]), lines[1:]
StringReconstructionProblem(sequences, k)
'''	

def GenomeAssemblywithPerfectCoverage(sequences):
	k, kmers = len(sequences[0])-1, set([])
	for i in range(len(sequences)):
		kmers.add(sequences[i][:k])
		kmers.add(sequences[i][-k:])
	print sorted(kmers)

'''
sequences = read_file('inpros80.txt')
#lines = read_file('rosalind_3gba.txt')
GenomeAssemblywithPerfectCoverage(sequences)
'''

from copy import deepcopy
def EulerCycle(nbrs, start):
	u, path = start, ''
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		#path += str(u) + '->'
		if path == '':
			path = str(u)
		else:
			path += str(u)[-1] 
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	#assert(u == start)	
	path += str(u)[-1]
	return path

def EulerTour(nbrs):
	path = ''
	#start = list(set(sum(nbrs.values(), [])) - set(nbrs.keys())) # last node
	start = list(set(nbrs.keys()) - set(sum(nbrs.values(), []))) # first node
	#print start
	u = start[0]
	while True:
		vertices = nbrs.get(u, [])
		nv = len(vertices)
		if nv == 0:
			break
		elif nv == 1:
			v = vertices[0]
		else:
			#nbrs1 = deepcopy(nbrs)
			vertices = deepcopy(nbrs.get(u, []))
			for w in vertices:
				nbrs[u].remove(w)
				count1 = reachableCount(nbrs, w)
				nbrs[u] += [w]
				count = reachableCount(nbrs, u)
				if count1 == count: # not a bridge
					v = w
					break
		if path == '':
			path = str(u)
		else:
			path += str(u)[-1]
		#print str(u) + '->' + str(v)
		vertices.remove(v)
		nbrs[u]	= vertices
		u = v
	path += str(u)[-1]
	return path
	
def constructDeBruijnGraph(strs):
	graph = {}
	for s in strs:
		graph[s[:-1]] = graph.get(s[:-1], []) + [s[1:]]
	return graph

def allKMers(str, k):
	return set([str[i:i+k] for i in range(len(str)-k+1)])

def constructDeBruijnGraph1(k):
	start = int(''.join(['1']*k))
	numbers, pow10, pow2 = set([start]), 10**k, 2**k
	s, count = start, 1
	while count < pow2:
		s *= 10
		nxt_num = s % pow10
		if nxt_num in numbers:
			s += 1
			nxt_num += 1
		#print nxt_num
		numbers.add(nxt_num)	
		count += 1
		if count % 100000 == 0:
			print count
	return s

'''	
lines = read_file('rosalind_newba3i.txt')
#k = 5 #5 #4 #3
#binstrs = ["".join(seq) for seq in itertools.product("01", repeat=k)]
#print binstrs
k, strs = int(lines[0]), lines[1:]
graph = constructDeBruijnGraph(strs) #binstrs
#graph = constructDeBruijnGraph(binstrs)
#print graph
path = EulerTour(graph) #binstrs[0]
#path = EulerCycle(graph, binstrs[0][:-1])
#path = str(constructDeBruijnGraph1(k))
print path
#path = path.replace('0->0', '0').replace('1->1', '1')
#print path
kmers = allKMers(path, k)
print kmers, len(kmers)
'''

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
#print NumberOfBreakPoints('+3 +4 +5 -12 -8 -7 -6 +1 +2 +10 +9 -11 +13 +14')
#print NumberOfBreakPoints('+1 +2 +3 +4 +5 +6 +7 +8 +9 +10 +11 +12 +13 +14 +15 +16 +17 +18 +19 +20 +21 +22 +23 +24 +25 +26 +27 -2311 -2310 -2309 -2308 -2307 -2306 -2305 -2304 -2303 -2302 -2301 -2300 -2299 -2298 -2297 -2296 -2295 -2294 -2293 -2292 -2291 -2290 -2289 -2288 -2287 -2286 -2285 -2284 -2283 -2282 -2281 -2280 -2279 -2278 -2277 -2276 -2275 -2274 -2273 -2272 -2271 -2270 -2269 -2268 -2267 -2266 -2265 +1975 +1976 +1977 +1978 +1979 +1980 +1981 +1982 +1983 +1984 +1985 +1986 +1987 +1988 +1989 +1990 +1991 +1992 +1993 +1994 +1995 +1996 +1997 +1998 +1999 +2000 +2001 +2002 +2003 +2004 +2005 +2006 +2007 +2008 +2009 +2010 +2011 +2012 +2013 +2014 +2015 +2016 +2017 +2018 +2019 +2020 +2021 +2022 +2023 +2024 +2025 +2026 +2027 +2028 +2029 +2030 +2031 +2032 +2033 +2034 +2035 +2036 +2037 +2038 +2039 +2040 +2041 +2042 +2043 +2044 +2045 +2046 +2047 +2048 +2049 +2050 +2051 +2052 +2053 +2054 +2055 +2056 +2057 +2058 +2059 +2060 +2061 +2062 +2063 +2064 +2065 +2066 +130 +131 -4231 -4230 -4229 -4228 -4227 -4226 -4225 -4224 -4223 -4222 -4221 -4220 -4219 -4218 -4217 -4216 -4215 -4214 -4213 -4212 -4211 -4210 -4209 -4208 -4207 -4206 -4205 -4204 -4203 -4202 -4201 -4200 -4199 -4198 -4197 -4196 -4195 -4194 -4193 -4192 -4191 -4190 -4189 -4188 -4187 -4186 -4185 -4184 -4183 -4182 -4181 -4180 -4179 -4178 -4177 -4176 -4175 -4174 -4173 -4172 -4171 -4170 -4169 -4168 -4167 -4166 -4165 +3923 +3924 +3925 +3926 +3927 +3928 +3929 +3930 +3931 +3932 +3933 +2169 +2170 +2171 +2172 +2173 +2174 +2175 +2176 +2177 +2178 +2179 +2180 +2181 +2182 +2183 +2184 +2185 +2186 +2187 +2188 +2189 +2190 +2191 +2192 +2193 +2194 +2195 +2196 +2197 +2198 +2199 +2200 +2201 +2202 +2203 +2204 +2205 +2206 +2207 +2208 +2209 +2210 +2211 +2212 +2213 +2214 +2215 +2216 +2217 +2218 +2219 +2220 +2221 +2222 +2223 +2224 +2225 +2226 +2227 +2228 +2229 +2230 +2231 +2232 +2233 +2234 +2235 +2236 +2237 +2238 +2239 +2240 +2241 +2242 +2243 +2244 +2245 +2246 +2247 +2248 +2249 +2250 +2251 +2252 +2253 +2254 +2255 +2256 +2257 +2258 +2259 +2260 +2261 +2262 +2263 +2264 -1974 -1973 -1972 -1971 -1970 -1969 -1968 -1967 -1966 -1965 -1964 -1963 -1962 -1961 -1960 -1959 -1958 -1957 -1956 -1955 -1954 -1953 -1952 -1951 -1950 -1949 -1948 -1947 -1946 -1945 -1944 -1943 -1942 -1941 -1940 -1939 -1938 -1937 -1936 -1935 -1934 -1933 -1932 -1931 -1930 -1929 -1928 -1927 -1306 -1305 -1304 -1303 -1302 -1301 -1300 -1299 -1298 +289 +290 +291 +292 +293 +294 +295 +296 +297 +298 +299 +300 +301 +302 +303 +304 +305 +306 +307 +308 +309 +310 +311 +312 +313 +314 +315 +316 +317 +318 +319 +320 +321 +322 +323 +324 +325 +326 +327 +328 +329 +330 +331 +332 +333 +334 +335 +336 +337 +338 +339 +340 +341 +342 +343 +344 +345 +346 +347 +348 +349 +350 +351 +352 +353 +354 +355 +356 +357 +358 +359 +360 +361 +362 +363 +364 +1201 +1202 +1203 -2470 -2469 -2468 -2467 -2466 -2465 -2464 -2463 -2462 -2461 -2460 -2459 -2458 -2457 -2456 -2455 -2454 -2453 -2452 +3569 +3570 +3571 +3572 +3573 +3574 +3575 +3576 +3577 +3578 +3579 +3580 +3581 +3582 +3583 +3584 +3585 +3586 +3587 +3588 +3589 +3590 +3591 +3592 +3593 +3594 +3595 +3596 +3597 +3598 +3599 +3600 +3601 +3602 +3603 +3604 +3605 +3606 +3607 +3608 +3609 +3610 +3611 +3612 +3613 +3614 +3615 +3616 +3617 +3618 +3619 +3620 +3621 +3622 +3623 +3624 +3625 +3626 +3627 +3628 +3629 +3630 +3631 +3632 +3633 +3634 +3635 +3636 +3637 +3638 +3639 +3640 +3641 +3642 +3643 +3644 +3645 +3646 +3647 +3648 +3120 +3121 +3122 +3123 +3124 +3125 +3126 +3127 +3128 +3129 +3130 +3131 +3132 +3133 +3134 +3135 +3136 +3137 +3138 +3139 +3140 +3141 +3142 +3143 +3144 +3145 +3146 +3147 +3148 +3149 +3150 +3151 +3152 +3153 +3154 +3155 +3156 +3157 +3158 +3159 +3160 +3161 +3162 +3163 +3164 +3165 +3166 +3167 +3168 +3169 +3170 +3171 +3172 +3173 +3174 +3175 +3176 +3177 +3178 +3179 +3180 +3181 +3182 +3183 +3184 +3185 +3186 +3187 +3188 +3189 +3190 +3191 +3192 +3193 +3194 +3195 +3196 +3197 +3198 +3199 +3200 +3201 +3202 +3203 +3204 +3205 +3206 +3207 +3208 +3209 +3210 +3211 +3212 +3213 +3214 +3215 +3216 +3217 +3218 +3219 +3220 +3221 +3222 +3223 +3224 +3225 +3226 +3227 +3228 +3229 +3230 +3231 +3232 +3233 +3234 +3235 -242 -241 -240 -239 -238 -237 -236 -235 -234 -233 -232 -231 -230 -229 -228 -227 -226 -225 -224 -223 -222 -221 -220 -219 -218 -217 -216 -215 -214 -213 -212 -211 -210 -209 -208 -207 -206 -205 -204 -203 -202 -201 -200 -199 -198 -197 -196 -195 -194 -193 -192 -191 -190 -189 -188 -187 -186 -3845 -3844 -3843 -3842 -3841 -3840 -3839 -3838 -3837 -3836 -3835 -3834 -3833 -3832 -3831 -3830 -3829 -3828 -3827 -3826 -3825 -3824 -3823 -3822 -3821 -3820 -3819 -3818 -3817 -3816 -3815 -3814 -3813 -3812 -3811 -3810 -3809 -3808 -3807 -3806 -3805 -3804 -3803 -3802 -3801 -3800 -3799 +1097 +1098 +1099 +1100 +1101 +1102 +1103 +1104 +1105 +1106 +1107 +1108 +1109 +1110 +1111 +1112 +1113 +1114 +1115 +1116 +1117 +1118 +1119 +1120 +1121 +1122 +1123 +1124 +1125 +1126 +1127 +1128 +1129 +1130 +1131 +1132 +1133 +1134 +1135 +1136 +1137 +1138 +1139 +1140 +1141 +1142 +1143 +1144 +1145 +1146 +1147 +1148 +1149 +1150 +1151 +1152 +1153 +1154 +1155 +1156 +1157 +1158 +1159 +1160 +1161 +1162 +1163 +1164 +1165 +1166 +1167 +1168 +1169 +1170 +1171 +1172 +1173 +1174 +1175 +1176 +1177 +1178 +1179 +1180 +1181 +1182 +1183 +1184 +1185 +1186 +1187 +1188 +1189 +1190 +1191 +1192 +1193 +1194 +1195 +1196 +1197 +1198 +1199 +1200 +365 +366 +367 +368 +369 +370 +371 +372 +373 +374 +375 +376 +377 +378 +379 +380 +381 +382 +383 +384 +385 +386 +387 +388 +389 +390 +391 +392 +393 +394 +395 +396 +397 +398 +399 +400 +401 +402 +403 +404 +405 +406 +407 +408 +409 +410 +411 +412 +413 +414 +415 +416 +417 +418 +419 +420 +421 +422 +423 +424 +425 +426 +427 +428 +429 +430 +431 +432 +433 +434 +435 +436 +437 +438 +439 +440 +441 +442 +443 +444 +445 +446 +447 +448 +449 +450 +451 +452 +453 +454 +455 +456 +457 +458 +459 +460 +461 +462 +463 +464 +465 +466 +467 +468 +469 +470 +471 +472 +473 +474 +475 +476 +477 +478 +479 +480 +481 +482 +483 +484 +485 +486 +487 +488 +489 +490 +491 +492 +493 +494 -3946 -3945 -3944 -3943 -3942 -3941 -3940 -3939 -3938 -3937 -3936 -3935 -3934 -2168 -2167 -2166 -2165 -2164 -2163 -2162 -2161 -2160 -2159 -2158 -2157 -2156 -2155 -2154 -2153 -2152 -2151 -2150 -2149 -2148 -2147 -2146 -2145 -2144 -2143 -2142 -2141 -2140 -2139 -2138 -2137 -2136 -2135 -2134 -2133 -2132 -2131 -2130 -2129 -2128 -2127 -2126 -2125 -2124 -2123 -2122 -2121 -2120 -2119 -2118 -2117 -2116 -2115 -2114 -2113 +2438 +2439 +2440 +2441 +2442 +2443 +2444 +2445 +2446 +2447 +2448 +2449 +2450 +2451 -3568 -3567 -3566 -3565 -3564 -3563 -3562 -3561 -3560 -3559 -3558 -3557 -3556 -3555 -3554 -3553 -3552 -3551 -3550 -3549 -3548 -3547 -3546 -3545 -3544 -3543 -3542 -3541 -3540 -3539 -3538 -3537 -3536 -3535 -3534 -3533 -3532 -3531 -3530 -3529 -3528 -3527 -3526 -3525 -3524 -3523 -3522 -3521 -3520 -3519 -3518 -3517 -3516 -3515 -3514 -3513 -3512 -3511 -3510 -3509 -3508 -3507 -3506 -3505 -3504 -3503 -3502 -3501 -3500 -3499 -3498 -3497 -3496 -3495 -3494 -3493 -3492 +1011 +1012 +1013 +1014 +1015 +1016 +1017 +1018 +1019 +1020 +1021 +1022 +1023 +1024 +1025 +1026 +1027 +1028 +1029 +1030 +1031 +1032 +1033 +1034 +1035 +1036 +1037 +1038 +1039 +1040 +1041 +1042 +1908 +1909 +1910 +1911 +1912 +1913 +1914 +1915 +1916 +1917 +1918 +1919 +1920 +1921 +1922 +1923 +1924 +1925 +1926 +1307 +1308 +1309 +1310 +1311 +1312 +1313 +1314 +1315 +1316 +1317 +1318 +1319 +1320 +1321 +1322 +1323 +1324 +1325 +1326 +1327 +1328 +1329 +1330 +1331 +1332 +1333 +1334 +1335 +1336 +1337 +1338 +1339 +1340 +1341 +1342 +1343 +1344 +1345 +1346 +1347 +1348 +1349 +1350 +1351 +1352 +1353 +1354 +1355 +1356 +1357 +1358 +1359 +1360 +1361 +1362 +1363 +1364 +1365 +1366 +1367 +1368 +1369 +1370 +1371 +1372 +1373 +1374 +1375 +1376 +1377 +1378 +1379 +1380 +1381 +1382 +1383 +1384 +1385 +1386 +1387 +1388 +1389 +1390 +1391 +1392 +1393 +1394 +1395 +1396 +1397 +1398 +1399 +1400 +1401 +1402 +1403 +1404 +1405 +1406 +1407 +1408 +1409 +1410 +1411 +1412 +1413 +1414 +1415 +1416 +3884 +3885 +3886 +3887 +3888 +3889 +3890 +3891 +3892 +3893 +3894 +3895 +3896 +3897 +3898 +3899 +3900 +3901 +3902 +3903 +3904 +3905 +3906 +3907 +3908 +3909 +3910 +3911 +3912 +3913 +3914 +3915 +3916 +3917 +3918 +3919 +3920 +3921 +3922 -4164 -4163 -4162 -4161 -4160 -4159 -4158 -4157 -4156 -4155 -4154 -4153 -4152 -4151 -4150 -4149 -4148 -4147 -4146 -4145 -4144 -4143 -4142 -4141 -4140 -4139 -4138 -4137 -4136 -2110 -2109 -2108 -2107 -2106 -2105 -3285 -3284 -3283 -3282 -3281 -3280 -3279 -3278 -3277 -3276 -3275 -3274 -3273 -3272 -3271 -3270 -3269 -3268 -3267 -3266 -3265 -3264 -3263 -3262 -3261 -3260 -3259 -3258 -3257 -3256 -3255 -3254 -3253 -3252 -3251 -3250 -3249 -3248 -3247 -3246 -3245 -3244 -3243 -3242 -3241 -3240 -3239 -3238 -3237 -3236 +243 +244 +245 +246 +247 +248 +249 +250 +251 +252 +253 +254 +255 +256 +257 +258 -2591 -2590 -2589 -2588 -2587 -2586 -2585 -2584 -2583 -2582 -2581 -2580 -2579 -2578 -2577 -2576 -2575 -2574 -2573 -2572 -2571 -2570 -2569 -2568 -2567 -2566 -2565 -2564 -2563 -2562 -2561 -2560 -2559 -2558 -2557 -2556 -2555 -2554 +1071 +1072 +1073 +1074 +1075 +1076 +1077 +1078 +1079 +1080 +1081 +1082 +1083 +1084 +1085 +1086 +1087 +1088 +1089 +1090 +1091 +1092 +1093 +1094 +1095 +1096 -3798 -3797 -3796 -3795 -3794 -3793 -3792 -3791 -3790 -3789 -3788 -3787 -3786 -3785 -3784 -3783 -3782 -3781 -3780 -3779 -3778 -3777 -3776 -3775 -3774 -3773 -3772 -3771 -3770 -3769 -3768 -3767 -3766 -3765 -3764 -3763 -3762 -3761 -3760 -3759 -3758 -3757 -3756 -3755 -3754 -3753 -3752 -3751 -3750 -3749 -3748 -3747 -3746 -3745 -3744 -3743 -3742 -3741 -3740 -3739 -3738 -3737 -3736 -3735 -3734 -3733 -3732 -3731 -3730 -3729 -3728 -3727 -3726 -3725 -3724 -3723 -3722 -3721 -3720 -3719 -3718 -3717 -3716 -3715 -3714 -3713 -3712 -3711 -3710 -3709 -3708 -3707 -3706 -3705 -3704 -3703 -3702 -3701 -3700 -3699 -3698 -3697 -3696 -3695 -3694 -3693 -3692 -3691 -3690 -3689 -3688 -3687 -3686 -3685 -3684 -3683 -3682 -3681 -3680 -3679 -3678 -3677 -3676 -3675 -3674 -3673 -3672 -3671 -3670 -3669 -3668 -3667 -3666 -3665 -3664 -3663 -3662 -3661 -3660 -3659 -3658 -3657 -3656 -3655 -3654 -3653 -3652 -3651 -3650 -3649 -3119 -3118 -3117 -3116 -3115 -3114 -3113 -3112 -3111 -3110 -3109 -3108 -3107 -3106 -3105 -3104 -3103 -3102 -3101 -3100 -3099 -3098 -3097 -3096 -3095 -3094 -3093 -3092 -3091 -3090 -3089 -3088 -3087 -3086 -3085 -3084 -3083 -3082 -3081 -3080 -3079 -3078 -3077 -3076 -3075 -3074 -3073 -3072 -3071 -3070 -3069 -3068 -3067 -3066 -3065 +3853 +3854 +3855 +3856 +3857 +3858 +3859 +3860 +3861 +3862 +3863 +3864 +3865 +3866 +3867 +3868 +3869 +3870 +3871 +3872 +3873 +3874 +3875 +3876 +3877 +3878 +3879 +3880 +3881 +3882 +3883 +1417 +1418 +1419 +1420 +1421 +1422 +1423 +1424 +1425 +1426 +1427 +1428 +1429 +1430 +1431 +1432 +1433 +1434 +1435 +1436 +1437 +1438 +1439 +1440 +1441 +1442 +1443 +1444 +1445 +1446 +1447 +1448 +1449 +1450 +1451 +1452 +1453 +1454 +1455 +1456 +1457 +1458 +1459 +1460 +1461 +1462 +1463 +1594 +1595 +1596 +1597 +1598 +1599 +1600 +1601 +1602 +1603 +1604 +1605 +1606 +1607 +1608 +1609 +1610 +1611 +1612 +1613 +1614 +1615 +1616 +1617 +1618 +1619 +1620 +1621 +1622 +1623 +1624 +1625 +1626 +1627 +1628 +1629 +1630 +1631 +1632 +1633 +1634 +1635 +1636 +1637 +1638 +1639 +1640 +1641 +1642 +1643 +1644 +1645 +1646 +1647 +1648 +1649 +1650 +1651 +1652 +1653 +1654 +1655 +1656 +1657 +1658 +1659 +1660 +1661 +1662 +1663 +1664 +1665 +1666 +1667 +1668 +1669 +1670 +1671 -3851 -3850 -3849 -3848 -3847 -3846 -185 -184 -183 -182 -181 -180 -179 -178 -177 -176 -175 -174 -173 -172 -171 -170 -169 -168 -167 -166 -165 -164 -163 -162 -161 -160 -159 -158 -157 -156 -155 -154 -153 -1818 -1817 -1816 -1815 -1814 -1813 -1812 -1811 -1810 -1809 -1808 -1807 -1806 -1805 -2553 -2552 -2551 -2550 -2549 -2548 -2547 -2546 -2545 -2544 -2543 -2542 -2541 -2540 -2539 -2538 -2537 -2536 -2535 -2534 -2533 -2532 -2531 -2530 -2529 -2528 -2527 -2526 -2525 -2524 -2523 -2522 -2521 -2520 -2519 -2518 -2517 -2516 -2515 -2514 +691 +692 +693 +694 +695 +696 +697 +698 +699 +700 +701 +702 +703 +704 +705 +706 +707 +708 +709 +710 +711 +712 +713 +714 +715 +716 +717 +718 +719 +720 +721 +722 +723 +724 +725 +726 +727 +728 +729 +730 +731 +732 +733 +734 +735 +736 +737 +738 +739 +740 +741 +742 +743 +744 +745 +746 +747 +748 +749 +750 +751 +752 +753 +754 +755 +756 +757 +758 +759 +760 +761 +762 +763 +764 +765 +766 +767 +768 +769 +770 +771 +772 +773 +774 +775 +776 +777 +778 +779 +780 +781 +782 +783 +784 +785 +786 +787 +788 +789 +790 +791 +792 +793 +794 +795 +796 +797 +798 +799 +800 +801 +802 +803 +804 +805 +806 +807 +808 +809 +810 +811 +812 +813 +814 +815 +816 +817 +818 +819 +820 +821 +822 +823 +824 +825 +826 +827 +828 +829 +830 +831 +832 +833 +834 +835 +836 +837 +838 +839 +840 +841 +842 +843 +844 +845 +846 +847 +848 +849 +850 +851 +852 +853 +854 +855 +856 +857 +858 +859 +860 +861 +862 +863 +864 +865 +866 +867 +868 +869 +870 +871 +872 +873 +874 +875 +876 +877 +878 +879 +880 +881 +882 +883 +884 +885 +886 +887 +888 +889 +890 +891 +892 +893 +894 +895 +896 +897 +898 +899 +900 +901 +902 +903 +904 +905 +906 +907 +908 +909 +910 +911 +912 +913 +914 +915 +916 +917 +918 +919 -1229 -1228 -1227 -1226 -1225 -1224 -1223 -1222 -1221 -1220 -1219 -1218 -1217 -1216 -1215 -1214 -1213 -1212 -1211 -1210 -1209 -1208 -1207 -1206 -1205 -1204 +2471 +2472 +2473 +2474 +2475 +2476 +2477 +2478 +2479 +2480 +3053 +3054 +3055 +3056 +3057 +3058 +3059 +3060 +3061 +3062 +3063 +3064 -3852 +1672 +1673 +1674 +1675 +1676 +1677 +1678 +1679 +1680 +1681 +1682 +1683 +1684 +1685 +1686 +1687 +1688 +1689 +1690 +1691 +1692 +1693 +1694 +1695 +1696 +1697 +1698 +1699 +1700 +1701 +1702 +1703 +1704 +1705 +1706 +1707 +1708 +1709 +1710 +1711 +1712 +1713 +1714 +1715 +1716 +1717 +1718 +1719 +1720 +1721 +1722 +1723 +1724 +1725 +1726 +1727 +1728 +1729 +1730 +1731 +1732 +1733 +1734 +1735 +1736 +1737 +1738 +1739 +1740 +1741 +1742 +1743 +1744 +1745 +1746 +1747 +1748 +1749 +1750 +1751 +1752 +1753 +1754 +1755 +1756 +1757 +1758 +1759 +1760 +1761 +1762 +1763 +1764 +1765 +1766 +1767 +1768 +1769 +1770 +1771 +1772 +1773 +1774 +1775 +1776 +1777 +1778 +1779 +1780 +1781 +1782 +1783 +1784 +1785 +1786 +1787 +1788 +1789 +1790 +1791 +1792 +1793 +1794 +1795 +1796 +1797 +1798 +1799 +1800 +1801 +1802 +1803 +1804 -1070 -1069 -1068 -1067 -1066 -1065 -1064 -1063 -1062 -1061 -1060 -1059 -1058 -1057 -1056 -1055 -1054 -1053 -1052 -1051 -1050 -1049 -1048 -1047 -1046 -1045 -1044 -1043 -1907 -1906 -1905 -1904 -1903 -1902 -1901 -1900 -1899 -1898 -1897 -1896 -1895 -1894 -1893 -1892 -1891 -1890 -1889 -1888 -1887 -1886 -1885 -1884 -1883 -1882 -1881 -1880 -1879 -1878 -1877 -1876 -1875 -1874 -1873 -1872 -1871 -1870 -1869 -1868 -1867 -1866 -1865 -1864 -1863 -1862 -1861 -1860 -1859 -1858 -1857 -1856 -1855 -1854 -1853 -1852 -1851 -1850 -1849 -1848 -1847 -1846 -1845 -1844 -1843 -1842 -1841 -1840 -1839 -1838 -1837 -1836 -1835 -1834 -1833 -1832 -1831 -1830 -1829 -1828 -1827 -1826 -1825 -1824 -1823 -1822 -1821 -1820 -1819 -152 -151 -150 -149 -148 -147 -146 -145 -144 -143 -142 -141 -140 -139 -138 -137 -136 -135 -134 -133 -132 +4232 +4233 +4234 +4235 +4236 +4237 +4238 +4239 +4240 -68 -67 -66 -65 -64 -63 -62 -61 -60 -59 -58 -57 -56 -55 -54 -53 -52 -51 -50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 +2312 +2313 +2314 +2315 +2316 +2317 +2318 +2319 +2320 +2321 +2322 +2323 +2324 +2325 +2326 +2327 +2328 +2329 +2330 +2331 +2332 +2333 +2334 +2335 +2336 +2337 +2338 +2339 +2340 +2341 +2342 +2343 +2344 +2345 +2346 +2347 +2348 +2349 +2350 +2351 +2352 +2353 +2354 +2355 +2356 +2357 +2358 +2359 +2360 +2361 +2362 +2363 +2364 +2365 +2366 +2367 +2368 +2369 +2370 +2371 +2372 +2373 +2374 +2375 +2376 +2377 +2378 +2379 +2380 +2381 +2382 +2383 +2384 +2385 +2386 +2387 +2388 +2389 +2390 +2391 +2392 +2393 +2394 +2395 +2396 +2397 +2398 +2399 +2400 +2401 +2402 +2403 +2404 +2405 +2406 +2407 +2408 +2409 +2410 +2411 +2412 +2413 +2414 +2415 +2416 +2417 +2418 +2419 +2420 +2421 +2422 +2423 +2424 +2425 +2426 +2427 +2428 +2429 +2430 +2431 +2432 +2433 +2434 +2435 +2436 +2437 -2112 -2111 -4135 -4134 -4133 -4132 -4131 -4130 -4129 -4128 -4127 -4126 -4125 -4124 -4123 -4122 -4121 -4120 -4119 -4118 -4117 -4116 -4115 -4114 -4113 -4112 -4111 -4110 -4109 -4108 -4107 -4106 -4105 +4024 +4025 +4026 +4027 +4028 +4029 +4030 +4031 +4032 +4033 +4034 +4035 +4036 +4037 +4038 +4039 +4040 +4041 +4042 +4043 +4044 +4045 +4046 +4047 +4048 +4049 +4050 +4051 +4052 +4053 +4054 +4055 +4056 +4057 +4058 +4059 +4060 +4061 +4062 +4063 +4064 +4065 +4066 +4067 +4068 +4069 +4070 +4071 +4072 +4073 +4074 +4075 +4076 +4077 +4078 +4079 +4080 +4081 +4082 +4083 +4084 +4085 +4086 +4087 +4088 +4089 +4090 +4091 +4092 +4093 +4094 +4095 +4096 +4097 +4098 +4099 +4100 +4101 +4102 +4103 +4104 -4023 -4022 -4021 -4020 -4019 -4018 -4017 -4016 -4015 -4014 -4013 -4012 -4011 -4010 -4009 -4008 -4007 -4006 -4005 -4004 -4003 -4002 -4001 -4000 -3999 -3998 -3997 -3996 -3995 -3994 -3993 -3992 -3991 -3990 -3989 -3988 -3987 -3986 -3985 -3984 -3983 -3982 -3981 -3980 -3979 -3978 -3977 -3976 -3975 -3974 -3973 -3972 -3971 -3970 -3969 -3968 -3967 -3966 -3965 -3964 -3963 -3962 -3961 -3960 -3959 -3958 -3957 -3956 -3955 -3954 -3953 -3952 -3951 -3950 -3949 -3948 -3947 +495 +496 +497 +498 +499 +500 +501 +502 +503 +504 +505 +506 +507 +508 +509 +510 +511 +512 +513 +514 +515 +516 +517 +518 +519 +520 +521 +522 +523 +524 +525 +526 +527 +528 +529 +530 +531 +532 +533 +534 +535 +536 +537 -610 -609 -608 -607 -606 -605 -604 -603 -602 -601 -600 -599 -598 -597 -596 -595 -594 -593 -592 -591 -590 -589 -588 -587 -586 -585 -584 -583 -582 -581 -580 -579 -578 -577 -576 -575 -574 -573 -572 -571 -570 -569 -568 -567 -566 -565 -564 -1493 -1492 -1491 -1490 -1489 -1488 -1487 -1486 -1485 -1484 -1483 -1482 -1481 -1480 -1479 -1478 -1477 -1476 -1475 -1474 -1473 -1472 -1471 -1470 -1469 -1468 -1467 -1466 -1465 -1464 -1593 -1592 -1591 -1590 -1589 -1588 -1587 -1586 -1585 -1584 -1583 -1582 -1581 -1580 -1579 -1578 -1577 -1576 -1004 -1003 -1002 -1001 -1000 -999 -998 -997 -996 -995 -994 -993 -992 -991 -990 -989 -988 -987 -986 -985 -984 -983 -982 -981 -980 -979 -978 -977 -976 -975 -974 -973 -972 -971 -970 -969 -968 -967 -966 -965 -964 -963 -962 -961 -960 -959 -958 -957 -956 -955 -954 -953 -952 -951 -950 -949 -948 -947 -946 -945 -944 -943 -942 -941 -940 -939 -938 -937 -936 -935 -934 -933 -932 -931 -930 -929 -928 -927 -926 -925 -924 -923 -922 -921 -920 +1230 +1231 +1232 +1233 +1234 +1235 +1236 +1237 +1238 +1239 +1240 +1241 +1242 +1243 +1244 +1245 +1246 +1247 +1248 +1249 +1250 +1251 +1252 +1253 +1254 +1255 +1256 +1257 +1258 +1259 +1260 +1261 +1262 +1263 +1264 +1265 +1266 +1267 +1268 +1269 +1270 +1271 +1272 +1273 +1274 +1275 +1276 +1277 +1278 +1279 +1280 +1281 +1282 +1283 +1284 +1285 +1286 +1287 +1288 +1289 +1290 +1291 +1292 +1293 +1294 +1295 +1296 +1297 -288 -287 -286 -285 -284 -283 -282 -281 -280 -279 -278 -277 -276 -275 -274 -273 -272 -271 -270 -269 -268 -267 -266 -265 -264 -263 -262 -261 -260 -259 +2592 +2593 +2594 +2595 +2596 +2597 +2598 +2599 +2600 +2601 +2602 +2603 +2604 +2605 +2606 +2607 +2608 +2609 +2610 +2611 +2612 -2643 -2642 -2641 -2640 -2639 -2638 -2637 -2636 -2635 -2634 -2633 -2632 -2631 -2630 -2629 -2628 -2627 -2626 -2625 -2624 -2623 -2622 -2621 -2620 -2619 -2618 -2617 -2616 -2615 -2614 -2613 +2644 +2645 +2646 +2647 +2648 +2649 +2650 +2651 +2652 +2653 +2654 +2655 +2656 +2657 +2658 +2659 +2660 +2661 +2662 +2663 +2664 +2665 +2666 +2667 +2668 +2669 +2670 +2671 +2672 +2673 +2674 +2675 +2676 +2677 +2678 +2679 +2680 +2681 +2682 +2683 +2684 +2685 +2686 +2687 +2688 +2689 +2690 +2691 +2692 +2693 +2694 +2695 +2696 +2697 +2698 +2699 +2700 +2701 +2702 +2703 +2704 +2705 +2706 +2707 +2708 +2709 +2710 +2711 +2712 +2713 +2714 +2715 +2716 +2717 +2718 +2719 +2720 +2721 +2722 +2723 +2724 +2725 +2726 +2727 +2728 +2729 +2730 +2731 +2732 +2733 +2734 +2735 +2736 +2737 +2738 +2739 +2740 +2741 +2742 +2743 +2744 +2745 +2746 +2747 +2748 +2749 +2750 +2751 +2752 +2753 +2754 +2755 +2756 +2757 +2758 +2759 +2760 +2761 +2762 +2763 +2764 +2765 +2766 +2767 +2768 +2769 +2770 +2771 +2772 +2773 +2774 +2775 +2776 +2777 +2778 +2779 +2780 +2781 +2782 +2783 +2784 +2785 +2786 +2787 +2788 +2789 +2790 +2791 +2792 +2793 +2794 +2795 +2796 +2797 +2798 +2799 +2800 +2801 +2802 +2803 +2804 +2805 +2806 +2807 +2808 +2809 +2810 +2811 +2812 +2813 +2814 +2815 +2816 +2817 +2818 +2819 +2820 +2821 +2822 +2823 +2824 +2825 +2826 +2827 +2828 +2829 +2830 +2831 +2832 +2833 +2834 +2835 +2836 +2837 +2838 +2839 +2840 +2841 +2842 +2843 +2844 +2845 +2846 +2847 +2848 +2849 +2850 +2851 +2852 +2853 +2854 +2855 +2856 +2857 +2858 +2859 +2860 +2861 +2862 +2863 +2864 +2865 +2866 +2867 +2868 +2869 +2870 +2871 +2872 +2873 +2874 +2875 +2876 +2877 +2878 +2879 +2880 +2881 +2882 +2883 +2884 +2885 +2886 +2887 +2888 +2889 +2890 +2891 +2892 +2893 +2894 +2895 +2896 +2897 +2898 +2899 +2900 +2901 +2902 +2903 +2904 +2905 +2906 +2907 +2908 +2909 +2910 +2911 +2912 +2913 +2914 +2915 +2916 +2917 +2918 +2919 +2920 +2921 +2922 +2923 +2924 +2925 +2926 +2927 +2928 +2929 +2930 +2931 +2932 +2933 +2934 +2935 +2936 +2937 +2938 +2939 +2940 +2941 +2942 +2943 +2944 +2945 +2946 +2947 +2948 +2949 +2950 +2951 +2952 +2953 +2954 +2955 +2956 +2957 +2958 +2959 +2960 +2961 +2962 +2963 +2964 +2965 +2966 +2967 +2968 +2969 +2970 +2971 +2972 +2973 +2974 +2975 +2976 +2977 +2978 +2979 +2980 +2981 +2982 +2983 +2984 +2985 +2986 +2987 +2988 +2989 +2990 +2991 +2992 +2993 +2994 +2995 +2996 +2997 +2998 +2999 +3000 +3001 +3002 +3003 +3004 +3005 +3006 +3007 +3008 +3009 +3010 +3011 +3012 +3013 +3014 +3015 +3016 +3017 +3018 +3019 +3020 +3021 +3022 +3023 +3024 +3025 +3026 +3027 +3028 +3029 +3030 +3031 +3032 +3033 +3034 +3035 +3036 +3037 +3038 +3039 +3040 +3041 +3042 +3043 +3044 +3045 +3046 +3047 +3048 +3049 +3050 +3051 +3052 +2481 +2482 +2483 +2484 +2485 +2486 +2487 +2488 +2489 +2490 +2491 +2492 +2493 +2494 +2495 +2496 +2497 +2498 +2499 +2500 +2501 +2502 +2503 +2504 +2505 +2506 +2507 +2508 +2509 +2510 +2511 +2512 +2513 -690 -689 -688 -687 -686 -685 -684 -683 -682 -681 -680 -679 -678 -677 -676 -675 -674 -673 -672 -671 -670 -669 -668 -667 -666 -665 -664 -663 -662 -661 -660 -659 -658 -657 -656 -655 -654 -653 -652 -651 -650 -649 -648 -647 -646 -645 -644 -643 -642 -641 -640 -639 -638 -637 -636 -635 -634 -633 -632 -631 -630 -629 -628 -627 -626 -625 -624 -623 -622 -621 -620 -619 -618 -617 -616 -615 -614 -613 -612 -611 +538 +539 +540 +541 +542 +543 +544 +545 +546 +547 +548 +549 +550 +551 +552 +553 +554 +555 +556 +557 +558 +559 +560 +561 +562 +563 +1494 +1495 +1496 +1497 +1498 +1499 +1500 +1501 +1502 +1503 +1504 +1505 +1506 +1507 +1508 +1509 +1510 +1511 +1512 +1513 +1514 +1515 +1516 +1517 +1518 +1519 +1520 +1521 +1522 +1523 +1524 +1525 +1526 +1527 +1528 +1529 +1530 +1531 +1532 +1533 +1534 +1535 +1536 +1537 +1538 +1539 +1540 +1541 +1542 +1543 +1544 +1545 +1546 +1547 +1548 +1549 +1550 +1551 +1552 +1553 +1554 +1555 +1556 +1557 +1558 +1559 +1560 +1561 +1562 +1563 +1564 +1565 +1566 +1567 +1568 +1569 +1570 +1571 +1572 +1573 +1574 +1575 +1005 +1006 +1007 +1008 +1009 +1010 -3491 -3490 -3489 -3488 -3487 -3486 -3485 -3484 -3483 -3482 -3481 -3480 -3479 -3478 -3477 -3476 -3475 -3474 -3473 -3472 -3471 -3470 -3469 -3468 -3467 -3466 -3465 -3464 -3463 -3462 -3461 -3460 -3459 -3458 -3457 -3456 -3455 -3454 -3453 -3452 -3451 -3450 -3449 -3448 -3447 -3446 -3445 -3444 -3443 -3442 -3441 -3440 -3439 -3438 -3437 -3436 -3435 -3434 -3433 -3432 -3431 -3430 -3429 -3428 -3427 -3426 -3425 -3424 -3423 -3422 -3421 -3420 -3419 -3418 -3417 -3416 -3415 -3414 -3413 -3412 -3411 -3410 -3409 -3408 -3407 -3406 -3405 -3404 +3321 +3322 +3323 +3324 +3325 +3326 +3327 +3328 +3329 +3330 +3331 +3332 +3333 +3334 +3335 +3336 +3337 +3338 +3339 +3340 +3341 +3342 +3343 +3344 +3345 +3346 +3347 +3348 +3349 +3350 +3351 +3352 +3353 +3354 +3355 +3356 +3357 +3358 +3359 +3360 +3361 +3362 +3363 +3364 +3365 +3366 +3367 +3368 +3369 +3370 +3371 +3372 +3373 +3374 +3375 +3376 +3377 +3378 +3379 +3380 +3381 +3382 +3383 +3384 +3385 +3386 +3387 +3388 +3389 +3390 +3391 +3392 +3393 +3394 +3395 +3396 +3397 +3398 +3399 +3400 +3401 +3402 +3403 -3320 -3319 -3318 -3317 -3316 -3315 -3314 -3313 -3312 -3311 -3310 -3309 -3308 -3307 -3306 -3305 -3304 -3303 -3302 -3301 -3300 -3299 -3298 -3297 -3296 -3295 -3294 -3293 -3292 -3291 -3290 -3289 -3288 -3287 -3286 -2104 -2103 -2102 +121 +122 +123 +124 +125 +126 +127 +128 +129 +2067 +2068 +2069 +2070 +2071 +2072 +2073 +2074 +2075 +2076 +2077 +2078 +2079 +2080 +2081 +2082 +2083 +2084 +2085 +2086 +2087 +2088 +2089 +2090 +2091 +2092 +2093 +2094 +2095 +2096 +2097 +2098 +2099 +2100 +2101 -120 -119 -118 -117 -116 -115 -114 -113 -112 -111 -110 -109 -108 -107 -106 +82 +83 +84 +85 +86 +87 +88 +89 +90 +91 +92 +93 +94 +95 +96 +97 +98 +99 +100 +101 +102 +103 +104 +105 -81 -4248 -4247 -4246 -4245 -4244 -4243 -4242 -4241 +69 +70 +71 +72 +73 +74 +75 +76 +77 +78 +79 +80 +4249 +4250 +4251 +4252 +4253 +4254 +4255 +4256 +4257 +4258 +4259 +4260 +4261 +4262 +4263 +4264 +4265 +4266')

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

'''
pat = '(\d+)->(\d+):(\d+)'
#lines = read_file("inp.txt")
#lines = read_file("Distance_Between_Leaves_inp.txt")
lines = read_file("rosalind_ba7a.txt")
n = int(lines[0])
alist = {}
for line in lines[1:]:
	m = re.match(pat, line)
	u, v, w = int(m.group(1)), int(m.group(2)), int(m.group(3))
	alist[u] = alist.get(u, []) + [(v, w)]

#print n, alist	
DistancesBetweenLeaves(n, alist)
'''

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
lines = read_file("inp1_2.txt")
#lines = read_file("rosalind_ba7b.txt")
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

'''	
#lines = read_file("inp4.txt")
#lines = read_file("Additive_Phylogeny.txt")
lines = read_file("rosalind_ba7c.txt")
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
'''

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
lines = read_file("inp7_1.txt")
#lines = read_file("UPGMA.txt")
#lines = read_file("rosalind_ba7d.txt")
n = int(lines[0])
D, i = {}, 0
for line in lines[1:]:
	dists = map(int, str.split(line))
	for j in range(n): D[i, j] = dists[j]
	i += 1
#print D

print dist([0, 2], [1, 3], D)

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

'''	
#lines = read_file("inp10.txt")
#lines = read_file("Neighbor_Joining.txt")
lines = read_file("rosalind_ba7e.txt")
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
'''

def dist(Data, i, j, n):
	return sum([(Data[i][k] - Data[j][k])**2 for k in range(n)]) 

def FarthestFirstTraversal(Data, k, m, n):
	#DataPoint <- an arbitrary point from Data
	#Centers <- the set consisting of the single point DataPoint 
	Centers = [0]
	while len(Centers) < k: 
		#DataPoint <- the point in Data maximizing d(DataPoint, Centers) 
		dmax, imax = -1, -1 
		for i in range(m):
			if i in Centers: continue
			d, c = min([(dist(Data, i, j, n), j) for j in Centers])
			if d > dmax: dmax, imax = d, i	
		#add DataPoint to Centers 
		Centers.append(imax)
	return [Data[c] for c in Centers]

'''	
lines = read_file("inp11.txt")
lines = read_file("rosalind_ba8a.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
for DataPoint in FarthestFirstTraversal(Data, k, m, n):
	print ' '.join(map(str, DataPoint))
'''

import math
def dist1(DataPoint1, DataPoint2, n):
	return sum([(DataPoint1[k] - DataPoint2[k])**2 for k in range(n)])

def SquaredErrorDistortion(Data, Centers, k, m, n):
	SSE = 0
	for i in range(m):
		d = min([dist1(Data[i], Centers[j], n) for j in range(len(Centers))])
		SSE += d
	return (1.0  * SSE) / m

'''
#lines = read_file("inp12.txt")
lines = read_file("rosalind_ba8b.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data, Centers = [], []
for line in lines[1:1+k]:
	Centers.append(map(float, str.split(line)))
for line in lines[1+k+1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
print SquaredErrorDistortion(Data, Centers, k, m, n)
'''

from copy import deepcopy
def centroid(D, C, n):
	c = [0.0 for i in range(n)]
	for j in range(n):
		for p in C:
			c[j] += Data[p][j]
	return [x / len(C) for x in c]		

def LloydAlgorithm(Data, k, m, n):
	Data_Center = {i:i for i in range(k)}
	Centers = [[i] for i in range(k)]
	max_iter = 100 #00
	for iter in range(max_iter):
		#print Centers
		#print [centroid(Data, Centers[j], n) for j in range(k)]
		changed, Temp_Centers = False, deepcopy(Centers)
		for i in range(m):
			prevc = Data_Center.get(i, None)
			d, c = min([(dist1(Data[i], centroid(Data, Centers[j], n), n), j) for j in range(k)])
			#print 'Assigned point', i, 'to cluster', c
			if prevc != c:
				if prevc != None: Temp_Centers[prevc].remove(i)
				Temp_Centers[c].append(i)
				Data_Center[i] = c
				changed = True
		if not changed: break		
		Centers = Temp_Centers	
	return [centroid(Data, Centers[j], n) for j in range(k)]

'''	
#lines = read_file("inp13.txt")
#lines = read_file("Lloyd.txt")
lines = read_file("rosalind_ba8c.txt")
k, n = map(int, str.split(lines[0]))
#Data = np.zeros((m, n))
Data = []
for line in lines[1:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
#print Data
for center in LloydAlgorithm(Data, k, m, n):
	print ' '.join(map(str, center))
'''

import numpy as np
from math import exp

def dist2(d1, d2, n):
	return sqrt(dist1(d1, d2, n))
	
def ExpectationMaximization(Data, k, m, n, beta):

	x = np.array([Data[i,:] for i in range(k)])
	#print x
	for iter in range(100):
		#Centers to Soft Clusters (E-step): After centers have been selected, assign each data point a 'responsibility' value for each cluster, 
		#where higher values correspond to stronger cluster membership. 
		Z = [sum([exp(-beta * dist2(Data[j,:], x[i,:], n)) for i in range(k)]) for j in range(m)]
		HiddenMatrix = np.array([[exp(-beta * dist1(Data[j,:], x[i,:], n)) / Z[j] for i in range(k)] for j in range(m)]).T
		#Soft Clusters to Centers (M-step): After data points have been assigned to soft clusters, compute new centers.
		x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
		#print x
	for i in range(k):
		print ' '.join(map(str, x[i,:]))

'''
lines = read_file("inp14.txt")
#lines = read_file("dataset_10933_7.txt")
k, n = map(int, str.split(lines[0]))
beta = float(lines[1])
Data = []
for line in lines[2:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
#print Data
#print k, m, n, beta
ExpectationMaximization(Data, k, m, n, beta)
'''

def dist(C1, C2, D):

	DC1C2 = 0
	for i in C1:
		for j in C2:
			DC1C2 += D[i,j]
	DC1C2 /= (1.0 * len(C1) * len(C2))
	return DC1C2
	
def HierarchicalClustering(D, n):
	#Clusters = n single-element clusters labeled 1, ... , n 
	#construct a graph T with n isolated nodes labeled by single elements 1, ... , n 
	#while there is more than one cluster 
	#find the two closest clusters Ci and Cj 
	#merge Ci and Cj into a new cluster Cnew with |Ci| + |Cj| elements
	#add a new node labeled by cluster Cnew to T
	#connect node Cnew to Ci and Cj by directed edges
	#remove the rows and columns of D corresponding to Ci and Cj
	#remove Ci and Cj from Clusters
	#add a row/column to D for Cnew by computing D(Cnew, C) for each C in Clusters 
	#add Cnew to Clusters 
	#assign root in T as a node with no incoming edges
	#return T 
	clusters, T = {}, {i:[] for i in range(n)}
	for i in range(n): clusters[i] = [i]
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
		print ' '.join(map(str, [c + 1 for c in clusters[id]]))
		T[id] = [i, j]
		T[i] = T.get(i, []) + [id]
		T[j] = T.get(j, []) + [id]
		#print 'merging', i, j
		D[id, id] = 0
		for m in cids:
			if m == i or m == j or m == id: continue
			D[m, id] = D[id, m] = dist(clusters[id], clusters[m], D)
		cids += [id]
		#remove rows and columns of D corresponding to C1 and C2
		del clusters[i]
		del clusters[j]
		#for p in cids:
		#	for q in cids:
		#		if (p == i or p == j or q == i or q == j) and (p, q) in D: del D[p, q]
		cids.remove(i)
		cids.remove(j)
	
	return T

'''	
#lines = read_file("inp15.txt")
lines = read_file("rosalind_ba8e.txt")
n = int(lines[0])
D, i = {}, 0
for line in lines[1:]:
	dists = map(float, str.split(line))
	for j in range(n): D[i, j] = dists[j]
	i += 1
#print D

T = HierarchicalClustering(D, n)
#for node1, node2  in sorted(T):
#	print node1, '->', node2, ':', T[node1, node2]
'''

def HMMParameterEstimation(x, alphabet, path, states):
	transition = {}
	for i in range(len(path) - 1):
		transition[path[i], path[i + 1]] = transition.get((path[i], path[i + 1]), 0) + 1.0
	#print transition
	Z = {state1:sum([transition.get((state1, state2), 0) for state2 in states]) for state1 in states}
	#print Z
	#transition = {(state1, state2):transition.get((state1, state2), 0) / Z[state1] if Z[state1] else 1.0 / len(states)  for (state1, state2) in transition}	
	#print transition
	print ' ' + ' '.join(states)
	for state1 in states:
		string = state1
		for state2 in states:
			transition[state1, state2] = transition.get((state1, state2), 0.0) / Z[state1] if Z[state1] else 1.0 / len(states)
			string += ' ' + str(transition[state1, state2])
		print string
	print '--------'
	emission = {}
	for i in range(len(x)):
		emission[path[i], x[i]] = emission.get((path[i], x[i]), 0) + 1.0
	Z = {state:sum([emission.get((state, symbol), 0) for symbol in alphabet]) for state in states}
	#emission = {(state, symbol):emission.get((state, symbol), 0) / Z[state] if Z[state] else 1.0 / len(alphabet) for (state, symbol) in emission}	
	print ' ' + ' '.join(alphabet)
	for state in states:
		string = state
		for symbol in alphabet:
			emission[state, symbol] = emission.get((state, symbol), 0.0) / Z[state] if Z[state] else 1.0 / len(alphabet)
			string += ' ' + str(emission[state, symbol])
		print string	
	return transition, emission

'''	
#lines = read_file("inp32.txt")
#lines = read_file("HMMParameterEstimation.txt")
lines = read_file("rosalind_ba10h.txt")
x = lines[0]
alphabet = str.split(lines[2])
path = lines[4]
states = str.split(lines[6])
#print x
#print alphabet
#print path
#print states
HMMParameterEstimation(x, alphabet, path, states)
'''

def ViterbiDecoding(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * 1 * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = max([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	ssink, state = max([(s[statel, n - 1], statel) for statel in states])
	path = state
	i = n - 2
	while i >= 0:
		smax, state = max([(s[statel, i] * transition[statel, state], statel) for statel in states])
		path = state + path
		i -= 1
	return path
	
def ViterbiLearningForEstimatingParametersOfHMM(niter, x, alphabet, states, transition, emission):
	for i in range(niter):
		path = ViterbiDecoding(x, states, transition, emission)
		#print path
		transition, emission = HMMParameterEstimation(x, alphabet, path, states)
		#print 'here1', transition
		#print 'here2', emission

'''		
#lines = read_file("inpros87.txt")
#lines = read_file("ViterbiLearning.txt")
#lines = read_file("rosalind_ba10i.txt")
niter = int(lines[0])
x = lines[2]
alphabet = str.split(lines[4])
states = str.split(lines[6])
transition, emission = {}, {}
i = 0
for line in lines[9:9+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[9+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(alphabet)):
		emission[states[i], alphabet[j]] = probs[j]
	i += 1
print x
print alphabet
print states
print transition
print emission
ViterbiLearningForEstimatingParametersOfHMM(niter, x, alphabet, states, transition, emission)	
'''

def forward(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = sum([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	s['sink'] = sum([s[statel, n - 1] for statel in states])
	#print s['sink']
	return s
	
def backward(x, states, transition, emission):
	
	s, n = {}, len(x)
	for state in states:
		s[state, n - 1] = 1
	for i in range(n - 2, -1, -1):
		for state in states:
			s[state, i] = sum([s[statel, i + 1] * transition[state, statel] * emission[statel, x[i + 1]] for statel in states])			

	return s

def HMMSoftDecodingProblem(x, states, transition, emission):
	pforward = forward(x, states, transition, emission)
	pbackward = backward(x, states, transition, emission)
	print ' ' + ' '.join(states)
	for i in range(len(x)):
		print ' '.join(map(str, [pforward[state, i] * pbackward[state, i] / pforward['sink'] for state in states]))

'''	
lines = read_file("inp34.txt")
lines = read_file("SoftDecoding.txt")
lines = read_file("rosalind_ba10j.txt")
x = lines[0]
symbols = str.split(lines[2])
states = str.split(lines[4])
transition, emission = {}, {}
i = 0
for line in lines[7:7+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[7+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
#initial = {state: 1.0 / len(states) for state in states}	
#print x
#print transition
#print emission
#print initial
HMMSoftDecodingProblem(x, states, transition, emission)
'''

def ProbabilityHiddenPath(path, transition, initial):

	prob = initial
	for i in range(len(path) - 1):
		prob *= transition[path[i], path[i + 1]]
	return prob

'''	
lines = read_file("inp24.txt")
lines = read_file("ProbabilityOfHiddenPath.txt")
lines = read_file("rosalind_ba10a.txt")
path = lines[0]
symbols = str.split(lines[2])
transition = {}
i = 0
for line in lines[5:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		transition[symbols[i], symbols[j]] = probs[j]
	i += 1
initial = 0.5
#print path
#print transition
#print initial
print ProbabilityHiddenPath(path, transition, initial)
'''

def ViterbiDecoding(x, states, transition, emission, initial):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * initial[state] * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = max([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	ssink, state = max([(s[statel, n - 1], statel) for statel in states])
	path = state
	i = n - 2
	while i >= 0:
		smax, state = max([(s[statel, i] * transition[statel, state], statel) for statel in states])
		path = state + path
		i -= 1
	print path

'''	
lines = read_file("inp26.txt")
lines = read_file("ViterbiAlgorithm.txt")
lines = read_file("rosalind_ba10c.txt")
x = lines[0]
symbols = str.split(lines[2])
states = str.split(lines[4])
transition, emission = {}, {}
i = 0
for line in lines[7:7+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[7+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
initial = {state: 1.0 / len(states) for state in states}	
#print x
#print transition
#print emission
#print initial
ViterbiDecoding(x, states, transition, emission, initial)
'''

def OutcomeLikelihood(x, states, transition, emission, initial):
	
	s, n = {}, len(x)
	for state in states:
		s[state, 0] = 1 * initial[state] * emission[state, x[0]]
	for i in range(1, n):
		for state in states:
			s[state, i] = sum([s[statel, i - 1] * transition[statel, state] * emission[state, x[i]] for statel in states])			
	ssink = sum([s[statel, n - 1] for statel in states])
	print ssink
	
'''
lines = read_file("inp27.txt")
lines = read_file("OutcomeLikelihood.txt")
lines = read_file("rosalind_ba10d.txt")
x = lines[0]
symbols = str.split(lines[2])
states = str.split(lines[4])
transition, emission = {}, {}
i = 0
for line in lines[7:7+len(states)]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(states)):
		transition[states[i], states[j]] = probs[j]
	i += 1
i = 0
for line in lines[7+len(states)+2:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
initial = {state: 1.0 / len(states) for state in states}	
#print x
#print transition
#print emission
#print initial
OutcomeLikelihood(x, states, transition, emission, initial)
'''

def ProbabilityOutcomeHiddenPath(path, hiddenpath, emission):
	
	prob = 1
	for i in range(len(path)):
		prob *= emission[hiddenpath[i], path[i]]
	return prob

'''	
lines = read_file("inp25.txt")
lines = read_file("ProbabilityOfOutcomeGivenHiddenPath.txt")
lines = read_file("rosalind_ba10b.txt")
path = lines[0]
symbols = str.split(lines[2])
hiddenpath = lines[4]
states = str.split(lines[6])
emission = {}
i = 0
for line in lines[9:]:
	probs = map(float, str.split(line)[1:])
	for j in range(len(symbols)):
		emission[states[i], symbols[j]] = probs[j]
	i += 1
	
print path
print hiddenpath
print emission
print ProbabilityOutcomeHiddenPath(path, hiddenpath, emission)
'''

def ProfileHMM(threshold, alphabet, alignments):
	
	nrow, ncol = len(alignments), len(alignments[0])
	transition, emission = {}, {}
	
	inscols = []
	for i in range(ncol):
		count = {a:0 for a in alphabet + ['-']}
		for j in range(nrow):
			count[alignments[j][i]] += 1
		#fracins = sum([1.0 for j in range(nrow) if alignments[j][i] == '-']) / nrow
		fracins = count['-'] / (1.0 * nrow)
		#print i, count['-'], nrow, fracins
		if fracins >= threshold:
			inscols += [i]
	#print inscols
	
	transtrs = []
	for i in range(nrow):
		curstate, nextstate, transtr = 'S', None, 'S'
		ii, im, id = 0, 1, 1
		for j in range(ncol):
			if not j in inscols:
				nextstate = 'D' + str(id) if alignments[i][j] == '-' else 'M' + str(im)
				#im, id = im + 1, id + 1
				ii = im
				id = im = im + 1
			else:
				#ii = im
				if alignments[i][j] == '-':
					continue
				else:
					nextstate = curstate if curstate[0] == 'I' else 'I' + str(ii)
			#if curstate != nextstate:	ii += 1
			transition[curstate, nextstate] = transition.get((curstate, nextstate), 0) + 1
			if alignments[i][j] != '-':
				emission[nextstate, alignments[i][j]] = emission.get((nextstate, alignments[i][j]), 0) + 1
			transtr += '->' + nextstate
			curstate = nextstate
		transtr += '->E'
		#print 'here', curstate
		nextstate = 'E'
		transition[curstate, nextstate] = transition.get((curstate, nextstate), 0) + 1
				
		transtrs.append(transtr)	
		#print alignments[i]
		#print transtr
		
	states = ['S']
	i, j, k = 0, 1, 1
	while j < im:
		states += ['I' + str(i)]
		i += 1
		states += ['M' + str(j)]
		j += 1
		states += ['D' + str(k)]
		k += 1
	states += ['I' + str(i)]
	#if i < ii:
	#	states += ['I' + str(i+1)]
	states += ['E']
	#print states
	#print transition
	#print emission
	
	#print states
	for state in states:
		#print state, {nextstate: transition[curstate, nextstate] for (curstate, nextstate) in transition if curstate == state}
		transfromstate = {nextstate: transition[curstate, nextstate] for (curstate, nextstate) in transition if curstate == state}
		totaltransfromstate = 1.0 * sum([transfromstate[nextstate] for nextstate in transfromstate])
		transfromstate = {nextstate: round(transfromstate[nextstate] / totaltransfromstate, 3) for nextstate in transfromstate}
		for nextstate in transfromstate:
			transition[state, nextstate] = transfromstate[nextstate]
	#print transition
	
	for state in states:
		#print state, {symbol: emission[curstate, symbol] for (curstate, symbol) in emission if curstate == state}
		emitfromstate = {symbol: emission[curstate, symbol] for (curstate, symbol) in emission if curstate == state}
		totalemitfromstate = 1.0 * sum([emitfromstate[symbol] for symbol in emitfromstate])
		emitfromstate = {symbol: round(emitfromstate[symbol] / totalemitfromstate, 3) for symbol in emitfromstate}
		for symbol in emitfromstate:
			emission[state, symbol] = emitfromstate[symbol]
	#print emission
	
	print '  ' + ' '.join(states)
	for state in states:
		line = state
		for state1 in states:
			line += ' ' + str(transition.get((state, state1), 0))
		print line		
	print '--------'
	print '  ' + ' '.join(alphabet)
	for state in states:
		line = state
		for symbol in alphabet:
			line += ' ' + str(emission.get((state, symbol), 0))
		print line		
		
	return states, transition, emission

'''
lines = read_file("inp28.txt")
#lines = read_file("ProfileHMM.txt")
lines = read_file("rosalind_ba10e.txt")
threshold = float(lines[0])
alphabet = str.split(lines[2])
alignments = lines[4:]
#print threshold
#print alphabet
#print alignments
ProfileHMM(threshold, alphabet, alignments)
'''

def NormalizeSmooth(vec, pseudocount):
	n, tot = len(vec), sum(vec)
	return [round((vec[i] + pseudocount) / (tot + n*pseudocount), 3) for i in range(n)]

def ProfileHMMWithPseudocounts(threshold, alphabet, alignment, pseudocount):
	states, transition, emission = ProfileHMM(threshold, alphabet, alignment)
	#ins = [state for state in states if state[0] == 'I']
	n = len(states)
	for i in range(n - 1):
		if states[i] == 'S':
			nextstates = ['I0', 'M1', 'D1']
		elif i >= n - 4 and i <= n - 2:
			num = int(states[i][1])
			nextstates = ['I' + str(num), 'E']
		else:
			num = int(states[i][1])
			nextstates = ['I' + str(num), 'M' + str(num + 1), 'D' + str(num + 1)]
		vec = []
		for nextstate in nextstates:
			vec.append(transition.get((states[i], nextstate), 0))
		vec = NormalizeSmooth(vec, pseudocount)
		for j in range(len(nextstates)):
			transition[(states[i], nextstates[j])] = vec[j]
		if states[i][0] == 'I' or states[i][0] == 'M':
			vec = []
			for symbol in alphabet:
				vec.append(emission.get((states[i], symbol), 0))
			vec = NormalizeSmooth(vec, pseudocount)
			j = 0
			for symbol in alphabet:
				emission[(states[i], symbol)] = vec[j]
				j += 1
		
	print '  ' + ' '.join(states)
	for state in states:
		line = state
		for state1 in states:
			line += ' ' + str(transition.get((state, state1), 0))
		print line		
	print '--------'
	print '  ' + ' '.join(alphabet)
	for state in states:
		line = state
		for symbol in alphabet:
			line += ' ' + str(emission.get((state, symbol), 0))
		print line		
	
	return states, transition, emission

'''	
lines = read_file("inp29.txt")
lines = read_file("ProfileHMMPseudocounts.txt")
lines = read_file("rosalind_ba10f.txt")
threshold, pseudocount = map(float, str.split(lines[0]))
alphabet = str.split(lines[2])
alignments = lines[4:]
#print threshold
#print alphabet
#print alignments
ProfileHMMWithPseudocounts(threshold, alphabet, alignments, pseudocount)
'''

def getCurStates(i):
	return ['I' + str(i-1), 'M' + str(i), 'D' + str(i)]

def getPrevStates(state, i):
	return [('M' + str(i - 1), i - 1), ('I' + str(i - 1), i), ('D' + str(i - 1), i - 1)]

def SequenceAlignmentwithProfileHMM(x, threshold, alphabet, alignment, pseudocount):
	
	states, transition, emission = ProfileHMMWithPseudocounts(threshold, alphabet, alignment, pseudocount)
	m = max(map(int, [state[1:] for state in states if state[0] == 'M']))
	#startStates = ['M1', 'D1', 'I0']
	#initial = {state: 1.0 / len(states) for state in startStates}	
	s, n = {}, len(x)
	#for state in startStates:
	#	s[state, 0] = 1 * initial[state] * emission.get((state, x[0]), 0)
	s['I0', 1, 1] = max([transition.get(('S', 'I0'), 0) * emission.get(('I0', x[0]), 0), transition.get(('I0', 'I0'), 0) * emission.get(('I0', x[0]), 0)])
	s['M1', 1, 1] = max([transition.get(('S', 'M1'), 0) * emission.get(('M1', x[0]), 0), transition.get(('I0', 'M1'), 0) * emission.get(('M1', x[0]), 0)])
	s['D1', 1, 0] = max([transition.get(('S', 'D1'), 0), transition.get(('I0', 'D1'), 0)])
	#print s
	#print m, n
	for i in range(2, m + 1):
		for state in getCurStates(i):
			for j in range(n):
				if state[0] == 'D':
					s[state, i, j] = max([s[prevstate, index, j] * transition.get((prevstate, state), 0) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])
				else:
					if i == 6: print 'here', state, i, j, getPrevStates(state, i), max([(s[prevstate, index, j] * transition.get((prevstate, state), 0), prevstate) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])
					s[state, i, j + 1] = max([s[prevstate, index, j] * transition.get((prevstate, state), 0) * emission.get((state, x[j]), 0) for (prevstate, index) in getPrevStates(state, i) if (prevstate, index, j) in s])			
	print s
	print 'here000', m, n
	
	i = m
	j = n
	
	print 'h', i, getCurStates(i)
	
	ssink, state = max([(s.get((state, i, j), 0), state) for state in getCurStates(i)])
	print ssink, state
	path = state
	print path
	
	i = m
	if state[0] != 'D':
		j -= 1
	while i > 0:
		#prevStates = getPrevStates(state, i)
		prevStates = [(p, index) if state[0] != 'I' else (p[0] + str(int(p[1:]) + 1), index) for (p, index) in getPrevStates(state, i)]
		print 'hhhh', i, j, state, [(s.get((prevstate, index, j), 0) * transition.get((prevstate, state), 0), j, prevstate) for (prevstate, index) in prevStates]
		if state[0] != 'I':
			i -= 1
		smax, state = max([(s.get((prevstate, index, j), 0) * transition.get((prevstate, state), 0), prevstate) for (prevstate, index) in prevStates])
		print smax, state
		path = state + ' ' + path
		print path
		if state[0] != 'D':
			j -= 1
	print path

'''
lines = read_file("inp30.txt")
#lines = read_file("AlignmentWithHMMProfile.txt")
lines = read_file("rosalind_ba10g.txt")
x = lines[0]
threshold, pseudocount = map(float, str.split(lines[2]))
alphabet = str.split(lines[4])
alignments = lines[6:]
#print threshold
#print alphabet
#print alignments
SequenceAlignmentwithProfileHMM(x, threshold, alphabet, alignments, pseudocount)
'''

# GibbsSampler
# first, import the random package
import random

# Input:  Integers k, t, and N, followed by a collection of strings Dna
# Output: GibbsSampler(Dna, k, t, N)
def GibbsSampler(Dna, k, t, N):
    Motifs = RandomMotifs(Dna, k, t)
    BestMotifs = Motifs # output variable
    for j in range(N):
        index = random.randint(0, t-1) #randomly generate integer between 1 and t
        #profile matrix formed from all strings in Motifs except for Motif_i
        Profile = ProfileWithPseudocounts(Motifs[:index]+Motifs[index+1:]) 
        #print index, Profile
        probs = [] 
        m = len(Dna[index])-k+1
        #print m
        for s in range(m):
            kmer = Dna[index][s:s+k]
            prob = 1
            for i in range(k):
                prob *= Profile[kmer[i]][i]
            probs.append(prob) 
        probs = [x / sum(probs) for x in probs]
        start = np.random.choice(range(m), p=probs)
        #print str
		#j = random.randint(0, len(Dna[i])-k)
        Motifs[index] = Dna[index][start:start+k] #Dna[i][j:j+k] #Profile-randomly generated k-mer in the i-th string
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs

# GibbsSampler
# first, import the random package
import random

# Input:  Integers k, t, and N, followed by a collection of strings Dna
# Output: GibbsSampler(Dna, k, t, N)
def GreedyMotifSearch(Dna, k, t, N):
    Motifs = [Dna[i][:k] for i in range(t)]
    BestMotifs = Motifs # output variable
    for j in range(len(Dna[0])-k+1):
        Motifs[0] = Dna[0][j:j+k]
		for i in range(1, t):
			Profile = ProfileWithPseudocounts(Motifs[:i]) 
			probs = [] 
			m = len(Dna[index])-k+1
			for s in range(m):
				kmer = Dna[index][s:s+k]
				prob = 1
				for i in range(k):
					prob *= Profile[kmer[i]][i]
				probs.append(prob) 
			probs = [x / sum(probs) for x in probs]
			start = np.random.choice(range(m), p=probs)
			Motifs[i] = Dna[index][start:start+k] #Dna[i][j:j+k] #Profile-randomly generated k-mer in the i-th string
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs	
	
# place all subroutines needed for GibbsSampler below this line
# Input:  A set of kmers Motifs
# Output: ProfileWithPseudocounts(Motifs)
def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = CountWithPseudocounts(Motifs)
    t1 = []
    for i in range(k):
        t1.append(sum([profile[key][i] for key in profile]))        
    for key in profile:
        profile[key] = [(profile[key][i] * 1.0) / t1[i] for i in range(k)]
    return profile

# Input:  A set of kmers Motifs
# Output: CountWithPseudocounts(Motifs)
def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    # insert your code here
    count = Count(Motifs)
    for key in count:
        count[key] = [x + 1 for x in count[key]]
    return count    

# Input:  A list of strings Dna, and integers k and t
# Output: RandomMotifs(Dna, k, t)
# HINT:   You might not actually need to use t since t = len(Dna), but you may find it convenient
def RandomMotifs(Dna, k, t):
    # place your code here.
    kmers = []
    for dna in Dna:
        i = random.randint(0, len(dna)-k)
        kmers.append(dna[i:i+k])
    return kmers

# Input:  A profile matrix Profile and a list of strings Dna
# Output: Motifs(Profile, Dna)
def Motifs(Profile, Dna, k):
    # insert your code here
    return [ProfileMostProbablePattern(dna, Profile, k) for dna in Dna]

# Insert your ProfileMostProbablePattern(Text, Profile) and Pr(Pattern, Profile) functions here.
def Pr(Text, Profile):
    # insert your code here
    #index = {'A':0, 'C':1, 'G':2, 'T':3}
    prob = 1
    for i in range(len(Text)):
        prob *= Profile[Text[i]][i]
    return prob

# Input:  A set of k-mers Motifs
# Output: The score of these k-mers.
def Score(Motifs):
    # Insert code here
    consensus_motif = Consensus(Motifs)
    score = 0
    for i in range(len(consensus_motif)):
        score += sum([1 for j in range(len(Motifs)) if consensus_motif[i] != Motifs[j][i]])
    return score    

# Copy your Consensus(Motifs) function here.
# Input:  A set of kmers Motifs
# Output: A consensus string of Motifs.
def Consensus(Motifs):
    # insert your code here
    k = len(Motifs[0])
    count = Count(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

# Copy your Count(Motifs) function here.
# Input:  A set of kmers Motifs
# Output: Count(Motifs)
def Count(Motifs):
    
    count = {} # initializing the count dictionary
    
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(0)
    
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def ProfileMostProbablePattern(Text, Profile, k):
    # insert your code here. Make sure to use Pr(Text, Profile) as a subroutine!
    maxval, maxkmer = -1, None
    for i in range(len(Text)-k+1):
        kmer = Text[i:i+k]
        val = Pr(kmer, Profile)
        if val > maxval:
            maxval, maxkmer = val, kmer
    return maxkmer      

### DO NOT MODIFY THE CODE BELOW THIS LINE ###
def RepeatedGibbsSampler(Dna, k, t, N):
    BestScore = float('inf')
    BestMotifs = []
    for i in range(20):
        Motifs = GibbsSampler(Dna, k, t, N)
        CurrScore = Score(Motifs)
        if CurrScore < BestScore:
            BestScore = CurrScore
            BestMotifs = Motifs
    return BestMotifs

'''
lines = read_file('inpros91.txt')
lines = read_file('gibbs.txt')
lines = read_file('rosalind_ba2g.txt')
k, t, N = map(int, lines[0].split())
Dna = lines[1:]
#print '\n'.join(RepeatedGibbsSampler(Dna, k, t, N))
'''
	
# Input:  Positive integers k and t, followed by a list of strings Dna
# Output: RandomizedMotifSearch(Dna, k, t)
def RandomizedMotifSearch(Dna, k, t):
    # insert your code here
    M = RandomMotifs(Dna, k, t)
    BestMotifs = M
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna, k)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs 

# Insert necessary subroutines here, including RandomMotifs(), ProfileWithPseudocounts(), Motifs(), Score(),
# and any subroutines that these functions need.

# Input:  A set of kmers Motifs
# Output: ProfileWithPseudocounts(Motifs)
def ProfileWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    profile = CountWithPseudocounts(Motifs)
    t1 = []
    for i in range(k):
        t1.append(sum([profile[key][i] for key in profile]))        
    for key in profile:
        profile[key] = [(profile[key][i] * 1.0) / t1[i] for i in range(k)]
    return profile

# Input:  A set of kmers Motifs
# Output: CountWithPseudocounts(Motifs)
def CountWithPseudocounts(Motifs):
    t = len(Motifs)
    k = len(Motifs[0])
    # insert your code here
    count = Count(Motifs)
    for key in count:
        count[key] = [x + 1 for x in count[key]]
    return count    

# Input:  A list of strings Dna, and integers k and t
# Output: RandomMotifs(Dna, k, t)
# HINT:   You might not actually need to use t since t = len(Dna), but you may find it convenient
def RandomMotifs(Dna, k, t):
    # place your code here.
    kmers = []
    for dna in Dna:
        i = random.randint(0, len(dna)-k)
        kmers.append(dna[i:i+k])
    return kmers

# Input:  A profile matrix Profile and a list of strings Dna
# Output: Motifs(Profile, Dna)
def Motifs(Profile, Dna, k):
    # insert your code here
    return [ProfileMostProbablePattern(dna, Profile, k) for dna in Dna]

# Insert your ProfileMostProbablePattern(Text, Profile) and Pr(Pattern, Profile) functions here.
def Pr(Text, Profile):
    # insert your code here
    #index = {'A':0, 'C':1, 'G':2, 'T':3}
    prob = 1
    for i in range(len(Text)):
        prob *= Profile[Text[i]][i]
    return prob

# Input:  A set of k-mers Motifs
# Output: The score of these k-mers.
def Score(Motifs):
    # Insert code here
    consensus_motif = Consensus(Motifs)
    score = 0
    for i in range(len(consensus_motif)):
        score += sum([1 for j in range(len(Motifs)) if consensus_motif[i] != Motifs[j][i]])
    return score    

# Copy your Consensus(Motifs) function here.
# Input:  A set of kmers Motifs
# Output: A consensus string of Motifs.
def Consensus(Motifs):
    # insert your code here
    k = len(Motifs[0])
    count = Count(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

# Copy your Count(Motifs) function here.
# Input:  A set of kmers Motifs
# Output: Count(Motifs)
def Count(Motifs):
    
    count = {} # initializing the count dictionary
    
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(0)
    
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def ProfileMostProbablePattern(Text, Profile, k):
    # insert your code here. Make sure to use Pr(Text, Profile) as a subroutine!
    maxval, maxkmer = -1, None
    for i in range(len(Text)-k+1):
        kmer = Text[i:i+k]
        val = Pr(kmer, Profile)
        if val > maxval:
            maxval, maxkmer = val, kmer
    return maxkmer      

### DO NOT MODIFY THE CODE BELOW THIS LINE ###
def RepeatedRandomizedMotifSearch(Dna, k, t):
    BestScore = float('inf')
    BestMotifs = []
    for i in range(1000):
        Motifs = RandomizedMotifSearch(Dna, k, t)
        CurrScore = Score(Motifs)
        if CurrScore < BestScore:
            BestScore = CurrScore
            BestMotifs = Motifs
    return BestMotifs

'''
lines = read_file('inpros92.txt')
lines = read_file('rosalind_ba2f.txt')
k, t = map(int, lines[0].split())
Dna = lines[1:]
print '\n'.join(RepeatedRandomizedMotifSearch(Dna, k, t))
'''

'''
from Bio import Entrez
Entrez.email = "your_name@your_mail_server.com"
handle = Entrez.efetch(db="nucleotide", id=["FJ817486, JX069768, JX469983"], rettype="fasta")
records = handle.read()
print records
'''

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
lines = read_file("rosalind_ba7f.txt")
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

# Soft KMeans Clustering
def ExpectationMaximization(Data, k, m, n, beta):

	x = np.array([Data[i,:] for i in range(k)])
	#print x
	for iter in range(100):
		#Centers to Soft Clusters (E-step): After centers have been selected, assign each data point a 'responsibility' value for each cluster, 
		#where higher values correspond to stronger cluster membership. 
		Z = [sum([exp(-beta * sqrt(dist1(Data[j,:], x[i,:], n))) for i in range(k)]) for j in range(m)]
		HiddenMatrix = np.array([[exp(-beta * sqrt(dist1(Data[j,:], x[i,:], n))) / Z[j] for i in range(k)] for j in range(m)]).T
		#Soft Clusters to Centers (M-step): After data points have been assigned to soft clusters, compute new centers.
		x = np.array([list(np.array((np.matrix(HiddenMatrix[i,:]) * np.matrix(Data)) / (np.matrix(HiddenMatrix[i,:]) * np.matrix([1.0 for _ in range(m)]).T)[0,0])[0,:]) for i in range(k)])
		#print x
	for i in range(k):
		print ' '.join(map(str, x[i,:]))

'''		
#lines = read_file("inp14.txt")
lines = read_file("rosalind_ba8d.txt")
k, n = map(int, str.split(lines[0]))
beta = float(lines[1])
Data = []
for line in lines[2:]:
	Data.append(map(float, str.split(line)))
m = len(Data)
Data = np.array(Data)
#print Data
#print k, m, n, beta
ExpectationMaximization(Data, k, m, n, beta)
'''

def Two_SUM(a):
	map = {}
	for i in range(len(a)):
		j = map[-a[i]] if (-a[i]) in map else -1
		map[a[i]] = i
		#if (a[i] != 0) and ((-a[i]) in map):
		if j != -1:
			return str(j+1) + ' ' + str(i+1)
	return -1

'''
lines = read_file('inpros11.txt')
lines = read_file('rosalind_2sum.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
for line in lines[1:]:
	print Two_SUM(map(int, str.split(line)))
'''

def Three_SUM(a):
	map = {}
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			map[a[i]+a[j]] = map.get(a[i]+a[j], []) + [(i+1, j+1)]
	for r in range(len(a)):
		indices = map[-(a[r])] if (-(a[r])) in map else -1
		if indices != -1:
			for (p, q) in indices:
				triples = sorted([p, q, r+1])
				#print triples
				p, q, r = triples[0], triples[1], triples[2]
				return str(p) + ' ' + str(q) + ' ' + str(r)
	return -1

'''
lines = read_file('inpros97.txt')
lines = read_file('rosalind_3sum.txt')	
n, m = map(int, str.split(lines[0]))
#print n, m
for line in lines[1:]:
	print Three_SUM(map(int, str.split(line)))
'''
