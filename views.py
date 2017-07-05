import smtplib, json
import os
import pdfkit

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from MyApp.models import ComplteStockDetails, DealersInfo, Person, Billings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
from TestStatic.settings import BASE_DIR
from MyApp.forms import StockForm, PersonForm, DealerForm

# Create your views here.
def load(request):
	return render(request, 'test.html')
'''
def app_login(request):
	return render(request, 'login.html')
'''
# Create your views here.


class LoadView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'login.html')


class LoginView(View):
	def get(self, request):
		try:
			if request.user.is_authenticated():
				return HttpResponseRedirect('/home/')
			else:
				return HttpResponseRedirect('/load/')
		except:
			return HttpResponseRedirect('/load/')

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST.get('user'), 
							password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/home/')
			else:
				return HttpResponseRedirect('/load/')

		else:
			return HttpResponseRedirect('/load/')


class HomePageView(View):
	def get(self, request, *args, **kwargs):
		try:
			if request.user.is_authenticated():
				return render_to_response('home.html', {'user': str(request.user)})
			else:
				return HttpResponseRedirect('/load/')
		except:
			return HttpResponseRedirect('/load/')


class LoadContactView(View):
	def get(self, request, *args, **kwargs):
		try:
			if request.user.is_authenticated():
				return render(request, 'contact.html')
			else:
				return HttpResponseRedirect('/load/')
		except:
			return HttpResponseRedirect('/load/')


class ContactView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			data = request.GET
			msg = MIMEMultipart()
			msg['From'] = "Pavana Medicals"
			msg['To'] = 'ramki0653@gmail.com'
			msg['Subject'] = "Comment :: " + str(data.get('name')) + " Mobile - "+ data.get('mobile') + " Mail - " + data.get('mail')
			message = data.get('comment')
			msg.attach(MIMEText(message))
			mailserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
			# identify ourselves to smtp gmail client
			mailserver.ehlo()
			# secure our email with tls encryption
			mailserver.starttls()
			# re-identify ourselves as an encrypted connection
			mailserver.ehlo()
			mailserver.login('pythontechiee@gmail.com', 'mypass@9043')

			mailserver.sendmail('pythontechiee@gmail.com','ramki0653@gmail.com',msg.as_string())

			mailserver.quit()
			return HttpResponseRedirect('/home/')
		else:
			return HttpResponseRedirect('/load/')


class LogoutView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			logout(request)
			return HttpResponseRedirect('/load/')
		else:
			return HttpResponseRedirect('/load/')


class StockView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			model = ComplteStockDetails
			objs = ComplteStockDetails.objects.all()
			for obj in objs:
				obj.price = obj.price_per_unit + (obj.price_per_unit * (float(obj.margin) + float(obj.vat)))
			return render_to_response('show_stock.html',
									  {'data': objs, 'itemnames': [obj.item_name for obj in objs]})
		else:
			return HttpResponseRedirect('/load/')


