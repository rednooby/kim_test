# -*- coding: utf -8-*-
'''
This is codes for detection
'''
import sys
sys.path.append('nnet')

import numpy as np
#from ApplyNeuralNetwork import nnet.ApplyNeuralNetwork
from ApplyNeuralNetwork import ApplyNeuralNetwork
import pymongo
import glob
import pefile
import os
import hashlib
import matplotlib.pyplot as plt
import urllib
import urllib2
import time
import mysql.connector
import webbrowser

alphabet = 'abcdef'

class Network:
	layerLen=None
	w=None

class _Machine:
    def __init__(self):
        self.e_lfanew_string = ""          # type of string
        self.e_lfanew_int = 0              # type of integer
        self.sizeOfOptionalHeader = 0      # type of integer
        self.target = 0                    # type of integer
        self.binary_value = 0              # type of integer
        self.hex_value = 0                 # type of integer
        self.hex_dict = dict()             # type of dictionary
        self.SectionHeaderTextPosition = 0 # type of integer
        self.textStart = 0                 # type of integer
        self.textEnd = 0                   # type of integer
        self.textSize = 0                  # type of integer
        self.hex_list = list()             # type of list
        self.hex_list_result = list()      # type of list
        self.hexResultDictionary = dict()  # type of dictionary
        self.LstDict = dict()              # type of dictionary
        self.Lastlist = list()             # type of list
        self.TempString = ""               # type of string
        self.testList = []                 # type of list
        self.controlResult = 0             # type of int 바이러스 인지 아닌지 확인한다.
        self.totalCount = 0                # type of int ngram 에 갯수가 500개가 되는지 확인한다.

    def fileBinary_Extraction(self, target): # 1
        self.target = target # file_Name
        self.binary_value = open(self.target, 'rb').read()
        self.hex_value = self.binary_value.encode('hex') # type : string
        ''' 00 0E EA 00'''
        # end of fileBinary_Extraction

    def PE_Structure_elfanewString(self): # 2
        s = ""  # string
        num = 0

        for i in range(0, len(self.hex_value) - 32, 32):
            testList = []
            for j in range(i, i + 31, 2):
                s += self.hex_value[j:j + 2]
                testList.append(s)
                s = ""
            self.hex_dict[num] = testList
            num += 16
        try:
            self.e_lfanew_string += str(self.hex_dict[48][13])
            self.e_lfanew_string += str(self.hex_dict[48][12])
        except:
            print "error"
            return 0
        else:
            return 1
        # end of PE_Structure_elfanewString

    def PE_Structure_elfanewInt(self): # 3
        # NT _header first
        z = 3
        for index in range(0, len(self.e_lfanew_string)):
            # 문자 일 경우
            if self.e_lfanew_string[index].lower() in alphabet:
                temp = alphabet.find(self.e_lfanew_string[index].lower()) + 10
                self.e_lfanew_int += temp * (16 ** z)
                z -= 1
            # 숫자 일 경우
            else:
                self.e_lfanew_int += (int(self.e_lfanew_string[index]) * (16 ** z))
                z -= 1
        # end of PE_Structure_elfanewInt

    def PE_Structure_sectionText_start_size(self, s): # 4
        test = s
        try:
            pe = pefile.PE(test)
        except:
            print "error"
            return 0
        else:
            self.sizeOfOptionalHeader = pe.FILE_HEADER.SizeOfOptionalHeader

            # print stu.sizeOfOptionalHeader
            temp = 4 + 20 + self.sizeOfOptionalHeader
            self.SectionHeaderTextPosition = temp + self.e_lfanew_int
            test = self.SectionHeaderTextPosition + 8 + 12 # position
            test_1  = self.SectionHeaderTextPosition + 8 + 8 # size

            '''  <<< start >>> '''
            index = test % 16
            temp=""
            if index == 0:  # index
                temp += str(self.hex_dict[test][1])
                temp += str(self.hex_dict[test][0])
            else:  # index != 0
                if index + 1 < 16:
                    temp += str(self.hex_dict[test - index][index + 1])
                    temp += str(self.hex_dict[test - index][index])
                else:
                    temp += str(self.hex_dict[(test - index) + 16][0])
                    temp += str(self.hex_dict[test - index][index])

            temp = ""
            temp += str(self.hex_dict[test - index][index + 1])
            temp += str(self.hex_dict[test - index][index])

            z = len(temp) - 1
            for index in range(0, len(temp)):
                if temp[index].lower() in alphabet:
                    n1 = alphabet.find(temp[index].lower()) + 10
                    self.textStart += n1 * (16 ** z)
                    z -= 1
                else:
                    self.textStart += (int(temp[index]) * (16 ** z))
                    z -= 1
                    #print "stu.textStart => {}".format(self.textStart)
                    #print "stu.textStart => hex{}".format(hex(self.textStart))

            '''  <<< size >>> '''
            index = test_1 % 16
            # print index
            temp = ""
            if index == 0:  # index
                temp += str(self.hex_dict[test_1][4])
                temp += str(self.hex_dict[test_1][3])
                temp += str(self.hex_dict[test_1][2])
                temp += str(self.hex_dict[test_1][0])
            else:  #
                if index + 1 < 16:
                    temp += str(self.hex_dict[test_1 - index][index + 3])
                    temp += str(self.hex_dict[test_1 - index][index + 2])
                    temp += str(self.hex_dict[test_1 - index][index + 1])
                    temp += str(self.hex_dict[test_1 - index][index + 0])
                else:
                    temp += str(self.hex_dict[(test_1 - index) + 16][0])
                    temp += str(self.hex_dict[test_1 - index][index])


            z = len(temp) - 1
            for index in range(0, len(temp)):
                if temp[index].lower() in alphabet:
                    n1 = alphabet.find(temp[index].lower()) + 10
                    self.textSize += n1 * (16 ** z)
                    z -= 1
                else:
                    self.textSize += (int(temp[index]) * (16 ** z))
                    z -= 1

                    #print "stu.textSize -> {}".format(self.textSize)
                    #print "stu.textSize -> hex_{}".format(hex(self.textSize))
            return 1
        # end of PE_Structure_sectionText_start_size

    def PE_Structure_sectionText_End(self): # 5
        self.textEnd = self.textStart + self.textSize
        # end of PE_Structure_sectionText_End

    def ngramConstruct(self): # 6
        for key in range(self.textStart*2, (self.textEnd*2)-7, 2):
            tempString = ""
            tempString += self.hex_value[key+0:key+2]
            tempString += " "
            tempString += self.hex_value[key+2:key+4]
            tempString += " "
            tempString += self.hex_value[key+4:key+6]
            tempString += " "
            tempString += self.hex_value[key+6:key+8]
            self.hex_list.append(tempString)
        # end of ngramConstruct

    def ngramSort(self): # 7
        ngram_dict = dict() # dictionary[key:value]
        for i in range(len(self.hex_list)-8):
            ngram = str(self.hex_list[i])
            if ngram in ngram_dict:
                ngram_dict[ngram] += 1
            else:
                ngram_dict[ngram] = 1

        dictList = [] # type of dictList is list

        for key, value in ngram_dict.iteritems():
            temp = []
            temp.append(value)
            temp.append(key)
            dictList.append(temp)

        # sort
        d1 = sorted(dictList, reverse=True)
        d2 = d1[0:500]
        d3 = [l[1] for l in d2]

        for ngram in d3:
            self.testList.append((int(ngram[0:2], 16)))
            self.testList.append((int(ngram[3:5], 16)))
            self.testList.append((int(ngram[6:8], 16)))
            self.testList.append((int(ngram[9:11], 16)))
            self.totalCount += 1
        # end of ngramSort

    def dataBase(self, result): # 8
        self.controlResult = result
        if not self.totalCount == 500:
            print "ngram 의 갯수가 500 개가 되지 않습니다."
            return ''' 종료 '''
        else: #--> self.totalCount == 500
            if self.controlResult == 0: # 정상파일 =======================================================
                print "정상파일 입니다.[DB]"
                connection = pymongo.MongoClient("192.168.8.142", 27017)  # Mongodb_TargetIp, portNumber
                db = connection.test  # testDB 접근
                collection = db.testCollection  # testDB의 testCollection 접근
                self.testList.append(0) # normal mark : 0
                data = collection.find_one({"ngram": self.testList})
                if data == None:
                    collection.insert({"ngram": self.testList})
                else:
                    print "있는 데이터 입니다."

            else: # 악성성 파일입니다. ====================================================================
                print "비정상파일 입니다.[DB]"
                connection = pymongo.MongoClient("192.168.8.142", 27017)  # Mongodb_TargetIp, portNumber
                db = connection.test  # testDB 접근
                collection = db.employees  # testDB의 testCollection 접근
                self.testList.append(1)  # innormal mark : 1
                data = collection.find_one({"ngram": self.testList})
                if data == None:
                    collection.insert({"ngram": self.testList})
                else:
                    print data
                    print "있는 데이터 입니다."

        # end of dataBase
    def getNgram(self):
    	return self.testList


