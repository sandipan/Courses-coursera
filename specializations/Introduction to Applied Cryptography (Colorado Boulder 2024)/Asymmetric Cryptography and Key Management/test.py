def phi(n):
	congruence_class = [i for i in range(1, n) if gcd(i, n) == 1]
	return congruence_class, len(congruence_class)

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def find_primitive_roots(n):
	c, p = phi(n)
	pr = []
	for a in c:
		row = [a**i % n for i in range(1, p+1)]
		print(row)
		s = set(row)
		if len(s) == p:
			pr.append(a)
	return pr
	
def find_discrete_log(a, m, y):
	_, p = phi(m)
	if a in find_primitive_roots(m):
		for b in range(1, p):
			if a**b % m == y:
				return b
	return None
	
n = 14 #9 #7
print(find_primitive_roots(n))
#print(find_discrete_log(3, 5, 4))
#print(find_discrete_log(2, 5, 3))
#print(find_discrete_log(5, 7, 4))
print(find_discrete_log(2, 11, 9))
#print(find_discrete_log(2, 11, 3))