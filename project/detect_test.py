'''
This is codes for detection
'''
import sys
sys.path.append('nnet')

import numpy as np
#from ApplyNeuralNetwork import nnet.ApplyNeuralNetwork
from ApplyNeuralNetwork import ApplyNeuralNetwork
import pymongo

class Network:
        layerLen=None
        w=None


'''
open input_file
'''
# arguments option
if len(sys.argv) is not 2:
        print >> sys.stderr, 'Usage: python %s [INPUT_FILE]' % sys.argv[0]
        exit(1)
# input file
f = open(sys.argv[1], 'r')


'''
==========================================
NGRAM EXTRACTION CODE

->dataToCheck
==========================================
'''
connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
collection = db.ngramData  # testDB testCollection

data = collection.find()
temp_l = []
for d in data:
	#print d
	temp_l.append(d['ngram'])

print len(temp_l)
for i in range(len(temp_l)):
	temp_l[i] = temp_l[i][:-1]
dataToCheck = np.array(temp_l, dtype='f')











'''
get best Network from DB
'''
bestNetwork = Network()

collection = db.weight  # testDB testCollection

data = collection.find()
tl=[]
for d in data:
	tl.append(d['bestNN_weight'])

tl_len = len(tl)
for i in range(tl_len-1,0,-1):
	if len(tl[i][0]) == len(tl[i-1][0]):
		tl[i-1] = tl[i-1]+tl[i]
		del tl[i]

for i in range(len(tl)):
	tl[i] = np.array(tl[i])

bestNetwork.w = tl
bestNetwork.layerLen = len(tl)+1


'''
detection
'''

detection_result = ApplyNeuralNetwork(bestNetwork, dataToCheck)

print detection_result

'''
if detection_result is [0 0] -> normal
if detection_result is [0 1] -> malware
else -> detection error
'''
