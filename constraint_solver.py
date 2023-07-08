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
	def second_derivative(v1, v2):
		return   ( first_derivative(v1, v2+dx) - first_derivative(v1, v2) ) / dx
	return second_derivative

'''
print(
	mixed_second_derivative(lambda v: sin(v[0])*v[1]**2, [10,10], 0, 1)(143,10.5)
	)'''

#  he entry of the ith row and the jth column in the hessian for function f at vector v
def hessian_item(f, i, j, vec):
	return ( d2_v(f) ) / ()
	