def get_file_list(path):
	file_list = glob.glob(path+'\*')
	if file_list == []:
		file_list = glob.glob(path)

	for i in range(len(file_list)):
		if os.path.isdir(file_list[i]):
			file_list[i] = get_file_list(file_list[i])
	return file_list


def make_1d_list(newlist,filelist):
	for file in filelist:
		if type(file) == type([]):
			make_1d_list(newlist,file)
		else:
			newlist.append(file)

# func [1] 해쉬값 추출
def sha1_for_largefile(filepath, blocksize=8192):
    sha_1 = hashlib.sha1()

    try:
        f = open(filepath, "rb")
    except IOError as e:
        print("file open error", e)
        return
    while True:
        buf = f.read(blocksize)
        if not buf:
            break
        sha_1.update(buf)
    return sha_1.hexdigest() # 해시값을 리턴한다.
# end of [ sha1_for_largefile ] function

# func [2] 해쉬값 이 데이터 베이스에 있는지 없는지 확인할 것
# hashString value 는 임의의 파일에 hash 값이 인자로 들어온다.
def isExist(hashString):
    result = 0
    connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
    db = connection.test  # testDB 접근
    collection = db.hashData # testDB의 testCollection 접근
    data = collection.find_one({"hexvalue": hashString})

    if data == None: # 데이터 베이스에 존재하지 않기 대문에 바이러스 토탈로 넘긴다.
        result = 0
        return result

    else:  # 데이터 베이스에 존재하기 바이러스 인걸로 끝낸다.
        print "Malware!!"
        result = 1
        return result

