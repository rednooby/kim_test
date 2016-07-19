import pymongo
import numpy as np

connection = pymongo.MongoClient("localhost", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
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
