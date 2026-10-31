def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            # ignore header line with genome information
            if not line[0] == '>':
                genome += line.rstrip()
    return genome

def reverseComplement(s):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    t = ''
    for base in s:
        t = complement[base] + t
    return t


def naive(p, t):
    occurrences = []
    ac, cc = 0, 0
    for i in range(len(t) - len(p) + 1):
        match = True
        for j in range(len(p)):
            cc += 1
            if t[i+j] != p[j]:
                match = False
                break
        if match:
            occurrences.append(i)
        ac += 1
    print(ac, cc)
    return occurrences

def naivemm(p, t, k):
    occurrences = []
    for i in range(len(t) - len(p) + 1):
        match = True
        count = 0
        for j in range(len(p)):
            if t[i+j] != p[j]:
                if count >= k:
                    match = False
                    break
                count += 1
        if match:
            occurrences.append(i)
        
    return list(set(occurrences))

def readFastq(filename):
    sequences = []
    qualities = []
    with open(filename) as fh:
        while True:
            fh.readline() # skip name line
            seq = fh.readline().rstrip() # read base sequence
            fh.readline() # skip placeholder line
            qual = fh.readline().rstrip() #base quality line
            if len(seq) == 0:
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities

def phred33ToQ(qual):
    return ord(qual) - 33

from bm_preproc import BoyerMoore

def boyer_moore(p, p_bm, t):
    """ Do Boyer-Moore matching. p=pattern, t=text,
        p_bm=BoyerMoore object for p """
    i = 0
    occurrences = []
    ac = 0
    while i < len(t) - len(p) + 1:
        shift = 1
        mismatched = False
        for j in range(len(p)-1, -1, -1):
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
        ac += 1
    print(ac)
    return occurrences


genome = readGenome('chr1.GRCh38.excerpt.fasta')
#print(genome)

p = 'GGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGG'

#print(naive(p, genome))
#print(len(genome) - len(p) + 1)
#p_bm = BoyerMoore(p, alphabet='ACGT')
#print(boyer_moore(p, p_bm, genome))

from kmer_index import Index

def queryIndex(p, t, index):
    k = index.k
    offsets = []
    for i in index.query(p):
        if p[k:] == t[i+k:i+len(p)]:  # verify that rest of P matches
            offsets.append(i)
    return offsets

def approximate_match_2(p, t):
    assert(len(p) == 24)
    index = Index(genome, 8)
    segment_length = 8
    n = 2
    all_matches = set()
    index_hits = 0
    ems = 0
    for i in range(n+1):
        start = i*segment_length
        end = min((i+1)*segment_length, len(p))
        matches = queryIndex(p[start:end], t, index)
        # Extend matching segments to see if whole p matches
        index_hits += len(matches)
        ems += len(naive(p[start:end], t))
        for m in matches:
            if m < start or m-start+len(p) > len(t):
                continue
            mismatches = 0
            for j in range(0, start):
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    if mismatches > n:
                        break
            for j in range(end, len(p)):
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    if mismatches > n:
                        break
            if mismatches <= n:
                all_matches.add(m - start)
    print(index_hits, ems)
    return list(all_matches)


from kmer_subindex import SubseqIndex

def approximate_match_sub_2(p, t):
    assert(len(p) == 24)
    subindex = SubseqIndex(genome, 8, 3)
    n = 2
    all_matches = set()
    index_hits = 0
    for i in range(3):
        matches = subindex.query(p[i:])
        # Extend matching segments to see if whole p matches
        index_hits += len(matches)
        for m in matches:
            mismatches = 0
            for start in [(i-1)%3, (i+1)%3]:
                end = min(start + 8*3, len(t))
                for j in range(start, end, 3):
                    if not p[j] == t[m+j]:
                        mismatches += 1
                        if mismatches > n:
                            break
            if mismatches <= n:
                all_matches.add(m - start)
    print(index_hits)
    return list(all_matches)

p = 'GGCGCGGTGGCTCACGCCTGTAAT'
#print(len(p))

#index = Index(genome, 8)
#queryIndex(p, genome, index)
#m = approximate_match_2(p, genome)
#print(m, len(m))

#m = naivemm(p, genome, 2)
#print(m, len(m))

#ind = SubseqIndex('ATATATATAT', 3, 2)
#print(ind.index)
#p = 'TTATAT'
#print(ind.query(p[0:]))
#print(ind.query(p[1:]))

m = approximate_match_sub_2(p, genome)
print(m, len(m))