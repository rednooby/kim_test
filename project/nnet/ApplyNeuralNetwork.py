import numpy as np
from threshold_matrix import threshold_matrix


def ApplyNeuralNetwork(network, data):
	out=[]
	for i in range(network.layerLen):
		out.append(None)
	out[0] = []
	for i in range(len(data)):
		out[0].append(-1)
	out[0] = [out[0]]
	for d in data.transpose().tolist():
		out[0].append(d)
	out[0] = np.array(out[0])
	for i in range(1,network.layerLen):
		out[i] = np.dot(network.w[i-1], out[i-1])
		out[i] = threshold_matrix(out[i])
		temp = []
		for j in range(len(data)):
			temp.append(-1)
		temp = [temp]
		for da in out[i].tolist() :
			temp.append(da)
		out[i] = np.array(temp)

	output = np.array(out[network.layerLen-1][1:])

	return output.transpose()
