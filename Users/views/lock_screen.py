#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from repository import models

def UserLockScreen(request):
	logout(request)
	obj = models.UserProfile.objects.get(email=request.GET.get("auth"))
	if request.method == "GET":
		if not request.GET:
			return redirect("/user/login")
	elif request.method == "POST":
		password = request.POST.get("password")
		authentication_user = authenticate(username=obj.email, password=password)
		if authentication_user:
			login(request, authentication_user)
			return redirect("/resume/list")
	
	return render(request, "lock-screen.html", {"obj": obj})