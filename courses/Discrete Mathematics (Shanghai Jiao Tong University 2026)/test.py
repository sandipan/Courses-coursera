# Week 3
from itertools import permutations, product
from scipy.special import comb
from statistics import mode
from collections import Counter
from math import factorial

def count_f_monotone_injective(m, n): # comb
	#print len(filter(lambda x: list(x) == sorted(x), list(permutations(range(1,n+1),m))))
	print(comb(n, m, exact=True)) 
	
def count_f_monotone(m, n): # comb with rep
	#print len(filter(lambda x: list(x) == sorted(x), list(product(range(1,n+1), repeat=m))))
	print(comb(n, m, exact=True, repetition=True)	) 
	
def C(n, r):
	k = 1
	t = 1.
	while k <= r:
		t *= (n - k + 1) / k
	return(round(t)) 	
	
def count_f_almost_injective(n):  
	#print filter(lambda x: max(Counter(x).values()) <= 2, list(product(range(1,n+1), repeat=n)))
	print(len(filter(lambda x: max(Counter(x).values()) <= 2, list(product(range(1,n+1), repeat=n)))))  #mode(x)
	s, t, k = factorial(n), 1, 1
	while 2*k <= n:
		t *= comb(n - 2*(k-1), 2, exact=True)
		s += t * comb(n, k, exact=True) * comb(n - k, n - 2*k, exact=True) * factorial(n-2*k)
		k += 1
	print (s)

def count_f_almost_injective_monotone(n):  
	#print filter(lambda x: max(Counter(x).values()) <= 2 and sorted(x) == list(x), list(product(range(1,n+1), repeat=n)))
	print(len(filter(lambda x: max(Counter(x).values()) <= 2 and sorted(x) == list(x), list(product(range(1,n+1), repeat=n))))) #mode(x)
	s, t, k = factorial(n), 1, 1
	while 2*k <= n:
		t *= comb(n - 2*(k-1), 2, exact=True)
		s += t * comb(n, k, exact=True) * comb(n - k, n - 2*k, exact=True) * factorial(n-2*k)
		k += 1
	print (s)
	
def count_f_walk(n, f_0, f_n): 
	cur = [f_0]
	for i in range(1, n+1):
		nxt = [x + 1 for x in cur] +  [x - 1 for x in cur]
		cur = nxt
		#print i, cur
	print(len([1 for x in cur if x == f_n])) 

def count_f_lipchitz(n, f_0, f_n): 
	cur = [f_0]
	for i in range(1, n+1):
		nxt = [x + 1 for x in cur] +  [x - 1 for x in cur] + cur
		cur = nxt
		#print i, cur
	print(len([1 for x in cur if x == f_n])) 
	
#count_f_monotone_injective(10, 20)	
#count_f_monotone(3, 10)	
#count_f_monotone(10, 2)	
#count_f_almost_injective(5)
#count_f_almost_injective_monotone(5)
#count_f_walk(15, 0, 0)
#count_f_lipchitz(7, 0, 0)

#print(bin(1152921504606846987))

visited = set() # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  #function for dfs 
    global en
    if node not in visited:
        #print (node)
        visited.add(node)
        for neighbour in graph.get(node, []):
            en += '0'
            dfs(visited, graph, neighbour)
            en += '1'

en = '0'
dfs(set(), {0:[1,2,3], 3:[4]}, 0)
#dfs(set(), {0:[1,2,3], 1:[4,5], 2:[6,7], 3:[9,10], 7:[8], 9:[11], 10:[12]}, 0)
en += '1'
print(en)

import networkx as nx
import matplotlib.pylab as plt

G = nx.Graph()
G.add_nodes_from(range(1,5))
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(1,4)
G.add_edge(1,3)
nx.draw_networkx(G)
plt.show()

T=nx.minimum_spanning_tree(G)
Ge = sorted(G.edges(data=False))
Te = sorted(T.edges(data=False))
Re = sorted(list(set(Ge)-set(Te)))
print(Ge)
print(Te)
print(Re)

#Tes = []
#for e in Te:
#	for f in Re:
		#T = sorted(list((set(Te) - set([e])) | set([f])))
