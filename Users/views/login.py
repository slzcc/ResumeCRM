#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from Permission.Authentication import check_permission
import datetime, re, os, time, requests, json
from django.contrib.auth import authenticate, login, logout
from Events import tasks, EventCode
import pytz, uuid
tz = pytz.timezone('Asia/Shanghai')

def UserLogin(request):

    error_msg = ""
    if request.method == "GET":

        if request.GET.get("next"):
          isValidation = True
        else:
          isValidation = False

        return render(request, "login.html", locals())

    elif request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        authentication_user = authenticate(username=username, password=password)

        _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
        _user = models.UserProfile.objects.get(email=username)
        if authentication_user:
            login(request, authentication_user)
            _describe = EventCode.EventCode["User.Login"]["zh"]["seccess"].format(username, )
            _status = 1
            _event_record = tasks.CommonRecordEventLog.delay(
              uuid=_user.uuid, 
              user_id=request.user.id, 
              event_type=EventCode.EventCode["User.Logout"]["type"],
              label=EventCode.EventCode["User.Login"]["label"], 
              request=None, 
              response=None, 
              describe=_describe, 
              status=_status,
              access=_access,
              source=_user.uuid,
              target=_user.uuid,
            )

            return redirect(request.GET.get("next", "/dashboard"))
        else:
            _describe = EventCode.EventCode["User.Login"]["zh"]["failed"].format(username,)
            _status = 2
            _event_record = tasks.CommonRecordEventLog.delay(
              uuid=uuid.uuid1(), 
              user_id=request.user.id, 
              event_type=EventCode.EventCode["User.Logout"]["type"],
              label=EventCode.EventCode["User.Login"]["label"], 
              request=None, 
              response=None, 
              describe=_describe, 
              status=_status,
              access=_access,
              source=uuid.uuid1(),
              target=_user.uuid,
            )
            error_msg = "Wrong Username or Password!"

        return render(request, "login.html", locals())