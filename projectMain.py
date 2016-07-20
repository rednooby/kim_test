# -*- coding: utf -8-*-
'''
    version : python 2
    thema : machine learing
'''
from multiprocessing import Process
import mysql.connector
import pefile
import time
import json
import pymongo
from pprint import pprint
from bson.objectid import ObjectId

alphabet = 'abcdef'

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
                connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
                db = connection.test  # testDB 접근
                collection = db.ngramData  # testDB의 testCollection 접근
                self.testList.append(0) # normal mark : 0
                data = collection.find_one({"ngram": self.testList})
                if data == None:
                    collection.insert({"ngram": self.testList})
                else:
                    print "있는 데이터 입니다."

            else: # 악성성 파일입니다. ====================================================================
                print "비정상파일 입니다.[DB]"
                connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
                db = connection.test  # testDB 접근
                collection = db.ngramData  # testDB의 testCollection 접근
                self.testList.append(1)  # innormal mark : 1
                data = collection.find_one({"ngram": self.testList})
                if data == None:
                    collection.insert({"ngram": self.testList})
                else:
                    print data
                    print "있는 데이터 입니다."

        # end of dataBase

def main():
    stu = _Machine()
    t = "test.exe"
    stu.fileBinary_Extraction(t) # ------------------> step 1
    stu.PE_Structure_elfanewString() # --------------> step 2
    stu.PE_Structure_elfanewInt() # -----------------> step 3
    stu.PE_Structure_sectionText_start_size(t) # ----> step 4
    stu.PE_Structure_sectionText_End() # ------------> step 5
    stu.ngramConstruct() # --------------------------> step 6
    stu.ngramSort() # -------------------------------> step 7
    stu.dataBase(0) # -------------------------------> step 8
    '''step 8 에서 정상 파일이면 : 0
    악성 파일이면 : 1'''
if __name__ == "__main__":
    main()