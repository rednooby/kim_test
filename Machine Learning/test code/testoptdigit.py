import numpy as np
import random
import sys 
from sigmoid import sigmoid
from deriv_sigmoid import deriv_sigmoid
from deriv_squared_error import deriv_squared_error
from numpy.linalg import inv 
from threshold_matrix import threshold_matrix
from NeuralNetworkLearn import NeuralNetworkLearn
from ApplyNeuralNetwork import ApplyNeuralNetwork

# training data
f_tra = open('testdata/optdigits_tra_trans.dat')
f_cv = open('testdata/optdigits_cv_trans.dat')

train_data = f_tra.read()[:-1].split('\n')
for i in range(len(train_data)):
	train_data[i] = train_data[i][:-1].split(' ')
train_data = np.array(train_data)

trainDataTran = train_data.transpose()[:-1].transpose()
trainClassTran_temp = train_data.transpose()[-1:].transpose()

train_size = len(train_data)
class_size = 10

class_list = ['0','1','2','3','4','5','6','7','8','9']
temp_array1 = []
for i in range(train_size):
	temp_array1.append(class_list)
temp_array1 = np.array(temp_array1)
temp_array2 = []
for i in range(train_size):
	tmp=[]
	val=trainClassTran_temp[i][0]
	for j in range(class_size):
		tmp.append(val)
	temp_array2.append(tmp)
temp_array2 = np.array(temp_array2)

for i in range(len(temp_array1)):
	for j in range(len(temp_array1[0])):
		if temp_array1[i][j] == temp_array2[i][j]:
			temp_array1[i][j] = 1
		else :
			temp_array1[i][j] = 0
trainClassTran = temp_array1

# test data

f_tra = open('testdata/optdigits_tra_trans.dat')
f_cv = open('testdata/optdigits_cv_trans.dat')

test_data = f_cv.read()[:-1].split('\n')
for i in range(len(test_data)):
	test_data[i] = test_data[i][:-1].split(' ')
test_data = np.array(test_data)

testDataTran = test_data.transpose()[:-1].transpose()
testClassTran_temp = test_data.transpose()[-1:].transpose()

test_size = len(test_data)
class_size = 10

class_list = ['0','1','2','3','4','5','6','7','8','9']
temp_array1 = []
for i in range(test_size):
	temp_array1.append(class_list)
temp_array1 = np.array(temp_array1)
temp_array2 = []
for i in range(test_size):
	tmp=[]
	val=testClassTran_temp[i][0]
	for j in range(class_size):
		tmp.append(val)
	temp_array2.append(tmp)
temp_array2 = np.array(temp_array2)

for i in range(len(temp_array1)):
	for j in range(len(temp_array1[0])):
		if temp_array1[i][j] == temp_array2[i][j]:
			temp_array1[i][j] = 1
		else :
			temp_array1[i][j] = 0
testClassTran = temp_array1

trainDataTran = np.array(trainDataTran, dtype='f')
trainClassTran = np.array(trainClassTran, dtype='f')
testDataTran = np.array(testDataTran, dtype='f')
testClassTran = np.array(testClassTran, dtype='f')



#Layers=[8,4,1]
Layers=[64,10]
errFunChgLmt = 1e-6;
weightChgLmt = 1e-4;
maxRound = 1000;
learnRate = 1;

#testnetwork = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainInput,trainDesiredOutput,trainInput,trainDesiredOutput)

print 'learning..'
bestNetwork = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainDataTran,trainClassTran,testDataTran,testClassTran)

print 'learning done.'
print bestNetwork.bestTrainErrFun
print bestNetwork.bestTestErrFun
print bestNetwork.bestTrainErrFunRate
print bestNetwork.bestTestErrFunRate
#print testnetwork.w
#print testnetwork.bestTrainErrFun
#print testnetwork.bestTrainErrFunRate


#print ApplyNeuralNetwork(testnetwork, trainInput)
