# -*- coding: utf -8 -*-

# ----------- [import section] ---------------
import simplejson
import urllib
import urllib2
import hashlib
import glob
import os
import time
import mysql.connector
import projectMain
import json
import pymongo
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
# hashString value 는 임의의 파일에 hash 값이 인자로 들어온다.
def isExist(hashString):
    result = 0
    connection = pymongo.MongoClient("192.168.8.141", 27017)  # Mongodb_TargetIp, portNumber
    db = connection.test  # testDB 접근
    collection = db.testCollection # testDB의 testCollection 접근
    data = collection.find_one({"hexvalue": hashString})

    if data == None: # 데이터 베이스에 존재하지 않기 대문에 바이러스 토탈로 넘긴다.
        result = 0
        return result

    else:  # 데이터 베이스에 존재하기 바이러스 인걸로 끝낸다.
        print "악성코드 파일 입니다."
        result = 1
        return result

# func [3] 해쉬값 바이러스 토탈로 넘기기
def virusTotal(resource, element, filName):
    tempResource = str(resource)
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource":tempResource,
                  "apikey":""}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json = response.read()
    time.sleep(15)
    json = str(json)
    result = json.count("true")

    print " ================== [ 테스트 현황 ] ===================== "
    print "[File_Name] : ",filName

    if result == 0: # 정상 파일 ---------------------------------------------------------
        print "[결과] 정상파일 입니다. "

    # ----------------------------------------------------------------------------------------------
    if result != 0: # 바이러스 파일이다. => 데이터 베이스에 적재할 경우의 수 존재
        print "[결과] 악성 파일 입니다. "

        # [악성파일] 해시값을 데이터 베이스에 적재한다.
        connection = pymongo.MongoClient("192.168.8.141", 27017)  # Mongodb_TargetIp, portNumber
        db = connection.test  # testDB 접근
        collection = db.testCollection  # testDB의 testCollection 접근
        data = collection.find_one({"hexvalue": tempResource})

        if data == None:  # 데이터 베이스에 존재하지 않기 때문에 db에 적재한다.
            collection.insert({"hexvalue": tempResource})

        else:   # 데이터 베이스에 존재하기 대문에 적재하지 않는다.
            print "악성코드 파일이 데이터 베이스에 존재합니다."

    # [ 웹으로 날릴 데이터 베이스 ] ==============================================================
    print "웹으로 데이터 결과를 날린다."
    response = ""
    if result == 0:
        response = "NO"
        print "정상 파일로 데이터를 넘기겠습니다."
    else:
        response = "YES"
        print "악성 파일로 데이터를 넘기겠습니다."

    con = mysql.connector.connect(host='192.168.0.116',
                                  user='test',
                                  password='qwer1234',
                                  database='jh')
    cur = con.cursor()
    test = "insert into s2 values("
    test += "'"
    test += tempResource # Hash value
    test += "'"

    test += ","

    test += "'"
    test += response # "yes" or "no"
    test += "'"

    test += " );"
    cur.execute(test)
    con.commit()
    con.close()
    # ==========================================================================================

    result_1 = 0

    stu = projectMain._Machine()
    stu.fileBinary_Extraction(element)  # ---------------------------------> step 1
    result_1 = stu.PE_Structure_elfanewString()  # ------------------------> step 2

    if result_1 == 0:
        print "end - 1"
    else:
        stu.PE_Structure_elfanewInt()  # ----------------------------------> step 3
        result_2 = stu.PE_Structure_sectionText_start_size(element)  # ----> step 4
        if result_2 == 0:
            print "end - 2"
        else:
            stu.PE_Structure_sectionText_End()  # -------------------------> step 5
            stu.ngramConstruct()  # ---------------------------------------> step 6
            stu.ngramSort()  # --------------------------------------------> step 7
            time.sleep(5) # 5초를 기다려라
            stu.dataBase(result)  # ---------------------------------------> step 8

# end of [ virusTotal ] function
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<  main >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main():
    testList = glob.glob("C:\\Users\\kimjh\\Desktop\\C\\*")
    for data in testList:
        resource = sha1_for_largefile(str(data)) # 해시값 추출
        result = isExist(resource)

        if result == 0:
            virusTotal(resource, str(data), data)

if __name__ == "__main__":
    main()
