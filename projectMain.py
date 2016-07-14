# -*- coding: utf -8-*-
'''
    version : python 2
    thema : machine learing
'''
import mysql.connector
import pefile
import mysql

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

    def step_0_function(self, target):
        self.target = target
        self.binary_value = open(self.target, 'rb').read()
        self.hex_value = self.binary_value.encode('hex')

    def step_1_function(self):
        testList = []  # list
        s = ""  # string
        num = 0

        for i in range(0, len(self.hex_value) - 32, 32):
            for j in range(i, i + 31, 2):
                s += self.hex_value[j:j + 2]
                testList.append(s)
                s = ""
            self.hex_dict[num] = testList
            num += 16
            testList = []
        self.e_lfanew_string += str(self.hex_dict[48][13])
        self.e_lfanew_string += str(self.hex_dict[48][12])
        #print "self.e_lfanew_string => {}".format(self.e_lfanew_string)

    def step_2_function(self):
        # NT _header first
        z = 3
        for index in range(0, len(self.e_lfanew_string)):
            if self.e_lfanew_string[index].lower() in alphabet:
                temp = alphabet.find(self.e_lfanew_string[index].lower()) + 10
                self.e_lfanew_int += temp * (16 ** z)
                z -= 1
            else:
                self.e_lfanew_int += (int(self.e_lfanew_string[index]) * (16 ** z))
                z -= 1
        #print "self.e_lfanew_int => {}".format(self.e_lfanew_int)
        #print "self.e_lfanew_int => hex_{}".format(hex(self.e_lfanew_int))

    def step_3_function(self, s):
        test = s
        pe = pefile.PE(test)
        self.sizeOfOptionalHeader = pe.FILE_HEADER.SizeOfOptionalHeader

        # print stu.sizeOfOptionalHeader
        temp = 4 + 20 + self.sizeOfOptionalHeader
        self.SectionHeaderTextPosition = temp + self.e_lfanew_int
        test = self.SectionHeaderTextPosition + 8 + 12 # position
        test_1  = self.SectionHeaderTextPosition + 8 + 8 # size

        '''  <<< start >>> '''
        index = test % 32
        temp = ""
        if index == 0:  # index
            temp += str(self.hex_dict[test][1])
            temp += str(self.hex_dict[test][0])
        else:  #
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
        index = test_1 % 32
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

    def step_4_function(self):
        self.textEnd = self.textStart + self.textSize

    def step_5_function(self):
        count = 0
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
            count += 1
        print count

        '''
        f_w = open("sample_1.txt", "w")
        u = 0
        count = 0
        for key in range(self.textStart, self.textEnd + 1, 16):
            for i in range(0, 13):
                tempString = ""
                tempString += self.hex_dict[key][i + 0]
                tempString += " "
                tempString += self.hex_dict[key][i + 1]
                tempString += " "
                tempString += self.hex_dict[key][i + 2]
                tempString += " "
                tempString += self.hex_dict[key][i + 3]
                self.hex_list.append(tempString)
                f_w.write(tempString)
                f_w.write('\n')
        for k, v in self.hex_dict.items():
            print k, v
        print count
        print self.hex_list
        # [ "00 00 00 00" ,
        '''
    def step_6_function(self):
        k = 0
        count = 0
        temp = []
        while len(self.hex_list) != 0:
            string_ = self.hex_list[0]
            if string_ in self.hex_list:
                s = self.hex_list.count(string_)
                if string_ not in temp:
                    temp.append(string_)
                    self.hex_list_result.append(string_ + " " +str(s))
                    count += 1
                self.hex_list.remove(string_)


        '''
        for i in range(0, len(self.hex_list)):
            count = 0
            s = ""
            for j in range(i, len(self.hex_list)):
                if self.hex_list[i] == self.hex_list[j] :
                    count += 1
            s += str(self.hex_list[i])
            if count != 0 :
                k+=1
                s += " "
                s += str(count)
                self.hex_list_result.append(s)
        '''
    def step_7_function(self, a):

        for i in range(0, len(self.hex_list)):
            sample = 0
            s = ""
            for j in range(i, a):
                if self.hex_list[i] == self.hex_list[j]:
                    sample += 1
            if sample != 0:
                s += str(self.hex_list[i])
                s += " "
                s += str(sample)
            if s not in self.Lastlist[0:i]:
                self.Lastlist.append(s)

    def stringWeight(self):
        fi_w = open("sample_2.txt", "w")
        for inline in self.hex_list_result:
            fi_w.write(inline)
            fi_w.write('\n')
        fi_w.close()

    def readAndWrite(self):
        fi = open("sample_2.txt", "r")
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
        fo = open("sample_sorted.txt", "w")
        '''
        0 0 0 0 244 135 185 211 185 211 244 ....
        '''
        lines = fi.readlines()

        # remove '\n'
        newlines = []
        for line in lines:
            temp = line.split(' ')
            temp[-1] = temp[-1][:-1]
            newlines.append(temp)

        # make dictionary list
        dictList = []
        for line in newlines:
            dictList.append({'data': line[0:4], 'freq': int(line[4])})
        # sort
        d2 = [(x['freq'], x) for x in dictList]
        d3 = sorted(d2, reverse=True)
        d4 = [y['data'] for (x, y) in d3]

        for ngram in d4[0:500]:
            for byte in ngram:
                fo.write(str(int(byte, 16)) + ' ')
                self.TempString += str(int(byte, 16)) + ','

    def dataBase(self):
        # database ----------------------------------------------------------------------

        con = mysql.connector.connect(host='localhost',
                                      user='root',
                                      password='1111',
                                      database='test')

        # 데이터베이스에 데이터가 있는지 확인을 먼저
        cur = con.cursor()
        test = "select exists ( select * from s1 where hex = "
        test += "'"
        test += self.TempString
        test += "'"
        test += " );"
        cur.execute(test)
        data = cur.fetchone()
        result = data[0]

        if result == 0:  # 데이터 베이스에 존재하지 않기 대문에 바이러스 토탈로 넘긴다.
            print "result => {}, ?".format(result)
            insertstmt = ""
            insertstmt += "insert into s1 (a) values ("
            insertstmt += "'"
            insertstmt += self.TempString
            insertstmt += "'"
            insertstmt += ");"
            cur.execute(insertstmt)
            con.commit()
        else:  # 데이터 베이스에 존재하기 바이러스 인걸로 끝낸다.
            print "result => {}, 데이터가 이미 존재한다.".format(result)

        con.close()


def main():
    stu = _Machine()
    t = "test.exe"
    stu.step_0_function(t)
    stu.step_1_function()
    stu.step_2_function()
    stu.step_3_function(t)
    stu.step_4_function()
    stu.step_5_function()
    stu.step_6_function()
    stu.stringWeight()
    stu.readAndWrite()
    stu.dataBase()

if __name__ == "__main__":
    main()
