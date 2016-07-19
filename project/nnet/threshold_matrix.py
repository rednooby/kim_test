'''
threshold of array
'''


import numpy as np


def threshold_matrix(array):
	row, col = len(array), len(array[0])

	for i in range(row):
		for j in range(col):
			if array[i][j] < 0:
				array[i][j] = 0
			else:
				array[i][j] = 1
	y=array
	return y
