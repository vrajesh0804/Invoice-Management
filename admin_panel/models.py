from django.db import models
from django import forms
from django.contrib.auth.models import User

class Login(models.Model):  
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)  
    password = models.CharField(max_length=255)  
    class Meta:  
        db_table = "login_data" 

class Invoice(models.Model):  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)  
    purpose = models.CharField(max_length=255)  
    date = models.DateField()  
    customer_id = models.CharField(max_length=255)  
    amount = models.CharField(max_length=255)  
    class Meta:  
        db_table = "invoice" 

class Customer(models.Model):  
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, default="") 
    company_name = models.CharField(max_length=255, default="") 
    description = models.CharField(max_length=255, default="") 
    phone = models.IntegerField(default=0) 
    email = models.EmailField(max_length=255, default="") 
    address = models.CharField(max_length=255, default="") 
    country_id = models.CharField(max_length=255, default="") 
    state_id = models.CharField(max_length=255, default="") 
    city_id = models.CharField(max_length=255, default="") 
    total_spending = models.IntegerField(default=0) 
    class Meta:  
        db_table = "customer" 