#		T = sorted(list((set(Te) - set([e])) | set([f])))
		#print(T)
#		Tes.append(T)

from itertools import combinations
Tes = list(combinations(list(G.edges), 3))
Tes = [x for (i, x) in enumerate(Tes) if not i in [3,7]]
print(len(Tes))

plt.figure(figsize=(10,8))		
i = 1
for T in Tes:
	Gt = nx.Graph()
	Gt.add_nodes_from(G.nodes)
	Gt.add_edges_from(T)
	print(Gt.nodes, Gt.edges)
	plt.subplot(4,3,i), nx.draw_networkx(Gt), plt.title(Gt.edges)
	i += 1
plt.suptitle('spanning tres')
plt.show()

G = nx.Graph()
G.add_nodes_from(range(len(Tes)))
for i in range(len(Tes)):
	for j in range(i+1, len(Tes)):
		if len(set(Tes[i]).intersection(Tes[j])) == 2:
			G.add_edge(i, j)
print(len(list(G.edges())))
nx.draw_networkx(G)
plt.show()
	
#s = Graph('spanning exchange', node_attr={'shape': 'plaintext'}, format='png')
# BBHE 
def plot_he_images(im_in, probs_in, im_out, probs_out, algo_name, s, e):
    plt.figure(figsize=(12,12))
    plt.gray()
    plt.subplot(221), plt.imshow(im_in, aspect='auto'), plt.axis('off'), plt.title('input', size=20)
    plt.subplot(222), plt.bar(range(s, e), probs_in[s:e], color='magenta')
    plt.title('input distribution of pixels\n(entropy = {:.3f})'.format(entropy(probs_in[s:e])), size=20)
    plt.subplot(223), plt.imshow(im_out, aspect='auto'), plt.axis('off'), plt.title('output (equalized)', size=20)
    plt.subplot(224), plt.bar(range(s, e), probs_out[s:e], color='magenta')
    plt.title('output distribution of pixels\n(entropy = {:.3f})'.format(entropy(probs_out[s:e])), size=20)
    plt.suptitle(f'Histogram Equalization with the {algo_name} algorithm', size=25)
    plt.tight_layout()
    plt.show()
    
def BBHE(im, probs):
    # computing mean brightness
    bbhe_mean = round(im.mean())
    print(bbhe_mean)

    # spliting historgam to two 
    p1, p2 = probs[:bbhe_mean], probs[bbhe_mean:]

    # normalizing histograms
    p1, p2 = p1 / sum(p1), p2 / sum(p2)

    # computing cumulative histograms
    c1, c2 = np.cumsum(p1), np.cumsum(p2)

    # LUT Transformation
    c1n = np.uint8(np.round((bbhe_mean-1) * c1))
    c2n = np.uint8(np.round(bbhe_mean + (255-bbhe_mean)*c2))
    
    im1 = im.copy()
    im1[im1 > bbhe_mean] = -1e-6
    im2 = im1.copy()
    probs_in = get_distr(im1)
    im1[im1 <= bbhe_mean] = c1n[im1[im1 <= bbhe_mean]]
    probs_out = get_distr(im1)
    plot_he_images(im2, probs_in, im1, probs_out, 'BBHE', 0, int(bbhe_mean))
    
    im1 = im.copy()
    im1[im1 < bbhe_mean] = -1e-6
    im2 = im1.copy()
    probs_in = get_distr(im1)
    im1[im1 > bbhe_mean] = c2n[im1[im1 > bbhe_mean]-bbhe_mean]
    probs_out = get_distr(im1)
    plot_he_images(im2, probs_in, im1, probs_out, 'BBHE', int(bbhe_mean), 256)

im_out = BBHE(im_in, probs_in)

def log(x):
    return np.log(x) if x > 0 else 0

