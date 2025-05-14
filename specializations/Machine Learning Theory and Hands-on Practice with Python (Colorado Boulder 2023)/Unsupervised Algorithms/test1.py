def compute_prob(pL = 3/8, TPR=0.95, FNR=0.2, times=10):
	# P(L|268) = 0.95
	# P(L|13457) = 0.2
	# P(268|L)
	#0.95*3/8
	# P(13457|L)
	#0.2*5/8
	# P(268|D) normalized
	#(0.05*3/8) / (0.05*3/8 + 0.8*5/8)
	# P(8)
	#(0.05/8) / (0.05*3/8 + 0.8*5/8)
	print(pL)
	for time in range(times):
		pL = TPR*pL / (TPR*pL + FNR*(1-pL))
		print(time, pL)
	return(pL)

compute_prob()
#compute_prob(2/5, 0.9, 0.1)

from scipy.sparse import csr_matrix
        
def pairwise_jaccard(X):
	"""Computes the Jaccard distance between the rows of `X`.
	"""
	X = X.astype(bool).astype(int)

	intrsct = X.dot(X.T)
	row_sums = intrsct.diagonal()
	unions = row_sums[:,None] + row_sums - intrsct
	return intrsct / unions

def pairwise_jaccard_sparse(X):
	"""Computes the Jaccard distance between the rows of `csr`,
	"""
	csr = csr_matrix(X)

	csr_rownnz = csr.getnnz(axis=1)
	intrsct = csr.dot(csr.T.asfptype().power(-1))
	intrsct[intrsct != 1.0] = 0
	print(intrsct)

	nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
	unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
	sim = intrsct.data / unions
	
	mask = (sim > 0) & (sim <= 1)
	data = sim[mask]
	indices = intrsct.indices[mask]

	rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
	indptr = np.r_[0, np.cumsum(rownnz)]

	out = csr_matrix((data, indices, indptr), intrsct.shape)
	return out.toarray()

def jaccard_sim_matrix(X):
	"""X is an integer array of features"""

	sparseX = csr_matrix(X)

	# make a binary version of the matrix
	binX = sparseX.copy()
	binX.data[:] = 1

	intersection = ((sparseX * binX.T) + (binX * sparseX.T))

	rowwise_sum = np.sum(sparseX, axis=1)
	union = np.repeat(rowwise_sum, intersection.shape[0], axis=1) + \
			np.repeat(rowwise_sum.T, intersection.shape[0], axis=0)

	return np.array(intersection / union)

#return jaccard_sim_matrix(Xr.T)
#return pairwise_jaccard(Xr.T)
return pairwise_jaccard_sparse(Xr.T)
#from sklearn.metrics import pairwise

#x = Xr.T #csr_matrix(Xr.T)
#return 1-pairwise.pairwise_distances(x, x, metric='jaccard')

#X = np.array([[5,4,2,3,1,0,0,0,0],[4,0,0,0,0,5,3,2,1]])
#jaccard_sim_matrix(X)
        
		
A = np.array([[1,2,1],[1,4,5]])
A = csr_matrix(A)
I = A.dot(A.T.asfptype().power(-1))
#A[A != 1] = 0
I.toarray()

from scipy.spatial import distance        
from scipy.sparse.csc import csc_matrix
from scipy.sparse import kron
A = np.random.random((3000, 3000)) #np.array([[1,2,0,3],[1,2,2,3]])
t0=time.perf_counter()
jac_sim(A)
t1=time.perf_counter()
print(t1-t0)
#print(1-distance.cdist(A, A, 'jaccard'), (A)) #jaccard_sim_matrix(A) #, pairwise_jaccard_sparse(A) 
#A = csc_matrix(A)
#A.data
# benchmark performance 
X = np.random.random((3000, 3000))
# binarize
X[X > 0.3] = 0
X[X>0] = 1
mat =  csr_matrix(X)

a = np.zeros(3000)
a[4] = a[100] = a[22] =1
a = csr_matrix(a)

print(mat.shape, a.shape, )
#my_jaccard1(mat, a)

def jaccard_sim_matrix(X):
    sparseX = csr_matrix(X)

    # make a binary version of the matrix
    binX = sparseX.copy()
    binX.data[:] = 1
    print(sparseX)
    print('here')
    print(binX)
    print('here')
    
    intersect = (sparseX.T @ sparseX)
    #intersect.data %= 2
    print(intersect)
    print('here 2')

    intersection = ((sparseX * binX.T) + (binX * sparseX.T))
    print(intersection)

    rowwise_sum = np.sum(sparseX, axis=1)
    print(rowwise_sum)
    union = np.repeat(rowwise_sum, intersection.shape[0], axis=1) + \
            np.repeat(rowwise_sum.T, intersection.shape[0], axis=0)
    print(union)
    
    #intrsct = X.dot(X.T)
    #        row_sums = intrsct.diagonal()
    #        unions = row_sums[:,None] + row_sums - intrsct
            
    return np.array(intersection / union)

