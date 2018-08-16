#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json,os
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
import datetime, re
import os, time, requests
from django.utils.safestring import mark_safe
from apscheduler.schedulers.blocking import BlockingScheduler
from django.contrib.auth import authenticate, login, logout
from Forms.userprofile import customUserCreationForm, customUpdateUserPasswordForm, customUpdateUserInfoForm
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

from CustomException import userException
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')


# 修改头像
def UpdateUserHeadPortrait(request):
	username = request.user.name
	username_id = request.user.id
	data = {}
	obj = models.UserProfile.objects.filter(id=username_id)

	if request.method == "POST":
		for i in request.POST:
			if i == "head_portrait":
				data[i] = "/".join(request.POST.get(i).split("/")[2:])
		if data:
			obj.update(**data)
			_describe = EventCode.EventCode["User.Update.HeadPortrait"]["zh"]["seccess"].format(request.user,)
			_status = 1
			_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=request.user.uuid, 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["User.Update.HeadPortrait"]["type"],
				label=EventCode.EventCode["User.Update.HeadPortrait"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=request.user.uuid,
			)
	elif request.method == "GET":
		pass
	return redirect("/user/profile")

# 修改密码
def UpdateUserPassword(request, obj_id):
	ret = {"status": "seccuss", "status_code": "200"}
	password1 = ""
	password2 = ""
	
	data = {}
	obj = models.UserProfile.objects.get(id=obj_id)
	if request.method == "POST":
		for i in request.POST:
			if i == "password1":
				password1 = request.POST.get(i)
			elif i == "password2":
				password2 = request.POST.get(i)
		try:
			if password1 and password2 and password1 != password2:
				raise userException.UserPasswordError("输入信息有误，或者密码不统一!")
			else:
				obj = models.UserProfile.objects.filter(id=obj_id).update(**data)
				_describe = EventCode.EventCode["User.Update.Password"]["zh"]["seccess"].format(request.user,)
				_status = 1
				_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
				_event_record = tasks.CommonRecordEventLog.delay(
					uuid=request.user.uuid, 
					user_id=request.user.id, 
					event_type=EventCode.EventCode["User.Update.Password"]["type"],
					label=EventCode.EventCode["User.Update.Password"]["label"], 
					request=None, 
					response=None, 
					describe=_describe, 
					status=_status,
					access=_access,
					source=request.user.uuid,
					target=request.user.uuid,
				)
				data["password"] = make_password(password1)
				obj = models.UserProfile.objects.filter(id=obj_id).update(**data)
				logout(request)
				return redirect("/user/login?next=/user/profile")

		except userException.UserPasswordError as e:
			print(e.value)

	elif request.method == "GET":
		form_obj = customUpdateUserPasswordForm(instance=obj)


	return redirect("/user/profile")
