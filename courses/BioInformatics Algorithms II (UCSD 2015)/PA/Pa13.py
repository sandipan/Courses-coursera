from PA4 import read_file

def ConvertingPeptideToPeptideVector(peptide, pmap):
	n = len(peptide)
	psum = 0
	ispec = []
	for i in range(n):
		psum += pmap[peptide[i]]
		ispec += [psum]
	pvec = [0] * ispec[n - 1]
	for i in range(n):
		pvec[ispec[i] - 1] = 1
	#print ' '.join(map(str, pvec))
	return [1] + pvec

def PeptideIdentification(specvec, peptide, pmap):
	n = len(peptide)
	m = len(specvec)
	peptide_checked = set([])
	#peptide_mass = {(i, i): pmap[peptide[i]] for i in range(n)}
	peptide_mass = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		peptide_mass[i][i] = pmap[peptide[i]]
	for i in range(n):
		for j in range(i + 1, n):
			#peptide_mass[i, j] =  peptide_mass[i, j - 1] + peptide_mass[j, j]
			peptide_mass[i][j] =  peptide_mass[i][j - 1] + peptide_mass[j][j]
	max_score_pep = 0, None
	for i in range(n):
		for j in range(i, n):
			#if peptide_mass[i, j] + 1 == m and not peptide[i:j+1] in peptide_checked: #if len(pepvec) == m:
			if peptide_mass[i][j] + 1 == m and not peptide[i:j+1] in peptide_checked: #if len(pepvec) == m:
				subpep = peptide[i:j+1]
				pepvec = ConvertingPeptideToPeptideVector(subpep, pmap)
				#print subpep
				#print pepvec
				score = sum([pepvec[k] * specvec[k] for k in range(m)])
				if score >= max_score_pep[0]:
					max_score_pep = score, subpep
					#print max_score_pep
				peptide_checked.add(subpep)		
				
	print 'Max:', max_score_pep
	return max_score_pep

'''	
lines = read_file('mass1.txt')
#lines = read_file('mass.txt')
fmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep] = mass

#lines = read_file('inp39.txt')
#lines = read_file('peptide_identification.txt')
lines = read_file('dataset_11866_2.txt')
specvec = map(int, str.split(lines[0]))
peptide = lines[1]
PeptideIdentification(specvec, peptide, fmap)
'''
'''
m = len(specvec)
pepvec = ConvertingPeptideToPeptideVector('ZXZXX', fmap)
print 'ZXZXX', len(pepvec), len(specvec)
print sum([pepvec[k] * specvec[k] for k in range(m)])
pepvec = ConvertingPeptideToPeptideVector('ZZXZX', fmap)
print 'ZZXZX', len(pepvec), len(specvec)
print sum([pepvec[k] * specvec[k] for k in range(m)])
#Output
#KLEAARSCFSTRNE
'''

def PSMSearch(SpectralVectors, Proteome, threshold, pmap):
	PSMSet = set([])
	for specvec in SpectralVectors:
		#print specvec
		specvec = map(int, str.split(specvec))
		score, peptide = PeptideIdentification(specvec, Proteome, pmap)
		if score >= threshold:
			PSMSet.add(peptide)
	return PSMSet

'''	
lines = read_file('mass1.txt')
#lines = read_file('mass.txt')
fmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep] = mass

#lines = read_file('inp40.txt')
#lines = read_file('psm_search.txt')
lines = read_file('dataset_11866_5.txt')
n = len(lines)
res = list(PSMSearch(lines[:n - 2], lines[n - 2], int(lines[n - 1]), fmap))
print
for pep in res:
	print pep
'''

def SizeOfSpectralDictionary(specvec, threshold, max_score, fmap):
	m = len(specvec)
	#print m
	#print fmap
	size = {(0, 0): 1}
	for i in range(1, m + 1):
		for t in range(max_score + 1):
			size[i, t] = 0
			for a in fmap:
				size[i, t] += size.get((i - fmap[a], t - specvec[i - 1]), 0)
	#print size
	print sum([size.get((m, t), 0) for t in range(threshold, max_score + 1)])
	
'''	
lines = read_file('mass1.txt')
#lines = read_file('mass.txt')
fmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep] = mass

#lines = read_file('inp41.txt')
#lines = read_file('size_spectral_dictionary.txt')
lines = read_file('dataset_11866_8.txt')
specvec = map(int, str.split(lines[0]))
threshold = int(lines[1])
max_score = int(lines[2])
#print specvec
#print threshold, max_score
SizeOfSpectralDictionary(specvec[1:], threshold, max_score, fmap)
'''

def ProbabilityOfSpectralDictionary(specvec, threshold, max_score, fmap):
	m = len(specvec)
	#print m
	#print fmap
	prob = {(0, 0): 1}
	for i in range(1, m + 1):
		for t in range(max_score + 1):
			prob[i, t] = 0.0
			for a in fmap:
				prob[i, t] += (1.0 / 20) * prob.get((i - fmap[a], t - specvec[i - 1]), 0.0)
	#print prob
	print sum([prob.get((m, t), 0.0) for t in range(threshold, max_score + 1)])
	
'''	
lines = read_file('mass1.txt')
#lines = read_file('mass.txt')
fmap = {}
for line in lines:
	pep, mass = str.split(line)
	mass = int(mass)
	fmap[pep] = mass

lines = read_file('inp41.txt')
lines = read_file('probability_spectral_dictionary.txt')
lines = read_file('dataset_11866_11.txt')
specvec = map(int, str.split(lines[0]))
threshold = int(lines[1])
max_score = int(lines[2])
#print specvec
#print threshold, max_score
ProbabilityOfSpectralDictionary(specvec[1:], threshold, max_score, fmap)
'''
