from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()


def getDownloadTypeChoicesValue(value):
	download_type_choices = models.StatisticalDownloadResume._meta.get_field("download_type")
	for item in download_type_choices.choices:
		if item[0] == value:
			return item[1]

def getResumeInfoChoicesValue(value):
	Resume_status_choices = models.ResumeInfo._meta.get_field("resume_status")
	for item in Resume_status_choices.choices:
		if item[0] == value:
			return item[1]

@register.simple_tag
def SetISubscribeTable(data):


	_view_list = ["邮箱", "电话", "收藏时间", "申请岗位", "简历状态"]
	view_list = ["username", "email", "phone", "trigger_time", "jobs", "resume_status", "id"]
	obj = data.values()
	ele = ''
	ele += '<thead><tr>'
	ele += '<th class="id="tech-companies-1-col-0"">{}</th>'.format("姓名")
	for index, item in enumerate(_view_list, 1):
		ele += '<th data-priority="{}">{}</th>'.format(index, item)
	ele += '</tr>'
	ele += '<tbody>'
	for item in obj:
		sub_obj = models.ResumeInfo.objects.get(id=item["resume_id"])
		ele += '<tr>'
		ele += '<th><a href="/resume/candidate/{}/change" target="_blank">{}</a></th>'.format(item["resume_id"],sub_obj.username)
		ele += '<td>{}</td>'.format(sub_obj.email)
		ele += '<td>{}</td>'.format(sub_obj.phone)
		ele += '<td>{}</td>'.format(item["trigger_time"].strftime('%y/%m/%d %H:%M'))
		ele += '<td>{}</td>'.format(sub_obj.jobs)
		ele += '<td>{}</td>'.format(getResumeInfoChoicesValue(sub_obj.resume_status))
		ele += '</tr>'
	ele += '</tbody>'
	return mark_safe(ele)