def read_file(filename):
	return [line.strip() for line in open(filename)]

def GenomePath(strs):
	path = strs[0]
	for s in strs[1:]:
		path += s[-1]
	print path

'''	
#lines = read_file('inp.txt')
#lines = read_file('GenomePathString.txt')
lines = read_file('dataset_198_3.txt')
GenomePath(lines)
'''

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

'''
peptide = 'VLWWHFIQYETN' #'LEQN'	
GeneratingTheoreticalSpectrumProblem(peptide)	
'''
import collections
def CyclopeptideScoringProblem(peptide, exp_spec):
	theo_spec = GeneratingTheoreticalSpectrumProblem(peptide)
	#print theo_spec
	#intersect = set(theo_spec).intersection(exp_spec))
	#exp_spec_ = [x for x in exp_spec if x in theo_spec]
	#print len(theo_spec), len(exp_spec)
	theo_spec_counter=collections.Counter(theo_spec)
	exp_spec_counter=collections.Counter(exp_spec)
	#print theo_spec_counter
	#print exp_spec_counter
	score = 0
	for m in exp_spec_counter:
		score += min(exp_spec_counter[m], theo_spec_counter.get(m, 0))
	print score	
	
#lines = read_file('inp1.txt')
#lines = read_file('dataset_102_3.txt')
#peptide, exp_spec = lines[0], map(int, lines[1].split())
#print peptide, exp_spec
#CyclopeptideScoringProblem(peptide, exp_spec)

exp_spec = '0 57 71 71 71 104 131 202 202 202 256 333 333 403 404'
peptide = 'MAMA'
CyclopeptideScoringProblem(peptide, map(int, exp_spec.split()))

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

def LinearpeptideScoringProblem(peptide, exp_spec):
	theo_spec = LinearSpectrum(peptide)
	#print theo_spec
	#intersect = set(theo_spec).intersection(exp_spec))
	#exp_spec_ = [x for x in exp_spec if x in theo_spec]
	#print len(theo_spec), len(exp_spec)
	theo_spec_counter=collections.Counter(theo_spec)
	exp_spec_counter=collections.Counter(exp_spec)
	#print theo_spec_counter
	#print exp_spec_counter
	score = 0
	for m in exp_spec_counter:
		score += min(exp_spec_counter[m], theo_spec_counter.get(m, 0))
	print score	

exp_spec = '0 97 97 129 129 194 203 226 226 258 323 323 323 355 403 452'
peptide = 'PEEP'
LinearpeptideScoringProblem(peptide, map(int, exp_spec.split()))

from math import sqrt
def LEADERBOARDCYCLOPEPTIDESEQUENCING(seq):
	l = len(seq)
	#n**2+n - 2(l-1)=0
	#n = (-1+sqrt(1+8*(l-1)))/2


# Quiz 1	
def allKMers(str, k):
	return set([str[i:i+k] for i in range(len(str)-k+1)])

'''	
#strs = ['0111010010', '0101010100', '1011100010', '1110001011', '0011100100', '0111010001']
strs = ['1011100010', '0101001101', '0111010010', '1000101110', '0011100100', '1101000111']
k = 3
for str in strs:
	kmers = allKMers(str, k)
	print str, kmers, len(kmers)
'''

def constructDeBruijnGraph(strs):
	graph, ingraph = {}, {}
	for s in strs:
		graph[s[:-1]] = graph.get(s[:-1], []) + [s[1:]]
		ingraph[s[1:]] = ingraph.get(s[1:], []) + [s[:-1]]
	return graph, ingraph

#lines = read_file('inp3.txt')	
#graph, ingraph = constructDeBruijnGraph(lines)
#print graph
#print ingraph
#print ingraph['AGA'], len(ingraph['AGA'])
#print graph['GCG'], len(graph['GCG'])

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

from copy import deepcopy
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

'''	
strs = read_file('inp3.txt')
#k = 5 #5 #4 #3
#binstrs = ["".join(seq) for seq in itertools.product("01", repeat=k)]
#print binstrs
graph, ingraph = constructDeBruijnGraph(strs) #binstrs
#graph = constructDeBruijnGraph(binstrs)
#print graph
path = EulerTour(graph) #binstrs[0]
#path = EulerCycle(graph, binstrs[0][:-1])
#path = str(constructDeBruijnGraph1(k))
print path
'''

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

def CyclopeptideScoringProblem(peptide, exp_spec):
	theo_spec = set(GeneratingTheoreticalSpectrumProblem(peptide))
	return len(theo_spec.intersection(exp_spec))

'''
th_spectrum = '0 71 101 113 131 184 202 214 232 285 303 315 345 416'
peptides = ['MIAT', 'MTAL', 'IAMT', 'TLAM', 'TMLA', 'MTAI']
for peptide in peptides:
	print peptide, (' '.join(map(str, GeneratingTheoreticalSpectrumProblem(peptide))) == th_spectrum)
'''

def get_all_substrings(string):
	length = len(string)+1
	return [string[x:y] for x in range(length) for y in range(length) if string[x:y]]

def consistent(peptide, spectrum):
	lines = read_file('mass.txt')
	map = {}
	for line in lines:
		pep, mass = str.split(line)
		map[pep] = int(mass)
	strings = get_all_substrings(peptide)	
	masses = []
	for string in strings:
		masses += [sum([map[x] for x in string])]
	#print sorted(masses), sorted(set(masses).intersection(spectrum))
	return sorted(set(masses).intersection(spectrum)) == sorted(masses)

'''	
spec = map(int, '0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333'.split())
peptides = ['CTV', 'ETC', 'CTQ', 'QCV', 'TVQ', 'VAQ']
for peptide in peptides:
	print peptide, consistent(peptide, spec) 
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

'''
rna_strings = ['CCCAGGACUGAGAUCAAU', 'CCCAGUACCGAGAUGAAU', 'CCGAGGACCGAAAUCAAC', 'CCAAGUACAGAGAUUAAC']

for rna in rna_strings:
	print rna, ProteinTranslationProblem(rna)
'''

def SpectralConvolution(spectrum):
	elements = {}
	for e1 in spectrum:
		for e2 in spectrum:
			e = abs(e1- e2)
			elements[e] = elements.get(e, 0) + 1
	print elements
	
exp_spec = '0 86 160 234 308 320 382'
SpectralConvolution(map(int, exp_spec.split()))
