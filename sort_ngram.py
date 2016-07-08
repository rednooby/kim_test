import time

start_time = time.time()

# input file
fi=open("sample.txt", "r")
'''
4D 4D F5 87 1
4D 5A 90 00 1
4D 5A F5 87 1
4D 5A 4E B9 1
4D 90 01 00 1
4D 90 75 08 1
4D 90 38 01 2
4D 90 38 41 8
....
'''
# output file
fo=open("sample_sorted.txt", "w")
'''
0 0 0 0 244 135 185 211 185 211 244 ....
'''



lines=fi.readlines()

# remove '\n'
newlines=[]
for line in lines:
	temp=line.split(' ')
	temp[-1]=temp[-1][:-1]
	newlines.append(temp)

# make dictionary list
dictList=[]
for line in newlines:
	dictList.append({'data':line[0:4], 'freq':int(line[4])})
# sort
d2=[(x['freq'],x) for x in dictList]
d3 = sorted(d2,reverse=True)
d4 = [y['data'] for (x,y) in d3]

for ngram in d4:
	for byte in ngram:
		fo.write(str(int(byte,16))+' ')
		#fo.write('%d ' % int(byte,16))
		#fo.write(byte+' ')


end_time = time.time()


#print processing time
print end_time - start_time