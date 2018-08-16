#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import datetime, re, os, time, requests, json
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Forms.permission import PermissionCreationForm, SystemPermissionCreationForm
from Forms.group import GroupCreationFormAll
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, Group
from django.utils.safestring import SafeString

@login_required
@check_permission(StatusCode["1407"])
def LinkPermission(request):
	search_key = request.GET.get('_q','')
	search_fields = ["name", "codename"]

	if search_key:
		q = Q()
		q.connector = 'OR'

		for search_field in search_fields:
			q.children.append(("%s__contains" % search_field, search_key))


		PermissionsList = list(Permission.objects.filter(q).values())
	else:
		PermissionsList = list(Permission.objects.all().values())

	status_code = 200

	AllGroupName = list(Group.objects.all().values("name", "id"))
	GroupDict = {}
	for i in list(Group.objects.all().values("name", "permissions")):
		if not i["name"] in GroupDict.keys():
			GroupDict[i["name"]] = []
		if i["permissions"]:
			GroupDict[i["name"]].append(i["permissions"])

	SendData = {}
	SendData["Permissions"]= PermissionsList
	SendData["AllGroupName"]= AllGroupName
	SendData["GroupDict"] = GroupDict

	if request.method == "GET":
		pass
	elif request.method == "POST":
		AcceptData = {}
		for i in request.POST:

			g_name, p_id = i.split("_")
			p_id = int(p_id)
			if not g_name in AcceptData.keys():
				AcceptData[g_name] = {}
				AcceptData[g_name]["name"] = g_name
				AcceptData[g_name]["permissions"] = []
			AcceptData[g_name]["permissions"].append(p_id)

		
		# 判断用户提交的 Group 权限是否与数据库中的一致，否则重写权限
		if AcceptData:
			for i in AcceptData:
				g_obj = Group.objects.get(name=i)
				if i in GroupDict.keys():
					if AcceptData[i]["permissions"] != GroupDict[AcceptData[i]["name"]]:
						g_obj.permissions.set(AcceptData[i]["permissions"])
			return redirect("/permission/link")
	
	GroupList = Group.objects.all().count()

	if GroupList >= 0:
		isGroup = True
	else:
		isGroup = False

	return render(request, "permissions_link.html", {
		"status": "seccuss",
        "status_code": status_code,
        "data": SendData,
        "isGroup": isGroup,
         })

@login_required
@check_permission(StatusCode["1407"])
def ListPermission(request):

	search_key = request.GET.get('_q','')
	search_fields = ["name", "codename"]

	if search_key:
		q = Q()
		q.connector = 'OR'

		for search_field in search_fields:
			q.children.append(("%s__contains" % search_field, search_key))


		PermissionsList = list(Permission.objects.filter(q).values())
	else:
		PermissionsList = list(Permission.objects.all().values())

	status_code = 200

	if request.method == "GET":
		obj = PermissionCreationForm()

	elif request.method == "POST":

		obj = PermissionCreationForm(data=request.POST)
		if obj.is_valid():
			obj.save()
		else:
			status_code = 402
		return redirect("/permission/list")

	permissions = {}
	permissions["permissions"]= PermissionsList
	return render(request, "permissions_list.html", {
		"obj": obj, 
		"status": "seccuss",
        "status_code": status_code,
        "permissions": SafeString(json.dumps(permissions)),
         })


@login_required
@check_permission(StatusCode["1407"])
def SettingPermission(request, sub_permission):
	status_code = 200

	if sub_permission == "settings":
		return redirect("/permissions/link")

	a = Permission.objects.get(codename=sub_permission)
	try:
		c = models.SystemPermission.objects.get(permissions__codename=sub_permission)
	except ObjectDoesNotExist:
		c = models.SystemPermission.objects.create(permissions=a, name=sub_permission)
		# pass
	
	if request.method == "GET":
		obj = SystemPermissionCreationForm(instance=c)
	elif request.method == "POST":
		obj = SystemPermissionCreationForm(instance=c, data=request.POST)
		if obj.is_valid():
			obj.save()
		else:
			status_code = 402
		return redirect("/permission/link")

	return render(request, "permissions_setting.html", {
		"obj": obj, 
		"status": "seccuss",
        "status_code": status_code,
        "obj_instance": a,
         })

def PermissionDelete(request):
	ret = {"status": "seccuss", "status_code": "200"}

	if request.method == "POST":
		AcceptData = {}
		for i in request.POST:
			if i == "PermissionsList":
				AcceptData[i] = json.loads(request.POST.get(i))
		obj = Permission.objects.filter(id__in=AcceptData["PermissionsList"]).delete()

	return JsonResponse(ret)

@login_required
@check_permission(StatusCode["1407"])
def PermissionChange(request, obj_id):


	obj = Permission.objects.get(id=obj_id)

	if request.method == "GET":
		form_obj = PermissionCreationForm(instance=obj)
	elif request.method == "POST":
		form_obj = PermissionCreationForm(instance=obj, data=request.POST)
		if form_obj.is_valid():
			form_obj.save()
			return redirect("/permission/list")

	return render(request, 'permissions_list_change.html', locals())



