#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')

def UserLogout(request):
	# _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
	# _access_user = request.user
	# if _access_user == "AnonymousUser":
	# 	print(1)
	# 	_describe = EventCode.EventCode["User.Logout"]["zh"]["seccess"].format(request.user)
	# 	_status = 1
	# 	_event_record = tasks.CommonRecordEventLog.delay(
	# 		uuid=request.user.uuid, 
	# 		user_id=request.user.id, 
	# 		event_type=EventCode.EventCode["User.Logout"]["type"],
	# 		label=EventCode.EventCode["User.Logout"]["label"], 
	# 		request=None, 
	# 		response=None, 
	# 		describe=_describe, 
	# 		status=_status,
	# 		access=_access,
	# 		source=request.user.uuid,
	# 		target=request.user.uuid,
	# 	)

	logout(request)
	
	return redirect("/user/login")