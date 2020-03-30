from django.contrib import admin
from app01 import models
# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.School)
admin.site.register(models.Department)
admin.site.register(models.ConsultRecord)