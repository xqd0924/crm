from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe

# Create your models here.
class UserInfo(AbstractUser):
    """
    员工表
    """

    employer = models.CharField(verbose_name='员工姓名', max_length=16)
    depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="code", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.employer

class Department(models.Model):
    """
    部门表
    市场部     1000
    销售       1001

    """
    title = models.CharField(verbose_name='部门名称', max_length=16)
    code = models.IntegerField(verbose_name='部门编号', unique=True, null=False)

    def __str__(self):
        return self.title

course_choices = (('LinuxL','linux中高级'),
                  ('PythonFullStack','python全栈开发'))

class Course(models.Model):
    """
    课程表
    如：
        Linux基础
        Linux架构师
        Python自动化开发精英班
        Python自动化开发架构师班
        Python基础班
		go基础班
    """
    name = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.name


class School(models.Model):
    """
    校区表
    如：
        北京沙河校区
        上海校区

    """
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class ClassList(models.Model):
    """
    班级表
    如：
        Python全栈  面授班  5期  10000  2017-11-11  2018-5-11
    """
    school = models.ForeignKey(verbose_name='校区', to='School')
    # course = models.ForeignKey(verbose_name='课程名称', to='Course')
    course = models.CharField('课程名称',choices=course_choices,max_length=32)
    semester = models.IntegerField(verbose_name="班级(期)")
    price = models.IntegerField(verbose_name="学费")
    start_date = models.DateField(verbose_name="开班日期")
    graduate_date = models.DateField(verbose_name="结业日期", null=True, blank=True)
    memo = models.CharField(verbose_name='说明', max_length=256, blank=True, null=True, )
    # teachers = models.ManyToManyField(verbose_name='任课老师', to='UserInfo',limit_choices_to={'depart_id__in':[1003,1004],})
    teachers = models.ManyToManyField(verbose_name='任课老师', to='UserInfo',related_name="abc",limit_choices_to={"depart__in":[1002,1005]})
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes',limit_choices_to={"depart":1001})

    class Meta:
        unique_together = ("school","course","semester")

    def __str__(self):
        return "{0}({1}期)".format(self.course, self.semester)


