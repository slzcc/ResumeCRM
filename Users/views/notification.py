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



def Notification(request):

    if request.method == "GET":

        data = models.Notification.objects.filter(to_user=request.user).order_by("-trigger_time")
        return render(request, "my_notification.html", locals())