def pairwise_jaccard_sparse(X):
    """Computes the Jaccard distance between the rows of `csr`,
    """
    csr = csr_matrix(X)

    csr_rownnz = csr.getnnz(axis=1)
    intrsct = csr.dot(csr.T)

    nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
    unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
    sim = intrsct.data / unions
    print(sim)

    mask = (sim > 0)
    data = sim[mask]
    indices = intrsct.indices[mask]

    rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
    indptr = np.r_[0, np.cumsum(rownnz)]

    out = csr_matrix((data, indices, indptr), intrsct.shape)
    return out.toarray()

def jac_sim(A):
    n = A.shape[0]
    A = csr_matrix(A)
    S = np.ones((n,n))
    for i in range(n):
        for j in range(i+1,n):
            v1, v2 = A.getrow(i), A.getrow(j)
            intersect = (v1 == v2).getnnz()
            union = (v1 + v2).getnnz()
            S[i,j] = S[j,i] = intersect / union
    return S
            
def jaccard_fast(v1,v2):
    common = (v1 == v2).getnnz()
    dis = (v1 != v2).getnnz()
    if common[0,0]:
        return 1.0-float(common[0,0])/float(common[0,0]+dis)
    else:
        return 0.0
    
def benchmark_jaccard_fast():
    for i in range(mat.shape[0]):
        jaccard_fast(mat.getrow(i),a)

def my_jaccard1(mat, a):
    common = (mat == a)#.getnnz(axis=1) #mat*a.T
    print(common.shape, common.dtype)
    cA = common.A.ravel()
    print(cA.shape)
    aM = kron(a,np.ones((mat.shape[0],1),int))
    print(aM.shape)
    dis = (mat!=aM).sum(1)
    ret = 1-cA/(cA+dis.A1)
    return ret   


from scipy.spatial import distance
x = np.array([[1,1,0],[1,0,0]])
x = x / np.linalg.norm(x, axis=1, keepdims=True)
x.dot(x.T), 1-distance.cdist(x, x, 'cosine')

 def normalize(x):
	#z = np.sqrt(np.sum(x.T@x)) #np.linalg.norm(x)
	#return x / z if z else x
	l2 = np.atleast_1d(np.linalg.norm(x, 2, axis=-1))
	l2[l2==0] = 1
	return x / np.expand_dims(l2, axis=-1)

def pairwise_jaccard_sparse(X):
    X = X >= 1
    csr = csr_matrix(X).astype(bool).astype(int)

    csr_rownnz = csr.getnnz(axis=1)
    intrsct = csr.dot(csr.T)

    nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
    unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
    sim = intrsct.data / unions

    mask = (sim > 0)
    data = sim[mask]
    indices = intrsct.indices[mask]

    rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
    indptr = np.r_[0, np.cumsum(rownnz)]

    out = csr_matrix((data, indices, indptr), intrsct.shape)
    return out.toarray()

x = np.array([[1,1,0],[1,0,1]])
1-distance.cdist(x, x, 'jaccard'), pairwise_jaccard_sparse(x)

x = Xr.T
n = x.shape[0]
S = np.ones((n, n))
for i in range(n):
	for j in range(i+1, n):
		S[i,j] = S[j,i] = jaccard(x[i], x[j])
#return S

def pairwise_jaccard_sparse(X):
    X = X >= 1
    csr = csr_matrix(X).astype(bool).astype(int)

    csr_rownnz = csr.getnnz(axis=1)
    intrsct = csr.dot(csr.T)

    nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
    unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
    sim = intrsct.data / unions
    print(csr_rownnz)
    print(intrsct.indptr) 
    print(intrsct.data) 
    print(intrsct.indices) 
    print('here', nnz_i) 
    print('here', csr_rownnz[intrsct.indices]) 
    print(unions)
    print(sim)

    #mask = (sim > 0)
    #data = sim[mask]
    #indices = intrsct.indices[mask]

    #rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
    #print('here', rownnz)
    #indptr = np.r_[0, np.cumsum(rownnz)]
    
    out = csr_matrix((sim, intrsct.indices, intrsct.indptr), intrsct.shape)
    #out = csr_matrix((data, indices, indptr), intrsct.shape)
    return out.toarray()

x = np.array([[1,1,0],[1,0,1], [1,1,1]])
pairwise_jaccard_sparse(x)

a = np.array([[1,0,1],[0,1,0],[0,0,1]])
col_mean = np.nanmean(a, axis=0)
print(col_mean)
a = a.T
np.where(np.equal(a, 0), col_mean, a)
#def func(x):
#    return x[x==0] = 
#np.apply_along_axis(func, 1, x)

#Baseline solution for Coursera course Unsupervised Algorithms

wb = cv2.xphoto.createGrayworldWB()
wb.setSaturationThreshold(0.99) #99)
img1 = wb.balanceWhite(img)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

b,g,r = cv2.split(noisy_img)           # get b,g,r
rgb_img = cv2.merge([r,g,b])     # switch it to rgb
b,g,r = cv2.split(dst)           # get b,g,r
rgb_dst = cv2.merge([r,g,b])     # switch it to rgb

