#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django import conf
from repository import models
import datetime, re, os, time, requests, json, urllib
from utils import encryption


def DownloadSourceResume(request):
	
	ret = {"status": "failed", "status_code": "403", "description": "There is no such permission."}
	FilePath = request.GET.get("file", None)
	obj_id = request.GET.get("uid", None)

	# 查询简历对象准备对用户记录下载简历次数
	record_download_resume =  models.ResumeInfo.objects.filter(id=int(obj_id))

	if request.method == "GET":
		LOCAL_FilePath = os.path.join(conf.settings.BASE_DIR, "static", FilePath)

		isExists = os.path.exists(os.path.dirname(LOCAL_FilePath))
		if not isExists: os.makedirs(os.path.dirname(LOCAL_FilePath))

		if FilePath and obj_id:
			urllib.request.urlretrieve(os.path.join(conf.settings.NGINX_MIRROR_ADDRESS, FilePath), LOCAL_FilePath)
			file=open(LOCAL_FilePath,'rb')  
			response =FileResponse(file)  
			response['Content-Type']='application/octet-stream'  
			response['Content-Disposition']='attachment;filename="{}"'.format(os.path.basename(LOCAL_FilePath))  

			# 记录用户下载事件
			models.StatisticalDownloadResume.objects.create(user=request.user, resume=record_download_resume.last())
			return response 
	return JsonResponse(ret)

def DownloadWordFile(request):

	# 暂未添加记录用户下载次数
	ret = {"status": "failed", "status_code": "403", "description": "There is no such permission."}
	if request.method == "GET":
		FilePath = request.GET.get("file", None)
		Token = request.GET.get("token", None)
		if FilePath and Token:
			attachmentName, currentTime = Token.split("|")
			_token = encryption.md5(FilePath + "|" + currentTime) + "|" + currentTime
			if not int(time.time()) - int(currentTime) > 10:
				if Token == _token:
					file=open(os.path.join(conf.settings.BASE_DIR, FilePath),'rb')  
					response =FileResponse(file)  
					response['Content-Type']='application/octet-stream'  
					response['Content-Disposition']='attachment;filename="{}"'.format(os.path.basename(FilePath))  
					return response 
	return JsonResponse(ret)