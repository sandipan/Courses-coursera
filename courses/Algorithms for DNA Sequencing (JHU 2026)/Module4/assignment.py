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

def editDistance(x, y):
    # Create distance matrix
    D = np.zeros((len(x)+1, len(y)+1), int)
    #for i in range(len(x)+1):
    #    D.append([0]*(len(y)+1))
    # Initialize first row and column of matrix
    for i in range(len(x)+1):
        D[i,0] = i
    for i in range(len(y)+1):
        D[0,i] = i
    # Fill in the rest of the matrix
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            distHor = D[i,j-1] + 1
            distVer = D[i-1,j] + 1
            if x[i-1] == y[j-1]:
                distDiag = D[i-1,j-1]
            else:
                distDiag = D[i-1,j-1] + 1
            D[i,j] = min(distHor, distVer, distDiag)
    # Edit distance is the value in the bottom right corner of the matrix
    return D[-1][-1]

def traceback(D, x, y):
    i, j = len(x), len(y)
    d = 0
    x_, y_ = '', ''

    while i > 0 and j > 0:
        if D[i, j] == D[i-1, j-1] + (x[i-1] != y[j-1]):
            # Match or substitution
            cost = (x[i-1] != y[j-1])
            x_ = x[i-1] + x_
            y_ = y[j-1] + y_
            d += cost
            i -= 1
            j -= 1

        elif D[i, j] == D[i-1, j] + 1:
            # Deletion
            x_ = x[i-1] + x_
            y_ = '-' + y_
            d += 1
            i -= 1

        else:
            # Insertion
            x_ = '-' + x_
            y_ = y[j-1] + y_
            d += 1
            j -= 1

    # Handle remaining characters
    while i > 0:
        x_ = x[i-1] + x_
        y_ = '-' + y_
        d += 1
        i -= 1

    #while j > 0:
        #x_ = '-' + x_
        #y_ = y[j-1] + y_
        #d += 1
        #j -= 1

    return x_, y_, d

import numpy as np

def substring_edit_distance(P, T):

    m, n = len(P), len(T)

    D = np.zeros((m+1, n+1), dtype=int)

    D[:, 0] = np.arange(m+1)

    for i in range(1, m+1):
        for j in range(1, n+1):
            D[i, j] = min(
                D[i-1, j] + 1,
                D[i, j-1] + 1,
                D[i-1, j-1] + (P[i-1] != T[j-1])
            )

    # Find the best ending position
    j = np.argmin(D[m, :])
    min_dist = D[m, j]

    # Traceback
    i = m
    x_, y_ = '', ''

    while i > 0:
        if j > 0 and D[i, j] == D[i-1, j-1] + (P[i-1] != T[j-1]):
            x_ = P[i-1] + x_
            y_ = T[j-1] + y_
            i -= 1
            j -= 1

        elif D[i, j] == D[i-1, j] + 1:
            x_ = P[i-1] + x_
            y_ = '-' + y_
            i -= 1

        else:
            x_ = '-' + x_
            y_ = T[j-1] + y_
            j -= 1

    start = j
    end = np.argmin(D[m, :])

    return x_, y_, min_dist, start, end, T[start:end], editDistance(P, T[start:end])

import numpy as np

#human_genome = readGenome('chr1.GRCh38.excerpt.fasta')
#p = 'GCTGATCGATCGTACG'
#print(substring_edit_distance(p, human_genome))
#p_, g_, d = traceback(D, p, human_genome)
#print(p_, d)
#print(g_)
#print(substring_edit_distance('GATTTACCAGATTGAG', human_genome))

from itertools import permutations

def overlap(a, b, min_length=3):
    """ Return length of longest suffix of 'a' matching
        a prefix of 'b' that is at least 'min_length'
        characters long.  If no such overlap exists,
        return 0. """
    start = 0  # start all the way at the left
    while True:
        start = a.find(b[:min_length], start)  # look for b's prefix in a
        if start == -1:  # no more occurrences to right
            return 0
        # found occurrence; check for full suffix/prefix match
        if b.startswith(a[start:]):
            return len(a)-start
        start += 1  # move just past previous match

def naive_overlap_map(reads, k):
    olaps = {}
    outgoing = set([])
    for a, b in permutations(reads, 2):
        if a[-k:] in b:
            olen = overlap(a, b, min_length=k)
            if olen > 0:
                olaps[(a, b)] = olen
                outgoing.add(a)
    return olaps, outgoing

