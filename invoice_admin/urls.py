"""invoice_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from admin_panel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user, name='login_user'),
]
# Dashboard Sider Urls
urlpatterns += [
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('dashboard_line_graph', views.dashboard_line_graph, name='dashboard_line_graph'),
]
# Invoice Url
urlpatterns += [
    path('invoice', views.invoice, name='invoice'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
    path('store_invoice', views.store_invoice, name='store_invoice'),
    path('edit_invoice/<id>', views.edit_invoice, name='edit_invoice'),
    path('delete_invoice/<id>', views.delete_invoice, name='delete_invoice'),
    path('update_invoice/<id>', views.update_invoice, name='update_invoice'),
]
# Customer Url
urlpatterns += [
    path('customer', views.customer, name='customer'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('store_customer', views.store_customer, name='store_customer'),
    path('edit_customer/<id>', views.edit_customer, name='edit_customer'),
    path('update_customer/<id>', views.update_customer, name='update_customer'),
    path('delete_customer/<id>', views.delete_customer, name='delete_customer'),
]
# Excel Url
urlpatterns += [
    path('excel', views.excel, name='excel'),
    path('import_customer_per_data',views.import_customer_per_data, name='import_customer_per_data'),
    path('import_invoice_per_data',views.import_invoice_per_data, name='import_invoice_per_data'),
]
