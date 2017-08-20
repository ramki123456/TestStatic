import csv
import sqlite3
conn = sqlite3.connect('/home/brahma/Documents/EmpManagement/sqlite3.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS aug19")
cur.execute("CREATE TABLE Aug19 (ID INTEGER, PRODUCTNAME TEXT, TYPE TEXT, MODEL TEXT, LOCATION TEXT);")
with open('/home/brahma/Documents/personal/excelfiles/Data.csv', 'r') as f:
    r = csv.reader(f, delimiter=',')
    next(r)
    for row in r:
    	data = row
    	cur.execute(
        '''INSERT INTO Aug19(ID, PRODUCTNAME, TYPE, MODEL,
       LOCATION) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');'''.format(
            data[0], data[1], data[2], data[3], data[4]))
    conn.commit()