def kittler_illingworth2(im):
    probs = get_distr(im)
    e = np.ones(255)*np.nan
    e_const = (1 + np.log(2*np.pi))/ 2
    for k in range(1, 256):
        ks1, ks2 = np.arange(k), np.arange(k, 256)
        p1, p2 = probs[:k], probs[k:]
        q1, q2 = np.sum(p1), np.sum(p2)
        m1, m2 = np.sum(ks1*p1) / q1, np.sum(ks2*p2) / q2
        v1, v2 = np.sum((ks1 - m1)**2*p1) / q1, np.sum((ks2 - m2)**2*p2) / q2
        cur_e = e_const - q1*log(q1) - q2*log(q2) + (q1*log(v1) + q2*log(v2))/2
        e[k-1] = cur_e
    t = np.argmin(e)
    return t, e

(new_thresh, _)=otsu(get_distr(im), im)

def gray2bgr(im):
    return np.repeat(im[:, :, np.newaxis], 3, axis=2)


def imflatfield(im, 𝜎):
    
    if len(im.shape) == 2:
        im = gray2bgr(im)
    
    im = im.astype('float32') / im.max() # A = im2single(I);
        
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)  # Ihsv = rgb2hsv(A);
    im_value = im_hsv[:, :, 2]  # A = Ihsv(:,:,3);
    fsz = int(2*np.ceil(2*𝜎) + 1);  # filterSize = 2*ceil(2*sigma)+1;
    # shading = imgaussfilt(A, sigma, 'Padding', 'symmetric', 'FilterSize', filterSize); % Calculate shading
    shading = cv2.GaussianBlur(im_value, (fsz, fsz), 𝜎, borderType=cv2.BORDER_REFLECT)
    mean_val = np.mean(im_value)  # meanVal = mean(A(:),'omitnan')
    #% Limit minimum to 1e-6 instead of testing using isnan and isinf after division.
    shading = np.maximum(shading, 1e-6)  # shading = max(shading, 1e-6);
    im_value = im_value * mean_val / shading  # B = A*meanVal./shading;
    #% Put processed V channel back into HSV image, convert to RGB
    im_hsv[:, :, 2] = im_value  # Ihsv(:,:,3) = B;
    im = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)  # B = hsv2rgb(Ihsv);
    im = np.round(np.clip(im*255, 0, 255)).astype(np.uint8)  # B = im2uint8(B);

    return im
	
def gray2bgr(im):
    return np.repeat(im[:, :, np.newaxis], 3, axis=2)


def imflatfield(im, 𝜎):
    
    if len(im.shape) == 2:
        im = gray2bgr(im)
    
    im = im.astype('float32') / im.max() # A = im2single(I);
        
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)  # Ihsv = rgb2hsv(A);
    im_value = im_hsv[:, :, 2]  # A = Ihsv(:,:,3);
    fsz = int(2*np.ceil(2*𝜎) + 1);  # filterSize = 2*ceil(2*sigma)+1;
    # shading = imgaussfilt(A, sigma, 'Padding', 'symmetric', 'FilterSize', filterSize); % Calculate shading
    shading = cv2.GaussianBlur(im_value, (fsz, fsz), 𝜎, borderType=cv2.BORDER_REFLECT)
    mean_val = np.mean(im_value)  # meanVal = mean(A(:),'omitnan')
    #% Limit minimum to 1e-6 instead of testing using isnan and isinf after division.
    shading = np.maximum(shading, 1e-6)  # shading = max(shading, 1e-6);
    im_value = im_value * mean_val / shading  # B = A*meanVal./shading;
    #% Put processed V channel back into HSV image, convert to RGB
    #im_hsv[:, :, 2] = im_value  # Ihsv(:,:,3) = B;
    #im = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR)  # B = hsv2rgb(Ihsv);
    im_value = np.round(np.clip(im_value*255, 0, 255)).astype(np.uint8)  # B = im2uint8(B);

    return im_value

im = cv2.cvtColor(cv2.imread('images/ship.jpg').astype('uint8'), cv2.COLOR_BGR2RGB)
segment_with_flatfield(im, 𝜎=25)

#im = cv2.cvtColor(cv2.imread('images/ship.jpg').astype('uint8'), cv2.COLOR_BGR2GRAY)
im = cv2.cvtColor(cv2.imread('images/ship.jpg').astype('uint8'), cv2.COLOR_BGR2RGB)
im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)  # Ihsv = rgb2hsv(A);
im = im_hsv[:, :, 2]  # A = Ihsv(:,:,3); 
segment_with_flatfield(im, 𝜎=25)
k, _ = otsu(im)
im_b = np.zeros_like(im)
im_b[im > k] = 255
plt.figure(figsize=(8,6))
plt.imshow(im_b), plt.axis('off')
plt.show()


