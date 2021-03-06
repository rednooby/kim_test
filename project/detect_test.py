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



'''
open input_file
'''
# arguments option
if len(sys.argv) is not 2:
        print >> sys.stderr, 'Usage: python %s [PATH TO DETECT]' % sys.argv[0]
        exit(1)


'''
==========================================
NGRAM EXTRACTION CODE
->dataToCheck
==========================================
'''

f_list = get_file_list(sys.argv[1])
#print f_list

detect_list=[]
filename_list=[]

print 'Extracting ngram...'
for file in f_list:
	stu = _Machine()
	t=file
	try:
		stu.fileBinary_Extraction(t)	
		stu.PE_Structure_elfanewString()
		stu.PE_Structure_elfanewInt()
		stu.PE_Structure_sectionText_start_size(t)
		stu.PE_Structure_sectionText_End()
		stu.ngramConstruct()
		stu.ngramSort()
		data = stu.getNgram()
		if len(data) == 2000:
			detect_list.append(data)
			filename_list.append(t)
	except:
		print 'file error'

print 'Done.'
print ''
print 'List of files to detect'
for filename in filename_list:
	print filename
print ''
print "%d files" % len(filename_list)
print ''
dataToCheck = np.array(detect_list, dtype='f')



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
print detection_result
'''
if detection_result is [0 0] -> normal
if detection_result is [0 1] -> malware
else -> detection error
'''
