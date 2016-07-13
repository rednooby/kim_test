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

a = np.array([[-1,2],[3,-4],[5,6]])
b=threshold_matrix(a)

print b
