#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

import os, time, requests, json, datetime, re, shutil
from django.utils.safestring import mark_safe

from CustomException import userException
from utils import FileFormatToPDF, encryption


def ViewerJSInterface(request):


	return render(request, "viewerjs.html")

def ViewerJSAccessFiles(request):

	FilePath = request.GET.get("file", None)
	Token = request.GET.get("token", None)
	if FilePath and Token:
		attachmentName, currentTime = Token.split("|")
		_token = encryption.md5(FilePath + "|" + currentTime) + "|" + currentTime
		if not int(time.time()) - int(currentTime) > 10:
			if Token == _token:
				session = requests.get(os.path.join(conf.settings.NGINX_MIRROR_ADDRESS, FilePath))
				response = HttpResponse(session.content, content_type='application/pdf')
				response['Content-Disposition'] = 'filename="{}"'.format(os.path.basename(FilePath))
				return response
	return JsonResponse({"status": "failed", "status_code": "403", "description": "There is no such permission."})