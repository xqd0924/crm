from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import auth
from django.contrib.auth import login,logout
from app01 import models,myforms
from django.views import View
from app01.utils.page import Pagination
from django.db.models import Q
from django import forms


# Create your views here.
def register(request):
    if request.method == 'GET':
        forms=myforms.RegForms()
        return render(request, 'register.html',{'forms':forms})
    elif request.method == 'POST':
        forms=myforms.RegForms(request.POST)
        if forms.is_valid():
            dic = forms.cleaned_data
            models.UserInfo.objects.create_user(**dic)
            return redirect('/login/')
        else:
            return render(request, 'register.html',{'errors':forms.errors})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/index/')
        else:
            error = '用户名或密码错误'
            return render(request, 'login.html', {'error': error})

def index(request):
    return render(request,'index.html')

class CustomerView(View):
    def get(self,request):
        if reverse('customer_list') == request.path:
            label = "公户列表"
            customer_list = models.Customer.objects.filter(consultant__isnull=True).all()
        elif reverse('mycustomers') == request.path:
            label = "我的客户"
            customer_list = models.Customer.objects.filter(consultant=request.user).all()

        val = request.GET.get('q')
        field = request.GET.get('field')
        if val:
            q = Q()
            q.children.append((field+'__contains',val))
            customer_list = customer_list.filter(q)
        current_page_num = request.GET.get('page',1)
        pagination = Pagination(current_page_num,customer_list.count(),request)
        customer_list = customer_list[pagination.start:pagination.end]

        path = request.path
        next = "?next=%s" % path
        return render(request,'customer_list.html',{'next':next,'customer_list': customer_list,'pagination':pagination,'label':label})

    def post(self,request):
        print(request.POST)
        func_str=request.POST.get('action')
        data=request.POST.getlist('selected_pk_list')
        if not hasattr(self,func_str):
            return HttpResponse("非法输入")
        else:
            func=getattr(self,func_str)
            queryset = models.Customer.objects.filter(pk__in=data)
            res=func(request, queryset)
            if res:
                return res
            ret=self.get(request)
            return ret

    def patch_delete(self, request, queryset):
        queryset.delete()

    def patch_reverse_gs(self, request, queryset):
        ret=queryset.filter(consultant__isnull=True)
        if ret:
            queryset.update(consultant=request.user)
        else:
            return HttpResponse('手速慢了！')

    def patch_reverse_sg(self, request, queryset):
        queryset.update(consultant=None)


# class AddCustomerView(View):
#     def get(self,request):
#         form = myforms.CustomerModelForm()
#         return render(request,'add_customer.html',{'form':form})
#
#     def post(self,request):
#         form=myforms.CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('customer_list'))
#         else:
#             return render(request, 'add_customer.html', {'form': form})
#
#
# class EditCustomerView(View):
#     def get(self,request,id):
#         edit_obj=models.Customer.objects.filter(pk=id).first()
#         form = myforms.CustomerModelForm(instance=edit_obj)
#         return render(request,'edit_customer.html',{'form':form})
#
    # def post(self,request,id):
    #     edit_obj = models.Customer.objects.filter(pk=id).first()
    #     form=myforms.CustomerModelForm(request.POST,instance=edit_obj)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(request.GET.get('next'))
    #     else:
    #         return render(request, 'edit_customer.html', {'form': form})


class AddEditCustomerView(View):
    def get(self,request,edit_id=None):
        edit_obj=models.Customer.objects.filter(pk=edit_id).first()
        form = myforms.CustomerModelForm(instance=edit_obj)
        return render(request,'add_edit_customer.html',{'form':form,'edit_obj':edit_obj})

    def post(self,request,edit_id=None):
        edit_obj = models.Customer.objects.filter(pk=edit_id).first()
        form=myforms.CustomerModelForm(request.POST,instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'add_edit_customer.html', {'form': form,'edit_obj':edit_obj})

class ConsultRecordView(View):
    def get(self,request):
        consult_record_list=models.ConsultRecord.objects.filter(consultant=request.user).all()
        customer_id=request.GET.get('customer_id')
        if customer_id:
            consult_record_list=consult_record_list.filter(customer_id=customer_id).all()
        return render(request,'consult_record.html',{'consult_record_list':consult_record_list})


class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model=models.ConsultRecord
        exclude=["delete_status"]


class AddEditConsultRecordView(View):
    def get(self,request,edit_id=None):
        edit_obj=models.ConsultRecord.objects.filter(pk=edit_id).first()
        form = ConsultRecordModelForm(instance=edit_obj)
        return render(request,'add_edit_consult_record.html',{'form':form,'edit_obj':edit_obj})

    def post(self,request,edit_id=None):
        edit_obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
        form=ConsultRecordModelForm(request.POST,instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('consult_record'))
        else:
            return render(request, 'add_edit_consult_record.html', {'form': form,'edit_obj':edit_obj})


def logout_s(request):
    logout(request)
    return redirect('/login/')