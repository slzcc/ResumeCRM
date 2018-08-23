#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
from Permission.Authentication import check_permission
import datetime, re, os, time, requests, json
from django.contrib.auth import authenticate, login, logout
from Events import tasks, EventCode
import pytz, uuid
tz = pytz.timezone('Asia/Shanghai')

ret = {"status": "seccuss", "status_code": "200"}

@login_required
# @check_permission(StatusCode["1407"])
def Notification(request):

	if request.method == "GET":
		data = models.Notification.objects.filter(to_user=request.user).order_by("-trigger_time")
		not_read_number = data.filter(read=False).count()
		if not_read_number >= 100:
			not_read_str = "99+"
		else:
			not_read_str = str(not_read_number)
			
		try:
			GetParameter = request.get_full_path().split("?")[1]
			for index, item in enumerate(list(data.values("uuid"))):
				if item["uuid"] == GetParameter.split("=")[1]:
					location_num = index
			
		except:
			GetParameter = ""
			location_num = 0
			location_str = "0"

	elif request.method == "POST":
		auth = request.POST.get("auth", None)
		obj = models.Notification.objects.filter(uuid=auth)

		# 修改 read
		obj.update(read=True)

		# 返回数据
		describe = obj.values_list("describe", flat=True)[0]
		user = obj.values_list("from_user__name", flat=True)[0]
		email = obj.values_list("from_user__email", flat=True)[0]
		title = obj.values_list("title", flat=True)[0]
		ret["auth"] = auth
		ret["describe"] = describe
		ret["user"] = str.capitalize(user)
		ret["my"] = request.user.name
		ret["email"] = email
		ret["title"] = title
		ret["trigger_time"] = (obj.last().trigger_time + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M')
		return JsonResponse(ret)
	return render(request, "my_notification.html", locals())