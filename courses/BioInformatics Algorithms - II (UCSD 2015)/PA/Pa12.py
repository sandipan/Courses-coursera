from PA4 import read_file
from PA8 import dist1
import numpy as np
from math import exp
	
def ConstructGraphOfSpectrum(s, map):
	s = [0] + s
	n = len(s)
	nbrs = {}
	for i in range(n):
		for j in range(i + 1, n):
			d = s[j] - s[i]
			if d in map:
				#print str(s[i]) + '->' + str(s[j]) + ':' + map[d] 
				nbrs[s[i]] = nbrs.get(s[i], []) + [s[j]]
	return nbrs

'''
lines = read_file('mass.txt')
rmap = {}
for line in lines:
	pep, mass = str.split(line)
	rmap[int(mass)] = pep
#print rmap	

lines = read_file('inp35.txt')
lines = read_file('dataset_11813_2.txt')
spectrum = map(int, str.split(lines[0]))
ConstructGraphOfSpectrum(spectrum, rmap)
'''

def IdealSpectrum(peptide, pmap):
	n = len(peptide)
	psum = 0
	ispec = [psum]
	for i in range(n):
		psum += pmap[peptide[i]]
		ispec += [psum]
	psum = 0
	for i in range(n - 1, 0, -1):
		psum += pmap[peptide[i]]
		ispec += [psum]
	return sorted(ispec)

def findAllPaths(spec, fmap, rmap):
	spec = [0] + spec
	src, sink = 0, spec[len(spec) - 1] 
	nbrs = ConstructGraphOfSpectrum(spec, rmap)
	visited, par = [], {}
	stack, visited = [0], visited + [0]
	#print v
	while len(stack) > 0:
		u = stack.pop()
		if u == sink:
			v = u
			pep = ''
			while v != src:
				pep += rmap[v - par[v]]
				v = par[v]
			ispec = IdealSpectrum(pep, fmap)
			if ispec == spec:
				return pep
			#else:
			#	visited.remove(sink)
		for v in nbrs.get(u, []):
			#if not v in visited: 	# dfs without visit flag
			par[v] = u
			stack.append(v)
			#print 'here', v
			visited.append(v)
			#else:
			#	visited.remove(v)

'''
lines = read_file('mass.txt')
fmap, rmap = {}, {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep], rmap[mass] = mass, pep
	
#print IdealSpectrum('GPG', fmap)
#lines = read_file('inp36.txt')
#lines = read_file('decoding_ideal_spectrum.txt')
lines = read_file('dataset_11813_4.txt')
spectrum = map(int, str.split(lines[0]))
print findAllPaths(spectrum, fmap, rmap)
'''

def ConvertingPeptideToPeptideVector(peptide, pmap):
	n = len(peptide)
	psum = 0
	ispec = []
	for i in range(n):
		psum += pmap[peptide[i]]
		ispec += [psum]
	#print ispec
	pvec = [0] * ispec[n - 1]
	for i in range(n):
		pvec[ispec[i] - 1] = 1
	print ' '.join(map(str, pvec))

'''	
lines = read_file('mass.txt')
fmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep] = mass
	
#ConvertingPeptideToPeptideVector('XZZXX', fmap)	
lines = read_file('dataset_11813_6.txt')
ConvertingPeptideToPeptideVector(lines[0], fmap)	
'''

def ConvertingPeptideVectorToPeptide(pvec, pmap):
	prefixes = [i + 1 for i in range(len(pvec)) if pvec[i] == 1]
	#print prefixes
	peptide = pmap[prefixes[0]]
	for i in range(len(prefixes) - 1):
		peptide += pmap[prefixes[i + 1] - prefixes[i]]
	print peptide

'''	
lines = read_file('mass.txt')
rmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	rmap[mass] = pep
	
lines = read_file('inp37.txt')
lines = read_file('dataset_11813_8.txt')
ConvertingPeptideVectorToPeptide(map(int, str.split(lines[0])), rmap)	
'''

def dfs(spec, nbrs, rmap):
	src, sink = 0, len(spec) - 1
	#print src, sink	
	par = {}
	stack = [0]
	max_pep_wts = (0, None) #(-float('inf'), None)
	#print v
	while len(stack) > 0:
		u = stack.pop()
		if u == sink:
			v = u
			pep, wt = '', 0
			while v != src:
				pep = rmap[v - par[v]] + pep
				wt += spec[v]
				#print 'here1', v, spec[v]
				v = par[v]
			#print 'here2', wt, pep
			if wt >= max_pep_wts[0]:
				max_pep_wts = wt, pep
				print max_pep_wts
		for v in nbrs.get(u, []):
			# dfs without visit flag
			par[v] = u
			stack.append(v)
			#print 'here', v
	print 'Max: ', max_pep_wts		

def PeptideSequencing(specvec, rmap):
	m = len(specvec)
	#specvec = [0] + specvec	# weight
	nbr_dag = {i:[] for i in range(m + 1)}
	for i in range(m + 1):
		for j in range(i + 1, m + 1):
			if j - i in rmap:
				nbr_dag[i] = nbr_dag.get(i, []) + [j]
	#print nbr_dag
	#print specvec
	dfs(specvec, nbr_dag, rmap)				

'''	
lines = read_file('mass1.txt')
#lines = read_file('mass.txt')
rmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	rmap[mass] = pep

#lines = read_file('inp38.txt')
#lines = read_file('peptide_sequencing.txt')
lines = read_file('dataset_11813_10.txt')
specvec = map(int, str.split(lines[0]))
PeptideSequencing(specvec, rmap)
#Output
#GGPGGPGGAGG
'''