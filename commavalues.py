import csv
import sqlite3
import time
import datetime
conn = sqlite3.connect('/home/brahma/Documents/EmpManagement/sqlite3.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS aug20")
cur.execute("CREATE TABLE Aug20 (ID INTEGER, PRODUCTNAME TEXT, TYPE TEXT, MODEL TEXT, LOCATION TEXT, DATE TEXT);")
with open('/home/brahma/Documents/personal/excelfiles/Data.csv', 'r') as f:
    r = csv.reader(f, delimiter=',')
    next(r)
    for row in r:
    	data = row
    	cur.execute(
        '''INSERT INTO Aug20(ID, PRODUCTNAME, TYPE, MODEL, LOCATION, DATE) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');'''.format(
            data[0], data[1], data[2], data[3], data[4], time.strftime("%d/%m/%Y")))
    conn.commit()