def imadjust(x,a,b,c,d,gamma=1):
    # Similar to imadjust in MATLAB.
    # Converts an image range from [a,b] to [c,d].
    # The Equation of a line can be used for this transformation:
    #   y=((d-c)/(b-a))*(x-a)+c
    # However, it is better to use a more generalized equation:
    #   y=((x-a)/(b-a))^gamma*(d-c)+c
    # If gamma is equal to 1, then the line equation is used.
    # When gamma is not equal to 1, then the transformation is not linear.

    y = ((((x - a) / (b - a)) ** (1/gamma)) * (d - c) + c).astype(np.uint8)
    return y

im = cv2.imread('images/me_dark.jpg', 0)
plt.figure(figsize=(20,10))
plt.subplot(151), plt.imshow(im), plt.axis('off'), plt.title('input', size=20)
i = 2
for 𝛾 in [1/10, 2, 5, 10]:
    im2 = imadjust(im, 0, 255, 0, 255, 𝛾)
    plt.subplot(1,5,i), plt.imshow(im2), plt.axis('off'), plt.title(r'corrected ($\gamma=$' + f'{𝛾})', size=20)
    i += 1
plt.tight_layout()
plt.show()

def rgb_to_hsv(r, g, b):
  r /= 255
  g /= 255
  b /= 255
  maxc = max(r, g, b)
  minc = min(r, g, b)
  v = maxc
  if minc == maxc:
      return 0.0, 0.0, v
  s = (maxc-minc) / maxc
  rc = (maxc-r) / (maxc-minc)
  gc = (maxc-g) / (maxc-minc)
  bc = (maxc-b) / (maxc-minc)
  if r == maxc:
      h = 0.0+bc-gc
  elif g == maxc:
      h = 2.0+rc-bc
  else:
      h = 4.0+gc-rc
  h = (h/6.0) % 1.0
  return h * 360, s * 100, v * 100
  
