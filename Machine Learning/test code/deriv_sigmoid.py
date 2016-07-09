from sigmoid import sigmoid

def deriv_sigmoid(x):
	return sigmoid(x) * (1 - sigmoid(x))

value = 10
print deriv_sigmoid(value)