#cv2.xphoto.bm3dDenoising(img, dst, 10, 4, 16, 2500, 400, 8, 1, 0.0, cv2.NORM_L2, cv2.xphoto.BM3D_STEPALL)
import numpy as np
from skimage.io import imread
from skimage.util import crop
import matplotlib.pylab as plt
from glob import glob

for f in glob('images/out/*lena*.png'):
    print(f)
    A = imread(f)
    fname = f.split('\\')[-1]

    # crop_width{sequence, int}: Number of values to remove from the edges of each axis. 
    # ((before_1, after_1), … (before_N, after_N)) specifies unique crop widths at the 
    # start and end of each axis. ((before, after),) specifies a fixed start and end 
    # crop for every axis. (n,) or n for integer n is a shortcut for before = after = n 
    # for all axes.
    B = crop(A, ((375, 402), (179, 179), (0,0)), copy=False)

    print(A.shape, B.shape)
    # (220, 220, 3) (70, 120, 3)

    #plt.figure(figsize=(10,7))
    #plt.subplots_adjust(0,0,1,1,0.01,0.01)
    #plt.imshow(B), plt.axis('off') 
    #plt.show()

    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(20,15))
    plt.subplots_adjust(0,0,1,0.95,0.02,0.02)
    gs1 = GridSpec(3, 3, left=0.05, right=0.95, wspace=0.05)
    ax1 = fig.add_subplot(gs1[:-2, :-1])
    ax1.imshow(imread('images/Img_02_10.jpg'), aspect='auto'), ax1.axis('off'), ax1.set_title('input image', size=20)
    ax2 = fig.add_subplot(gs1[:-2, -1])
    ax2.imshow(imread('images/Img_02_05.jpg'), aspect='auto'), ax2.axis('off'), ax2.set_title('guide image', size=20)
    ax3 = fig.add_subplot(gs1[-2:, :])
    ax3.imshow(B), ax3.axis('off')
    #plt.show()
    plt.savefig('images/out1/{}'.format(fname))
    plt.close()
import numpy as np
from skimage.io import imread
from skimage.util import crop
import matplotlib.pylab as plt
from glob import glob

for f in glob('C:/Users/Sandipan.Dey/Downloads/dd.tar/out/*umbc*.png'):
    print(f)
    A = imread(f)
    fname = f.split('\\')[-1]

    # crop_width{sequence, int}: Number of values to remove from the edges of each axis. 
    # ((before_1, after_1), … (before_N, after_N)) specifies unique crop widths at the 
    # start and end of each axis. ((before, after),) specifies a fixed start and end 
    # crop for every axis. (n,) or n for integer n is a shortcut for before = after = n 
    # for all axes.
    B = crop(A, ((140, 140), (10, 10), (0,0)), copy=False)

    #print(A.shape, B.shape)
    # (220, 220, 3) (70, 120, 3)

    #plt.figure(figsize=(10,7))
    #plt.subplots_adjust(0,0,1,1,0.01,0.01)
    #plt.imshow(B), plt.axis('off') 
    #plt.show()

    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(15,15))
    plt.subplots_adjust(0,0,1,0.95,0.02,0.02)
    gs1 = GridSpec(3, 3, left=0.05, right=0.95, wspace=0.05)
    ax1 = fig.add_subplot(gs1[:-2, :-1])
    ax1.imshow(imread('C:/Users/Sandipan.Dey/Desktop/Img_02_04.jpg'), aspect='auto'), ax1.axis('off'), ax1.set_title('input image', size=20)
    ax2 = fig.add_subplot(gs1[:-2, -1])
    ax2.imshow(imread('C:/Users/Sandipan.Dey/Desktop/umbc.jpg'), aspect='auto'), ax2.axis('off'), ax2.set_title('guide image', size=20)
    ax3 = fig.add_subplot(gs1[-2:, :])
    ax3.imshow(B), ax3.axis('off')
    #plt.show()
    plt.savefig('images/out/{}'.format(fname))
    plt.close()
	
def dream(model,
          base_img,
          end_layer=30,
          octave_n=6,
          octave_scale=1.4,
          control=None,
          distance=objective_L2):
    
    octaves = [base_img]
    for i in range(octave_n - 1):
        octaves.append(ndimage.zoom(octaves[-1], (1, 1, 1.0 / octave_scale, 1.0 / octave_scale),  order=1))
    
    print(len(octaves))
    detail = np.zeros_like(octaves[-1])
    for octave, octave_base in enumerate(octaves[::-1]):
        h, w = octave_base.shape[-2:]
        if octave > 0:
            h1, w1 = detail.shape[-2:]
            detail = ndimage.zoom(detail, (1, 1, 1.0 * h / h1, 1.0 * w / w1), order=1)
        plt.figure(figsize=(20,10))
        plt.subplot(121), plt.imshow(np.transpose(octave_base[0], (1,2,0))), plt.axis('off')
        plt.subplot(122), plt.imshow(np.transpose(detail[0], (1,2,0))), plt.axis('off')
        plt.tight_layout()
        plt.show()
        input_oct = octave_base + detail
        out = make_step(input_oct, model, control, end_layer=end_layer, distance=distance)
        detail = out - octave_base
        