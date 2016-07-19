'''
sigmoid function
'''

import numpy as np

def sigmoid(x):
	y = 1.0/(1+np.exp(-x))
	return y