class Customer(models.Model):
    """
    客户表
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')

    name = models.CharField(verbose_name='学生姓名', max_length=16)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    education_choices = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办专科'),
        (7, '高中'),
        (8, '其他')
    )
    education = models.IntegerField(verbose_name='学历', choices=education_choices, blank=True, null=True, )
    graduation_school = models.CharField(verbose_name='毕业学校', max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name='所学专业', max_length=64, blank=True, null=True)

    experience_choices = [
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    ]
    experience = models.IntegerField(verbose_name='工作经验', blank=True, null=True, choices=experience_choices)
    work_status_choices = [
        (1, '在职'),
        (2, '无业')
    ]
    work_status = models.IntegerField(verbose_name="职业状态", choices=work_status_choices, default=1, blank=True,
                                      null=True)
    company = models.CharField(verbose_name="目前就职公司", max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name="当前薪资", max_length=64, blank=True, null=True)

    source_choices = [
        (1, "qq群"),
        (2, "内部转介绍"),
        (3, "官方网站"),
        (4, "百度推广"),
        (5, "360推广"),
        (6, "搜狗推广"),
        (7, "腾讯课堂"),
        (8, "广点通"),
        (9, "高校宣讲"),
        (10, "渠道代理"),
        (11, "51cto"),
        (12, "智汇推"),
        (13, "网盟"),
        (14, "DSP"),
        (15, "SEO"),
        (16, "其它"),
    ]
    source = models.SmallIntegerField('客户来源', choices=source_choices, default=1)
    referral_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="转介绍自学员",
        help_text="若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
        related_name="internal_referral"
    )
    # course = models.ManyToManyField(verbose_name="咨询课程", to="Course")

    status_choices = [
        (1, "已报名"),
        (2, "未报名")
    ]
    status = models.IntegerField(
        verbose_name="状态",
        choices=status_choices,
        default=2,
        help_text=u"选择客户此时的状态"
    )

    consultant = models.ForeignKey(verbose_name="课程顾问", to='UserInfo', related_name='consultanter',
                                   limit_choices_to={'depart_id': 1001},null=True,blank=True)
    course = MultiSelectField('咨询课程',choices=course_choices,null=True,blank=True)
    date = models.DateField(verbose_name="咨询日期", auto_now_add=True)
    recv_date = models.DateField(verbose_name="当前课程顾问的接单日期", null=True, blank=True)
    last_consult_date = models.DateField(verbose_name="最后跟进日期", null=True,blank=True)
    class_list = models.ManyToManyField('ClassList',verbose_name='已报班级',blank=True)

    def __str__(self):
        return self.name
    def get_classlist(self):
        l=[]
        for cls in self.class_list.all():
            l.append(str(cls))
        return mark_safe('<br>'.join(l))
    def get_status(self):
        status_color={
            1:'green',
            2:'orange'
        }
        return mark_safe("<span style='background-color:%s;color:white'>%s</span>"%(status_color[self.status],self.get_status_display()))

class ConsultRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name="所咨询客户", to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="跟踪人", to='UserInfo', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="跟进日期", auto_now_add=True)
    note = models.TextField(verbose_name="跟进内容...")
    delete_status = models.BooleanField(verbose_name="删除状态", default=False)

    def __str__(self):
        return self.customer.name + ":" + str(self.consultant)


class Student(models.Model):
    """
    学生表（已报名）
    """
    customer = models.OneToOneField(verbose_name='客户信息', to='Customer')

    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    emergency_contract = models.CharField(max_length=32, blank=True, null=True, verbose_name='紧急联系人')

    class_list = models.ManyToManyField(verbose_name="已报班级", to='ClassList', blank=True)
    company = models.CharField(verbose_name='公司', max_length=128, blank=True, null=True)
    location = models.CharField(max_length=64, verbose_name='所在区域', blank=True, null=True)
    position = models.CharField(verbose_name='岗位', max_length=64, blank=True, null=True)
    salary = models.IntegerField(verbose_name='薪资', blank=True, null=True)
    welfare = models.CharField(verbose_name='福利', max_length=256, blank=True, null=True)
    date = models.DateField(verbose_name='入职时间', help_text='格式yyyy-mm-dd', blank=True, null=True)
    memo = models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.username


class CourseRecord(models.Model):
    """
    上课记录表 （班级记录）
    """
    class_obj = models.ForeignKey(verbose_name="班级", to="ClassList")
    day_num = models.IntegerField(verbose_name="节次", help_text=u"此处填写第几节课或第几天课程...,必须为数字")
    teacher = models.ForeignKey(verbose_name="讲师", to='UserInfo',limit_choices_to={"depart_id__in":[1002,1003]})
    date = models.DateField(verbose_name="上课日期", auto_now_add=True)

    course_title = models.CharField(verbose_name='本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(verbose_name='本节课程内容概要', blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField(verbose_name='本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(verbose_name='作业描述', max_length=500, blank=True, null=True)
    exam = models.TextField(verbose_name='踩分点', max_length=300, blank=True, null=True)

    def __str__(self):
        return "{0} day{1}".format(self.class_obj, self.day_num)


class StudyRecord(models.Model):
    '''
    学生记录
    '''
    course_record = models.ForeignKey(verbose_name="第几天课程", to="CourseRecord")
    student = models.ForeignKey(verbose_name="学员", to='Student')
    record_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('noshow', "缺勤"),
                      ('leave_early', "早退"),
                      )
    record = models.CharField("上课纪录", choices=record_choices, default="checked", max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, ' D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(verbose_name='作业评语', max_length=255, blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    stu_memo = models.TextField(verbose_name='学员备注', blank=True, null=True)
    date = models.DateTimeField(verbose_name='提交作业日期', auto_now_add=True)

    def __str__(self):
        return "{0}-{1}".format(self.course_record, self.student)

class Enrollment(models.Model):
    """
    报名表
    """
    customer=models.ForeignKey('Customer',verbose_name='客户名称',on_delete=models.CASCADE)
    why_us=models.TextField('为什么报名',max_length=1024,default=None,blank=True,null=True)
    your_expectation=models.TextField('期望值',max_length=1024,blank=True,null=True)
    enrolled_date=models.DateTimeField(auto_now_add=True,verbose_name='报名日期')
    memo=models.TextField('备注',blank=True,null=True)
    delete_status = models.BooleanField(verbose_name="删除状态", default=False)
    enrollment_class=models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)

    class Meta:
        unique_together=('enrollment_class','customer')

pay_type_choices=(('deposit',"订金/报名费"),
                  ('tuition',"学费"),
                  ('transfer',"转班"),
                  ('dropout',"退学"),
                  ('refund',"退款"),)

class_type_choice=((1,"脱产班"),(2,"网络班"),(3,"周末班"),)

class PaymentRecord(models.Model):
    """
    缴费记录表
    """
    customer=models.ForeignKey('Customer',verbose_name='客户',on_delete=models.CASCADE)
    pay_type=models.CharField("费用类型",choices=pay_type_choices,max_length=64,default='deposit')
    paid_fee=models.IntegerField("费用数额",default=0)
    note = models.TextField('备注', blank=True, null=True)
    date=models.DateTimeField("交款日期",auto_now_add=True)
    course=models.CharField("课程名",choices=course_choices,max_length=64,blank=True,null=True)
    class_type=models.CharField("班级类型",choices=class_type_choice,max_length=64,blank=True,default='N/A')
    enrolment_class=models.ForeignKey('ClassList',verbose_name="所报班级",blank=True,null=True, on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name="销售", to='UserInfo', on_delete=models.CASCADE)
    delete_status = models.BooleanField(verbose_name="删除状态", default=False)

    status_choices=((1,'未审核'),(2,'已审核'),)
    status=models.IntegerField(verbose_name='审核',default=1,choices=status_choices)
    confirm_date=models.DateTimeField(verbose_name="确认日期",null=True,blank=True)
    confirm_user=models.ForeignKey(verbose_name="确认人",to='UserInfo',related_name='confirms',blank=True,null=True,
                                   on_delete=models.CASCADE)