def virusTotal(resource, element, fileName, APIkey):
    tempResource = str(resource)
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource":tempResource,
                  "apikey":APIkey}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json = response.read()
    json = str(json)
    result = json.count("true")

    if result < 10: # 정상 파일 ---------------------------------------------------------
        print "  %s : not malware (%d engines)" % (fileName, result)
        return (0, result, tempResource)
    # ------------------------------------[----------------------------------------------------------
    else: # 바이러스 파일이다. => 데이터 베이스에 적재할 경우의 수 존재
        print "  %s : malware (%d engines)" % (fileName, result)
        return (1 ,result, tempResource)


'''
open input_file
'''
# arguments option
if len(sys.argv) is 1:
    print "Default Path: C:\\DetectionTest"
    print ''
    f_list = get_file_list("C:\\DetectionTest")
elif len(sys.argv) is not 2:
    print >> sys.stderr, 'Usage: python %s [PATH TO DETECT]' % sys.argv[0]
    exit(1)
else:
    print "Path: %s" % sys.argv[1]
    print ''
    f_list = get_file_list(sys.argv[1])

fileToDetect_list=[]
make_1d_list(fileToDetect_list,f_list)


'''
# Detect malware by Hash DB
'''
temp_list = []
hash_list = []
print 'Detection by hash value in DB'
for file in fileToDetect_list:
	hash_value = sha1_for_largefile(str(file))
	result = isExist(hash_value)
	if result == 0:
		temp_list.append(file)
		hash_list.append(hash_value)
print 'Done.'
print ''
fileToDetect_list = temp_list	# list of files to detect


'''
## Detection by Virus Total API
'''
print 'Virus Total API Detection Result'

k1 = "408377a089c6dd9860e6006750c9e832ca8a73d9bb4825e47bbf8ea1ca5c1a5f"
k2 = "c2f5edb9c68df4a96b67276a4c66a522ae316f33781ff026a49381a6ba2e77f2"
k3 = "cda13808c3ce0dfc3ee40fff23f0b3acfbbc648442370a777d6125504455ce6d"
k4 = "5b8d384d78cdfb06187891ba71ef718634bc97e3c720da968beadf5ef654165c"
k5 = "8c70bb7653fcbade33a6364e991d1fac614128810c7cbc51cec6aee35d8b6ed9"
k6 = "a7677e9d9aab695aa11a53ac6d64caa11c4573a47d7bfc4003735a54fef0bca4"
k7 = "559615cef6ec81a70207208195b6f682dfc9ec7bb9e32609b5640b9606c1c36f"
k8 = "d91aec94b6d5494ed7ab5a7ac79ca3dedc0051ada686812393459b21dc630704"
k9 = "2d5d0f6b8a9d5eabb38f084d4c3a6d0a74f27ea592e026285dad50298bc34b29"
k10 = "7e6f911e8e3c4601ec9a27df6f3ab4e9aaf1f66380c44ff83610ecd688ddfa19"
key_list = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10]
VT_result = dict()	# {FileName : (result, VT_count, File Name)}
i=0
while(i<len(fileToDetect_list)):
	key = key_list[i%len(key_list)] 
	VT_result[fileToDetect_list[i]] = virusTotal(hash_list[i], str(fileToDetect_list[i]), fileToDetect_list[i], key)
	# (result, VT_count, File Name)
	time.sleep(15/float(len(key_list)))
	i += 1


