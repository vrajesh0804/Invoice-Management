from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from admin_panel.models import Login, Invoice, Customer, Country, State, City
from admin_panel.forms import LoginForm, InvoiceForm, CustomerForm, CountryForm, StateForm, CityForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import hashlib
from datetime import date
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
import numpy as np
import pandas as pd
import xlsxwriter
import xlwt
import datetime
import sweetify
import csv
import xlrd
from tablib import Dataset


# Create your views here.

def login_user(request):
	if request.method == 'GET':
		return render(request, 'login_page.html', {'site_title':'INVOICE MANAGEMENT | LOGIN PAGE'})
	else:
		user_data = Login.objects.all()
		for data in user_data:
			username = data.username
			password = data.password
		filled_username = request.POST['username']			
		filled_password = request.POST['password']
		filled_password_hash = hashlib.md5(filled_password.encode()).hexdigest()
		if filled_password_hash == password and filled_username == username:
			return redirect(dashboard)
		else:
			messages.error(request, "Enter Valid Username and Password")
			return redirect(login_user)

def logout(request):
	messages.error(request, "Logout Successfully")
	return redirect(login_user)

def dashboard(request):
	customer_data = Customer.objects.all().count()
	invoice_data = Invoice.objects.all().count()
	return render(request, 'dashboard.html', {'site_title':'DASHBOARD', 'customer_data':customer_data, 'invoice_data':invoice_data})

def dashboard_line_graph(request):
	labels = []
	data = []
	queryset = Customer.objects.values('customer_name','total_spending')
	for entry in queryset:
		labels.append(entry['customer_name'])
		data.append(entry['total_spending'])
	return JsonResponse(data={
		'labels': labels,
		'data': data,	
	})

# Invoice Code
def invoice(request):
	customer_data = Customer.objects.all()
	invoice_data = Invoice.objects.all()
	return render(request, 'invoice/index.html', {'site_title':'INVOICE', 'invoice_data':invoice_data, 'customer_data':customer_data})

def create_invoice(request):
	today = date.today()
	date_today = today.strftime('%Y-%m-%d')
	customer = Customer.objects.all()
	return render(request, 'invoice/create.html', {'site_title':'CREATE INVOICE', 'date_today':date_today, 'customer':customer})

def store_invoice(request):
	if request.method == "POST":
		invoice_store = InvoiceForm(request.POST)
		customer_data = Customer.objects.get(id=request.POST['customer_id'])
		if customer_data.total_spending is None:
			customer_data.total_spending = request.POST['amount']
		else:
			entered_amount = int(request.POST['amount'])
			old_value = int(customer_data.total_spending)
			new_value = old_value + entered_amount
			customer_data.total_spending = new_value
		email = 'vrajesh@yopmail.com'
		# Mail code
		subject = 'Invoice Created Successfully'
		message = f'Invoice has been created Successfully. Please login and check your invoice http://127.0.0.1:8000/'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email]
		send_mail(subject, message, email_from, recipient_list)
		invoice_store.save()
		customer_data.save()
		messages.error(request, "Invoice Added Successfully.")
		return redirect('invoice')
	else:
		messages.error(request, "Something missing")
		return redirect('create_invoice')

def edit_invoice(request, id):
	invoice_data = Invoice.objects.get(id=id)
	today = date.today()
	date_today = today.strftime('%Y-%m-%d')
	customer = Customer.objects.get(id=invoice_data.customer_id)
	return render(request, 'invoice/edit.html', {'customer':customer,'date_today':date_today, 'site_title':'EDIT INVOICE', 'invoice_data':invoice_data})

def update_invoice(request, id):
	if request.method == "POST":
		email = 'vrajesh@yopmail.com'
		invoice_data = Invoice.objects.get(id=id)
		invoice_update = InvoiceForm(request.POST, instance=invoice_data)
		# Mail code
		subject = f'Invoice Updated : {invoice_data.name}'
		message = f'''Invoice has been Updated Successfully. 
Please login and check your invoice http://127.0.0.1:8000/
Here is your detail 
Invoice Name : {invoice_data.name}
Customer Name : {invoice_data.customer_id}
Amount : {invoice_data.amount}
Created : {invoice_data.date}'''
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email]
		send_mail(subject, message, email_from, recipient_list)
		invoice_update.save()
		messages.info(request,"Invoice Updated Successfully. Invoice Name {}: ".format(invoice_data.name))
		return redirect('invoice')
	else:
		messages.error(request,"Error")
		return redirect('invoice')

# End of Invoice Code
# Customer Code
def customer(request):
	customer_data = Customer.objects.all()
	for data in customer_data:
		country = Country.objects.get(id=data.country_id)
		state = State.objects.get(id=data.state_id)
		city = City.objects.get(id=data.city_id)
	return render(request, 'customer/index.html', {'country':country, 'site_title':'CUSTOMER', 'customer_data':customer_data, 'state':state, 'city':city})

