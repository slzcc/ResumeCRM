from django.db import models
from django.contrib.auth.models import User, Permission, Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import force_text, python_2_unicode_compatible
# 定义时区
import pytz
# pytz.country_timezones('cn')
tz = pytz.timezone('Asia/Shanghai')
import uuid


# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # password = models.CharField(_('password'), max_length=128, help_text=mark_safe("""<a class='btn-link' href='password'>重设</a>"""))

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=64, verbose_name="姓名")
    head_portrait = models.CharField(max_length=64, verbose_name="头像", default="profile-photos/system/1.png")
    # role = models.ManyToManyField("Role", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=64, verbose_name="联系电话", blank=True, null=True)
    location = models.CharField(max_length=64, verbose_name="国家", default="CN", blank=True, null=True)

    describe = models.TextField('备注', blank=True, null=True, default=None)

    # is_admin = models.BooleanField(default=False) # 是否 admin

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class WorkPlace(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="工作地点")

    def __str__(self):
        return self.name

class Company(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="公司名称")
    level = models.CharField(max_length=32, verbose_name="公司级别")
    def __str__(self):
        return self.name

class Department(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="部门名称")
    head = models.CharField(max_length=32, verbose_name="部门负责人")
    mail = models.EmailField(verbose_name="邮件地址")
    phone = models.SmallIntegerField(verbose_name="联系电话")
    company = models.ForeignKey("Company", verbose_name="所属公司", related_name='c', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Menu(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    url_type = models.SmallIntegerField(choices=url_type_choices, default=1)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.url_name

    class Meta:
        unique_together = ('name','url_name')

class Project(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="项目名称")
    department = models.ForeignKey("Department", verbose_name="所属部门", related_name='d', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PositionInfo(models.Model):

    jobLevel_type_choices = (
        (1, '低'),
        (2, '中'),
        (3, '高'),
    )

    jobState_type_choices = (
        (1, '不紧急'),
        (2, '正常'),
        (3, '紧急'),
    )

    degree_type_choices = (
        (1, '专科'),
        (2, '本科'),
        (3, '研究生'),
        (4, '硕士'),
        (5, '博士以上'),
        (6, '不限'),
    )

    personnel_costs_choices = (
        (1, 'A1'),
        (2, 'B1'),
        (3, 'C1'),
    )

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    personnel_type = models.BooleanField(default=True, verbose_name="正式人员")
    onsite = models.BooleanField(default=False, verbose_name="Onsite")
    on_business_trip = models.BooleanField(default=False, verbose_name="出差")
    equipped_computer = models.BooleanField(default=True, verbose_name="配备电脑")

    create_at = models.DateField(verbose_name="需求提交日期", null=True)
    apply_information = models.CharField(max_length=16, verbose_name="应聘原因")
    jobs = models.CharField(max_length=32, verbose_name="岗位名称")
    personnel_attr = models.CharField(max_length=32, verbose_name="人员属性", null=True, blank=True)
    work_time = models.CharField(max_length=32, verbose_name="工作年限")
    position_requirements = models.CharField(max_length=128, verbose_name="岗位需求信息", null=True, blank=True)
    search_key = models.CharField(max_length=32, verbose_name="岗位关键字", null=True, blank=True)
    jobs_highlight = models.CharField(max_length=32, verbose_name="岗位亮点", null=True, blank=True)
    project_size = models.CharField(max_length=32, verbose_name="岗位规模", null=True, blank=True)
    referral_bonus = models.CharField(max_length=32, verbose_name="推荐奖金", null=True, blank=True)
    customers = models.CharField(max_length=16, verbose_name="客户介绍", null=True, blank=True)
    describe = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注")
    salary = models.CharField(max_length=32, verbose_name="薪资范围")

    number = models.SmallIntegerField(verbose_name="需求人数")
    personnel_costs = models.SmallIntegerField(choices=personnel_costs_choices, default=3, verbose_name="人员成本类型")
    degree = models.SmallIntegerField(choices=degree_type_choices, default=1, verbose_name="学历要求")
    joblevel = models.SmallIntegerField(choices=jobLevel_type_choices, default=1, verbose_name="岗位级别")
    state = models.SmallIntegerField(choices=jobState_type_choices, default=2, verbose_name="紧急程度")

    customer_name = models.ForeignKey("Company", related_name="cn", verbose_name="客户名称", on_delete=models.CASCADE)
    customer_level = models.ForeignKey("Company", related_name="cl", verbose_name="客户级别", on_delete=models.CASCADE)
    work_place = models.ForeignKey("WorkPlace", related_name="wp", verbose_name="工作地点", on_delete=models.CASCADE)
    department_demand = models.ForeignKey("Department", related_name="dd", verbose_name="需求部门", on_delete=models.CASCADE)
    department_head = models.ForeignKey("Department", related_name="dh", verbose_name="部门负责人", on_delete=models.CASCADE)
    customer_id = models.ForeignKey("Company", related_name="cid", verbose_name="客户编号", on_delete=models.CASCADE)
    projects_name = models.ForeignKey("Project", related_name="pname", verbose_name="项目名称", on_delete=models.CASCADE)
    projects_id = models.ForeignKey("Project", related_name="pid", verbose_name="项目编号", on_delete=models.CASCADE)

    candidate = models.ManyToManyField("ResumeInfo", related_name="cc", verbose_name="候选人")

    def __str__(self):
        return self.jobs

class ResumeInfo(models.Model):

    resume_status_choices = (
        (0, '已面试'),
        (1, '已复试'),
        (2, '已录用'),
        (3, '未联系'),
    )
    id = models.BigAutoField(primary_key=True)

    age = models.SmallIntegerField(verbose_name="年龄", null=True, blank=True)
    phone = models.CharField(max_length=32, verbose_name="手机号", null=True, blank=True)
    qq = models.CharField(max_length=32, verbose_name="QQ 号", null=True, blank=True)

    birthday = models.DateField(verbose_name="出生日期", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="上传时间", null=True, blank=True)
    cnterview_time = models.DateTimeField(verbose_name="约谈时间", null=True, blank=True)
    modify_time = models.DateTimeField(verbose_name="修改时间", null=True, blank=True)

    email = models.EmailField(verbose_name="电子邮箱", null=True, blank=True)

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    nation = models.CharField(max_length=8, verbose_name="民族", null=True, blank=True)
    track_progress = models.CharField(max_length=32, verbose_name="跟踪进度", null=True, blank=True)
    work_place = models.CharField(max_length=32, verbose_name="期望工作地", null=True, blank=True)
    username = models.CharField(max_length=32, verbose_name="姓名")
    work_time = models.CharField(max_length=32, verbose_name="工作年限", null=True, blank=True)
    place_residence = models.CharField(max_length=32, verbose_name="居住地", null=True, blank=True)
    origin = models.CharField(max_length=32, verbose_name="籍贯", null=True, blank=True)
    jobs = models.CharField(max_length=32, verbose_name="应聘岗位", null=True, blank=True)
    salary = models.CharField(max_length=32, verbose_name="薪酬", null=True, blank=True)
    english_level = models.CharField(max_length=32, verbose_name="英语水平", null=True, blank=True)
    degree = models.CharField(max_length=32, verbose_name="学历", null=True, blank=True)
    graduated_school = models.CharField(max_length=32, verbose_name="毕业学校", null=True, blank=True)
    professional = models.CharField(max_length=32, verbose_name="所学专业", null=True, blank=True)
    learning_type = models.CharField(max_length=32, verbose_name="在校形式", null=True, blank=True)
    duty_time = models.CharField(max_length=32, verbose_name="到岗时间", null=True, blank=True)
    job_addr = models.CharField(max_length=32, verbose_name="求职地点", null=True, blank=True)
    high = models.CharField(max_length=32, verbose_name="身高", null=True, blank=True)
    old_company = models.CharField(max_length=32, verbose_name="上家公司名称", null=True, blank=True)
    old_jobs = models.CharField(max_length=32, verbose_name="上家职位名称", null=True, blank=True)
    language = models.CharField(max_length=32, verbose_name="语言", null=True, blank=True)

    gender = models.BooleanField(default=True, verbose_name="性别")
    current_situation = models.BooleanField(default=True, verbose_name="是否离职")
    nature_work = models.BooleanField(default=True, verbose_name="是否全职")
    marital_status = models.BooleanField(default=False, verbose_name="已婚")

    resume_status = models.SmallIntegerField(choices=resume_status_choices, default=3, verbose_name="状态")

    # resume_id = models.BigAutoField(verbose_name="简历ID", default="0000001", blank=True)
    resume_associated = models.ForeignKey('self', verbose_name="关联 ID", null=True, blank=True, on_delete=models.CASCADE)

    zh_filename = models.ManyToManyField("ResumeName", related_name="fne", verbose_name="中文简历", blank=True)
    en_filename = models.ManyToManyField("ResumeName", related_name="efne", verbose_name="英文简历", blank=True)
    resume_source = models.ManyToManyField("ResumeSource", related_name="rse", verbose_name="简历来源", blank=True)

    # zh_filename = models.ForeignKey("ResumeName", related_name="fne", verbose_name="中文简历", null=True, blank=True, on_delete=models.CASCADE)
    # en_filename = models.ForeignKey("ResumeName", related_name="efne", verbose_name="英文简历", null=True, blank=True, on_delete=models.CASCADE)
    # resume_source = models.ForeignKey("ResumeSource", related_name="rse", verbose_name="简历来源", null=True, blank=True, on_delete=models.CASCADE)

    custom_label = models.ManyToManyField("CustomLabel", related_name="cll", verbose_name="标签", blank=True)
    upload_user = models.ManyToManyField("UserProfile", related_name="uu", verbose_name="上传人员", blank=True)
    agent = models.ManyToManyField("UserProfile", related_name="at", verbose_name="经办人", blank=True)
    workflow = models.ManyToManyField("ResumeWorkFlow", related_name="wf", verbose_name="流程状态", blank=True)
    status = models.ManyToManyField("ResumeStatus", related_name="sts", verbose_name="状态", blank=True)
    search_key = models.ManyToManyField("Keyword", related_name="sk", verbose_name="关键字", blank=True)
    personal_assessment = models.ManyToManyField("PersonalAssessment", related_name="pa", verbose_name="个人评价", blank=True)
    education_info = models.ManyToManyField("EducationInfo", related_name="ei", verbose_name="教育简历", blank=True)
    project_info = models.ManyToManyField("ProjectInfo", related_name="pi", verbose_name="项目简历", blank=True)
    work_info = models.ManyToManyField("WorkInfo", related_name="wi", verbose_name="工作简历", blank=True)
    user_comments = models.ManyToManyField("Comment", related_name="cts", verbose_name="评论", blank=True)
    raw_text = models.ManyToManyField("ResumeSourceText", related_name="rt", verbose_name="原文", blank=True)
    comprehensive_ability = models.ManyToManyField("ComprehensiveAbility", related_name="ceay", verbose_name="综合能力", blank=True)

    def __str__(self):
        return self.username

class ComprehensiveAbility(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="综合能力", null=True, blank=True)

    def __str__(self):
        return self.describe

class Comment(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="评论", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, default=timezone.now)
    user = models.ForeignKey("UserProfile", related_name="cuu", verbose_name="创建人员", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.describe


class ProjectInfo(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="项目简历")
    level = models.CharField(max_length=16, verbose_name="级别", null=True, blank=True)

    def __str__(self):
        return self.describe

class EducationInfo(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="教育简历", null=True, blank=True)
    level = models.CharField(max_length=16, verbose_name="级别", null=True, blank=True)

    def __str__(self):
        return self.describe

class WorkInfo(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="工作简历", null=True, blank=True)
    level = models.CharField(max_length=16, verbose_name="级别", null=True, blank=True)

    def __str__(self):
        return self.describe

class PersonalAssessment(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="个人介绍", null=True, blank=True)
    level = models.CharField(max_length=16, verbose_name="级别", null=True, blank=True)

    def __str__(self):
        return self.describe

class Keyword(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.CharField(max_length=256, verbose_name="关键字", null=True, blank=True)
    level = models.SmallIntegerField(verbose_name="级别", null=True, blank=True)

    def __str__(self):
        return self.describe


class ResumeSourceText(models.Model):

    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(max_length=128, verbose_name="识别码")
    describe = models.TextField(verbose_name="简历原文", null=True, blank=True)

    def __str__(self):
        return self.describe

class ResumeWorkFlow(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    status = models.TextField(verbose_name="简历工作流", null=True, blank=True)

    def __str__(self):
        return self.status

class ResumeStatus(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    status = models.TextField(verbose_name="简历状态", null=True, blank=True)

    def __str__(self):
        return self.status

class CustomLabel(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="标签", null=True, blank=True)

    def __str__(self):
        return self.name

class ResumeName(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=128, verbose_name="简历名称", null=True, blank=True)
    source = models.ForeignKey("ResumeSource", verbose_name="简历来源", blank=True, null=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="上传时间", null=True, blank=True, default=timezone.now)
    download_num = models.SmallIntegerField(verbose_name="下载次数", null=True, blank=True)

    def __str__(self):
        return self.name

class ResumeSource(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="简历来源", unique=True)

    def __str__(self):
        return self.name

class SystemPermission(models.Model):

    permission_type_chioces = (
        (1, 'GET'), 
        (2, 'POST'),
        (3, '*'),
    )

    permissions = models.ForeignKey(Permission, blank=True, related_name="cgp", verbose_name=_('permissions'), null=True, on_delete=models.CASCADE, unique=True)
    # url = models.CharField('URL名称', max_length=255, blank=True, null=True, unique=True)
    url = models.ForeignKey(Menu, blank=True, related_name="murl", verbose_name=_('meuns'), null=True, on_delete=models.CASCADE)

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    per_method = models.SmallIntegerField('请求方法', choices=permission_type_chioces, default=1)
    argument_list = models.TextField('参数列表', help_text='JSON 格式数据，多个参数之间用英文半角逗号隔开, ex: {"_page": "", "_so": ""..}', blank=True, null=True, default="*")
    describe = models.CharField('描述', max_length=255, blank=True, null=True)
    name = models.CharField('权限名称', max_length=255, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = '权限表'
    #     verbose_name_plural = verbose_name
        # permissions = (
        #     ('repository_resume_table_list', '可以访问 Resume 首页所有数据'),
        #     ('repository_resume_table_user_info', '可以访问 Resume 每个候选人的详细信息'),
        #     ('repository_resume_table_user_info_change', '可以访问 Resume 每个候选人的信息信息进行修改'),
        #     ('repository_resume_table_user_info_update', '可以上传 Resume 简历并解析'),
        #     ('repository_resume_table_user_info_search', '可以搜索 Resume 候选人数据'),
        # )

class Email(models.Model):

    name = models.CharField(max_length=32, verbose_name="名称", null=True, blank=True, unique=True)
    form_address = models.EmailField(verbose_name="发件人地址", null=True, blank=True)
    form_name = models.CharField(max_length=32, verbose_name="发件人名称", null=True, blank=True)

    smtp_server = models.CharField(max_length=32, verbose_name="SMTP 服务器地址", null=True, blank=True)
    smtp_port = models.CharField(max_length=5, verbose_name="SMTP 服务器端口", null=True, blank=True)
    smtp_username = models.CharField(max_length=32, verbose_name="用户名", null=True, blank=True)
    smtp_password = models.CharField(max_length=32, verbose_name="密码", null=True, blank=True)
    smtp_ssl = models.BooleanField(default=True, verbose_name="开启 SSL")
    uuid = models.CharField(max_length=128, verbose_name="识别码")

    def __str__(self):
        return self.name


class ResumeTemplate(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="名称", null=True, blank=True, unique=True)
    url = models.CharField(max_length=255, verbose_name="地址", null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.name

class SystemSetting(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="名称", null=True, blank=True, unique=True)
    string_value = models.CharField(max_length=128, verbose_name="字符串值", null=True, blank=True, unique=True)
    num_value = models.IntegerField(verbose_name="数字值", null=True, blank=True, unique=True)
    bool_value = models.BooleanField(default=True, verbose_name="布尔值")
    describe = models.TextField(verbose_name="描述", null=True, blank=True)
    
    def __str__(self):
        return self.name

class PreferreResumeTemplate(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="名称", null=True, blank=True, unique=True)
    resume_template = models.ForeignKey("ResumeTemplate", related_name="prt", verbose_name="简历模板", blank=True, on_delete=models.CASCADE, null=True, unique=True)
    
    def __str__(self):
        return self.name

class PreferreEmail(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(max_length=32, verbose_name="名称", null=True, blank=True, unique=True)
    email_server = models.ForeignKey("Email", related_name="pfe", verbose_name="SMTP服务", blank=True, on_delete=models.CASCADE, null=True, unique=True)
    
    def __str__(self):
        return self.name

class StatisticalDownloadResume(models.Model):

    download_resume_type_choices = (
        (0, '原件'),
        (1, 'PDF'),
        (2, '模板'),
    )

    resume = models.ForeignKey("ResumeInfo", related_name="sdrr", verbose_name="简历信息", blank=True, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(verbose_name="下载次数", default=1)
    download_time = models.DateTimeField(verbose_name="下载时间", null=True, blank=True, default=timezone.now)
    user = models.ForeignKey("UserProfile", related_name="sdru", verbose_name="下载人员", blank=True, on_delete=models.CASCADE, null=True)
    download_type = models.SmallIntegerField(choices=download_resume_type_choices, default=0, verbose_name="下载类型")

    objects = ResumeInfo()
    
    def __str__(self):
        return force_text(self.resume)

class StoredEventType(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    name = models.CharField(
        max_length=64, unique=True, verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

class EventLog(models.Model):

    envent_status_choices = (
        (0, '失联'),
        (1, '成功'),
        (2, '失败'),
        (3, '警告'),
        (4, '进行'),
        (5, '暂停'),
    )

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    label = models.CharField(max_length=64, verbose_name="标签")
    trigger_time = models.DateTimeField(verbose_name="时间", null=True, blank=True, default=timezone.now)
    request = models.TextField(verbose_name="请求对象", null=True, blank=True)
    response = models.TextField(verbose_name="响应对象", null=True, blank=True)
    event_type = models.ForeignKey("StoredEventType", related_name="elet", verbose_name="事件类型", blank=True, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("UserProfile", related_name="eluser", verbose_name="Role", blank=True, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(choices=envent_status_choices, default=1, verbose_name="状态")
    describe = models.TextField(verbose_name="描述", null=True, blank=True)
    access = models.CharField(max_length=84, verbose_name="访问信息", null=True, blank=True)
    source_object = models.CharField(max_length=128, verbose_name="源对象", null=True, blank=True)
    target_object = models.CharField(max_length=128, verbose_name="目标对象", null=True, blank=True)

    def __str__(self):
        return self.uuid

class ResumeSubscription(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    number = models.IntegerField(verbose_name="数量", default=1)
    trigger_time = models.DateTimeField(verbose_name="收藏时间", auto_now=True)
    status = models.BooleanField(default=True, verbose_name="收藏状态")
    user = models.ForeignKey("UserProfile", related_name="rspuser", verbose_name="收藏人员", on_delete=models.CASCADE)
    resume = models.ForeignKey("ResumeInfo", related_name="rspresume", verbose_name="简历", on_delete=models.CASCADE)
    

    objects = ResumeInfo()
    
    def __str__(self):
        return force_text(self.resume)

class Notification(models.Model):

    uuid = models.CharField(max_length=128, verbose_name="识别码")
    title = models.CharField(max_length=128, verbose_name="标题", null=True, blank=True)
    to_user = models.ForeignKey("UserProfile", related_name="nftouser", verbose_name="通知人员", on_delete=models.CASCADE, null=True, blank=True)
    from_user = models.ForeignKey("UserProfile", related_name="nffromuser", verbose_name="发送人员", on_delete=models.CASCADE, null=True, blank=True)
    trigger_time = models.DateTimeField(verbose_name="时间", null=True, blank=True, default=timezone.now)
    describe = models.TextField(verbose_name="描述", null=True, blank=True)
    read = models.BooleanField(default=False, verbose_name=_('Read'))

    def __str__(self):
        return self.uuid