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
	url_list = json.dumps({"url": conf.settings.SOLR_SERVER_URL + "solr/gettingstarted/dataimport?command=full-import&clean=true&entity=resume_source_text"})
	data = {"minute": "*", "hour": "*", "day_of_month": "*", "month_of_year": "*"}
	crontab_time = crojob_models.CrontabSchedule.objects.create(**data)

	data = {'enabled': True, 'crontab':crontab_time, 'name': 'solr', 'enabled': True, 'kwargs': {}, 'task': 'Cronjob.tasks.full_update_solr','args': [], 'description': ''}

	crojob_models.PeriodicTask.objects.create(**data)
	obj = crojob_models.PeriodicTask.objects.filter(name="solr")
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


def setResumeCustomLabel(requests):
	try:
		models.CustomLabel.objects.create(name="lock", priority=0, code="fa fa-lock", uuid=uuid.uuid1())
		models.CustomLabel.objects.create(name="english", priority=1, code="mdi mdi-etsy", uuid=uuid.uuid1())
		models.CustomLabel.objects.create(name="unlock", priority=2, code="fa fa-unlock", uuid=uuid.uuid1())
	except:
		pass
		
	return HttpResponse("")


def setSettings(request):
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    _user = models.UserProfile.objects.get(id=1)

    # Unlock
    AutoUnlockResume = models.SystemSetting.objects.filter(name="AutoUnlockResume").last()
    if not AutoUnlockResume:
        _set_uuid = uuid.uuid1()
        obj = DownloadRN = models.SystemSetting.objects.create(name="AutoUnlockResume", num_value="180", uuid=_set_uuid)
        _describe = EventCode.EventCode["System.General.Create"]["zh"]["seccess"].format(_user.name,  str(obj.id), obj.name)
        _status = 1
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=_set_uuid, 
            user_id=1, 
            event_type=EventCode.EventCode["System.General.Create"]["type"],
            label=EventCode.EventCode["System.General.Create"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=_user.uuid,
            target=_set_uuid,
        )

    # Download Resume Number
    DownloadRN = models.SystemSetting.objects.filter(name="DownloadRN").last()
    if not DownloadRN:
        _set_uuid = uuid.uuid1()
        obj = DownloadRN = models.SystemSetting.objects.create(name="DownloadRN", num_value="10", uuid=_set_uuid)
        _describe = EventCode.EventCode["System.General.Create"]["zh"]["seccess"].format(_user.name,  str(obj.id), obj.name)
        _status = 1
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=_set_uuid, 
            user_id=1, 
            event_type=EventCode.EventCode["System.General.Create"]["type"],
            label=EventCode.EventCode["System.General.Create"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=_user.uuid,
            target=_set_uuid,
        )

    # SMTP
    PreferreEmail = models.PreferreEmail.objects.all().last()
    if not PreferreEmail:
        _set_uuid = uuid.uuid1()

        models.PreferreEmail.objects.all().delete()
        obj = models.PreferreEmail.objects.create(name="default", uuid=_set_uuid)
        _describe = EventCode.EventCode["System.General.Create"]["zh"]["seccess"].format(_user.name,  str(obj.id), obj.name)
        _status = 1
        
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=_set_uuid, 
            user_id=1, 
            event_type=EventCode.EventCode["System.General.Create"]["type"],
            label=EventCode.EventCode["System.General.Create"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=_user.uuid,
            target=_set_uuid,
        )
        
    # Resume Template
    PreferreResumeTemplate = models.PreferreResumeTemplate.objects.all().last()
    if not PreferreResumeTemplate:
        _set_uuid = uuid.uuid1()

        models.PreferreResumeTemplate.objects.all().delete()
        obj = models.PreferreResumeTemplate.objects.create(name="default", uuid=_set_uuid)
        _describe = EventCode.EventCode["System.General.Create"]["zh"]["seccess"].format(_user.name,  str(obj.id), obj.name)
        _status = 1
        
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=_set_uuid, 
            user_id=1, 
            event_type=EventCode.EventCode["System.General.Create"]["type"],
            label=EventCode.EventCode["System.General.Create"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=_user.uuid,
            target=_set_uuid,
        )
    return HttpResponse("")