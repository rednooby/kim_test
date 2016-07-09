import numpy as np


def threshold_matrix(matrix):
	row, col = matrix.size/matrix[0].size, matrix[0].size

	for i in range(row):
		for j in range(col):
			if matrix.item(i,j) < 0:
				matrix[i,j] = 0
			else:
				matrix[i,j] = 1
	y=matrix
	return y

a = np.matrix('-1 2; 3 -4; 5 6')
b=threshold_matrix(a)

print b
