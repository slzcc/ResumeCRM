#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django import conf
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

from repository import models
from django.utils.safestring import mark_safe
from Forms.userprofile import customUserCreationForm

@check_permission(StatusCode["1407"])
def UserRegistrys(request):
	ret = {"status": "seccuss", "status_code": "200"}

	if request.method == "GET":
		obj = customUserCreationForm()

	elif request.method == "POST":
		obj = customUserCreationForm(data=request.POST)
		if obj.is_valid():
			obj.save()
			return redirect('/resume/list')
		
	return render(request, "register.html", {"obj": obj})
