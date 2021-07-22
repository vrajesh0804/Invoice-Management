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
    currency_symbol = models.CharField(max_length=255, default="")
    created_at = models.CharField(max_length=255, default="", blank="True")  
    updated_at = models.CharField(max_length=255, default="", blank="True")  
    class Meta:  
        db_table = "invoice" 


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    class Meta:  
        db_table = "country" 

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:  
        db_table = "state" 

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    class Meta:  
        db_table = "city" 

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
    created_at = models.CharField(max_length=255, default="", blank="True")  
    updated_at = models.CharField(max_length=255, default="", blank="True")  
    class Meta:  
        db_table = "customer" 


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    symbol = models.CharField(max_length=255, default="")
    price_dif = models.IntegerField(default=0)
    class Meta:  
        db_table = "currency" 