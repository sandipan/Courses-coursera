import hw1, bm_preproc as bmp, kmer_index as kind

def naive(p, t):
    occurrences = []
    alignments, comparisons = 0, 0
    for i in range(len(t) - len(p) + 1):  # loop over alignments
        match = True
        alignments += 1
        for j in range(len(p)):  # loop over characters
            comparisons += 1
            if t[i+j] != p[j]:  # compare characters
                match = False
                break
        if match:
            occurrences.append(i)  # all chars matched; record
    print '#alignments:', alignments
    print '#character comparisons:', comparisons
    return occurrences

def boyer_moore(p, p_bm, t):
    """ Do Boyer-Moore matching. p=pattern, t=text,
        p_bm=BoyerMoore object for p """
    i = 0
    occurrences = []
    alignments, comparisons = 0, 0
    while i < len(t) - len(p) + 1:
        shift = 1
        mismatched = False
        alignments += 1
        for j in range(len(p)-1, -1, -1):
            comparisons += 1
            if p[j] != t[i+j]:
                skip_bc = p_bm.bad_character_rule(j, t[i+j])
                skip_gs = p_bm.good_suffix_rule(j)
                shift = max(shift, skip_bc, skip_gs)
                mismatched = True
                break
        if not mismatched:
            occurrences.append(i)
            skip_gs = p_bm.match_skip()
            shift = max(shift, skip_gs)
        i += shift
    print '#alignments:', alignments
    print '#character comparisons:', comparisons
    return occurrences
	
sequence = hw1.readGenome('chr1.GRCh38.excerpt.fasta')
#print len(sequence)

# Q1-3
pattern =  'GGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGG'
		    
#print len(pattern)
#print len(sequence) - len(pattern) + 1

naive(pattern, sequence)
boyer_moore(pattern, bmp.BoyerMoore(pattern), sequence)

#Q4-5
def Index_assisted_approximate_matching(p, t, num_mis):
	m = len(p)
	k = m / (num_mis + 1)
	#print m, k
	ind = kind.Index(t, k)
	indices = []
	for i in range(num_mis + 1):
		indices += [index - i*k for index in ind.query(p[i*k:])]
	print '# total index hits:', len(indices)
	indices = set(indices)
	#print sorted(indices)
	count = 0
	for index in indices:
		t_index = t[index:index+m]
		mismatches = 0
		for i in range(m):
			if t_index[i] != p[i]:
				mismatches += 1
			#if mismatches > num_mis: break	
		#print t_index, p, mismatches
		if mismatches <= num_mis:
			count += 1
	#print len(indices)
	print '# times of occurence:', count		
	
pattern = 'GGCGCGGTGGCTCACGCCTGTAAT'
Index_assisted_approximate_matching(pattern, sequence, 2)

#Q-6
import bisect
   
class SubseqIndex(object):
    """ Holds a subsequence index for a text T """

    def __init__(self, t, k, ival):
        """ Create index from all subsequences consisting of k characters
            spaced ival positions apart.  E.g., SubseqIndex("ATAT", 2, 2)
            extracts ("AA", 0) and ("TT", 1). """
        self.k = k  # num characters per subsequence extracted
        self.ival = ival  # space between them; 1=adjacent, 2=every other, etc
        self.index = []
        self.span = 1 + ival * (k - 1)
        for i in range(len(t) - self.span + 1):  # for each subseq
            self.index.append((t[i:i+self.span:ival], i))  # add (subseq, offset)
        self.index.sort()  # alphabetize by subseq

    def query(self, p):
        """ Return index hits for first subseq of p """
        subseq = p[:self.span:self.ival]  # query with first subseq
        i = bisect.bisect_left(self.index, (subseq, -1))  # binary search
        hits = []
        while i < len(self.index):  # collect matching index entries
            if self.index[i][0] != subseq:
                break
            hits.append(self.index[i][1])
            i += 1
        return hits

def Index_assisted_subsequence_approximate_matching(p, t, num_mis):
	m = len(p)
	k = m / (num_mis + 1)
	ival = num_mis + 1
	#print m, k, ival
	ind = SubseqIndex(t, k, ival)
	indices = []
	for i in range(num_mis + 1):
		indices += [index - i for index in ind.query(p[i:])]
	print '# total index hits:', len(indices)
	indices = set(indices)
	#print sorted(indices)
	count = 0
	for index in indices:
		t_index = t[index:index+m]
		mismatches = 0
		for i in range(m):
			if t_index[i] != p[i]:
				mismatches += 1
			#if mismatches > num_mis: break	
		#print t_index, p, mismatches
		if mismatches <= num_mis:
			count += 1
	#print len(indices)
	print '# times of occurence:', count		
	
pattern = 'GGCGCGGTGGCTCACGCCTGTAAT'
		   
Index_assisted_subsequence_approximate_matching(pattern, sequence, 2)
	