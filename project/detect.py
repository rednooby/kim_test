'''
This is codes for detection
'''
import numpy as np
from ApplyNeuralNetwork import nnet.ApplyNeuralNetwork
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


bestNetwork = Network()
'''
==========================================
GET BEST NETWORK FROM DB

-> bestNetwork
==========================================
'''

detection_result = ApplyNeuralNetwork(bestNetwork, dataToCheck)


'''
if detection_result is [0 0] -> normal
if detection_result is [0 1] -> malware
else -> detection error
'''
