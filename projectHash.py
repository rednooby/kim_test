# -*- coding: utf -8 -*-
# 정상 파일 적재 코드
# 2016-07-21 ver3.0
# 작성자: 김준현

# ----------- [import section] ---------------
import mysql.connector
import urllib
import urllib2
import hashlib
import glob
import os
import time
import projectMain
import json
import pymongo

# --------------------------------------------

# func [1] 해쉬값 추출 [문제 없다.]
def sha1_for_largefile(filepath, blocksize=8192):
    sha_1 = hashlib.sha1()
    try:
        f = open(filepath, "rb")
    except IOError as e:
        print("file open error", e)
        return '''종료'''
    while True:
        buf = f.read(blocksize)
        if not buf:
            break
        sha_1.update(buf)

    return sha_1.hexdigest()  # 해시값을 리턴한다.


# end of [ sha1_for_largefile ] function

# func [2] 해쉬값 이 데이터 베이스에 있는지 없는지 확인할 것
# hashString value 는 임의의 파일에 hash 값이 인자로 들어온다.
def isExist(hashString):
    result = 0
    connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
    db = connection.test  # testDB 접근
    collection = db.hashData  # testDB의 hashData에 접근
    data = collection.find_one({"hexvalue": hashString})

    if data == None:  # 데이터 베이스에 존재하지 않기 대문에 바이러스 토탈로 넘긴다.
        print "[1] 바이러스 토탈로 넘기겠습니다."
        result = 0
        return result

    else:  # 데이터 베이스에 존재하기 바이러스 인걸로 끝낸다.
        print "[1] 악성코드 파일 입니다."
        result = 1
        return result


# func [3] 해쉬값 바이러스 토탈로 넘기기
def virusTotal(resource, filName, key, count):
    tempResource = str(resource)

    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": tempResource,
                  "apikey": key} # virus total api key
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json_str = response.read()

    json_str = str(json_str)
    print json_str
    result = json_str.count("true")

    print "[File_Name] : ", filName

    if result == 0:  # 정상 파일 ---------------------------------------------------------
        print "[결과] 정상파일 입니다. "
        # [정상파일] 해시값을 데이터 베이스에 적재하지 않는다.
    # ----------------------------------------------------------------------------------------------

    else:  # 바이러스 파일이다. => 데이터 베이스에 적재할 경우의 수 존재
        # result > 10
        print "[결과] 악성 파일 입니다. "
        # [악성파일] 해시값을 데이터 베이스에 적재한다.
        connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
        db = connection.test  # testDB 접근
        collection = db.hashData  # testDB의 testCollection 접근
        data = collection.find_one({"hexvalue": tempResource})

        if data == None:  # 데이터 베이스에 존재하지 않기 때문에 db에 적재한다.
            print " 데이터 베이스에 존재하지 않기 때문에 db 에 적재한다."
            collection.insert({"hexvalue": tempResource})

        else:  # 데이터 베이스에 존재하기 대문에 적재하지 않는다.
            print "악성코드 파일이 데이터 베이스에 존재합니다."

    '''
    # [ 웹으로 날릴 데이터 베이스 ] ==============================================================
    count = filName.count("\\")
    if not count == 0:
        s = filName.split("\\")
        print s
        filName = s[-1]
    start = json_str.find("positives")+12
    end = json_str.find("sha256")-3
    response1 = json_str[start:end] + "/56"
    # ===========================================================================================

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
    test += tempResource # Hash value [col 1 name: hex ]
    test += "'"
    test += ","
    test += "'"
    test += response # "yes" or "no" value [col 2 name: ng]
    test += "'"
    test += ","
    test += "'"
    test += response1  # "35/55" value [col3 name : vt]
    test += "'"
    test += ","
    test += "'"
    test += filName  # "filename" value [col4 name : filename]
    test += "'"
    test += " );"
    cur.execute(test)
    con.commit()
    con.close()
    # ==========================================================================================
    '''
    stu = projectMain._Machine()
    step1 = stu.fileBinary_Extraction(filName)  # ---------------------------------> step 1
    if step1 == 0:
        print "error 인한 종료"
        return

    else:  # step1 == 1
        # element는 파일경로와 파일이름이 들어있는 문자열이다.
        result_1 = stu.PE_Structure_elfanewString()  # ----------------------------> step 2
        if result_1 == 0:
            print "error [1] [종료]"
            return
        else:
            stu.PE_Structure_elfanewInt()  # --------------------------------------> step 3
            result_2 = stu.PE_Structure_sectionText_start_size(filName)  # --------> step 4
            if result_2 == 0:
                print "error [2] [종료]"
                return
            else:  # result_2 == 1
                stu.PE_Structure_sectionText_End()  # -------------------------> step 5
                result_3 = stu.ngramConstruct()  # ---------------------------------------> step 6
                if result_3 == 1:
                    result_4 = stu.ngramSort()  # --------------------------------------------> step 7
                    # time.sleep(10)  # 10초를 기다려라
                    if result_4 == 0:
                        print "error [3] 종료"
                        return
                    else:
                        stu.dataBase(result, count)  # ---------------------------------------> step 8
                else:
                    return


# end of [ virusTotal ] function

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<  main >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def main():
    f_w = open("report.txt", "w")
    dataCount = 0
    oCount = 0
    testList = glob.glob("C:\\Users\\kimjh\\Desktop\\normal\\*")  # 검사할 파일의 경로

    # virus total api ----------------------------------------------------------------
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
    key_list = [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]
    # ---------------------------------------------------------------------------------
    i = 0

    while(i < len(testList)):
        key = key_list[i%len(key_list)]
        print " ================== [ 테스트 현황 ] [{0:d}] 번째 데이터 입니다. ===================== ".format(dataCount+1)
        resource = sha1_for_largefile(str(testList[i]))  # 해시값 추출
        result = isExist(resource)
        if result == 0:
            virusTotal(resource, testList[i], key, oCount)
        dataCount += 1
        time.sleep(15/float(len(key_list)))
        i += 1

    f_w.write("---------------------- [ 결과 ] ----------------------------")
    f_w.write("\n")
    f_w.write("[전체 파일 갯수 => ")
    f_w.write(str(dataCount))
    f_w.write("]")
    f_w.write("\n")
    f_w.write("[적재된 ngram 갯수 => ")
    f_w.write(str(oCount))
    f_w.write("]")
    f_w.write("\n")
    f_w.write("[적재되지 못한 ngram 갯수 => ")
    f_w.write(str(dataCount-oCount))
    f_w.write("]")
    f_w.write("\n")
    f_w.write("------------------------------------------------------------")
    f_w.close()

if __name__ == "__main__":
    main()
