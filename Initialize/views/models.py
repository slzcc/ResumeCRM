#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
from django_celery_beat import models as crojob_models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

import datetime, re, os, time, requests, json
import pytz, uuid, datetime
from Events import tasks, EventCode
tz = pytz.timezone('Asia/Shanghai')

def setModels_id(request):
	obj = models.ResumeInfo(id=100000)
	obj.save()

	obj = models.ResumeSourceText(id=100000)
	obj.save()
	return HttpResponse("")

def setDefaultUser(request):
	try:
		models.UserProfile.objects.create(name="system", email="system@resumecrm.com", is_staff=True, is_superuser=True, uuid=uuid.uuid1(), password=make_password("D2#20cPUCaLe"))
	except:
		pass
	try:
		models.UserProfile.objects.create(name="admin", email="admin@resumecrm.com", is_staff=True, is_superuser=True, uuid=uuid.uuid1(), password=make_password("admin"))
	except:
		pass
	return HttpResponse("")


def setCrojob_inSolrData(request):
	url_list = json.dumps({"url": "http://10.30.0.41:8983/solr/gettingstarted/dataimport?command=full-import&clean=true&entity=resume_source_text"})
	data = {"minute": "*", "hour": "*", "day_of_month": "*", "month_of_year": "*"}
	crontab_time = crojob_models.CrontabSchedule.objects.create(**data)

	data = {'enabled': True, 'crontab':crontab_time, 'name': 'solr', 'enabled': True, 'kwargs': {}, 'task': 'Cronjob.tasks.full_update_solr','args': [], 'description': ''}

	crojob_models.PeriodicTask.objects.create(**data)
	obj = models.PeriodicTask.objects.filter(name="solr")
	obj.update(kwargs=url_list)
	return HttpResponse("")

def setEventType(request):

	EventType_list = [
		"User",
		"Permission",
		"System",
		"Search",
		"Resume",
	]
	
	for item in EventType_list:
		try:
			_set_uuid = uuid.uuid1()
			obj = models.StoredEventType.objects.create(name=item, uuid=_set_uuid)
			
		except:
			pass
	return HttpResponse("")