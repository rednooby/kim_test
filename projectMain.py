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
        self.testList = []
    def step_0_function(self, target):
        self.target = target # file_Name
        self.binary_value = open(self.target, 'rb').read()
        self.hex_value = self.binary_value.encode('hex') # type : string
        ''' 00 0E EA 00'''
        # end of step_02

    def step_1_function(self):
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
        # end of step_1

    def step_2_function(self):
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
        #print "self.e_lfanew_int => {}".format(self.e_lfanew_int)
        #print "self.e_lfanew_int => hex_{}".format(hex(self.e_lfanew_int))
        # end of step_2

    def step_3_function(self, s):
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

    def step_4_function(self):
        self.textEnd = self.textStart + self.textSize

    def step_5_function(self):
        print self.textStart , self.textEnd
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



    def step_6_function(self):
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
        print d3
        for ngram in d3:
            self.testList.append((int(ngram[0:2], 16)))
            self.testList.append((int(ngram[3:5], 16)))
            self.testList.append((int(ngram[6:8], 16)))
            self.testList.append((int(ngram[9:11], 16)))


    def dataBase(self):
        print self.TempString
        connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
        db = connection.test  # testDB 접근
        collection = db.employees  # testDB의 testCollection 접근
        data = collection.find_one({"ngram": self.testList})

        if data == None:
            collection.insert({"ngram": self.testList})
        else:
            print data
            print "있는 데이터 입니다."
        print "this is test"

        # database ----------------------------------------------------------------------
        '''  MySQL Databaseb
        con = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password='1111',
                                      database='test')

        # 데이터베이스에 데이터가 있는지 확인을 먼저
        cur = con.cursor()
        test = "select exists ( select * from s1 where a = "
        test += "'"
        test += self.TempString
        test += "'"
        test += " );"
        cur.execute(test)
        data = cur.fetchone()
        result = data[0]

        if result == 0:
            print "result => {}, ?".format(result)
            insertstmt = ""
            insertstmt += "insert into s1 (a) values ("
            insertstmt += "'"
            insertstmt += self.TempString
            insertstmt += "'"
            insertstmt += ");"
            cur.execute(insertstmt)
            con.commit()
        else:
            print "result => {}, 데이터가 이미 존재한다.".format(result)

        con.close()
         '''

def main():
    stu = _Machine()
    t = "C:\\Users\\Win7\\Desktop\\test\\*"

    start_time = time.time()

    stu.step_0_function(t)
    stu.step_1_function()
    stu.step_2_function()
    stu.step_3_function(t)
    stu.step_4_function()
    stu.step_5_function()
    stu.step_6_function()
    print stu.testList
    # stu.stringWeight()
    # stu.readAndWrite()
    # stu.dataBase()
    print stu.TempString
    end_time = time.time()

    print end_time - start_time

if __name__ == "__main__":
    main()