class LoadShopPageView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return render(request, 'shop_page.html', {'count': range(2, 50)},
						  context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/load/')


class LoadMainShopPage(View):
	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			loop_content = range(int(request.POST.get('no_of_products')))
			objs = ComplteStockDetails.objects.all()
			return render_to_response('select_shop_page.html',
		    						  {'objs': objs,
		    						   'looping': loop_content},
		    						  context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/load/')

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/load_shop_page/')
		else:
			return HttpResponseRedirect('/load/')


class BachtoHomeView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return render_to_response('login_welcome.html', {'user': request.user.username})
		else:
			return HttpResponseRedirect('/load/')


class SelectedStockSearchView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			objs = ComplteStockDetails.objects.filter(item_name=str(request.GET.get('itemname')))
			for obj in objs:
				obj.price = obj.price_per_unit + (obj.price_per_unit * (float(obj.margin) + float(obj.vat)))
			
			return render_to_response('show_stock.html',
									  {'data': objs,
									   'itemnames': [i.item_name for i in ComplteStockDetails.objects.all()]})
		else:
			return HttpResponseRedirect('/load/')

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')
		else:
			return HttpResponseRedirect('/load/')


class ShowDealerView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			objs = DealersInfo.objects.all()
			return render_to_response('dealers.html', {'data': objs})
		else:
			return HttpResponseRedirect('/load/')

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/home/')
		else:
			return HttpResponseRedirect('/load/')



class ShowBillingCart(View):
	def post(self, request, *args, **kwargs):
		users = Person.objects.all()
		if request.user.is_authenticated():
			dictionary = dict(request.POST.viewitems())
			test_list = []
			for key in range(len(dictionary.get('item_name_s'))):
							
				if str(dictionary.get('item_name_s')[key]) != str('') and int(dictionary.get('req_qnt')[key])>0:
					try:
						bill_stock_obj = ComplteStockDetails.objects.get(batch_num=int(dictionary.get('item_name_s')[key]))
						if bill_stock_obj and bill_stock_obj.quantity and (int(bill_stock_obj.quantity) > int(dictionary.get('req_qnt')[key])):
							total_price = (float(bill_stock_obj.price_per_unit) + (
								float(bill_stock_obj.price_per_unit) * (float(
									bill_stock_obj.margin) + float(
									bill_stock_obj.vat)))) * float(dictionary.get('req_qnt')[key])
							total_ppu = (float(bill_stock_obj.price_per_unit) + (
								float(bill_stock_obj.price_per_unit) * (float(
									bill_stock_obj.margin) + float(
									bill_stock_obj.vat))))

							test_list.append({'obj': bill_stock_obj,
											  'quantity': dictionary.get('req_qnt')[key],
											  'tp': total_price,
											  'total_ppu': total_ppu})
					except:
						continue
		        else:
		            pass
			sum_of_all_elements = sum([x['tp'] for x in test_list])
			return render_to_response('show_final_billing_cart.html', {
		        'test_list': test_list, 'sum': sum_of_all_elements, 'users': users},
		        context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/load/')

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/load_shop_page/')
		else:
			return HttpResponseRedirect('/load/')

class GoFinalBillingView(View):
	def post(self, request, *args, **kwargs):
		final_list = []
		dictionary = dict(request.POST)
		if request.user.is_authenticated() and dictionary.get('bill_user')[0]:
			batch_numbers = dictionary['batch_nums']
			item_names = dictionary['item_nums']
			company_names = dictionary['company_names']
			ppus = dictionary['ppus']
			quantities = dictionary['quantities']
			tps = dictionary['tps']
			for i in range(len(batch_numbers)):
			    try:
			        obj = ComplteStockDetails.objects.get(batch_num=batch_numbers[i])
			    except:
			        obj = None
			    if obj and obj.quantity and (int(obj.quantity) >= int(quantities[i])) :
			        obj.quantity = int(obj.quantity) - int(quantities[i])
			        obj.save()
			        final_list.append({'batch_num': batch_numbers[i], 
			        				   'item_name': item_names[i],
			                           'company': company_names[i], 
			                           'ppu': ppus[i], 
			                           'quantity': quantities[i],
			                           'tp': tps[i]})
			    else:
			    	continue
			per_obj = Person.objects.get(user = dictionary.get('bill_user')[0])
			bill_obj = Billings(bill_items=final_list, bill_user=per_obj, bill_amount=float(dictionary['sum'][0]))
			bill_obj.save()
			c = render_to_response('billing.html', {'final_list': final_list, 'sum': dictionary['sum'],
								   'inv_number': bill_obj.bill_number, 'inv_date': bill_obj.bill_date, 
								   'user': dictionary.get('bill_user')})
			
			fp = open('billing.html', 'w')
			fp.write(str(c))
			fp.close()
			
			return render_to_response('final_billing.html',
				{'final_list': final_list, 'user_details': per_obj,
				'sum': dictionary['sum']}, context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/load_shop_page/')


class SendInvoiceView(View):
	def post(self, request):
		mail = request.POST.get('email_id')
		msg = MIMEMultipart('alternative')
		msg['From'] = 'pythontechiee@gmail.com'
		msg['To'] = mail
		msg['Subject'] = "Your Invoice Details Bill"
		c = open('billing.html', 'r').read()
		part2 = MIMEText(c, 'html')
		msg.attach(part2)
		mailserver = smtplib.SMTP("smtp.mail.yahoo.com",587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('pythontechiee@gmail.com', 'mypass@9043')
		mailserver.sendmail('pythontechiee@gmail.com', 
							mail,
							msg.as_string())
		mailserver.close()
		return HttpResponseRedirect('/home/')

def print_page(request):
	#config = pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf')
	#path_wkthmltopdf = r'C:/Python27/wkhtmltopdf/bin/wkhtmltopdf.exe'
	#config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	import pdb
	pdb.set_trace()
	path_wkthmltopdf = r'C:/wkhtmltopdf/bin/wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	pdfkit.from_file('billing.html', 'out.pdf', configuration=config)
	# os.system('lpr out.pdf')
	return HttpResponseRedirect('/home')


class ShowBillingsView(View):
	def get(self, request):
		if request.user.is_authenticated():
			objs = Billings.objects.all().order_by('-bill_date')
			users = Person.objects.all() 
			return render(request, 'billings.html', {'billings': objs, 'users': users})
		else:
			return HttpResponseRedirect('/load/')


	def post(self, request):
		if request.user.is_authenticated():
			objs = Billings.objects.all()
			users = Person.objects.all()
			return render(request, 'billings.html', {'billings': objs, 'users': users})
		else:
			return HttpResponseRedirect('/load/')

class GenerateBillView(View):
	def get(self, request, bill_num=None):
		import pdb
		pdb.set_trace()
		if request.user.is_authenticated() and bill_num:
			obj = Billings.objects.get(bill_number=int(bill_num))
			inv_number = obj.bill_number
			inv_date = obj.bill_date
			user = obj.bill_user.user
			final_list = obj.bill_items
			sum1 = obj.bill_amount
			c = render_to_response('bill_for_each_invoice.html',
								   {'inv_number': inv_number, 
								   'inv_date': inv_date,
								   'user': user,
								   'final_list': final_list,
								   'sum1': sum1})
			path_wkthmltopdf = r'C:/wkhtmltopdf/bin/wkhtmltopdf.exe'
			config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
			fp = open('test_bill_test.html', 'w')
			fp.write(str(c))
			fp.close()
			pdfkit.from_file('test_bill_test.html', '{BASE_DIR}/Bills/{bill_num}_{user}_{date}{month}{year}.pdf'.format(
				BASE_DIR=BASE_DIR, bill_num=str(inv_number), user=user, date=inv_date.date().day,
				month=inv_date.date().month, year=inv_date.date().year), configuration=config)
			os.remove('test_bill_test.html')
			return HttpResponseRedirect('/home/')
		else:
			return HttpResponseRedirect('/load/')

class GetBillsByDateView(View):
	def get(self, request):
		if request.user.is_authenticated():
			try:
				objs = Billings.objects.filter(bill_date__range=[request.GET['start'], request.GET['end']]).order_by('-bill_date')
				users = Person.objects.all() 
				return render(request, 'billings.html', {'billings': objs, 'users': users})
			except:
				return HttpResponseRedirect('/billings/')
		else:
			return HttpResponseRedirect('/load/')

class GetBillsByUserView(View):
	def get(self, request):
		if request.user.is_authenticated():
			try:
				objs = Billings.objects.filter(bill_user__user=str(request.GET['customer'])).order_by('-bill_date')
				users = Person.objects.all() 
				return render(request, 'billings.html', {'billings': objs, 'users': users})
			except:
				return HttpResponseRedirect('/billings/')
		else:
			return HttpResponseRedirect('/load/')

class ShowProfitView(View):
	def get(self, request):
		if request.user.is_authenticated():
			obj_bills = Billings.objects.all()
			users = Person.objects.all()
			data_list = []
			for bill in obj_bills:
				data = {}
				data['bill_num'] = bill.bill_number
				data['bill_amount'] = bill.bill_amount
				data['bill_date'] = bill.bill_date
				data['actual_amount'] = float(
					sum([ComplteStockDetails.objects.get(
						batch_num=item['batch_num']).price_per_unit * int(
						item['quantity']) for item in bill.bill_items]))
				data['profit'] = float(data['bill_amount'])-data['actual_amount']
				data['user'] = str(bill.bill_user.user)
				data_list.append(data)
			total_profit = sum([list_['profit'] for list_ in data_list])
			return render(request, 'profit_bills.html',
						  {'data': data_list, 'users': users,
						  'total_profit': total_profit})
		else:
			return HttpResponseRedirect('/load/')


class ProfitBillsByDateView(View):
	def get(self, request):
		if request.user.is_authenticated():
			try:
				obj_bills = Billings.objects.filter(bill_date__range=[request.GET['start'], request.GET['end']]).order_by('-bill_date')
				users = Person.objects.all()
				data_list = []
				for bill in obj_bills:
					data = {}
					data['bill_num'] = bill.bill_number
					data['bill_amount'] = bill.bill_amount
					data['bill_date'] = bill.bill_date
					data['actual_amount'] = float(
						sum([ComplteStockDetails.objects.get(
							batch_num=item['batch_num']).price_per_unit * int(
							item['quantity']) for item in bill.bill_items]))
					data['profit'] = float(data['bill_amount'])-data['actual_amount']
					data['user'] = str(bill.bill_user.user)
					data_list.append(data)
				total_profit = sum([list_['profit'] for list_ in data_list])
				return render(request, 'profit_bills.html',
							  {'data': data_list, 'users': users,
							  'total_profit': total_profit})
			except:
				return HttpResponseRedirect('/profit/')
		else:
			return HttpResponseRedirect('/load/')


class ProfitBillsByUserView(View):
	def get(self, request):
		if request.user.is_authenticated():
			try:
				obj_bills = Billings.objects.filter(bill_user__user=str(request.GET['customer'])).order_by('-bill_date')
				users = Person.objects.all()
				data_list = []
				for bill in obj_bills:
					data = {}
					data['bill_num'] = bill.bill_number
					data['bill_amount'] = bill.bill_amount
					data['bill_date'] = bill.bill_date
					data['actual_amount'] = float(
						sum([ComplteStockDetails.objects.get(
							batch_num=item['batch_num']).price_per_unit * int(
							item['quantity']) for item in bill.bill_items]))
					data['profit'] = float(data['bill_amount'])-data['actual_amount']
					data['user'] = str(bill.bill_user.user)
					data_list.append(data)
				total_profit = sum([list_['profit'] for list_ in data_list])
				return render(request, 'profit_bills.html',
							  {'data': data_list, 'users': users,
							  'total_profit': total_profit})
			except:
				return HttpResponseRedirect('/profit/')
		else:
			return HttpResponseRedirect('/load/')


class AddPersonPageView(View):
	def get(self, request):
		if request.user.is_authenticated():
			form = PersonForm()
			return render(request, 'add_dealer_page.html', {'form': form})

class AddPersonView(View):
	def post(self, request):
		import pdb
		pdb.set_trace()
		if request.user.is_authenticated():
			form = PersonForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/home/')
			else:
				return HttpResponseRedirect('/add_person_page/')
		else:
			return HttpResponseRedirect('/load/')


class AddDealerPageView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			form = DealerForm()
			return render(request, 'add_dealer_page.html', {'form': form})
		else:
			return HttpResponseRedirect('/load/')


class AddDealerView(View):
	def post(self, request):
		if request.user.is_authenticated():
			form = DealerForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/home/')
			else:
				return HttpResponseRedirect('/add_dealer_page/')
		else:
			return HttpResponseRedirect('/load/')

##############  Profit/Loss Code for all the bills ############################
'''
obj_bills = Billings.objects.all()
for bill in obj_bills:
	data = {}
	data['bill_num'] = bill.bill_number
	data['bill_amount'] = bill.bill_amount
	data['actual_amount'] = float(
		sum([ComplteStockDetails.objects.get(batch_num=item['batch_num']).price_per_unit * int(item['quantity']) for item in bill.bill_items]))
	data['profit'] = float(data['bill_amount'])-data['actual_amount']
	data['user'] = bill.bill_user.user
	data_list.append(data)
'''
############  For getting profile for all the billings  ########################
'''
[float(item_data.['bill_amount'])-item_data['actual_amount'] for item_data in data_list]
'''
################################################################################

######################  Excel Creation  ########################################
'''
pandas.DataFrame(
	{'Date': [str(obj.bill_date.date()) for obj in objs],
	 'INVOICE NUMBER': [obj.bill_number for obj in objs],
	 'Invoice Amount': [obj.bill_amount for obj in objs]}).to_excel(
	 'test.xlsx', sheet_name='sheet1', index=False)
'''
################################################################################
