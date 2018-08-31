#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

import os, time, requests, json, datetime, re, shutil
from django.utils.safestring import mark_safe

from CustomException import userException
from utils import FileFormatToPDF, encryption

def isExistPDF(request):
	ret = {"status": "seccuss", "status_code": "200"}

	attachmentName = request.GET.get("attachmentName")
	mandatory_parsing = request.GET.get("mandatory_parsing", False)

	currentTime = str(int(time.time()))
	if os.path.basename(attachmentName).split(".")[1] != "pdf":
		
		data = {"type": "url", "url": os.path.join(conf.settings.NGINX_MIRROR_ADDRESS, attachmentName), "mandatory_parsing": mandatory_parsing}

		url = conf.settings.TRANSCODE_PDF_ADDRESS
		domain = url.split("/")[2].split(":")[0]
		domain_ip = ""
		if not isIP(domain):
			domain_ip = getIP(domain)
			url = url.replace(domain, domain_ip)

		session = requests.post(url=url, data=data)
		url = "/".join(json.loads(session.text)["account_url"].split("/")[3:])
	else:
		url = attachmentName
	ret["sourceFileUrl"] = attachmentName
	_token = encryption.md5(url + "|" + currentTime) + "|" + currentTime
	ret["targetFileUrl"] = os.path.join("http://",request.get_host(),"/ViewerJS/AccessFiles?file={}&token={}".format(url, _token))
	return JsonResponse(ret)