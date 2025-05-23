def read_file(filename):
	return [line.strip() for line in open(filename)]

#lines = read_file('dna.example.fasta')	
lines = read_file('dna1.fasta')	

# Q1
num_records = sum([1 for line in lines if line[0] == '>'])
print 'Q1', num_records

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

sequences, ids = get_seq_fasta(lines)
#print sequences
#print len(sequences)	

# Q2
print 'Q2', max([len(sequence) for sequence in sequences])

# Q3
print 'Q3', min([len(sequence) for sequence in sequences])

def find_orf(sequence, frame, start_codon = 'ATG', stop_codons = set(['TAA', 'TAG', 'TGA'])): # need to modify
	i, start, stop, orfs = frame - 1, None, None, []
	while i < len(sequence) - 3:
		if sequence[i:i+3] == start_codon and not start: # already got start codon, wait for stop
			start = i
		elif sequence[i:i+3] in stop_codons:
			stop = i + 2
			if start and stop and start < stop:	# must stop
				orf = sequence[start:stop+1]
				orfs += [(orf, start, stop)]
				start = stop = None
		i += 3
	return orfs

# Q4	
orfs = []
for sequence in sequences:
	orfs += find_orf(sequence, 2)
	
orfs = [orf for orf in orfs if orf[0]]
#print orfs
orf_lens = [len(orf[0]) for orf in orfs]
#print orf_lens
print 'Q4', max(orf_lens)

# Q5
orfs = []
for sequence in sequences:
	orfs += find_orf(sequence, 3)
orfs = [orf for orf in orfs if orf[0]]
#print orfs
orf_lens_poss = [(len(orf[0]), orf[1] + 1) for orf in orfs]
#print orf_lens_poss
print 'Q5', max(orf_lens_poss)[1]

# Q6
orfs = []
for frame in range(1, 4):
	for sequence in sequences:
		orfs += find_orf(sequence, frame)
	
orfs = [orf for orf in orfs if orf[0]]
#print orfs
orf_lens = [len(orf[0]) for orf in orfs]
#print orf_lens
print 'Q6', max(orf_lens)

# Q7
#id = 'gi|142022655|gb|EQ086233.1|160' # example
id = 'gi|142022655|gb|EQ086233.1|97'
seq = sequences[ids[id]]
#print id, seq
orfs = []
for frame in range(1, 4):
	orfs += find_orf(seq, frame)
#print orfs
#print [len(orf[0]) for orf in orfs]
print 'Q7', max([len(orf[0]) for orf in orfs])

# Q8
k = 6
kmers = {}
for sequence in sequences:
	for i in range(len(sequence) - k + 1):
		kmers[sequence[i:i+k]] = kmers.get(sequence[i:i+k], 0) + 1
max_val = max(kmers.values())
#print [(kmer, kmers[kmer]) for kmer in kmers if kmers[kmer] == max_val]
print 'Q8', [(kmer, kmers[kmer]) for kmer in kmers if kmers[kmer] == max_val][0]

# Q9
k = 12
kmers = {}
for sequence in sequences:
	for i in range(len(sequence) - k + 1):
		kmers[sequence[i:i+k]] = kmers.get(sequence[i:i+k], 0) + 1
max_val = max(kmers.values())
#print [(kmer, kmers[kmer]) for kmer in kmers if kmers[kmer] == max_val]
print 'Q9', len([(kmer, kmers[kmer]) for kmer in kmers if kmers[kmer] == max_val])
		
# Q10
k = 7
kmers = ['GCGGCGC', 'CGGCGGC', 'GCCGCCG', 'CGGCGCT']
counts = {kmer:0 for kmer in kmers}
for sequence in sequences:
	for i in range(len(sequence) - k + 1):
		if sequence[i:i+k] in kmers:
			counts[sequence[i:i+k]] += 1
#print counts
max_val = max(counts.values())
print 'Q10', [(kmer, counts[kmer]) for kmer in counts if counts[kmer] == max_val][0]
		