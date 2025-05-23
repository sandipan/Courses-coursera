import hw1

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
		
sequences, qualities = hw1.readFastq('ads1_week4_reads.fq')
#print len(sequences), len(sequences[0])

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
				
		'''
		node_pairs = [node_pair for node_pair in overlaps if node_pair[0] == i or node_pair[0] == j]
		for node_pair in node_pairs:
			#print node_pair
			if sequences[node_pair[1]] in sequences[id]: # contains
				overlaps[id, node_pair[1]] = len(sequences[node_pair[1]])
			else:
				overlaps[id, node_pair[1]] = overlap(sequences[id], sequences[node_pair[1]], k) #overlaps[node_pair]
			#olen = overlap(sequences[node_pair[1]], sequences[id], k)
			#if olen >= k: overlaps[node_pair[1], id] = olen
			del overlaps[node_pair]
		node_pairs = [node_pair for node_pair in overlaps if node_pair[1] == i or node_pair[1] == j]
		for node_pair in node_pairs:
			if sequences[node_pair[0]] in sequences[id]: # contains
				overlaps[node_pair[0], id] = len(sequences[node_pair[0]])
			else:
				overlaps[node_pair[0], id] = overlap(sequences[node_pair[0]], sequences[id], k) #overlaps[node_pair]
			#olen = overlap(sequences[id], sequences[node_pair[0]], k)
			#if olen >= k: overlaps[id, node_pair[0]] = olen
			del overlaps[node_pair]
		'''
		
		id += 1
		#print sequences, overlaps
		
	return ''.join(sequences.values())

#print greedy_shortest_superstring(['AAA', 'AAB', 'ABA', 'ABB', 'BAA', 'BAB', 'BBA', 'BBB'], k=1)		
assembled_genome = greedy_shortest_superstring(sequences, k=30)		
print assembled_genome, len(assembled_genome)

print 'Q1', len([1 for i in range(len(assembled_genome)) if  assembled_genome[i] == 'A'])
print 'Q2', len([1 for i in range(len(assembled_genome)) if  assembled_genome[i] == 'T'])

# BioPython
from Bio.Blast import NCBIWWW
fasta_string = assembled_genome
result_handle = NCBIWWW.qblast("blastn", "nt", fasta_string)
from Bio.Blast import NCBIXML
blast_record = NCBIXML.read(result_handle)
len(blast_record.alignments)
E_VALUE_THRESH = 0.01
eval_seq = {}
for alignment in blast_record.alignments:
	for hsp in alignment.hsps:
		if hsp.expect < E_VALUE_THRESH:
			#print('****Alignment****')
			print('sequence:', alignment.title)
			#print('length:', alignment.length)
			print('e value:', hsp.expect)
			eval_seq[hsp.expect] = eval_seq.get(hsp.expect, []) + [alignment.title]
			#print(hsp.query)
			#print(hsp.match)
			#print(hsp.sbjct)

print 'Q3:', [(k, eval_seq[k]) for k in sorted(eval_seq)[:5]]
			