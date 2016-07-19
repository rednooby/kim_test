import numpy as np
from NeuralNetworkLearn import NeuralNetworkLearn
from ApplyNeuralNetwork import ApplyNeuralNetwork
import pymongo
'''
!!!!!!!!!!!!!!!!!!!!!!!
SUPPOSE ngram data in DB is as follows:

[0,0,0,0,144,144,144,144, ..., 255,0,10,55,1] (last one(1) is identifying data 1:malware, 0:normal)
!!!!!!!!!!!!!!!!!!!!!!
'''

connection = pymongo.MongoClient("localhost", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
collection = db.employees  # testDB testCollection
data = collection.find()


ngram_list=[]
for ngram in data:
        ngram_list.append(ngram['ngram'])

trainingdata = np.array(ngram_list)
trainingdata = np.array(ngram_list, dtype='f')

trainData = np.array(ngram_list, dtype='f')
trainClass = trainData.transpose()[-1:].transpose()
trainData = trainData.transpose()[:-1].transpose()
# match the size of array
trainClass = np.insert(trainClass,0,0.0,axis=1)

###################
##
##  for test
##
trialData = trainData[200:]
trialClass = trainClass[200:]

trainData = trainData[:200]
trainClass = trainClass[:200]
##
##
###################

print 'Training Data Amount'
print len(trainData)


Layers=[2000,1300,2]
errFunChgLmt = 1e-6;
weightChgLmt = 1e-4;
maxRound = 1000;
learnRate = 1;

###### Learn NN ##########
print 'Learning...'
bestNetwork = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainData,trainClass)
print 'Done.'

print bestNetwork.bestTrainErrFun
print bestNetwork.bestTrainErrFunRate


print 'Trial Data Amount'
print len(trialData)


###### Apply NN ################
classifiedClass = ApplyNeuralNetwork(bestNetwork, trialData)

length = len(trialData)
success_count = 0
for i in range(length):
	if (classifiedClass[i][0] == trialClass[i][0]) and (classifiedClass[i][1] == trialClass[i][1]):
		success_count += 1
print 'classified Class'
print classifiedClass
print ''
print 'original Class'
print trialClass

print 'Trial Error Rate'
print 1-(success_count/float(length))
