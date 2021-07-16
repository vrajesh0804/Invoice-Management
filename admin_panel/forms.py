from django import forms  
from admin_panel.models import Login, Invoice, Customer

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
