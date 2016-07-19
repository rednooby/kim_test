import pefile
import sys
import time
import pymongo

# arguments option
if len(sys.argv) is not 2:
	print >> sys.stderr, 'Usage: python %s [INPUT_FILE] ' % sys.argv[0]
	exit(1)

# input file
f = open(sys.argv[1], 'r')
hex_value = f.read().encode('hex')

# make a dictionary of ngram
ngram_dict = dict()

for i in range(len(hex_value)-8):
	ngram = hex_value[i:i+8]
	if ngram in ngram_dict:
		ngram_dict[ngram] += 1
	else:
		ngram_dict[ngram] = 1

dictList = []

for key, value in ngram_dict.iteritems():
	temp = []
	temp.append(value)
	temp.append(key)
	dictList.append(temp)

'''
============================================
ngram in total hex data
NOT .text SECTION
============================================
'''
	
# sort
d1 = sorted(dictList, reverse=True)	
if len(d1) < 500:
	print 'error'
	exit(-1)
d2 = d1[0:500]
d3 = [l[1] for l in d2]

data = []
for ngram in d3:
	data.append(int(ngram[0:2],16))
	data.append(int(ngram[2:4],16))
	data.append(int(ngram[4:6],16))
	data.append(int(ngram[6:8],16))
data.append(1)


#### DB connection

connection = pymongo.MongoClient("localhost", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
collection = db.employees  # testDB testCollection



collection.insert({'ngram':data})
#collection.remove({})
'''
data = collection.find()
for d in data:
	print d

end_time = time.time()
'''


print sys.argv[1]
