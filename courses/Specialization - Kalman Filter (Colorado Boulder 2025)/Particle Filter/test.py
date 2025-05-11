def approx_rect(x, g, w=None):
  Nr = len(x) - 1
  if not w:
    w = (max(x) - min(x)) / Nr
  else:
    w = len(x)
  xmin = 0 
  #xmin = min(x)
  return sum([w*g[xmin + (i+1/2)*w] for i in range(Nr+1)])

def approx_trap(x, g, w=None):
  n = len(g)
  Nr = len(x) - 1
  xmin, xmax = min(x), max(x)
  if not w:
    w = (xmax - xmin) / Nr
  print(w)
  return w*(g[xmin] + g[xmax]) / 2 + sum([w*g[xmin + i*w] for i in range(1,Nr)]) 

#w = 0.5
x = [0.25, 0.75, 1.25, 1.75]
g = [0.0625, 0.5625, 1.5625, 3.0625]
g = {k: v for k, v in zip(x, g)}
print(approx_rect(x, g))

x = [0, 0.5, 1, 1.5, 2]
g = [0, 0.25, 1, 2.25, 4]
g = {k: v for k, v in zip(x, g)}
print(approx_trap(x, g))

#x = [0.5, 1.5, 2, 2.5]
#g = [0.125, 3.375, 15.625, 42.875]
#g = {k: v for k, v in zip(x, g)}
#print(approx_rect(x, g, 1))

x = list(range(5))
g = [x**3 for x in range(5)]
g = {k: v for k, v in zip(x, g)}
print(approx_trap(x, g, 1))