#phi_genome, _ = readFastq('ERR266411_1.for_asm.fastq')
#print(phi_genome)
#ol, ou = naive_overlap_map(phi_genome, 30)
#print(len(ol), len(ou))


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

import itertools

def scs(ss):
    """ Returns shortest common superstring of given
        strings, which must be the same length """
    shortest_sup = None
    for ssperm in itertools.permutations(ss):
        sup = ssperm[0]  # superstring starts as first string
        for i in range(len(ss)-1):
            # overlap adjacent strings A and B in the permutation
            olen = overlap(ssperm[i], ssperm[i+1], min_length=1)
            # add non-overlapping portion of B to superstring
            sup += ssperm[i+1][olen:]
        if shortest_sup is None or len(sup) < len(shortest_sup):
            shortest_sup = sup  # found shorter superstring
    return shortest_sup  # return shortest

def scslist(ss):
    """ Returns shortest common superstring of given
        strings, which must be the same length """
    slist = {}
    shortest_sup = None
    for ssperm in itertools.permutations(ss):
        sup = ssperm[0]  # superstring starts as first string
        for i in range(len(ss)-1):
            # overlap adjacent strings A and B in the permutation
            olen = overlap(ssperm[i], ssperm[i+1], min_length=1)
            # add non-overlapping portion of B to superstring
            sup += ssperm[i+1][olen:]
        if shortest_sup is None or len(sup) <= len(shortest_sup):
            shortest_sup = sup  # found shorter superstring
            slist[len(shortest_sup)] = slist.get(len(shortest_sup), []) + [shortest_sup]
    return shortest_sup, slist  # return shortest

s = ['CCT', 'CTT', 'TGC', 'TGG', 'GAT', 'ATT']
ss = scs(s)
#print(ss, len(ss))
#slist = scslist(s)
#print(slist)

def pick_maximal_overlap(reads, k):
    """ Return a pair of reads from the list with a
        maximal suffix/prefix overlap >= k.  Returns
        overlap length 0 if there are no such overlaps."""
    reada, readb = None, None
    best_olen = 0
    for a, b in itertools.permutations(reads, 2):
        if a[-k:] in b:
            olen = overlap(a, b, min_length=k)
            if olen > best_olen:
                reada, readb = a, b
                best_olen = olen
    return reada, readb, best_olen

def greedy_scs(reads, k):
    """ Greedy shortest-common-superstring merge.
        Repeat until no edges (overlaps of length >= k)
        remain. """
    read_a, read_b, olen = pick_maximal_overlap(reads, k)
    while olen > 0:
        reads.remove(read_a)
        reads.remove(read_b)
        reads.append(read_a + read_b[olen:])
        read_a, read_b, olen = pick_maximal_overlap(reads, k)
    return ''.join(reads)

v_genome, _ = readFastq('ads1_week4_reads.fq')
#print(v_genome)

#ss = greedy_scs(v_genome, 30)
#print(ss, len(ss))


import heapq

def greedy_scs_heap(reads, k):
    """Greedy shortest-common-superstring using precomputed
       overlaps and a max-priority queue."""

    # Assign unique IDs (also handles duplicate read strings)
    active = {i: read for i, read in enumerate(reads)}
    next_id = len(active)

    # Max-heap: negative overlap length, read IDs
    heap = []

    # Compute all initial pairwise overlaps only once
    ids = list(active)

    for i in ids:
        for j in ids:
            if i != j:
                olen = overlap(active[i], active[j], k)
                if olen > 0:
                    heapq.heappush(heap, (-olen, i, j))

    # Greedy merging
    while heap:
        neg_olen, i, j = heapq.heappop(heap)

        # Skip obsolete candidates
        if i not in active or j not in active:
            continue

        olen = -neg_olen

        # Merge the two reads
        merged = active[i] + active[j][olen:]

        del active[i]
        del active[j]

        # Assign a new ID to the merged read
        new_id = next_id
        next_id += 1
        active[new_id] = merged

        # Compute only overlaps involving the new read
        for other_id, other_read in active.items():
            if other_id == new_id:
                continue

            # New read -> existing read
            o1 = overlap(merged, other_read, k)
            if o1 > 0:
                heapq.heappush(heap, (-o1, new_id, other_id))

            # Existing read -> new read
            o2 = overlap(other_read, merged, k)
            if o2 > 0:
                heapq.heappush(heap, (-o2, other_id, new_id))

    return ''.join(active.values())

ss = greedy_scs_heap(v_genome, 30)
print(ss, len(ss))

from collections import Counter
print(Counter(ss))
