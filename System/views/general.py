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
import pytz, uuid, datetime
from Events import tasks, EventCode
tz = pytz.timezone('Asia/Shanghai')


@login_required
@check_permission(StatusCode["1407"])
def GeneralList(request):
    ret = {"status": "seccuss", "status_code": "200"}

    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
    
    DownloadRN = models.SystemSetting.objects.filter(name="DownloadRN").last()

    AutoUnlockResume = models.SystemSetting.objects.filter(name="AutoUnlockResume").last()
    
    PreferreEmail = models.PreferreEmail.objects.all().last()

    AllEmail = models.Email.objects.all().values("id", "name")

    EmailList = []
    for i in list(AllEmail):
        newAllEmail = {}
        newAllEmail["value"] = i["id"]
        newAllEmail["text"] = i["name"]
        EmailList.append(newAllEmail)

    PreferreResumeTemplate = models.PreferreResumeTemplate.objects.all().last()

    AllResumeTemplate =  models.ResumeTemplate.objects.all().values("id", "name")

    ResumeTemplateList = []
    for i in list(AllResumeTemplate):
        newAllResumeTemplate = {}
        newAllResumeTemplate["value"] = i["id"]
        newAllResumeTemplate["text"] = i["name"]
        ResumeTemplateList.append(newAllResumeTemplate)

    if request.method == "GET":
        pass
    elif request.method == "POST": 
        for i in request.POST:
            # Download Resume Number
            if i == "download-resume-number":
                if not request.POST.get(i) == "Empty":
                    try:
                        if int(request.POST.get(i)):
                            obj = models.SystemSetting.objects.filter(name="DownloadRN")
                            obj.update(num_value=int(request.POST.get(i)))
                            _describe = EventCode.EventCode["System.General.Update.Info"]["zh"]["seccess"].format(request.user,  str(obj.last().id), obj.last().name)
                            _status = 1
                            _event_record = tasks.CommonRecordEventLog.delay(
                                uuid=obj.last().uuid, 
                                user_id=request.user.id, 
                                event_type=EventCode.EventCode["System.General.Update.Info"]["type"],
                                label=EventCode.EventCode["System.General.Update.Info"]["label"], 
                                request=None, 
                                response=None, 
                                describe=_describe, 
                                status=_status,
                                access=_access,
                                source=request.user.uuid,
                                target=obj.last().uuid,
                            )
                    except:
                        pass

            # Upload Unlock Time
            if i == "upload-resume-unlock-time":
                if not request.POST.get(i) == "Empty":
                    try:
                        if int(request.POST.get(i)):
                            obj = models.SystemSetting.objects.filter(name="AutoUnlockResume")
                            obj.update(num_value=int(request.POST.get(i)))
                            _describe = EventCode.EventCode["System.General.Update.Info"]["zh"]["seccess"].format(request.user,  str(obj.last().id), obj.last().name)
                            _status = 1
                            _event_record = tasks.CommonRecordEventLog.delay(
                                uuid=obj.last().uuid, 
                                user_id=request.user.id, 
                                event_type=EventCode.EventCode["System.General.Update.Info"]["type"],
                                label=EventCode.EventCode["System.General.Update.Info"]["label"], 
                                request=None, 
                                response=None, 
                                describe=_describe, 
                                status=_status,
                                access=_access,
                                source=request.user.uuid,
                                target=obj.last().uuid,
                            )
                    except:
                        pass

            # Save Email
            if i == "email":
                if request.POST.get(i) == "Not Selected":
                    obj = models.PreferreEmail.objects.all()
                    obj.update(email_server="")
                else:
                    email_obj = models.Email.objects.filter(name=request.POST.get(i)).last()
                    obj = models.PreferreEmail.objects.all()
                    obj.update(email_server=email_obj.id)
                    _describe = EventCode.EventCode["System.General.Update.Info"]["zh"]["seccess"].format(request.user,  str(obj.last().id), "General.Email." + obj.last().name)
                    _status = 1
                    _event_record = tasks.CommonRecordEventLog.delay(
                        uuid=obj.last().uuid, 
                        user_id=request.user.id, 
                        event_type=EventCode.EventCode["System.General.Update.Info"]["type"],
                        label=EventCode.EventCode["System.General.Update.Info"]["label"], 
                        request=None, 
                        response=None, 
                        describe=_describe, 
                        status=_status,
                        access=_access,
                        source=request.user.uuid,
                        target=obj.last().uuid,
                    )
            # Save Resume Template
            if i == "resume-template":
                if request.POST.get(i) == "Not Selected":
                    obj = models.PreferreResumeTemplate.objects.all()
                    obj.update(resume_template="")
                else:
                    resume_template_obj = models.ResumeTemplate.objects.filter(name=request.POST.get(i)).last()
                    obj = models.PreferreResumeTemplate.objects.all()
                    obj.update(resume_template=resume_template_obj.id)
                _describe = EventCode.EventCode["System.General.Update.Info"]["zh"]["seccess"].format(request.user,  str(obj.last().id), "General.ResumeTemplate." + obj.last().name)
                _status = 1
                _event_record = tasks.CommonRecordEventLog.delay(
                    uuid=obj.last().uuid, 
                    user_id=request.user.id, 
                    event_type=EventCode.EventCode["System.General.Update.Info"]["type"],
                    label=EventCode.EventCode["System.General.Update.Info"]["label"], 
                    request=None, 
                    response=None, 
                    describe=_describe, 
                    status=_status,
                    access=_access,
                    source=request.user.uuid,
                    target=obj.last().uuid,
                )
        return JsonResponse(ret)
    return render(request, 'general.html', locals())

