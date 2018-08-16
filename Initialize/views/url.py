#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models

import json, re

UrlList = []
def GetAllUrlNames(ClearAll=False):
	if ClearAll:
		models.Menu.objects.all().delete()

	for app_name in conf.settings.INSTALLED_APPS:
		if not re.search('django', app_name):
			items = __import__(app_name)
			try:
				for item in items.urls.urlpatterns:
					if item.name and not item.name in UrlList:
						UrlList.append(item.name)
						data = {"name": item.name, "url_name": item.name}
						obj = models.Menu.objects.create(**data)
			except AttributeError as e:
				pass

def SetUrlNameDatabaseList(request):
	GetAllUrlNames(ClearAll=True)
	return HttpResponse('')