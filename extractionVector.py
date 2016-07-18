import mysql.connector
# database ----------------------------------------------------------------------

con = mysql.connector.connect(host = 'localhost',
                              user='root',
                              password='1111',
                              database='test')
cur = con.cursor()

test = "select * from s1;"
cur.execute(test)
data = cur.fetchone()
#print data

data = cur.fetchone()
data = str(data)
#print data
vector = list()
s = data[3:len(data)-4].split(',')
for element in s:
    vector.append(int(element))
print vector
vector.append(1)
con.close()







