from django import forms  
from admin_panel.models import Login, Invoice, Customer, City, State, Country

class LoginForm(forms.ModelForm):  
    class Meta:  
        model = Login  
        fields = "__all__"  

class InvoiceForm(forms.ModelForm):  
    class Meta:  
        model = Invoice  
        fields = "__all__"  

class CustomerForm(forms.ModelForm):  
    class Meta:  
        model = Customer  
        fields = "__all__"  

class CityForm(forms.ModelForm):
    class Meta:
        model = City  
        fields = "__all__"  

class StateForm(forms.ModelForm):
    class Meta:
        model = State  
        fields = "__all__"  

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country  
        fields = "__all__"  
