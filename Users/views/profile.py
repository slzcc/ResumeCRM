#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
import json, os
from django.contrib.auth import authenticate, login, logout
from Forms.userprofile import customUpdateUserPasswordForm, customUpdateUserInfoForm
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')


@login_required
# @check_permission(StatusCode["1407"])
def UserProfiles(request):
	ret = {"status": "seccuss", "status_code": "200"}
	data = {}

	imgList = []
	fileList = os.listdir(os.path.join(conf.settings.BASE_DIR, "static", "profile-photos", "system"))
	for i in fileList:
		imgList.append(os.path.join("profile-photos", "system", i))

	username = request.user.name
	username_id = request.user.id
	obj = models.UserProfile.objects.get(id=username_id)

	if request.method == "GET":
		form_userPassword_obj = customUpdateUserPasswordForm(instance=obj)
		form_userInfo_obj = customUpdateUserInfoForm(instance=obj)

	elif request.method == "POST":
		
		form_userInfo_obj = customUpdateUserInfoForm(instance=obj, data=request.POST)
		if form_userInfo_obj.is_valid():
			_save_data = form_userInfo_obj.save()
			_describe = EventCode.EventCode["User.Update.Info"]["zh"]["seccess"].format(request.user, )
			_status = 1
			_access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=request.user.uuid, 
				user_id=request.user.id, 
				event_type=EventCode.EventCode["User.Update.Info"]["type"],
				label=EventCode.EventCode["User.Update.Info"]["label"], 
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=_access,
				source=request.user.uuid,
				target=request.user.uuid,
			)
		else:
			print("Not Data!",request.POST)

	return render(request, "profile.html", locals())
