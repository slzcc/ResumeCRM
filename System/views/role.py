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
from Forms.group import GroupCreationForm, GroupCreationFormAll

from django.contrib.auth.models import Group
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
def RoleList(request):
	status_code = 200
	error_status = ""

	obj = Group.objects.all()
	GroupCountList = {}

	for item in list(obj):
		GroupCountList[item.name] = {}
		GroupCountList[item.name]["count"] = item.user_set.count()
		GroupCountList[item.name]["id"] = item.id

	if request.method == "GET":
		obj = GroupCreationForm()
		
	elif request.method == "POST":
		obj = GroupCreationForm(data=request.POST)
		if obj.is_valid():
			_save_name = obj.save()
			_save_obj = Group.objects.get(name=_save_name)
			_describe = EventCode.EventCode["System.Role.Create"]["zh"]["seccess"].format(request.user,  _save_obj.id, _save_name)
			_status = 1
			_set_uuid = uuid.uuid1()
			_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_set_uuid,
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.Role.Create"]["type"],
				label=EventCode.EventCode["System.Role.Create"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_set_uuid,
			)
			error_status = 0
			return redirect("/system/role/list")
		else:
			status_code = 402
			error_status = 1

		# return redirect("/system/role/list")


	return render(request, 'role.html', {
        'obj': obj,
        "status": "seccuss",
        "status_code": status_code,
        "GroupCountList": GroupCountList,
        "error_status": error_status,
         })	

@login_required
@check_permission(StatusCode["1407"])
def RoleChange(request, obj_id):

	AcceptData = {}
	obj = Group.objects.get(id=obj_id)
	
	if request.method == "GET":
		form_obj = GroupCreationFormAll(instance=obj)

	elif request.method == "POST":
		for i in request.POST:
			AcceptData[i] = request.POST.getlist(i, None)

		form_obj = GroupCreationFormAll(instance=obj, data=request.POST)
		if form_obj.is_valid():
			_save_name = form_obj.save()
			_describe = EventCode.EventCode["System.Role.Update.Info"]["zh"]["seccess"].format(request.user,  obj.id, _save_name)
			_status = 1
			_set_uuid = uuid.uuid1()
			_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=_set_uuid, 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.Role.Update.Info"]["type"],
				label=EventCode.EventCode["System.Role.Update.Info"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_set_uuid,
			)

			if not "data" in AcceptData.keys():
				obj.user_set.clear()
			else:
				obj.user_set.set(AcceptData["data"])
			return redirect("/system/role/list")

	return render(request, 'role_change.html', {
		"obj_id": obj_id,
		"obj": obj,
		"form_obj": form_obj,
		})

# @check_permission
def RoleDelete(request):
	ret = {"status": "seccuss", "status_code": "200"}

	if request.method == "POST":
		AcceptData = {}

		_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
		
		for i in request.POST:
			if i == "RoleList":
				AcceptData[i] = json.loads(request.POST.get(i))

		obj = Group.objects.filter(id__in=AcceptData["RoleList"])

		for item in list(obj.values("id", "name")):
			_describe = EventCode.EventCode["System.Role.Delete"]["zh"]["seccess"].format(request.user,  item["id"], item["name"])
			_status = 1
			_set_uuid = uuid.uuid1()
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=uuid.uuid1(), 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["System.Role.Delete"]["type"],
				label=EventCode.EventCode["System.Role.Delete"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=_set_uuid,
			)
		obj.delete()

	return JsonResponse(ret)