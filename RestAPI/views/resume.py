#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import conf
from django.utils.safestring import mark_safe

from Public.service.resume import table_config
from repository import models
from Permission.Authentication import check_permission

import os, json

def OneCandidateAllInfo(request, uid):

    """ Views Resume API INFO """

    data = models.ResumeInfo.objects.filter(id=int(uid)).values()
    data = list(data)[0]
    for i in models.ResumeInfo._meta.get_fields():
        cc = models.ResumeInfo._meta.get_field(i.name)
        queryset = {}
        if cc.get_internal_type() in 'ManyToManyField':
            try:
                if cc.remote_field.related_name:
                    queryset[cc.remote_field.related_name+"__username"] = data["username"]
                    obj = cc.related_model.objects.filter(**queryset).values()
                    obj_list = list(obj)
                    if obj_list:
                        data[i.name] = obj_list
            except AttributeError:
                print(i.name, " is Other Table ManyToManyField.")
    return JsonResponse(data)

def GetUserProfileInfo(request, uid):

    ret = {"status": "seccuss", "status_code": "200"}

    if request.method == "POST":
        query_user_info = list(models.UserProfile.objects.filter(id=uid).values("name","head_portrait"))
        result = {
            "head_portrait": query_user_info[0]["head_portrait"],
            "name": query_user_info[0]["name"]
        }
        return JsonResponse(result)