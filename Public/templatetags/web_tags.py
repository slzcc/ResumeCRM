from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from django.contrib.auth.models import Group
from repository import models

register = Library()

@register.simple_tag
def SetSelectd(obj_id):
	DisplayField = "email"

	Data = {}
	ele = ''

	Data["SelectUser"] = []
	GroupOfUserList = list(Group.objects.get(id=obj_id).user_set.all().values(DisplayField))
	for i in GroupOfUserList:
		Data["SelectUser"].append(i[DisplayField])

	Data["UserList"] = []
	AllUserList = list(models.UserProfile.objects.all().values("id", DisplayField))
	for i in AllUserList:
		if not i[DisplayField] == "system@resumecrm.com":
			Data["UserList"].append(i[DisplayField])

	for i in AllUserList:
		if not i[DisplayField] == "system@resumecrm.com":
			if i[DisplayField] in Data["SelectUser"]:
				ele += '<option selected value="{}">{}</option>'.format(i["id"],i[DisplayField])
			else:
				ele += '<option value="{}">{}</option>'.format(i["id"],i[DisplayField])
			
	return mark_safe(ele)

@register.simple_tag
def SetGroupUserCount(data):
	ele = ''
	for k,v in data.items():
		ele += """<tr>"""
		ele += """<td><input row-select="true" type="checkbox" value="{}"></td>""".format(v["id"])
		ele += """<td><a href="{}/change">{}</a></td><td>{}</td>""".format(v["id"],k,v["count"])
		ele += """</tr>""" 
		
	return mark_safe(ele)

@register.simple_tag
def SetResumeSourceTbody(data):
	ele = ''
	for item in data:
		ResumeSource_Resume_Counts = models.ResumeInfo.objects.filter(resume_source__name=item["name"]).count()
		ele += """<tr>"""
		ele += """<td><input row-select="true" type="checkbox" value="{}"></td>""".format(item["id"])
		ele += """<td><a href="{}/change">{}</a></td><td>{}</td>""".format(item["id"],item["name"],ResumeSource_Resume_Counts)
		ele += """</tr>""" 
	return mark_safe(ele)

@register.simple_tag
def SetSystemUserTbody(data):
	ele = ''
	SourceData = {}

	style_list= ["pink", "purple", "primary", "success", "info"]
	for item in data:
		if item["name"] == "system":
			pass
		elif not item["email"] in SourceData.keys():
			SourceData[item["email"]] = {}
			SourceData[item["email"]]["name"] = item["name"]
			SourceData[item["email"]]["phone"] = item["phone"]
			SourceData[item["email"]]["id"] = item["id"]
			SourceData[item["email"]]["is_staff"] = item["is_staff"]
			SourceData[item["email"]]["is_active"] = item["is_active"]
			SourceData[item["email"]]["groups"] = []
			SourceData[item["email"]]["groups"].append(item["groups__name"])
		else:
			SourceData[item["email"]]["groups"].append(item["groups__name"])
	for k, v in SourceData.items():
		ele += """<tr>"""
		ele += """<td><input row-select="true" type="checkbox" value="{}"></td>""".format(v["id"])
		ele += """<td><a href="{}/change">{}</a></td>""".format(v["id"],k)
		ele += """<td>{}</td>""".format(v["name"])
		ele += """<td>{}</td>""".format(v["phone"])
		if v["groups"][0]:
			sub_ele = ""
			for item_i, item_v in enumerate(v["groups"]):
				if item_i == 4:
					sub_ele += """<span class="badge label-table badge-{}">{}</span> """.format(style_list[item_i], item_v)
					sub_ele += """... """
				elif item_i > 4:
					pass
				else:
					sub_ele += """<span class="badge label-table badge-{}">{}</span> """.format(style_list[item_i], item_v)
					
			ele += """<td class="footable-visible footable-last-column">{}</td>""".format(sub_ele)
		else:
			ele += """<td class="footable-visible footable-last-column">{}</td>""".format(None)
		if v["is_staff"]:
			ele += """<td class="footable-visible footable-last-column"><span class="badge label-table badge-success">{}</span></td>""".format("Yes")
		else:
			ele += """<td class="footable-visible footable-last-column"><span class="badge label-table badge-dark">{}</span></td>""".format("No")
		if v["is_active"]:
			ele += """<td class="footable-visible footable-last-column"><span class="badge label-table badge-primary">{}</span></td>""".format("Active")
		else:
			ele += """<td class="footable-visible footable-last-column"><span class="badge label-table badge-danger">{}</span></td>""".format("Disabled")
		ele += """</tr>""" 

	return mark_safe(ele)

@register.simple_tag
def SetSystemEmailTbody(data):
	ele = ''
	for item in data:
		ele += """<tr>"""
		ele += """<td><input row-select="true" type="checkbox" value="{}"></td>""".format(item["id"])
		ele += """<td><a href="{}/change">{}</a></td>""".format(item["id"],item["name"])
		ele += """<td>{}</td>""".format(item["form_address"])
		ele += """<td>{}</td>""".format(item["smtp_server"])
		ele += """</tr>""" 
	return mark_safe(ele)

@register.simple_tag
def SetPermissionLinkTable(data):
	""" Data in AllGroupName、GroupDict、Permissions field """

	has_group = 0

	ele = ''
	th_head = '<thead>'
	th_tail = '</thead>'
	tb_head = '<tbody>'
	tb_tail = '</tbody>'
	th_head += """<tr><th data-toggle="true" class="footable-visible footable-first-column footable-sortable">权限名称<span class="footable-sort-indicator"></span></th>"""
	
	for permission in data["Permissions"]:
		tb_head += """<tr><td><a href="{}/setting">{}</a></td>""".format(permission["codename"], permission["name"])


		for group in data["AllGroupName"]:
			if not has_group >= len(data["AllGroupName"]):
				th_head += """<th name={} g_id={} data-priority=1 >{}</th>""".format(group["name"], group["id"], group["name"])
				has_group += 1
			if permission["id"] in data["GroupDict"][group["name"]]:
				tb_head += """<td><input row-select="true" checked name={} type="checkbox" value={} id={} content_type_id={}></td>""".format(group["name"]+"_"+str(permission["id"]), permission["id"], permission["id"], permission["content_type_id"])
			else:
				tb_head += """<td><input row-select="true" name={} type="checkbox" value={} id={} content_type_id={}></td>""".format(group["name"]+"_"+str(permission["id"]), permission["id"], permission["id"], permission["content_type_id"])

		tb_head += "</tr>"


	th_head += "</tr>" + th_tail
	ele += th_head
	ele += tb_head + tb_tail
	return mark_safe(ele)

@register.simple_tag
def SetResumeTemplateTbody(data):
	ele = ''
	for item in data:
		ele += """<tr>"""
		ele += """<td><input row-select="true" type="checkbox" value="{}"></td>""".format(item["id"])
		ele += """<td><a href="{}/change">{}</a></td>""".format(item["id"],item["name"])
		ele += """<td>{}</td>""".format(item["url"])
		ele += """</tr>""" 
	return mark_safe(ele)




