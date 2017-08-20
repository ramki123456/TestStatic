import sqlite3
import xlrd

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponse,HttpResponseRedirect
from MyApp.models import ExcelProduct

# Create your views here.

def home(request):
	return HttpResponse('hi hari, welcome to App')

def load_facebook(request):
	return HttpResponseRedirect('http://www.facebook.com')

def welcome(request):
	return render(request,'welcome.html')

def loginview(request):
	return render(request,'login.html')

def my_login(request):
	#import pdb
	#pdb.set_trace()
	username = request.GET['uname']
	password = request.GET['pwd']
	return render_to_response('login_welcome.html', {'uname':username})

class LoadExcelDataView(View):
	def get(self, request, *args, **kwargs):
		conn = sqlite3.connect('/home/brahma/Documents/personal/mystuff/MyPro/test.db')
		curs = conn.cursor()
		curs.execute("DROP TABLE IF EXISTS Aug20")
		curs.execute("CREATE TABLE Aug20 (ID INTEGER, PRODUCTNAME TEXT, TYPE TEXT, MODEL TEXT, LOCATION TEXT);")
		workbook = xlrd.open_workbook('/home/brahma/Documents/personal/excelfiles/Data.xls')
		# Reading the particular sheet data using sheet_index
		sheet = workbook.sheet_by_index(0)
		# Looping over the rows of Sheet
		for r in range(1, sheet.nrows):
			data = sheet.row(r)
			#obj = ExcelProduct(product_name=data[1].value, _type=data[2].value, _model=data[3].value, location=data[4].value)
			#obj.save()
			print data[1].value
			curs.execute("INSERT INTO Aug20(PRODUCTNAME, TYPE, MODEL, LOCATION) VALUES ('{0}', '{1}', '{2}', '{3}');".format(
				data[1].value, data[2].value, data[3].value, data[4].value))
			conn.commit()
		
		return HttpResponse("All the data were loaded into Database...")
