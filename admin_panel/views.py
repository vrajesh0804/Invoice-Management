from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from admin_panel.models import Login, Invoice, Customer
from admin_panel.forms import LoginForm, InvoiceForm, CustomerForm
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

@login_required(login_url='/')
def logout(request):
	messages.error(request, "Logout Successfully")
	return redirect(login_user)

@login_required(login_url='/')
def dashboard(request):
	customer_data = Customer.objects.all().count()
	invoice_data = Invoice.objects.all().count()
	return render(request, 'dashboard.html', {'site_title':'DASHBOARD', 'customer_data':customer_data, 'invoice_data':invoice_data})

@login_required(login_url='/')
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
@login_required(login_url='/')
def invoice(request):
	invoice_data = Invoice.objects.all()
	return render(request, 'invoice/index.html', {'site_title':'INVOICE', 'invoice_data':invoice_data})

@login_required(login_url='/')
def create_invoice(request):
	today = date.today()
	date_today = today.strftime('%Y-%m-%d')
	customer = Customer.objects.all()
	return render(request, 'invoice/create.html', {'site_title':'CREATE INVOICE', 'date_today':date_today, 'customer':customer})

@login_required(login_url='/')
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

@login_required(login_url='/')
def edit_invoice(request, id):
	invoice_data = Invoice.objects.get(id=id)
	today = date.today()
	date_today = today.strftime('%Y-%m-%d')
	customer = Customer.objects.get(id=invoice_data.customer_id)
	return render(request, 'invoice/edit.html', {'customer':customer,'date_today':date_today, 'site_title':'EDIT INVOICE', 'invoice_data':invoice_data})

@login_required(login_url='/')
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

@login_required(login_url='/')
def delete_invoice(request, id):
	invoice_delete = Invoice.objects.get(id=id)
	customer_data = Customer.objects.get(id=invoice_delete.customer_id)
	customer_data.total_spending = int(customer_data.total_spending) - int(invoice_delete.amount)
	email = 'vrajesh@yopmail.com'
		# Mail code
	subject = f'Invoice Deleted Successfully : {invoice_delete.name}'
	message = f'''Invoice has been deleted Successfully. 
Please login and check your invoice http://127.0.0.1:8000/'''
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject, message, email_from, recipient_list)
	customer_data.save()
	invoice_delete.delete()
	messages.info(request,"Invoice Deleted Successfully. Invoice Name: {} ".format(invoice_delete.name))
	return redirect('invoice')

# End of Invoice Code
# Customer Code
@login_required(login_url='/')
def customer(request):
	customer_data = Customer.objects.all()
	return render(request, 'customer/index.html', {'site_title':'CUSTOMER', 'customer_data':customer_data})

@login_required
def create_customer(request):
	return render(request, 'customer/create.html', {'site_title':'CREATE CUSTOMER'})

@login_required(login_url='/')
def store_customer(request):
	if request.method == "POST":
		customer_store = CustomerForm(request.POST)
		if customer_store.is_valid():
			customer_store.save()
			return redirect('create_customer')
		else:
			return render(request, 'customer/create.html', {'site_title':'CREATE CUSTOMER', 'error':'Data Missing'})
	else:
		return redirect('create_customer')

@login_required(login_url='/')
def edit_customer(request, id):
	customer_data = Customer.objects.get(id=id)
	return render(request, 'customer/edit.html', {'site_title':'EDIT INVOICE', 'customer_data':customer_data})

@login_required(login_url='/')
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

@login_required(login_url='/')
def delete_customer(request, id):
	customer_delete = Customer.objects.get(id=id)
	customer_invoice_data = Invoice.objects.filter(customer_id=customer_delete.id)
	customer_invoice_data.delete()
	customer_delete.delete()
	messages.info(request,"Customer Deleted Successfully. Invoice Name: {} ".format(customer_delete.customer_name))
	return redirect('customer')

# End of Customer Code
@login_required(login_url='/')
def excel(request):
	customer_data = Customer.objects.all()
	invoice_data = Invoice.objects.all()
	return render(request, 'excel/index.html', {'site_title':'EXCEL', 'customer_data':customer_data, 'invoice_data':invoice_data})

@login_required(login_url='/')
def import_customer_per_data(request):
	invoice_data = Invoice.objects.filter(customer_id=request.POST['customer_name']).values_list('name', 'purpose', 'date', 'amount')
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
	messages.info(request,"Exported Data Successfully")
	return redirect(excel)

@login_required(login_url='/')
def import_invoice_per_data(request):
	invoice_data = Invoice.objects.filter(id=request.POST['invoice_name']).values_list('name', 'purpose', 'date', 'amount')
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
	messages.info(request,"Exported Data Successfully")
	return redirect(excel)


