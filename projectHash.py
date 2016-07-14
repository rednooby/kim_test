# -*- coding: utf -8 -*-
# ----------- [import section] ---------------
import simplejson
import urllib
import urllib2
import hashlib
import glob
import os
import sys
import mysql.connector
import projectMain
# --------------------------------------------

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
def isExist(hashString):
    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='1111',
                                  database='test')
    cur = con.cursor()
    test = "select exists ( select * from s3 where hex = "
    test += "'"
    test += str(hashString)
    test += "'"
    test += " );"
    cur.execute(test)
    data = cur.fetchone()
    con.close()
    result = data[0]
    if result == 0: # 데이터 베이스에 존재하지 않기 대문에 바이러스 토탈로 넘긴다.
        print "result => {}, ?".format(result)
        return result
    else: # 데이터 베이스에 존재하기 바이러스 인걸로 끝낸다.
        print "result => {}, virus".format(result)
        return result


# func [3] 해쉬값 바이러스 토탈로 넘기기
def virusTotal(resource, element):
    tempResource = str(resource)
    url = "https://www.virustotal.com/vtapi/v2/file/rescan"
    print "resource {}".format(resource)
    parameters = {"resource":tempResource,
                  "apikey":"a7677e9d9aab695aa11a53ac6d64caa11c4573a47d7bfc4003735a54fef0bca4"}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json = response.read()
    json = str(json)
    print json
    index = json.find("response_code")
    print " index -->", index

    if not index == -1:
        result = int(json[index+16])
        print result
        if result == 0: # 바이러스 파일이 아니다 => 그럼 데이터베이스에 적재할 필요없다.
            print "result => {} ,  not virus".format(result)
            return ''' END '''
        if result == 1: # 바이러스 파일이다. => 데이터 베이스에 적재할 경우의 수 존재
            print "result => {} ,  virus".format(result)
            # 데이터 베이스
            con = mysql.connector.connect(host='localhost',
                                          user='root',
                                          password='1111',
                                          database='test')

            cur = con.cursor()
            test = "select exists ( select * from s3 where hex = "
            test +="'"
            test += tempResource
            test += "'"
            test += " );"
            cur.execute(test)
            data = cur.fetchone()
            result = data[0]
            if result == 0:  # 데이터 베이스에 존재하지 않기 때문에 db에 적재한다.
                print "result => {}, not exist".format(result)
                # 데이터 베이스에 적재하는 쿼리문 입력할 것
                test = "insert into s3 values("
                test += "'"
                test += tempResource
                test += "'"
                test += " );"
                cur.execute(test)
                con.commit()
            else:  # 데이터 베이스에 존재하기 대문에 적재하지 않는다.
                print "result => {}, exist".format(result)

            stu = projectMain._Machine()
            stu.step_0_function(element)
            stu.step_1_function()
            stu.step_2_function()
            stu.step_3_function(element)
            stu.step_4_function()
            stu.step_5_function()
            stu.step_6_function()
            stu.stringWeight()
            stu.readAndWrite()
            stu.dataBase()
            con.close()


# end of [ virusTotal ] function

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<  main >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main():
    testList = glob.glob("C:\\Users\\kimjh\\Desktop\\C\\*.exe")
    print testList
    for data in testList:
        '''
        tempList = str(data).split("\\")
        element = ""
        element +="C:\\"
        for i in range(1, len(tempList)):
            element += str(tempList[i])
            if not i == len(tempList)-1:
                element +="\\"
        '''
        resource = sha1_for_largefile(str(data)) # 해시값 추출
        result = isExist(resource)
        #element = tempList[len(testList) - 1]

        if result == 0:
            virusTotal(resource, str(data))

if __name__ == "__main__":
    main()