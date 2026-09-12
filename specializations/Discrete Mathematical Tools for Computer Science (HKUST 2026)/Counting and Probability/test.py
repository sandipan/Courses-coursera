from scipy.special import perm, comb, factorial

print(perm(8,3))
print(perm(6,2))


def num_colorings(n, colors):
    coloring = [''] * n

    def backtrack(pos):
        # All benches have been colored
        if pos == n:
            return 1

        count = 0

        for c in colors:
            # Cannot use the same color as the previous bench
            if pos > 0 and coloring[pos - 1] == c:
                continue

            coloring[pos] = c          # Choose
            count += backtrack(pos + 1)  # Explore
            coloring[pos] = ''         # Undo (backtrack)

        return count

    return backtrack(0)

print(num_colorings(7, ['R', 'G', 'B']))

# -------  
# RGB
#               #1
#         / \ \  
#        R G  B
#       /\
#      B G      #2
#     /\
#    R  G       #3
#   /\
#  B  G         #4

# 3 + 3.2 + 3.2^2 + 3.2^3 + 3.2^4 + 3.2^5 + 3.2^6 = 3(2^7-1)=3x127=381 # dont count every node in the tree, count only the leaves, which is 3x2^6
# 1   2     3       4       5       6       7
    
# 5--0 # 6x2=12
# (1,2,3,4)--(0,5) # 4x2x6x2=96 

print('----')
n = 23
print(comb(n,8), 2*comb(n,7))
#print(factorial(4)*perm(5,4))
print(2*factorial(4)*factorial(4))
# P1C1P2C2P3C3P4C4
# C1P1C2P2C3P3C4P4
print(factorial(3)*factorial(4))
print(comb(4,2)*comb(5,2)*factorial(4))
print(2*comb(5,3)*comb(5,1))
# 1,3,5,7,9: 5 odd
# 2,4,6,8,10: 5 even
# 3 odd 1 even
# 3 even 1 odd

# 2^(6-k/2).3^(k/4)

# (n, k) (a^(3/4))^(n-k) (a^(-2/3))^k
# 3(n-k)/4 = 2k/3 = > 9n-9k=8k => 9n = 17k, n = 17 => k = 9

# (52,5) + (51,5) + .. + (47,5) + (46,5)


print(factorial(5)/factorial(3) + factorial(5)/factorial(2)/factorial(2) - factorial(4)/factorial(2))
print(3**6-3*2**6+3)
print(4**4-factorial(4))

# 120 = 75 + 60 + 45 - n(E & F) - n(E & S) - n(S & F) + n(E & S & F)
# n(E & F) + n(E & S) + n(S & F) - n(E & S & F) = 60
# n(Only E) => n(E) - n(E & S) - n(E & F) + n(E & S & F) = 75 - 60 + n(S & F) = 15 + n(S & F)
# n(Only F) => n(F) - n(F & S) - n(E & F) + n(E & S & F) = 45 - 60 + n(E & S) = -15 + n(E & S)
# n(Only S) => n(S) - n(F & S) - n(E & S) + n(E & S & F) = 60 - 60 + n(E & F) = n(E & F)
# sum: 60 + n(E & S & F)

print(2/5*1/3+3/5*2/3) 
print(600-(600/2+600/3-600/6))
print(120/2+120/3+120/5-120/6-120/15-120/10+120/30)
print(120/2+120/3-120/6)
print(factorial(4)*(1-1+1/2-1/6+1/24))
print(factorial(3)*4*factorial(3), factorial(6))
print((2+3+5)/21) 


# 1.1/6  + 2.5/6.1/6 + 3.(5/6)^2.1/6 + ... = 1/6. 1/(1/6)^2=6
print(0.4+0.6*0.4+0.6**2*0.4)
print(1/(1+(0.2*0.3)/(0.9*0.7)))
print((comb(48,3)*3+comb(48,2)*3+comb(48,1))/comb(51,4))
#print((49*72+48)/comb(51,4))
print((comb(48,3)*comb(4,2)+comb(48,2)*comb(4,3)+comb(48,1)*comb(4,4))/(comb(48,4)*comb(4,1)+comb(48,3)*comb(4,2)+comb(48,2)*comb(4,3)+comb(48,1)*comb(4,4)))


