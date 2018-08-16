from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()

def getResumeInfoChoicesValue(value):
	Resume_status_choices = models.ResumeInfo._meta.get_field("resume_status")
	for item in Resume_status_choices.choices:
		if item[0] == value:
			return item[1]

@register.simple_tag
def SetIUploadTable(data):
	_view_list = ["邮箱", "电话", "上传时间", "申请岗位", "简历状态"]
	view_list = ["username", "email", "phone", "create_time", "jobs", "resume_status", "id"]
	obj = data.values(*view_list)
	ele = ''
	ele += '<thead><tr>'
	ele += '<th class="id="tech-companies-1-col-0"">{}</th>'.format("姓名")
	for index, item in enumerate(_view_list, 1):
		ele += '<th data-priority="{}">{}</th>'.format(index, item)
	ele += '</tr>'
	ele += '<tbody>'
	for item in obj:
		ele += '<tr>'
		ele += '<th><a href="/resume/candidate/{}/change" target="_blank">{}</a></th>'.format(item["id"],item["username"])
		ele += '<td>{}</td>'.format(item["email"])
		ele += '<td>{}</td>'.format(item["phone"])
		ele += '<td>{}</td>'.format((item["create_time"] + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'))
		ele += '<td>{}</td>'.format(item["jobs"])
		ele += '<td>{}</td>'.format(getResumeInfoChoicesValue(item["resume_status"]))
		ele += '</tr>'
	ele += '</tbody>'
	return mark_safe(ele)