#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

from Forms.resume import ResumeBaseInfoFrom,ResumeSourceFrom

import json, re, requests
from repository import models
from django.utils.safestring import mark_safe

from django import conf
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')

ret = {"status": "seccuss", "status_code": "200"}

@login_required
@check_permission(StatusCode["1407"])
def ResumeSource(request):
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    ResumeSourceData = models.ResumeSource.objects.all().values("name","id")

    if request.method == "GET":
        obj = ResumeSourceFrom()

    elif request.method == "POST":
        obj = ResumeSourceFrom(data=request.POST)
        if obj.is_valid():
            _save_name = obj.save(commit=False)
            _set_uuid = uuid.uuid1()
            _save_name.uuid = _set_uuid
            _save_name = obj.save()
            _save_obj = models.ResumeSource.objects.get(name=_save_name)
            _describe = EventCode.EventCode["Resume.Source.Create"]["zh"]["seccess"].format(request.user, str(_save_obj.id), _save_name)
            _status = 1
            _event_record = tasks.CommonRecordEventLog.delay(
                uuid=_set_uuid,
                user_id=request.user.id, 
                event_type=EventCode.EventCode["Resume.Source.Create"]["type"],
                label=EventCode.EventCode["Resume.Source.Create"]["label"], 
                request=None, 
                response=None, 
                describe=_describe, 
                status=_status,
                access=_access,
                source=request.user.uuid,
                target=_set_uuid,
            )
            return redirect("/resume/source/list")
        else:
            status_code = 402
            _save_name = dict(obj.data)["name"][0]
            _describe = EventCode.EventCode["Resume.Source.Create"]["zh"]["failed"].format(request.user, _save_name)
            _status = 2
            _set_uuid = uuid.uuid1()
            _event_record = tasks.CommonRecordEventLog.delay(
                uuid=_set_uuid, 
                user_id=request.user.id, 
                event_type=EventCode.EventCode["Resume.Source.Create"]["type"],
                label=EventCode.EventCode["Resume.Source.Create"]["label"], 
                request=None, 
                response=None, 
                describe=_describe, 
                status=_status,
                access=_access,
                source=request.user.uuid,
                target=_set_uuid,
            )
            return redirect("/resume/source/list")
    return render(request, 'resume_source.html', {
        "ResumeSourceData": list(ResumeSourceData),
        "obj": obj
        })
    
@login_required
@check_permission(StatusCode["1407"])
def ResumeSourceChange(request, obj_id):

    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    obj = models.ResumeSource.objects.get(id=obj_id)
    if request.method == "GET":
        form_obj = ResumeSourceFrom(instance=obj)
    elif request.method == "POST":
        form_obj = ResumeSourceFrom(instance=obj,data=request.POST)
        if form_obj.is_valid():
            _save_name = form_obj.save()
            _save_obj = models.ResumeSource.objects.get(name=_save_name)
            _describe = EventCode.EventCode["Resume.Source.Update.Info"]["zh"]["seccess"].format(request.user, str(_save_obj.id),  _save_name)
            _status = 1
            _event_record = tasks.CommonRecordEventLog.delay(
                uuid=_save_obj.uuid, 
                user_id=request.user.id, 
                event_type=EventCode.EventCode["Resume.Source.Update.Info"]["type"],
                label=EventCode.EventCode["Resume.Source.Update.Info"]["label"], 
                request=None, 
                response=None, 
                describe=_describe, 
                status=_status,
                access=_access,
                source=request.user.uuid,
                target=_save_obj.uuid,
            )
            return redirect("/resume/source/list")
        else:
            status_code = 402
            _save_name = dict(form_obj.data)["name"][0]
            _describe = EventCode.EventCode["Resume.Source.Update.Info"]["zh"]["failed"].format(request.user, _save_name)
            _status = 2
            _set_uuid = uuid.uuid1()
            _event_record = tasks.CommonRecordEventLog.delay(
                uuid=_set_uuid, 
                user_id=request.user.id, 
                event_type=EventCode.EventCode["Resume.Source.Update.Info"]["type"],
                label=EventCode.EventCode["Resume.Source.Update.Info"]["label"], 
                request=None, 
                response=None, 
                describe=_describe, 
                status=_status,
                access=_access,
                source=request.user.uuid,
                target=_set_uuid,
            )
            return redirect("/resume/source/list")

    return render(request, 'resume_source_change.html', locals())

def ResumeSourceDelete(request):

    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    if request.method == "POST":
        AcceptData = {}
        for i in request.POST:
            if i == "ResumeSourceList":
                AcceptData[i] = json.loads(request.POST.get(i))
        obj = models.ResumeSource.objects.filter(id__in=AcceptData["ResumeSourceList"])
        for item in list(obj.values("id", "name", "uuid")):
            _describe = EventCode.EventCode["Resume.Source.Delete"]["zh"]["seccess"].format(request.user, item["id"], item["name"])
            _status = 1
            _event_record = tasks.CommonRecordEventLog.delay(
                uuid=item["uuid"], 
                user_id=request.user.id, 
                event_type=EventCode.EventCode["Resume.Source.Delete"]["type"],
                label=EventCode.EventCode["Resume.Source.Delete"]["label"], 
                request=None, 
                response=None, 
                describe=_describe, 
                status=_status,
                access=_access,
                source=request.user.uuid,
                target=item["uuid"],
            )
        obj.delete()

    return JsonResponse(ret)