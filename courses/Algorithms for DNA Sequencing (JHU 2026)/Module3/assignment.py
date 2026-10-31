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

human_genome = readGenome('chr1.GRCh38.excerpt.fasta')
p = 'GCTGATCGATCGTACG'
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

phi_genome, _ = readFastq('ERR266411_1.for_asm.fastq')
#print(phi_genome)
ol, ou = naive_overlap_map(phi_genome, 30)
print(len(ol), len(ou))