def hsv_to_rgb(h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
		
from skimage.color import rgb2hsv, hsv2rgb
im_in = plt.imread('images/me_dark.jpg')
print(im_in.dtype)
probs_in = get_distr(im_in)

im_out_che = rgb2hsv(im_in.copy())
print(im_out_che.dtype, im_out_che.max())
im_out_che[...,2] = CHE((100*im_out_che[...,2]).astype(np.uint8), probs_in)/100
im_out_che = hsv2rgb(im_out_che)

def CLAHE(im, wsz=8, threshold=0.3):    
    h, w = im.shape
    out = np.zeros(im.shape) # Declare output variable
    im = np.pad(im.copy(), ((wsz//2, wsz//2), (wsz//2, wsz//2)), mode = 'reflect')
    for x in range(wsz//2, h + wsz//2):
        print(x)
        for y in range(wsz//2, w + wsz//2):
            blk = im[x-wsz//2:x+wsz//2, y-wsz//2:y+wsz//2]
            probs = get_distr(blk)
            clipped = probs > threshold
            probs[clipped] = threshold
            diff_probs = 1 - probs.sum()
            probs[~clipped] += diff_probs / 256
            out[x - wsz//2, y - wsz//2] = (255*np.cumsum(probs))[im[x,y]]
    return out

wsz = 32 
im_out_clahe = rgb2hsv(im_in.copy())
im_out_clahe[...,2] = CLAHE((100*im_out_clahe[...,2]).astype(np.uint8), wsz)/100
im_out_clahe = hsv2rgb(im_out_clahe)

plt.figure(figsize=(15,6))
plt.subplots_adjust(0,0,1,0.95,0.05,0.05)
plt.subplot(131), plt.imshow(im_in), plt.axis('off'), plt.title('input', size=20)
plt.subplot(132), plt.imshow(im_out_che), plt.axis('off'), plt.title('output (CHE)', size=20)
plt.subplot(133), plt.imshow(im_out_clahe), plt.axis('off'), plt.title('output (CLAHE)', size=20)
plt.show()

def hue_adjust(img, angle):
    hsv = rgb2hsv(img)
    hue = 360*hsv[...,0]
    hsv[...,0] = (hue + angle % 360) / 360
    return hsv2rgb(hsv)

from skimage.color import rgb2hsv, hsv2rgb
im_in = plt.imread('images/parrot.jpg')
print(im_in.dtype)
im_out = hue_adjust(im_in, 60)
plt.figure(figsize=(15,8))
plt.subplots_adjust(0,0,1,0.95,0.05,0.05)
plt.subplot(121), plt.imshow(im_in), plt.axis('off'), plt.title('input', size=20)
plt.subplot(122), plt.imshow(im_out), plt.axis('off'), plt.title(r'output (Hue shifted / rotated by $60^o$)', size=20)
plt.show()

def sepia(img):
    #im = np.reshape(img, (-1,3))
    im = img.copy()
    im = im / im.max()
    M = np.array([[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.131]])
    im = im @ M.T
    #im = np.reshape(im, img.shape)
    im = im / im.max()
    return im
    
im = plt.imread('images/bridge4.jpeg')
im2 = sepia(im)

plt.figure(figsize=(15,8))
plt.subplots_adjust(0,0,1,0.95,0.05,0.05)
plt.subplot(121), plt.imshow(im), plt.axis('off'), plt.title('input', size=20)
plt.subplot(122), plt.imshow(im2), plt.axis('off'), plt.title(r'output (with sepia filter)', size=20)
plt.show()


import seaborn as sns
M = np.array([[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.131]])
sns.heatmap(M, annot=True, fmt=".3f", annot_kws={
                'fontsize': 16,
                'fontweight': 'bold',
                'fontfamily': 'serif'
            })
			
def CLAHE(im, wsz=8, threshold=0.3):    
    h, w = im.shape
    out = np.zeros(im.shape) # Declare output variable
    im = np.pad(im.copy(), ((wsz//2, wsz//2), (wsz//2, wsz//2)), mode = 'reflect')
    for x in range(wsz//2, h + wsz//2):
        print(x)
        for y in range(wsz//2, w + wsz//2):
            blk = im[x-wsz//2:x+wsz//2, y-wsz//2:y+wsz//2]
            probs = get_distr(blk)
            clipped = probs > threshold
            probs[clipped] = threshold
            diff_probs = 1 - probs.sum()
            probs[~clipped] += diff_probs / 256
            out[x - wsz//2, y - wsz//2] = (255*np.cumsum(probs))[im[x,y]]
    return out

from skimage.color import rgb2hsv, hsv2rgb
im_in = plt.imread('images/me_dark.jpg')
print(im_in.dtype)
probs_in = get_distr(im_in)

im_out_che = rgb2hsv(im_in.copy())
print(im_out_che.dtype, im_out_che.max())
im2 = CHE((256*im_out_che[...,2]).astype(np.uint8), probs_in)
im_out_che[...,2] = im2 / im2.max()
im_out_che = hsv2rgb(im_out_che)

wsz = 64 
im_out_clahe = rgb2hsv(im_in.copy())
im2 = CLAHE((256*im_out_clahe[...,2]).astype(np.uint8), wsz)
im_out_clahe[...,2] = im2 / im2.max()
im_out_clahe = hsv2rgb(im_out_clahe)

plt.figure(figsize=(15,6))
plt.subplots_adjust(0,0,1,0.95,0.05,0.05)
plt.subplot(131), plt.imshow(im_in), plt.axis('off'), plt.title('input', size=20)
plt.subplot(132), plt.imshow(im_out_che), plt.axis('off'), plt.title('output (CHE)', size=20)
plt.subplot(133), plt.imshow(im_out_clahe), plt.axis('off'), plt.title('output (CLAHE)', size=20)
plt.show()

#print(filtered_events.groupby('event_id').agg({'vid':['min'], 'indx_vid':['min']}).pipe(lambda x: x.set_axis(x.columns.map('_'.join), axis=1)))    