def create_customer(request):
	date_today = date.today()
	today = date_today.strftime('%Y-%m-%d')
	country_data = Country.objects.all()
	return render(request, 'customer/create.html', {'today':today,'site_title':'CREATE CUSTOMER', 'country_data':country_data})

def ajax_load_states(request):
	country_id = request.GET.get('country_id')
	states = State.objects.filter(country_id=country_id).all()
	return render(request, 'customer/filter/state_filter.html', {'states': states})

def ajax_load_cities(request):
	state_id = request.GET.get('state_id')
	cities = City.objects.filter(state_id=state_id).all()
	return render(request, 'customer/filter/city_filter.html', {'cities': cities})

def store_customer(request):
	if request.method == "POST":
		customer_store = CustomerForm(request.POST)
		if customer_store.is_valid():
			customer_store.save()
			messages.info(request,'Customer Added Successfully')
			return redirect('customer')
		else:
			messages.info(request,'Data Missing')
			return redirect('create_customer')
	else:
		return redirect('customer')

def edit_customer(request, id):
	date_today = date.today()
	today = date_today.strftime('%Y-%m-%d')
	customer_data = Customer.objects.get(id=id)
	country_data = Country.objects.all()
	country = Country.objects.get(id=customer_data.country_id)
	state = State.objects.get(id=customer_data.state_id)
	state_data = State.objects.filter(country_id=country.id)
	city = City.objects.get(id=customer_data.city_id)
	city_data = City.objects.filter(state_id=state.id)
	return render(request, 'customer/edit.html', {'today':today,'city':city,'country_data':country_data,'country':country,'site_title':'EDIT INVOICE', 'customer_data':customer_data, 'state':state, 'state_data':state_data, 'city_data':city_data})

def update_customer(request, id):
	if request.method == "POST":
		customer_data = Customer.objects.get(id=id)
		customer_update = CustomerForm(request.POST, instance=customer_data)
		customer_update.save()
		messages.info(request,"Customer Updated Successfully. Invoice Name {}: ".format(customer_data.customer_name))
		return redirect('customer')
	else:
		messages.error(request,"Error")
		return redirect('customer')


def import_customer(request):
	customer_data = CustomerForm()
	dataset = Dataset()
	new_persons = request.FILES['excel_file']
	if not new_persons.name.endswith('xlsx'):
		messages.info(request,"Make sure your imported excel is same as sample excel.. Only XLSX File Accepted")
		return redirect(customer)

	imported_data = dataset.load(new_persons.read(),format='xlsx')
	for data in imported_data:
		try:

			country_data = Country.objects.get(name=data[7])
			state_data = State.objects.get(name=data[8])
			city_data = City.objects.get(name=data[9])
			value = Customer(
				data[0],
				data[1],
				data[2],
			 	data[3],
			 	data[4],
			 	data[5],
			 	data[6],
			 	country_data.id,
			 	state_data.id,
			 	city_data.id
		 	)
			value.save() 
			messages.info(request,"Customer Imported Successfully.")
			return redirect(customer)
		except:
			messages.info(request,"Something not right...")
			return redirect(customer)

def export_customer(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Customer Name', 'Company Name', 'Description', 'Phone', 'Email', 'Address', 'Total Spending'])
	users = Customer.objects.all().values_list('customer_name','company_name','description','phone','email','address', 'total_spending')
	for user in users:
		writer.writerow(user)
	response['Content-Disposition'] = 'attachment; filename="'+user[0]+'.csv"'
	return response

# End of Customer Code
def excel(request):
	customer_data = Customer.objects.all()
	invoice_data = Invoice.objects.all()
	return render(request, 'excel/index.html', {'site_title':'EXCEL', 'customer_data':customer_data, 'invoice_data':invoice_data})

def import_customer_per_data(request):
	invoice_data = Invoice.objects.filter(customer_id=request.POST['customer_name']).values_list('name', 'purpose', 'date', 'amount')
	if not invoice_data :
		messages.info(request, 'No Invoice Found of Appropriate Customer')
		return redirect(invoice)
	else:
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Invoice')
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		columns = ['Invoice Name', 'Purpose', 'Created Date', 'Amount']
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)
		font_style = xlwt.XFStyle()
		for row in invoice_data:
			row_num += 1
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="'+row[0]+'.xls"'
		wb.save(response)
		return response

# End of Version 1.0
# Version 1.1 BEGINS

# Project View
def project(request):
	return HttpResponse("project")

def create_project(request):
	return HttpResponse("create_project")

def store_project(request):
	return HttpResponse("store_project")

def edit_project(request, id):
	return HttpResponse("edit_project")

def update_project(request, id):
	return HttpResponse("update_project")

def delete_project(request, id):
	return HttpResponse("delete_project")


# End of Project