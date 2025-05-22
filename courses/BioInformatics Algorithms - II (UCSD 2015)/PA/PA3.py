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
	
#Patterns, Text, d = ["dna"], "panamabananas", 1 
#MultipleApproximatePatternMatching(Text, Patterns, d)
#Patterns, Text, d = ["ATT", "GCC", "GCTA", "TATT"], "ACATGCTACTTT", 1
#MultipleApproximatePatternMatching(Text, Patterns, d)
#MultipleApproximatePatternMatching2(Text, Patterns, d)

def read_file(filename):
	return [line.strip() for line in open(filename)]

#lines = read_file("out1.txt")
#print ' '.join(map(str, sorted(map(int, str.split(lines[0])))))


lines = read_file("dataset_304_6.txt")
#lines = read_file("MultipleApproximatePatternMatching.txt")
Patterns, Text, d = str.split(lines[1]), lines[0], int(lines[2])
#print Text
#print len(Patterns)
#print d
MultipleApproximatePatternMatching(Text, Patterns, d)

'''
def MultipleApproximatePatternMatching1(Text, Patterns, d):
	
	n = len(Text)
	print n
	positions = []
	for i in range(n):
		if i % 1000 == 0: print i
		for pattern in Patterns:
			m = len(pattern)
			if i + m >= n: break
			mismatch = 0
			for j in range(m):
				if pattern[j] != Text[i + j]: mismatch += 1
				if mismatch > d: break
			if mismatch <= d:
				positions += [i]
	print positions
	
def binary_search_helper(arr, pat, Text, begin_index, end_index)  :
  
	if begin_index > end_index:
		return begin_index
	else:
		middle_index = (begin_index + end_index) / 2
		string = Text[arr[middle_index]:arr[middle_index]+len(pat)]
		#print string
	if string == pat:
		return middle_index
	elif pat > string:
		return binary_search_helper(arr, pat, Text, middle_index + 1, end_index)
	else:
		return binary_search_helper(arr, pat, Text, begin_index, middle_index - 1)

# for [1,3,5,7,9], searching for 6 will return index for 7 for insertion
# if exact match is found, then return that index
def binary_search(arr, pat, Text):
	
	return binary_search_helper(arr, pat, Text, 0, len(arr) - 1)

def MultipleApproximatePatternMatching2(Text, Patterns, d):
	
	n = len(Text)
	m = max([len(p) for p in Patterns])
	suffixarray = [Text[i:i+m] for i in range(n - d)]
	suffixindex = sorted(range(len(suffixarray)), key=lambda k: suffixarray[k])
	print sorted(suffixarray), suffixindex
	positions = []
	for pattern in Patterns:
		m = len(pattern)
		for i in range(d + 1):
			index = binary_search(suffixindex, pattern[i:], Text)
			print pattern[i:], suffixindex[index], Text[suffixindex[index]:]
			k = 0
			while index + k < len(suffixindex):
				start, mismatch = suffixindex[index + k], i
				for j in range(m-i):
					if start + j >= n or Text[start + j] != pattern[i+j]: mismatch += 1
					if mismatch > d: break
				if mismatch > d: break
				else: 
					positions += [start-i]
					k += 1
				#print pattern[i:], index, Text[index:]
	print sorted(positions)
'''