def read_file(filename):
	return [line.strip() for line in open(filename)]

def Count(Text, Pat):	
	n, m = len(Text), len(Pat)
	return sum([1 for i in range(n) if Text[i:i+m] == Pat])	

#print Count('GCGCG', 'GCG')	
#print Count('CGCGATACGTTACATACATGATAGACCGCGCGCGATCATATCGCGATTATC', 'CGCG')	
#lines = read_file('dataset_2_6.txt')
#print Count(lines[0], lines[1])	

def MostFreqKmer(Text, k):	
	kmers = {}
	for i in range(len(Text)-k+1):
		kmers[Text[i:i+k]] = kmers.get(Text[i:i+k], 0) + 1
	print kmers
	print [kmer for kmer in kmers if kmers[kmer] == max(kmers.values())]

#MostFreqKmer('TAAACGTGAGAGAAACGTGCTGATTACACTTGTTCGTGTGGTAT', 3)
	
def ReverseComplementProblem(Text):
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
	return ''.join([complement[x] for x in Text])[::-1] 

#print ReverseComplementProblem('GATTACA')

def hamming(s1, s2):
	return sum([1 for i in range(len(s1)) if s1[i] != s2[i]])

s1, s2 = 'TGACCCGTTATGCTCGAGTTCGGTCAGAGCGTCATTGCGAGTAGTCGTTTGCTTTCTCAAACTCC', 'GAGCGATTAAGCGTGACAGCCCCAGGGAACCCACAAAACGTGATCGCAGTCCATCCGATCATACA'
#print len(s1)
#print hamming(s1, s2)	
lines = read_file('dataset_9_3.txt')
#print hamming(lines[0], lines[1])

def MaxSkew(s):
	n = len(s)
	skew, nC, nG = [0] * (n + 1), 0, 0
	for i in range(n):
		if s[i] == 'C':
			nC += 1
		elif s[i] == 'G':
			nG += 1
		skew[i + 1] = nG - nC		
	print n, skew	
	print max([(skew[i], i) for i in range(n + 1)])
	
#MaxSkew('CATTCCAGTACTTCATGATGGCGTGAAGA')	

def ApproximatePatternCount(Text, Pattern, d):
	count = 0
	for i in range(len(Text)-len(Pattern)+1):
		Pattern1 = Text[i:i+len(Pattern)]
		if hamming(Pattern, Pattern1) <= d:
			count += 1
	return count

lines = read_file('inp.txt')	
lines = read_file('dataset_9_6.txt')	
#print ApproximatePatternCount(lines[1], lines[0], int(lines[2]))
#print ApproximatePatternCount('TACGCATTACAAAGCACA', 'AA', 1)

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
	return out

#nbrs = GeneratedNeighborhoodString('ACGT', 3)
#print nbrs, len(nbrs)

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
	print min_dist, medianstr

'''	
dstrs = ['CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC',
'GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC',
'GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG']
k = 7
MedianStringProblem(k, dstrs)
for s in ['ATAACGG', 'GAACCAC', 'GTCAGCG', 'CGTGTAA', 'TAGTTTC', 'AACGCTG']:
	print s, dist_str(s, dstrs)
'''

#0.2 * 0.3 * 1.0 * 0.4 * 0.5 * 0.9

