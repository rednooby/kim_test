import numpy as np
import random

class Network:
	layerLen=None
	trainErrFun=None
	trainErrFunRate=None
	testErrFun=None
	testErrFunRate=None
	w=None

	bestTrainErrFun=None
	bestTrainErrFunRate=None
	bestTestErrFun=None
	bestTestErrFunRate=None


#def NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainInput,trainDesiredOut,testInput,testDesiredOutput):

def NeuralNetworkLearn(Layers,trainInput,trainDesiredOut):
	inputRow, inputCol = trainInput.size/trainInput[0].size, trainInput[0].size
	outputRow, outputCol = trainDesiredOut.size/trainDesiredOut[0].size, trainDesiredOut[0].size


	# initialization
	network=Network()

	layerLen = len(Layers)
	#layerLen = Layers[0].size
	network.layerLen = layerLen

	# randomize the weight matricies
	network.w = []
	for i in range(layerLen-1):
		network.w.append(None)
	for i in range(layerLen-2):
		w_array = np.zeros(shape=(Layers[i+1],Layers[i]+1))
		for row in range(w_array.size/w_array[0].size):
			for col in range(w_array[0].size):
				w_array[row,col] = 1-2.0*random.random()
		network.w[i] = w_array
	temp_w_array = np.zeros(shape=(Layers[layerLen-1],Layers[layerLen-2]+1))
	for row in range(temp_w_array.size/temp_w_array[0].size):
		for col in range(temp_w_array[0].size):
			temp_w_array[row,col] = 1-2.0*random.random()
	network.w[layerLen-2] = temp_w_array






'''
----CODE TEST-------------------------------------------------
'''

# initialization
network=Network()


Layers=[8,4,2]
layerLen = 3
#layerLen = Layers[0].size
network.layerLen = layerLen

# randomize the weight matricies
network.w = []
for i in range(layerLen-1):
	network.w.append(None)
for i in range(layerLen-2):
	w_array = np.zeros(shape=(Layers[i+1],Layers[i]+1))
	for row in range(w_array.size/w_array[0].size):
		for col in range(w_array[0].size):
			w_array[row,col] = 1-2.0*random.random()
	network.w[i] = w_array
temp_w_array = np.zeros(shape=(Layers[layerLen-1],Layers[layerLen-2]+1))
for row in range(temp_w_array.size/temp_w_array[0].size):
	for col in range(temp_w_array[0].size):
		temp_w_array[row,col] = 1-2.0*random.random()
network.w[layerLen-2] = temp_w_array
print network.w

for i in range(len(network.w)):
	print i
	print network.w[i]
