import numpy as np
from math import sin
		
DX = 0.0001

# d^2/dxdy
# vec = vector 
# i1, i2 = indies of the 2 variables in the vector
def mixed_second_derivative(f, vec, i1, i2, dx = DX):
	def vec_replaced(v1, v2):
		return [v1 if idx == i1 else v2 if idx == i2 else val 
			for idx, val in enumerate(vec)]
	def first_derivative(v1, v2):
		return ( f(vec_replaced(v1+dx, v2)) - f(vec_replaced(v1, v2))) / dx
	if i1==i2:
		return  ( first_derivative(vec[i1]+dx, vec[i2]) - first_derivative(vec[i1], vec[i2]) ) / dx
	return   ( first_derivative(vec[i1], vec[i2]+dx) - first_derivative(vec[i1], vec[i2]) ) / dx

# should be collomb vector I think
def gradient(f,vec, dx =  DX):
	def vec_replaced(i, v):
		return [v if idx == i else val for idx, val in enumerate(vec)]
	grad = []
	for idx, val in enumerate(vec):
		grad.append(
			  ( f(vec_replaced(idx, vec[idx]+dx)) - f(vec) ) / dx
		)
	return np.c_[grad]
'''
print(
	mixed_second_derivative(lambda v: sin(v[0])*v[1]**2, [143,10.5], 0, 1)
	)'''

# works
def hessian(f, vec):
	l = len(vec)
	H = np.zeros((l,l))
	for i in range(l):
		for j in range(l):
			H[j][i] = mixed_second_derivative(f, vec, i, j)
	return H

# just for testing
def f(v):
	x, y, z = v
	return x**2+y**2+z**2

#damped newtons method
def newtons_method(f, vec_start, n_iters, damping_factor = 0.1):
	guess = vec_starts
	for _ in range(n_iters):
		print(guess)
		guess = (guess 
			- (np.linalg.inv(damping_factor*np.identity(len(vec_start)) + hessian(f, guess)) 
		   @ gradient(f, guess)).transpose()[0])
	return guess

print (newtons_method(f, [10,234,14], 100))
'''
def f(v):
	x, y, z = v
	return 2*y*x**4 + 2*y**3 + 2*x*z**3'''
	
# print(gradient(f, [1,1,1])) works


'''
print(np.linalg.det(hessian(f, [-1,-1,-1]))) i think it works https://www.allmath.com/hessian-matrix-calculator.php#examples-of-hessian-matrix
print(hessian(f, [1,1,1]))
print(hessian(f, [-1,-1,-1]))
'''

