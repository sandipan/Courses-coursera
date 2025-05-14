def extended_gcd(a, b):
  assert a >= b and b >= 0 and a + b > 0
  if b == 0:
    d, x, y = a, 1, 0
  else:
   (d, p, q) = extended_gcd(b, a % b)
   x = q
   y = p - q * (a // b)
  assert a % d == 0 and b % d == 0
  assert d == a * x + b * y
  return (d, x, y)

def gcd(a, b):
  swapped = False
  if a < b:
    a, b, swapped = b, a, True
  d, x, y = extended_gcd(a, b)
  if swapped:
    x, y = y, x
  return (d, x, y)

def lcm(a, b):
   assert a != 0 and b != 0
   return a*b // gcd(a,b)[0]
  
def diophantine(a, b, c):
	d, x, y = gcd(a,b)
	assert c % d == 0
	k = c // d
	# return (x y) such that a * x + b * y = c
	return (k*x, k*y)
	
def divide(a, b, n):
  d, x, y = gcd(a, n)
  assert n > 1 and a > 0 and d == 1  
  # return the number x s.t. x = b / a (mod n) and 0 <= x <= n-1.
  return (b*x) % n

#divide(7, 2, 9)

def ChineseRemainderTheorem(n1, r1, n2, r2):
  (x, y) = ExtendedEuclid(n1, n2)
  return (n1*x*r2 + n2*y*r1) % (n1*n2)
  
def FastModularExponentiation(b, k, m):
  # your code here
  res = b % m 
  for i in range(k):
    res = (res * res) % m
  return res

#print(FastModularExponentiation(3, 2, 100))

def FastModularExponentiation(b, e, m):
  # your code here
  d = e
  p = b % m
  res = 1
  while d != 0:
    #print(e, d)
    e = d % 2
    if e:
      res = (res * p) % m
    d //= 2
    p = (p * p) % m
  return res

def primes_list(n):
  lst = list(range(2,n))
  i = 0
  while lst[i]*lst[i] < n:
    for j in range(n//lst[i]+1):
      m = lst[i]*j
      if m in lst:
        lst.remove(m)
    i += 1
  return lst

#FastModularExponentiation(3, 5, 100)

#ChineseRemainderTheorem(11, 3, 17, 7)
print(lcm(1980,1848))
print(diophantine(17, 11, 4))

for q1 in range(11):
	for q2 in range(17):
		if 11*q1 - 17*q2 == 4:
			print(q1, q2)
			break