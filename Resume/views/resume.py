#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests, json, re
from Forms.resume import ResumeBaseInfoFrom,ResumeSourceFrom
from HttpCode.StatusCode import StatusCode

from Public.service.resume import table_config
from repository import models
from django.utils.safestring import mark_safe

from django import conf

@login_required
@check_permission()
def ResumeView(request):

    if request.method == "GET":

        obj = models.ResumeSource.objects.all().values_list("name")
        ele = ""
        if obj:
            for i in list(obj):
                for j in i:
                    ele += "<option value={}>{}</option>".format(j, j)
        ele = mark_safe(ele)


        try:
            page = int(request.GET.get('_page'))
        except:
            page = 1

        return render(request, 'resume.html', {"ele": ele})

    elif request.method == "POST":

        # 删除
        data = json.loads(request.POST.get("post_list"))
        for i in data:

            p = models.ResumeInfo.objects.filter(id=i['id'])
            if p.exists():
                models.ResumeName.objects.filter(fne__id=int(uid)).delete()
                models.ResumeName.objects.filter(efne__id=int(uid)).delete()
                models.PersonalAssessment.objects.filter(pa__id=int(uid)).delete()
                models.EducationInfo.objects.filter(ei__id=int(uid)).delete()
                models.ProjectInfo.objects.filter(pi__id=int(uid)).delete()
                models.WorkInfo.objects.filter(wi__id=int(uid)).delete()
                models.Comment.objects.filter(cts__id=int(uid)).delete()
                models.ResumeSourceText.objects.filter(rt__id=int(uid)).delete()
                models.ComprehensiveAbility.objects.filter(ceay__id=int(uid)).delete()
            i.pop("id")
            p.update(**i)
        return HttpResponse("")


def GetUserProfileInfo_back(request, uid):

    ret = {"status": "seccuss", "status_code": "200"}

    if request.method == "POST":
        query_user_info = list(models.UserProfile.objects.filter(id=uid).values("head_portrait"))
        result = {
            "head_portrait": query_user_info[0]["head_portrait"]
        }

        return JsonResponse(result)

# @login_required
def GetUserProfileInfo(request, uid):

    ret = {"status": "seccuss", "status_code": "200"}

    if request.method == "POST":
        query_user_info = list(models.UserProfile.objects.filter(id=uid).values("name","head_portrait"))
        result = {
            "head_portrait": query_user_info[0]["head_portrait"],
            "name": query_user_info[0]["name"]
        }

        return JsonResponse(result)

def DeleteResumeList(request):
    if request.method == "POST":
        for i in request.POST:
            models.ResumeInfo.objects.filter(id=i).delete()

    ret = {"status": "seccuss", "status_code": "200"}
    return JsonResponse(ret)


