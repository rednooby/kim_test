s = "AtomSetup.exe"

bin_data = open(s, 'rb').read()
hex_data = bin_data.encode('hex')
f_write = open("test.txt", 'w')
# totol print
'''
for index_ in range(0, len(hex_data)):
	print hex_data[index_],

	if not index_ == 0 and index_ %32 == 0:
		print
'''
'''
count = 0
for index_ in range(0, len(hex_data)):
    tempList = list()
    count += 1
    tempList.append(hex_data[index_])
    if count == 8:
        f_write(tempList)
        f_write('\n')
        count = 0
'''

for index_ in range(2048, len(hex_data)):

    if hex_data[index_] == '0':
        if hex_data[index_: index_ + 32] == '0' * 32:
            break
        else:
            print hex_data[index_],
    else:
        print hex_data[index_],

    if not index_ == 2048 and index_ % 32 == 0:
        print

