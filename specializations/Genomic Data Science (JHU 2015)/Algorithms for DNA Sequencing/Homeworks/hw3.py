import hw1

def editDistance(x, y):
    # Create distance matrix
    D = []
    for i in range(len(x)+1):
        D.append([0]*(len(y)+1))
       
    # Initialize first row and column of matrix
    for i in range(len(x)+1):
        D[i][0] = i
    for i in range(len(y)+1):
        D[0][i] = 0 #i
       
    # Fill in the rest of the matrix
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            distHor = D[i][j-1] + 1
            distVer = D[i-1][j] + 1
            if x[i-1] == y[j-1]:
                distDiag = D[i-1][j-1]
            else:
                distDiag = D[i-1][j-1] + 1
            D[i][j] = min(distHor, distVer, distDiag)
       
    # Edit distance is the value in the bottom right corner of the matrix
    return min(D[-1]) #D[-1][-1]
	
sequence = hw1.readGenome('chr1.GRCh38.excerpt.fasta')

# Q 1-2
pattern = 'GCTGATCGATCGTACG'
print 'Q1', editDistance(pattern, sequence)

pattern = 'GATTTACCAGATTGAG'
print 'Q2', editDistance(pattern, sequence)

# Q 3-4
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
		
sequences, qualities = hw1.readFastq('ERR266411_1.for_asm.fastq')
#print len(sequences), sequences[0]

k = 30
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

#for i in range(len(sequences)):
#	prefix = sequences[i][:k]
#	for j in kmers.get(prefix, set([])) - set([i]):
#		overlap_len = overlap(sequences[j], sequences[i], k)
#		if overlap_len > 0:
#			overlaps[j, i] = max(overlaps.get((j, i), 0), overlap_len)
			
print 'Q3', len(overlaps)

print 'Q4', len(set([e[0] for e in overlaps]))