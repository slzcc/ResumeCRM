#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .tasks import SendWebSocketNotificationTasks
import os 

def TriggerStream(request):
	if request.method == "GET":
		print(request.get_full_path(), )

		auth = request.GET.get("auth")
		target = request.GET.get("auth")
		content = request.GET.get("auth")
		location = request.get_host()
		try:
			GetParameter = request.get_full_path().split("?")[1]
			_ws = "ws://{}{}?{}".format(location, os.path.join("/websocket/message/send"), GetParameter)
			SendWebSocketNotificationTasks.delay(_ws)
		except:
			pass
	return HttpResponse("")

# http://127.0.0.1:8088/notification/message/send?auth=6c1adf56-a29d-11e8-bc59-0242ac150007&target=c98497b8-a29d-11e8-bfa9-0242ac150007&content=%E5%A5%BD%E5%A5%BD%E7%8E%A9~