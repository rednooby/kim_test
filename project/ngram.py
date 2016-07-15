import pefile
import sys
import time

start_time = time.time()

# arguments option
if len(sys.argv) is not 3:
	print >> sys.stderr, 'Usage: python %s [INPUT_FILE] [TARGET]' % sys.argv[0]
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
	
# sort
d1 = sorted(dictList, reverse=True)	
d2 = d1[0:500]
d3 = [l[1] for l in d2]

# target file
fo = open(sys.argv[2], "w")
data = ""
for ngram in d3:
	data = data+str(int(ngram[0:2],16))+' '+str(int(ngram[2:4],16))+' '+str(int(ngram[4:6],16))+' '+str(int(ngram[6:8],16))+' '
fo.write(data)

end_time = time.time()


#print processing time
print end_time - start_time
