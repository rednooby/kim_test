import numpy as np
import random
import sys
from sigmoid import sigmoid
from deriv_sigmoid import deriv_sigmoid
from deriv_squared_error import deriv_squared_error
from numpy.linalg import inv

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

#def NeuralNetworkLearn(Layers,errFunChgLmt,weightChgLmt,maxRound,trainInput,trainDesiredOut):
def NeuralNetworkLearn(Layers,trainInput,trainDesiredOut):
	inputRow, inputCol = len(trainInput), len(trainInput[0])
	outputRow, outputCol = len(trainDesiredOut), len(trainDesiredOut[0])

	# initialization
	network=Network()

	layerLen = len(Layers)
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

	# initialize stopping conditions
	errFunChg = sys.float_info.max;  # assuming the intial weight matrices are bad
	weightChg = sys.float_info.max;
	round_count = 0;
	min_trainErrFun = sys.float_info.max;


	while errFunChg > errFunChgLmt and weightChg > weightChgLmt and round_count < maxRound:
		m = inputRow  # number of examples

		# forwardProp
		out = []
		for i in range(layerLen):
			out.append(None)
		out[0] = []
		for i in range(m):
			out[0].append(-1)
		out[0] = [out[0]]
		for train in trainInput.transpose().tolist():
			out[0].append(train)
		out[0] = np.array(out[0])
		z=[]
		for i in range(layerLen):
			z.append(None)
		for i in range(layerLen-1):
			z[i+1] = np.dot(network.w[i],out[i]) # z = w*o

			temp_list = []
			for j in range(m):
				temp_list.append(-1)
			out[i+1]=[temp_list]
			for z_val in sigmoid(z[i+1]).tolist():
				out[i+1].append(z_val)
			out[i+1] = np.array(out[i+1])

		output = np.array(out[layerLen-1][1:])

		err = np.mean((output-np.array(trainDesiredOut).transpose()) * (output-np.array(trainDesiredOut).transpose()), axis=0)

'''
garbage
		# forwardProp
		out = []
		for i in range(layerLen):
			out.append(None)
		out[0] = []
		for i in range(m):
			out[0].append(-1)
		out[0] = [out[0]]
		for train in trainInput.transpose().tolist():
			out[0].append(train)
		out[0] = np.array(out[0])
		z=[]
		for i in layerLen:
			z.append(None)
		for i in layerLen-1:
			z[i+1] = np.dot(network.w[i],out[i]) # z = w*o
			tmp = []
			for j in range(m):
				tmp.append(-1)
			out[i+1] = [np.array(tmp), sigmoid(z[i+1])] # out=1/(1+e^(-z))
		output = out[layerLen-1][2:]

		err = np.mean(output-np.array(trainDesiredOut).transpose(), axis=0)
		last_errFun = np.mean(err)


		# backPropagation

		delta = []
		for i in range(layerLen):
			delta.append(None)
		delta[layerLen-1] = deriv_sigmoid(output) * deriv_squared_error(output, np.array(trainDesiredOut).transpose())
			# calculate delta_input
		
''' 



'''
----CODE TEST-------------------------------------------------
'''
trainInput = np.array([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2]])
trainDesiredOut = np.array([[3],[4],[5]])



Layers=[8,4,1]
###########NeuralNetworkLearn(Layers,trainInput,trainDesiredOut)


print '-------------------trainInput-----------'
print trainInput
print '-----------------trainDesiredOut----------'
print trainDesiredOut

inputRow, inputCol = len(trainInput), len(trainInput[0])
outputRow, outputCol = len(trainDesiredOut), len(trainDesiredOut[0])

print inputRow
print inputCol

# initialization
network=Network()

Layers=[8,4,1]
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
			w_array[row,col] = 1.5
			####w_array[row,col] = 1-2.0*random.random()
	network.w[i] = w_array
temp_w_array = np.zeros(shape=(Layers[layerLen-1],Layers[layerLen-2]+1))
for row in range(temp_w_array.size/temp_w_array[0].size):
	for col in range(temp_w_array[0].size):
		temp_w_array[row,col] = 1.5
		####temp_w_array[row,col] = 1-2.0*random.random()
network.w[layerLen-2] = temp_w_array
print network.w

for i in range(len(network.w)):
	print i
	print network.w[i]



# initialize stopping conditions
errFunChg = sys.float_info.max;  # assuming the intial weight matrices are bad
weightChg = sys.float_info.max;
round_count = 0;
min_trainErrFun = sys.float_info.max;







m = inputRow  # number of examples

# forwardProp
out = []
for i in range(layerLen):
	out.append(None)
out[0] = []
for i in range(m):
	out[0].append(-1)
out[0] = [out[0]]
for train in trainInput.transpose().tolist():
	out[0].append(train)
out[0] = np.array(out[0])
z=[]
for i in range(layerLen):
	z.append(None)
for i in range(layerLen-1):
	z[i+1] = np.dot(network.w[i],out[i]) # z = w*o

	temp_list = []
	for j in range(m):
		temp_list.append(-1)
	out[i+1]=[temp_list]
	for z_val in sigmoid(z[i+1]).tolist():
		out[i+1].append(z_val)
	out[i+1] = np.array(out[i+1])

output = np.array(out[layerLen-1][1:])

err = np.mean((output-np.array(trainDesiredOut).transpose()) * (output-np.array(trainDesiredOut).transpose()), axis=0)



print 'OUTPUT'
print output
# back Propagation
delta = []
for i in range(layerLen):
	delta.append(None)
delta[layerLen-1] = deriv_sigmoid(output) * deriv_squared_error(output, np.array(trainDesiredOut).transpose())

print 'delta[2]'
print delta[layerLen-1]
	# calculate delta_input
		



'''

train data size  8
train class size  1
train data 3
3*8
3*1

Layers = [8 4 1]


w[0] = 4*9   (4 * (8+1) )
w[1] = 1*5   (1 * (4+1) )


out[0] = 9*3
out[1] = 5*3
out[2] = 2*3
'''
