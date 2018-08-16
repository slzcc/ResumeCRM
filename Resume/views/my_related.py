#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
import requests, json, re, datetime
from repository import models
from django.utils.safestring import mark_safe
from django import conf
import pytz
# pytz.country_timezones('cn')
tz = pytz.timezone('Asia/Shanghai')


@login_required
@check_permission()
def IamTrackingResume(request):

    if request.method == "GET":
        data = models.ResumeInfo.objects.filter(agent=request.user).order_by("-create_time")
    return render(request, 'IamTracking.html', locals())


@login_required
@check_permission()
def IUploadResume(request):

	if request.method == "GET":

		# 今天上传的数量
		dt_to = datetime.datetime.now()
		dt_from = dt_to - datetime.timedelta(hours=dt_to.hour, minutes=dt_to.minute, seconds=dt_to.second, microseconds=dt_to.microsecond)

		TodayUploadNumber = models.ResumeInfo.objects.filter(upload_user=request.user, create_time__range=[dt_from + datetime.timedelta(hours=+8), dt_to + datetime.timedelta(hours=+8)]).count()
		
		# 历史上传的数量
		HistoryUploadNumber = models.ResumeInfo.objects.filter(upload_user=request.user).count()
	
		data = models.ResumeInfo.objects.filter(upload_user=request.user).order_by("-create_time")
	return render(request, 'IUpload.html', locals())


@login_required
@check_permission()
def IDownloadResume(request):

	if request.method == "GET":
		# 今天下载的数量
		dt_to = datetime.datetime.now()
		dt_from = dt_to - datetime.timedelta(hours=dt_to.hour, minutes=dt_to.minute, seconds=dt_to.second, microseconds=dt_to.microsecond)
		TodayDownloadNumber = models.StatisticalDownloadResume.objects.filter(user_id=request.user, download_time__range=[dt_from + datetime.timedelta(hours=+8), dt_to + datetime.timedelta(hours=+8)]).count()
        
		# 历史下载的数量
		HistoryDownloadNumber = models.StatisticalDownloadResume.objects.filter(user_id=request.user).count()
		data = models.StatisticalDownloadResume.objects.filter(user_id=request.user).order_by("-download_time")
	return render(request, 'IDownload.html', locals())


@login_required
@check_permission()
def ISubscribeResume(request):

    if request.method == "GET":


        data = models.ResumeSubscription.objects.filter(user=request.user, status=True).order_by("-trigger_time")
    return render(request, 'ISubscribe.html', locals())