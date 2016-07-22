# -*- coding: utf -8 -*-
# ���� ���� ���� �ڵ�
# 2016-07-21 ver3.0
# �ۼ���: ������

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

# func [1] �ؽ��� ���� [���� ����.]
def sha1_for_largefile(filepath, blocksize=8192):
    sha_1 = hashlib.sha1()
    try:
        f = open(filepath, "rb")
    except IOError as e:
        print("file open error", e)
        return '''����'''
    while True:
        buf = f.read(blocksize)
        if not buf:
            break
        sha_1.update(buf)
    return sha_1.hexdigest()  # �ؽð��� �����Ѵ�.


# end of [ sha1_for_largefile ] function

# func [2] �ؽ��� �� ������ ���̽��� �ִ��� ������ Ȯ���� ��
# hashString value �� ������ ���Ͽ� hash ���� ���ڷ� ���´�.
def isExist(hashString):
    result = 0
    connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
    db = connection.test  # testDB ����
    collection = db.hashData  # testDB�� hashData�� ����
    data = collection.find_one({"hexvalue": hashString})

    if data == None:  # ������ ���̽��� �������� �ʱ� �빮�� ���̷��� ��Ż�� �ѱ��.
        print "[1] ���̷��� ��Ż�� �ѱ�ڽ��ϴ�."
        result = 0
        return result

    else:  # ������ ���̽��� �����ϱ� ���̷��� �ΰɷ� ������.
        print "[1] �Ǽ��ڵ� ���� �Դϴ�."
        result = 1
        return result


# func [3] �ؽ��� ���̷��� ��Ż�� �ѱ��
def virusTotal(resource, element, filName):
    tempResource = str(resource)
    '''
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": tempResource,
                  "apikey": ""} # ������ api
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json_str = response.read()
    time.sleep(15) # 15 second delay !!!
    json_str = str(json_str)
    print json_str
    result = json_str.count("true")

    print "[File_Name] : ", filName
    '''
    result = 0
    if result <= 10:  # ���� ���� ---------------------------------------------------------
        print "[���] �������� �Դϴ�. "
        # [��������] �ؽð��� ������ ���̽��� �������� �ʴ´�.
    # ----------------------------------------------------------------------------------------------

    else:  # ���̷��� �����̴�. => ������ ���̽��� ������ ����� �� ����
        # result > 10
        print "[���] �Ǽ� ���� �Դϴ�. "
        # [�Ǽ�����] �ؽð��� ������ ���̽��� �����Ѵ�.
        connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
        db = connection.test  # testDB ����
        collection = db.hashData  # testDB�� testCollection ����
        data = collection.find_one({"hexvalue": tempResource})

        if data == None:  # ������ ���̽��� �������� �ʱ� ������ db�� �����Ѵ�.
            print " ������ ���̽��� �������� �ʱ� ������ db �� �����Ѵ�."
            collection.insert({"hexvalue": tempResource})

        else:  # ������ ���̽��� �����ϱ� �빮�� �������� �ʴ´�.
            print "�Ǽ��ڵ� ������ ������ ���̽��� �����մϴ�."

    '''
    # [ ������ ���� ������ ���̽� ] ==============================================================
    count = filName.count("\\")
    if not count == 0:
        s = filName.split("\\")
        print s
        filName = s[-1]
    start = json_str.find("positives")+12
    end = json_str.find("sha256")-3
    response1 = json_str[start:end] + "/56"
    # ===========================================================================================
    print "������ ������ ����� ������."
    response = ""
    if result == 0:
        response = "NO"
        print "���� ���Ϸ� �����͸� �ѱ�ڽ��ϴ�."
    else:
        response = "YES"
        print "�Ǽ� ���Ϸ� �����͸� �ѱ�ڽ��ϴ�."
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
    result_1 = 0
    stu = projectMain._Machine()
    step1 = stu.fileBinary_Extraction(element)  # ---------------------------------> step 1
    if step1 == 0:
        print "error ���� ����"
        return ''' The End '''

    else:  # step1 == 1
        # element�� ���ϰ�ο� �����̸��� ����ִ� ���ڿ��̴�.
        result_1 = stu.PE_Structure_elfanewString()  # ----------------------------> step 2
        if result_1 == 0:
            print "error [1] [����]"
            return ''' The End'''
        else:
            stu.PE_Structure_elfanewInt()  # --------------------------------------> step 3
            result_2 = stu.PE_Structure_sectionText_start_size(element)  # --------> step 4
            if result_2 == 0:
                print "error [2] [����]"
                return '''The End'''
            else:  # result_2 == 1
                stu.PE_Structure_sectionText_End()  # -------------------------> step 5
                result_3 = stu.ngramConstruct()  # ---------------------------------------> step 6
                if result_3 == 1:
                    result_4 = stu.ngramSort()  # --------------------------------------------> step 7
                    # time.sleep(10)  # 10�ʸ� ��ٷ���
                    if result_4 == 0:
                        print "error [3] ����"
                        return '''The End'''
                    else:
                        stu.dataBase(result)  # ---------------------------------------> step 8
                else:
                    return'''The End'''


# end of [ virusTotal ] function

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<  main >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def main():
    dataCount = 1
    testList = glob.glob("C:\\Users\\Win7\\Desktop\\normal\\*")  # �˻��� ������ ���
    for data in testList:
        print " ================== [ �׽�Ʈ ��Ȳ ] [{0:d}] ��° ������ �Դϴ�. ===================== ".format(dataCount)
        resource = sha1_for_largefile(str(data))  # �ؽð� ����
        result = isExist(resource)
        if result == 0:
            virusTotal(resource, str(data), data)
        dataCount += 1


if __name__ == "__main__":
    main()

