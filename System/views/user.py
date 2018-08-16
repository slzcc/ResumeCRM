#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import os, time, requests, json,datetime, re
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Forms.userprofile import customUserCreationForm, customUpdateUserPasswordForm, customUpdateUserInfoForm, customUpdateUserInfoForm_user

from django.utils.safestring import SafeString
from CustomException import userException
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')

@login_required
@check_permission(StatusCode["1407"])
def UserList(request):
	status_code = 200
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
	AllUserProfileList = list(models.UserProfile.objects.all().values("email","name","phone","groups__name","id","is_active", "is_staff"))
	if request.method == "GET":
		obj = customUserCreationForm()

	elif request.method == "POST":
		obj = customUserCreationForm(data=request.POST)
		if obj.is_valid():
			_save_name = obj.save(commit=False)
			_set_uuid = uuid.uuid1()
			_save_name.uuid = _set_uuid
			_save_name = obj.save()
			_save_obj = models.UserProfile.objects.get(email=_save_name)
			_describe = EventCode.EventCode["System.User.Create"]["zh"]["seccess"].format(request.user,  str(_save_obj.id), _save_name)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_set_uuid,
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.User.Create"]["type"],
				label=EventCode.EventCode["System.User.Create"]["label"], 
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
			_save_name = dict(obj.data)["email"][0]
			_describe = EventCode.EventCode["System.User.Create"]["zh"]["failed"].format(request.user,  _save_name)
			_status = 1
			_set_uuid = uuid.uuid1()
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_set_uuid,
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.User.Create"]["type"],
				label=EventCode.EventCode["System.User.Create"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_set_uuid,
			)

		return redirect("/system/user/list")

	return render(request, 'user.html', locals())

@login_required
@check_permission(StatusCode["1407"])
def UserChange(request, obj_id):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	obj = models.UserProfile.objects.get(id=obj_id)

	if request.method == "GET":

		form_userPassword_obj = customUpdateUserPasswordForm(instance=obj)
		form_userInfo_obj = customUpdateUserInfoForm_user(instance=obj)

	elif request.method == "POST":

		form_userInfo_obj = customUpdateUserInfoForm_user(instance=obj, data=request.POST)
		if form_userInfo_obj.is_valid():
			_save_name = form_userInfo_obj.save()
			_save_obj = models.UserProfile.objects.get(email=_save_name)
			_describe = EventCode.EventCode["System.User.Update.Info"]["zh"]["seccess"].format(request.user,  str(_save_obj.id), _save_name)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_save_obj.uuid,
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.User.Update.Info"]["type"],
				label=EventCode.EventCode["System.User.Update.Info"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_save_obj.uuid,
			)
			groups_list = request.POST.getlist("groups", None)
			if groups_list:
				obj.groups.set(groups_list)
			else:
				obj.groups.clear()
			return redirect("/system/user/list")
		else:
			print("Not Data!",request.POST)

	return render(request, 'user_change.html', locals())

def UpdateUserPassword(request, obj_id):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

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
				data["password"] = make_password(password1)

				obj = models.UserProfile.objects.filter(id=obj_id)
				obj.update(**data)
				_describe = EventCode.EventCode["System.User.Update.Password"]["zh"]["seccess"].format(request.user,  str(obj.last().id), obj.last().email)
				_status = 1
				_event_record = tasks.CommonRecordEventLog.delay(
					uuid=obj.last().uuid,
					user_id=request.user.id, 
					event_type=EventCode.EventCode["System.User.Update.Password"]["type"],
					label=EventCode.EventCode["System.User.Update.Password"]["label"], 
					request=None, 
					response=None, 
					describe=_describe, 
					status=_status,
					access=_access,
					source=request.user.uuid,
					target=obj.last().uuid,
				)
				return redirect('/system/user/{}/change'.format(obj_id))

		except userException.UserPasswordError as e:
			print(e.value)

	elif request.method == "GET":
		form_obj = customUpdateUserPasswordForm(instance=obj)


	return redirect('/system/user/list')

# @check_permission
def UserDelete(request):
	_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

	ret = {"status": "seccuss", "status_code": "200"}

	if request.method == "POST":
		AcceptData = {}
		for i in request.POST:
			if i == "UserList":
				AcceptData[i] = json.loads(request.POST.get(i))
		obj = models.UserProfile.objects.filter(id__in=AcceptData["UserList"])
		for item in list(obj.values("id", "email", "uuid")):
			_describe = EventCode.EventCode["System.User.Delete"]["zh"]["seccess"].format(request.user,  item["id"], item["email"])
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=item["uuid"], 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.User.Delete"]["type"],
				label=EventCode.EventCode["System.User.Delete"]["label"], 
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