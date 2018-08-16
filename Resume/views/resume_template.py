#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
from Forms.resume import ResumeTemplateFrom
import os, time, requests, json,datetime, re
from django.utils.safestring import mark_safe, SafeString
from Storage.upload_nginx import UploadNginx

from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')

@login_required
@check_permission(StatusCode["1407"])
def ResumeTemplate(request):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	ResumeTemplateList = list(models.ResumeTemplate.objects.all().values("name","url","id"))
	if request.method == "GET":
		obj = ResumeTemplateFrom()
		
	elif request.method == "POST":
		
		file_data = request.FILES.get("file", None)
		path = os.path.join(conf.settings.BASE_DIR, 'static', 'firmware', "temporary")

		# 把文件内容保存到本地
		f = open(os.path.join(path, file_data.name), 'wb')
		for line in file_data.chunks():
			f.write(line)
		f.close()

		session = UploadNginx(url=conf.settings.NGINX_UPLOAD_ADDRESS, fileName=file_data.name, filePath=os.path.join(path, file_data.name), storagePath="firmware/resume/templates")
		data = {}
		data["name"] = request.POST.get("name")
		data["url"] =  "/".join(json.loads(session)["account_url"].split("/")[3:])
		obj = ResumeTemplateFrom(data=data)
		if obj.is_valid():
			_save_name = obj.save(commit=False)
			_set_uuid = uuid.uuid1()
			_save_name.uuid = _set_uuid
			obj.save()
			_save_obj = models.ResumeTemplate.objects.get(name=data["name"])
			_describe = EventCode.EventCode["Resume.Template.Create"]["zh"]["seccess"].format(request.user, str(_save_obj.id), data["name"])
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_set_uuid,
				user_id=request.user.id, 
				event_type=EventCode.EventCode["Resume.Template.Create"]["type"],
				label=EventCode.EventCode["Resume.Template.Create"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_set_uuid,
			)
			
		return redirect("/resume/template/list")


	return render(request, 'resume_template.html', {
        'obj': obj,
        "ResumeTemplateList": ResumeTemplateList,
         })	

@login_required
@check_permission(StatusCode["1407"])
def ResumeTemplateChange(request, obj_id):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	AcceptData = {}
	obj = models.ResumeTemplate.objects.get(id=obj_id)
	
	if request.method == "GET":
		form_obj = ResumeTemplateFrom(instance=obj)

	elif request.method == "POST":
		for i in request.POST:
			AcceptData[i] = request.POST.getlist(i, None)

		form_obj = ResumeTemplateFrom(instance=obj, data=request.POST)
		if form_obj.is_valid():
			_save_name = form_obj.save()
			_save_obj = models.ResumeTemplate.objects.get(name=_save_name)
			_describe = EventCode.EventCode["Resume.Template.Update.Info"]["zh"]["seccess"].format(request.user, str(_save_obj.id), _save_name)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_save_obj.uuid, 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["Resume.Template.Update.Info"]["type"],
				label=EventCode.EventCode["Resume.Template.Update.Info"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_save_obj.uuid,
			)

			return redirect("/resume/template/list")

	return render(request, 'resume_template_change.html', {
		"obj_id": obj_id,
		"obj": obj,
		"form_obj": form_obj,
		})

# @check_permission
def ResumeTemplateDelete(request):
	ret = {"status": "seccuss", "status_code": "200"}
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	if request.method == "POST":
		AcceptData = {}
		for i in request.POST:
			if i == "TemplateList":
				AcceptData[i] = json.loads(request.POST.get(i))
		obj = models.ResumeTemplate.objects.filter(id__in=AcceptData["TemplateList"])
		for item in list(obj.values("id", "name", "uuid")):
			_describe = EventCode.EventCode["Resume.Template.Delete"]["zh"]["seccess"].format(request.user, item["id"], item["name"])
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=item["uuid"], 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["Resume.Template.Delete"]["type"],
				label=EventCode.EventCode["Resume.Template.Delete"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=item["uuid"],
			)

		obj.delete()

	return JsonResponse(ret)