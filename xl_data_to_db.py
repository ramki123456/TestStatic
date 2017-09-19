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

    
    
    def upload_csv(request):
	csv_path_name = csvparse()
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			return HttpResponse("File is not CSV type please upload csv file")
        #if file is too large, return
		if csv_file.multiple_chunks():
			return HttpResponse("Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
	except Exception as e:
		print str(e)
	filepath = os.path.join(csv_path_name+"/", "csv_file")
	return HttpResponse("File has been uploaded successfully")
