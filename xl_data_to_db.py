import sqlite3

import xlrd

conn = sqlite3.connect('/home/hanumanth/Desktop/exceldata.db')
cur = conn.cursor()
cur.execute("CREATE TABLE PCFC (ID INTEGER, PRODUCTNAME TEXT, TYPE TEXT, MODEL TEXT, LOCATION TEXT);")

workbook = xlrd.open_workbook('/home/hanumanth/Desktop/Data.xls')
sheet = workbook.sheet_by_index(0)
for r in range(0, sheet.nrows):
    data = sheet.row(r)
    cur.execute(
        '''INSERT INTO PCFC(ID, PRODUCTNAME, TYPE, MODEL,
        LOCATION) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');'''.format(
            data[0].value, data[1].value, data[2].value, data[3].value, data[4].value))
    conn.commit()
