import numpy as np
from NeuralNetworkLearn import NeuralNetworkLearn
from ApplyNeuralNetwork import ApplyNeuralNetwork

# training data
f_tra = open('testdata/optdigits_tra_trans.dat', 'r')

	# remove '\n'
train_data = f_tra.read()[:-1].split('\n')
f_tra.close()
	# remove '\r'
for i in range(len(train_data)):
	if train_data[i][-1] == '\r':
		train_data[i] = train_data[i][:-1]
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
f_cv = open('testdata/optdigits_cv_trans.dat', 'r')

	# remove '\n'
test_data = f_cv.read()[:-1].split('\n')
f_cv.close()
	# remove '\r'
for i in range(len(test_data)):
	if test_data[i][-1] == '\r':
		test_data[i] = test_data[i][:-1]
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


Layers=[64,10]
errFunChgLmt = 1e-6;
weightChgLmt = 1e-4;
maxRound = 1000;
learnRate = 1;


print 'Learning...'
bestNetwork = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainDataTran,trainClassTran,testDataTran,testClassTran)
print 'Done.'

print bestNetwork.bestTrainErrFun
print bestNetwork.bestTestErrFun
print bestNetwork.bestTrainErrFunRate
print bestNetwork.bestTestErrFunRate




# trial data
f_tri = open('testdata/optdigits_trial_trans.dat', 'r')

	# remove '\n'
trial_data = f_tri.read()[:-1].split('\n')
f_tri.close()
	# remove '\r'
for i in range(len(trial_data)):
	if trial_data[i][-1] == '\r':
		trial_data[i] = trial_data[i][:-1]
for i in range(len(trial_data)):
	trial_data[i] = trial_data[i][:-1].split(' ')
trial_data = np.array(trial_data)

trialDataTran = trial_data.transpose()[:-1].transpose()
trialClassTran_temp = trial_data.transpose()[-1:].transpose()

trial_size = len(trial_data)
class_size = 10

class_list = ['0','1','2','3','4','5','6','7','8','9']
temp_array1 = []
for i in range(trial_size):
	temp_array1.append(class_list)
temp_array1 = np.array(temp_array1)
temp_array2 = []
for i in range(trial_size):
	tmp=[]
	val=trialClassTran_temp[i][0]
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
trialClassTran = temp_array1


trialDataTran = np.array(trialDataTran, dtype='f')
trialClassTran = np.array(trialClassTran, dtype='f')


classifiedClassTran = ApplyNeuralNetwork(bestNetwork, trialDataTran)
print 'classified Class'
print classifiedClassTran
print ''
print 'original Class'
print trialClassTran
