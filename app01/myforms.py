from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from app01 import models

class RegForms(forms.Form):
    username = forms.CharField(min_length=3, max_length=8, label='用户名',
                               error_messages={'min_length': '太短了', 'max_length': '太长了',
                                               'required': '该字段必填'},
                               widget=widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=3, max_length=8, label='密码',
                               error_messages={'min_length': '太短了', 'max_length': '太长了',
                                               'required': '该字段必填'},
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    employer = forms.CharField(min_length=3, max_length=8, label='员工姓名',
                               error_messages={'min_length': '太短了', 'max_length': '太长了',
                                               'required': '该字段必填'},
                               widget=widgets.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        name = self.cleaned_data.get('username')
        user = models.UserInfo.objects.filter(username=name).first()
        if user:
            raise ValidationError('该用户名已经被注册')
        else:
            return name


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({'class':'form-control'})

