from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()


def getStatusTypeChoicesValue(value):

	style_list = ["pink", "success", "danger", "warning", "info", "purple"]
	download_type_choices = models.EventLog._meta.get_field("status")
	for index, item in enumerate(download_type_choices.choices):
		if item[0] == value:
			return style_list[index], item[1]

def getResumeInfoChoicesValue(value):
	Resume_status_choices = models.ResumeInfo._meta.get_field("resume_status")
	for item in Resume_status_choices.choices:
		if item[0] == value:
			return item[1]

@register.simple_tag
def SetAudutTable(data):

	
	_view_list = ["触发时间", "操作用户", "事件类型", "状态", "描述", "访问地址", "源" ,"目标"]
	obj = data.values()
	ele = ''
	ele += '<thead><tr>'
	ele += '<th class="id="tech-companies-1-col-0"">{}</th>'.format("对象")
	for index, item in enumerate(_view_list, 1):
		ele += '<th data-priority="{}">{}</th>'.format(index, item)
	# ele += '<th data-priority="">{}</th>'.format("")
	ele += '</tr>'
	ele += '<tbody>'
	for item in obj:
		user_obj = models.UserProfile.objects.get(id=item["user_id"])
		event_type_obj =  models.StoredEventType.objects.get(id=item["event_type_id"])
		ele += '<tr>'
		ele += '<th><a href="" target="_blank">{}</a></th>'.format(item["uuid"])
		ele += '<td>{}</td>'.format((item["trigger_time"] + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'))
		ele += '<td><small class="text-{}"><b>{}</b></small></td>'.format("warning" if user_obj.name != "System" else "success", user_obj.name)
		ele += '<td><code>{}</code></td>'.format(event_type_obj.name + "." + item["label"])
		status_index, status_value = getStatusTypeChoicesValue(item["status"])
		ele += '<td><span class="badge badge-{}">{}</span></td>'.format(status_index, status_value)
		ele += '<td data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{}">{}</td>'.format(item["describe"], item["describe"][0:32]+" ...")
		ele += '<td><code>{}</code></td>'.format(item["access"])
		ele += '<td><code>{}</code></td>'.format(item["source_object"])
		ele += '<td><code>{}</code></td>'.format(item["target_object"])
		ele += '</tr>'
	ele += '</tbody>'
	return mark_safe(ele)

