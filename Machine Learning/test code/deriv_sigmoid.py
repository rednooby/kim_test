from sigmoid import sigmoid

def deriv_sigmoid(x):
	return sigmoid(x) * (1 - sigmoid(x))
