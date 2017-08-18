import sqlite3

import xlrd

print "Connecting to Sqlite Database..........."
conn = sqlite3.connect('/home/hanumanth/Desktop/newDB.bb')

print "Connected succesfully."
print "Creating cursor to execute the DB queries......"
curs = conn.cursor()
print "Cursor created successfully"

print "Wait...Opeing Excel file.."
workbook = xlrd.open_workbook('/home/hanumanth/Desktop/Data.xls')
print "reading the particular sheet of excel file..."
# Reading the particular sheet data using sheet_index
sheet = workbook.sheet_by_index(0)
# Looping over the rows of Sheet
for r in range(0, sheet.nrows):
    print "Loading {0} row of Excel file".format(r)
    data = sheet.row(r)
    # print data[1].value
    curs.execute(
        '''INSERT INTO exceltable(ID, PRODUCTNAME, TYPE, MODEL, /'''
        '''LOCATION) VALUES ('{0}', '{1}', '{2}', '{3}','{4}');'''.format(
            data[0].value, data[1].value, data[2].value, data[3].value,
            data[4].value))
    conn.commit()
    print "{0} row inserted into DB table....:)".format(r)

print "I am done... All the rows were in Database.. Go and check..."
# curs.execute("INSERT INTO PCFC (id, ProductName,
# Type, Model, Location) VALUES (cell.value(0);")
# conn.commit()
