import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def LR(X, y):
	reg = LinearRegression().fit(X, y)
	#reg.score(X, y)
	x = X.flatten()
	xbar, ybar = x.mean(), y.mean()
	print(xbar, ybar)
	print(np.sum((x-xbar)*(y-ybar)) / np.sum((x-xbar)**2))
	print(reg.coef_)
	print(reg.intercept_)
	yhat = reg.predict(X)
	RSS = np.sum((y-yhat)**2)
	n = len(x)
	RSE = np.sqrt(RSS / (n-2))
	print(RSS, RSE)
	Mx = (np.vstack((np.ones(len(x)), x))).T
	print(Mx.T)
	print(Mx.T@Mx)
	print(np.linalg.inv(Mx.T@Mx))
	print(Mx.T@y)
	print(np.linalg.solve(Mx.T@Mx, Mx.T@y))

print('start')
#X = np.array([[-2], [-1], [0], [1], [2]]) #np.array([[0], [0], [10], [10]])
#y = np.array([-7/2, -3, 0, 3, 7/2])
#LR(X, y)

def TS():
	b = -0.001 #2.939
	ts = -0.18 #9.42
	s = 0.0059 #0.3119
	print(b / s, b - 2*s, b + 2*s)

def PR(X, y, Xtest, k = 2):
	poly = PolynomialFeatures(degree=k, include_bias=False)
	poly_features = poly.fit_transform(X)
	poly_reg_model = LinearRegression()
	poly_reg_model.fit(poly_features, y)
	print(poly_reg_model.coef_)
	print(poly_reg_model.intercept_)
	print(poly_reg_model.predict(poly.fit_transform(Xtest)))
	x = X.flatten()
	n = len(x)
	Mx = np.ones((n, k+1))
	for i in range(1,k+1):
		Mx[:,i] = x**i
	print(Mx.T)
	print(Mx.T@Mx)
	print(np.linalg.inv(Mx.T@Mx))
	print(Mx.T@y)
	b = np.linalg.solve(Mx.T@Mx, Mx.T@y)
	print(b)
	xtest = Xtest.flatten()
	Mxtest = np.ones((1, k+1))
	for i in range(1,k+1):
		Mxtest[:,i] = xtest**i
	print(Mxtest@b)


#X = np.array([[1], [2], [3], [4]])
#y = np.array([2, 5, 13, 20])
#PR(X, y, np.array([[2],]))

def compute_prob(b, x):
	return 1/(1+ np.exp(-np.sum(b * x)))

print(compute_prob(np.array([-1, 0.01, 0.0004]), np.array([1, 35, 1900])))
print(0.65 / 0.0004)


