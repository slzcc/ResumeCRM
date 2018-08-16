#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django import conf
from repository import models
from Permission.Authentication import check_permission
from django.contrib.auth import authenticate, login, logout


def UserForgotPassword(request):
	ret = {"status": "seccuss", "status_code": "200"}
	if request.method == "GET":

		return render(request, "recoverpw.html")
	elif request.method == "POST":
			
		return JsonResponse(ret)