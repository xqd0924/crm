# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-03-14 21:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20200313_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='为什么报名')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='期望值')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='报名日期')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户名称')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.CharField(choices=[('deposit', '订金/报名费'), ('tuition', '学费'), ('transfer', '转班'), ('dropout', '退学'), ('refund', '退款')], default='deposit', max_length=64, verbose_name='费用类型')),
                ('paid_fee', models.IntegerField(default=0, verbose_name='费用数额')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='交款日期')),
                ('course', models.CharField(blank=True, choices=[('LinuxL', 'linux中高级'), ('PythonFullStack', 'python全栈开发')], max_length=64, null=True, verbose_name='课程名')),
                ('class_type', models.CharField(blank=True, choices=[(1, '脱产班'), (2, '网络班'), (3, '周末班')], default='N/A', max_length=64, verbose_name='班级类型')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('status', models.IntegerField(choices=[(1, '未审核'), (2, '已审核')], default=1, verbose_name='审核')),
                ('confirm_date', models.DateTimeField(blank=True, null=True, verbose_name='确认日期')),
                ('confirm_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirms', to=settings.AUTH_USER_MODEL, verbose_name='确认人')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='销售')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('school', 'course', 'semester')]),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrolment_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='所报班级'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrollment_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='所报班级'),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('enrollment_class', 'customer')]),
        ),
    ]