'''
NGRAM EXTRACTION
'''
detect_list=[]	# data
filename_list=[]	# file name
print 'Extracting ngram...'
for file in fileToDetect_list:
	stu = _Machine()
	try:
		stu.fileBinary_Extraction(file)	
		stu.PE_Structure_elfanewString()
		stu.PE_Structure_elfanewInt()
		stu.PE_Structure_sectionText_start_size(file)
		stu.PE_Structure_sectionText_End()
		stu.ngramConstruct()
		stu.ngramSort()
		data = stu.getNgram()
		if len(data) == 2000:
			detect_list.append(data)
			filename_list.append(file)
			print "  %s done." % file
	except:
		print '  %s file open error' % file

print 'Extraction done.'
print ''
print 'List of files to detect by Neural Network'
for filename in filename_list:
	print filename
print ''
print "%d files" % len(filename_list)
print ''
dataToCheck = np.array(detect_list, dtype='f')	# Test Data



'''
get best Network from DB
'''
bestNetwork = Network()

connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
collection = db.weight  # testDB testCollection

data = collection.find()
tl=[]
for d in data:
	tl.append(d['bestNN_weight'])
tl_len = len(tl)
# merge splitted weight
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
print 'Detection result'
for i in range(len(filename_list)):
	tempstr = str(detection_result[i].tolist())
	if tempstr == '[0.0, 1.0]':
		print "%s  : MALWARE" % filename_list[i]
	else:
		print "%s  : NOT MALWARE" % filename_list[i]

########################################################################

'''
result counting
'''
NN_result = dict()	# {filename: 0 or 1}
ct=0
for i in range(len(detection_result)):
	if detection_result[i].tolist() == [0.0, 1.0]:
		ct += 1
		NN_result[filename_list[i]] = 1
	else:
		NN_result[filename_list[i]] = 0

print 'Detection rate: %d/%d ' % (ct,len(filename_list))
print '%f' % (ct/float(len(filename_list)))

'''
graph
'''
'''
mal_size = ct
nor_size = len(filename_list)-ct
err_size = len(fileToDetect_list)-len(filename_list)
labels = 'malware:'+str(mal_size), 'normal:'+str(nor_size), 'detection error:'+str(err_size)
sizes = [mal_size, nor_size, err_size]
colors = ['orange', 'green', 'grey']
explode = (0,0,0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.show()
'''

'''
insert result to DB
'''
con = mysql.connector.connect(host='192.168.0.116',
                                  user='test',
                                  password='qwer1234',
                                  database='jh')

cur = con.cursor()
for key in VT_result.keys():
	#(1, vt_count, hashval)
	(result,vtcount,hashvalue) = VT_result[key]
	test = "insert into s2 values("
	test += "'"
	test += hashvalue # Hash value [col 1 name: hex ]
	test += "'"
	test += ","
	test += "'"
	nn_result = NN_result.get(key)
	if nn_result == 1:
		test += "YES"
	elif nn_result == 0:
		test += "NO"
	else:
		test += ""
	test += "'"
	test += ","
	test += "'"
	test += str(vtcount)+"/"+"56"  # "35/55" value [col3 name : vt]
	test += "'"
	test += ","
	test += "'"
	f_name = key
	cnt = f_name.count("\\")
	if not cnt == 0:
		s = f_name.split("\\")
		f_name = s[-1] 
	test += f_name  # "filename" value [col4 name : filename]
	test += "'"
	test += " );"
	cur.execute(test)
con.commit()
con.close()
print "result inserted to DB"

url='http://192.168.0.147:8080/3_ML/hash_list.jsp'
webbrowser.open(url)