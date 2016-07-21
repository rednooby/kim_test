'''

'''


import numpy as np
import random
import sys
from sigmoid import sigmoid
from deriv_sigmoid import deriv_sigmoid
from deriv_squared_error import deriv_squared_error


class Network:
	layerLen=None
	trainErrFun=None
	trainErrFunRate=None
	w=None

	bestTrainErrFun=None
	bestTrainErrFunRate=None


def NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainInput,trainDesiredOutput):
	inputRow, inputCol = len(trainInput), len(trainInput[0])
	outputRow, outputCol = len(trainDesiredOutput), len(trainDesiredOutput[0])

	# each input vector has a corresponding desired output
	if inputRow != outputRow:
		print >> sys.stderr, 'The number of input vectors and desired ouput do not match'
		sys.exit(-1)

	# equivalent dimensions
	if inputCol != Layers[0]:
		print >> sys.stderr, 'Dimensions of input (%d) does not match input layer (%d)' % (inputCol, Layers[0])
		sys.exit(-1)
	elif outputCol != Layers[-1]:
		print >> sys.stderr, 'Dimensions of output (%d) does not match output layer (%d)' % (outputCol,Layers[-1])
		sys.exit(-1)
		
	# initialization
	network=Network()

	layerLen = len(Layers)
	network.layerLen = layerLen

	network.trainErrFun = [];
	network.trainErrFunRate = [];

	bestNetwork=network

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


	# Learning Process
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
			# E(w)
		err = np.mean((output-np.array(trainDesiredOutput).transpose()) * (output-np.array(trainDesiredOutput).transpose()), axis=0)
		last_errFun = np.mean(err)



		# back Propagation
		delta = []
		for i in range(layerLen):
			delta.append(None)
		delta[layerLen-1] = deriv_sigmoid(output) * deriv_squared_error(output, np.array(trainDesiredOutput).transpose())
		
			# calculate delta_input
		for i in range(layerLen-1,1,-1):
			x = out[i-1][1:]
			d = delta[i]
			delta[i-1] = deriv_sigmoid(x) * np.dot(network.w[i-1].transpose()[1:], d)
		OutDelta = []
		for i in range(layerLen):
			OutDelta.append(None)
		for i in range(layerLen-1,0,-1):
			x = out[i-1]
			d = delta[i]
			OutDelta[i] = np.dot(d, x.transpose())

		# update
		weightChg=0
		for i in range(layerLen-1,0,-1):
			change = learnRate/float(m) * OutDelta[i]
			network.w[i-1] = network.w[i-1] - change
			weightChg = max(weightChg, abs(change).max())
		round_count = round_count+1

		# forwardProp, check error(train)
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
		
		trainErr = np.mean((output-np.array(trainDesiredOutput).transpose()) * (output-np.array(trainDesiredOutput).transpose()), axis=0)
		trainErrFun=np.mean(trainErr)
		max_values = [i.max() for i in output.transpose()]
		temp_output = []
		for i in range(len(output)):
			temp_output.append(max_values)
		temp_output = np.array(temp_output)
		output_match = output == temp_output
		correct=trainDesiredOutput.transpose() == output_match
		correct_int=[]
		for i in range(len(correct)):
			correct_int.append([1 if val==True else 0 for val in correct[i]])
		correct_int = np.array(correct_int)
		trainErrFunRate = 1-np.mean(correct_int)
		
		network.trainErrFun.append(trainErrFun)
		network.trainErrFunRate.append(trainErrFunRate)
		
		errFunChg=abs(trainErrFun - last_errFun)

		
		# lowest training error
		if trainErrFun < min_trainErrFun:
			min_trainErrFun = trainErrFun
			min_trainErrFunRate = trainErrFunRate
			
		
			bestNetwork = network
			bestNetwork.bestTrainErrFun = min_trainErrFun
			bestNetwork.bestTrainErrFunRate = min_trainErrFunRate
		#while errFunChg > errFunChgLmt and weightChg > weightChgLmt and round_count < maxRound:
		'''
		print errFunChg
		print float(errFunChgLmt)
		print weightChg
		print float(weightChgLmt)
		print round_count
		print maxRound
		print ''
		'''

	print 'Round count while learning : %d' % round_count
	print ''
	print 'Arguments check'
	print '  errFunChg'
	print errFunChg
	print '  weightChg'
	print weightChg

	return bestNetwork
