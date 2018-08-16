#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import os, time, requests, datetime, re, shutil, json
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from Forms.email import EmailCreationForm
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')


@login_required
@check_permission(StatusCode["1407"])
def EmailList(request):
	status_code = 200
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	AllEmailList = list(models.Email.objects.all().values('name', 'form_address', 'smtp_server',"id"))

	if request.method == "GET":

		obj = EmailCreationForm()

	elif request.method == "POST":
		obj = EmailCreationForm(data=request.POST)
		if obj.is_valid():
			_save_name = obj.save(commit=False)
			_set_uuid = uuid.uuid1()
			_save_name.uuid = _set_uuid
			_save_name = obj.save()
			_save_obj = models.Email.objects.get(name=_save_name)
			_describe = EventCode.EventCode["System.Email.Create"]["zh"]["seccess"].format(request.user,  str(_save_obj), _save_name)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
			    uuid=_set_uuid, 
			    user_id=request.user.id, 
			    event_type=EventCode.EventCode["System.Email.Create"]["type"],
			    label=EventCode.EventCode["System.Email.Create"]["label"], 
			    request=None, 
			    response=None, 
			    describe=_describe,
			    status=_status,
			    access=_access,
			    source=request.user.uuid,
			    target=_set_uuid,
			)
		else:
			status_code = 402
		return redirect("/system/email/list")

	return render(request, 'email.html', locals())

@login_required
@check_permission(StatusCode["1407"])
def EmailChange(request, obj_id):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	obj = models.Email.objects.get(id=obj_id)
	if request.method == "GET":
		from_obj = EmailCreationForm(instance=obj)
	elif request.method == "POST":
		from_obj = EmailCreationForm(instance=obj, data=request.POST)
		if from_obj.is_valid():
			_save_name = from_obj.save()
			print(_save_name)
			_save_obj = models.Email.objects.get(name=_save_name)
			_describe = EventCode.EventCode["System.Email.Update.Info"]["zh"]["seccess"].format(request.user,  str(_save_obj.id), _save_name)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
			    uuid=_save_obj.uuid, 
			    user_id=request.user.id, 
			    event_type=EventCode.EventCode["System.Email.Update.Info"]["type"],
			    label=EventCode.EventCode["System.Email.Update.Info"]["label"], 
			    request=None, 
			    response=None, 
			    describe=_describe, 
			    status=_status,
			    access=_access,
			    source=request.user.uuid,
			    target=_save_obj.uuid,
			)
		else:
			status_code = 402
		return redirect("/system/email/list")
		
	return render(request, 'email_change.html', {"from_obj": from_obj, "obj": obj})

def SendEmailDataInterface(request, obj_id):

	ret = {"status": "seccuss", "status_code": "200"}
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	obj = models.Email.objects.get(id=obj_id)
	if request.method == "GET":
		pass
	elif request.method == "POST":
		AcceptData = {}
		AcceptData["send-to"] = []
		for i in request.POST:
			if i == "send-to":
				AcceptData[i].append(request.POST.get(i))
			elif i == "content":
				AcceptData[i] = json.loads(request.POST.get(i))
			else:
				AcceptData[i] = request.POST.get(i)

		if AcceptData["content"]:

			msgRoot = MIMEMultipart('related')
			msgRoot['From']=formataddr(["ResumeCRM", obj.smtp_username])
			msgRoot['To']=formataddr(["", AcceptData["send-to"][0]])
			subject = AcceptData["send-subject"]
			msgRoot['Subject'] = Header(subject, 'utf-8')

			msgAlternative = MIMEMultipart('alternative')
			msgRoot.attach(msgAlternative)

			# mail_msg = AcceptData["content"].replace("\r", '').replace("\\r", '').replace("\n", '').replace("\\n", '')
			mail_msg = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
			<head>
			<meta name="viewport" content="width=device-width" />
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
			<title>Minton - Responsive Admin Dashboard Template</title>


			<style type="text/css">img {
			max-width: 100%;
			}
			body {
			-webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em;
			}
			body {
			background-color: #f6f6f6;
			}
			@media only screen and (max-width: 640px) {
			  body {
			    padding: 0 !important;
			  }
			  h1 {
			    font-weight: 800 !important; margin: 20px 0 5px !important;
			  }
			  h2 {
			    font-weight: 800 !important; margin: 20px 0 5px !important;
			  }
			  h3 {
			    font-weight: 800 !important; margin: 20px 0 5px !important;
			  }
			  h4 {
			    font-weight: 800 !important; margin: 20px 0 5px !important;
			  }
			  h1 {
			    font-size: 22px !important;
			  }
			  h2 {
			    font-size: 18px !important;
			  }
			  h3 {
			    font-size: 16px !important;
			  }
			  .container {
			    padding: 0 !important; width: 100% !important;
			  }
			  .content {
			    padding: 0 !important;
			  }
			  .content-wrap {
			    padding: 10px !important;
			  }
			  .invoice {
			    width: 100% !important;
			  }
			}
			</style>
			</head>

			  <body itemscope itemtype="http://schema.org/EmailMessage" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
			"""
			mail_msg += AcceptData["content"].replace("\r", '').replace("\\r", '').replace("\n", '').replace("\\n", '')

			mail_msg+=  """</body></html>"""

			msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

			try:
				server=smtplib.SMTP_SSL(obj.smtp_server, obj.smtp_port)
				server.login(obj.smtp_username, obj.smtp_password)
				server.sendmail(obj.smtp_username, AcceptData["send-to"], msgRoot.as_string())
				print("邮件发送成功")
				# server.quit()  # 关闭连接
				_describe = EventCode.EventCode["System.Email.Send.Email"]["zh"]["seccess"].format(request.user,  obj.id, ", ".join(AcceptData["send-to"]))
				_status = 1
				_event_record = tasks.CommonRecordEventLog.delay(
				    uuid=obj.uuid, 
				    user_id=request.user.id, 
				    event_type=EventCode.EventCode["System.Email.Send.Email"]["type"],
				    label=EventCode.EventCode["System.Email.Send.Email"]["label"], 
				    request=None, 
				    response=None, 
				    describe=_describe, 
				    status=_status,
				    access=_access,
				    source=request.user.uuid,
				    target=obj.uuid,
				)
			except smtplib.SMTPException:
				print("Error: 无法发送邮件")

	return JsonResponse(ret)



def EmailDelete(request):
	ret = {"status": "seccuss", "status_code": "200"}
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	if request.method == "POST":
		AcceptData = {}
		for i in request.POST:
			if i == "EmailList":
				AcceptData[i] = json.loads(request.POST.get(i))
		obj = models.Email.objects.filter(id__in=AcceptData["EmailList"])
		for item in list(obj.values("id", "name", "uuid")):
			_describe = EventCode.EventCode["System.Email.Delete"]["zh"]["seccess"].format(request.user,  item["id"], item["name"])
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
			    uuid=item["uuid"], 
			    user_id=request.user.id, 
			    event_type=EventCode.EventCode["System.Email.Delete"]["type"],
			    label=EventCode.EventCode["System.Email.Delete"]["label"], 
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

