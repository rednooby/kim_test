import pefile
import sys
import time

start_time = time.time()

if len(sys.argv) is not 3:
	print >> sys.stderr, 'Usage: python %s [INPUT_FILE] [TARGET]' % sys.argv[0]
	exit(1)

f = open(sys.argv[1], 'r')
hex_value = f.read().encode('hex')

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
	temp.append(key[0:2])
	temp.append(key[2:4])
	temp.append(key[4:6])
	temp.append(key[6:8])
	temp.append(value)
	dictList.append(temp)
	





##############3


newlines=dictList

# make dictionary list
dictList=[]
for line in newlines:
	dictList.append({'data':line[0:4], 'freq':int(line[4])})
# sort
d2=[(x['freq'],x) for x in dictList]
d3 = sorted(d2,reverse=True)
d4 = [y['data'] for (x,y) in d3]

fo = open(sys.argv[2], "w")
for ngram in d4[0:500]:
	for byte in ngram:
		fo.write(str(int(byte,16))+' ')
		#fo.write('%d ' % int(byte,16))
		#fo.write(byte+' ')


end_time = time.time()


#print processing time
print end_time - start_time
