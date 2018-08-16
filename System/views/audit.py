#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import os, json

@login_required
@check_permission(StatusCode["1407"])
def AuditList(request):
    ret = {"status": "seccuss", "status_code": "200"}


    data = models.EventLog.objects.all().order_by("-trigger_time")
    return render(request, 'audit.html', locals())

