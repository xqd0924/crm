"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.user_login),
    url(r'^logout/$', views.logout_s),
    url(r'^register/', views.register),
    url(r'^index/', views.index),
    url(r'^customers/list/', views.CustomerView.as_view(), name='customer_list'),
    url(r'^mycustomers/', views.CustomerView.as_view(), name='mycustomers'),
    url(r'^customer/add', views.AddEditCustomerView.as_view(), name='addcustomer'),
    url(r'^customer/edit/(\d+)', views.AddEditCustomerView.as_view(), name='editcustomer'),
    url(r'^consult_record/$', views.ConsultRecordView.as_view(), name='consult_record'),
    url(r'^consult_record/add', views.AddEditConsultRecordView.as_view(), name='add_consult_record'),
    url(r'^consult_record/edit/(\d+)', views.AddEditConsultRecordView.as_view(), name='edit_consult_record'),
]
