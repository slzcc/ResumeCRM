#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
from Forms.resume import ResumeInfoFrom
import datetime, re, shutil, json, os, time, requests
from django.utils.safestring import mark_safe
from Events import tasks, EventCode
import pytz, uuid, datetime
tz = pytz.timezone('Asia/Shanghai')

def _TimeRange(now_time, old_time):
    CurrentTimeDifference = (now_time - old_time)
    CurrentTimeDifference = CurrentTimeDifference + datetime.timedelta(hours=+8)
    if CurrentTimeDifference.seconds < 10:
        return "刚刚"
    elif CurrentTimeDifference.seconds < 60:
        return "1 分钟内"
    elif CurrentTimeDifference.seconds < 180:
        return "3 分内"
    elif CurrentTimeDifference.seconds < 600:
        return "10 分钟内"
    elif CurrentTimeDifference.seconds < 1800:
        return "30 分钟内"
    elif CurrentTimeDifference.seconds/60 <= 60:
        return "1 小时内"
    elif CurrentTimeDifference.seconds/60 <= 180:
        return "3 小时内"
    elif CurrentTimeDifference.days < 0:
        return "今天"
    elif CurrentTimeDifference.days <= 1:
        return "昨天"
    elif CurrentTimeDifference.days <= 3:
        return "3 天内"
    elif CurrentTimeDifference.days <= 7:
        return "1 周内"
    elif CurrentTimeDifference.days <= 31:
        return "1 个月内"
    elif CurrentTimeDifference.days <= 180:
        return "半年内"
    elif CurrentTimeDifference.days <= 365:
        return "1 年内"
    elif  CurrentTimeDifference.days >= 365:
        return "1 年前"

def SetManytoManyField_inHTMLs(objs, value):
    data = ''
    if objs.values(value)[0][value]:
        lists = list(objs.values(value))[0][value].split("\n")
        for item in lists:
            data += """<p>{}</p>""".format(item)
    return data

def SetManytoManyField_inStrs(objs, value):
    data = ''
    if objs.values(value)[0][value]:
        lists = list(objs.values(value))[0][value].split("\n")
        for item in lists:
            data += """{}""".format(item)
    return data

@login_required
@check_permission(StatusCode["1407"])
def GetResumeInfoView(request, obj_id):
    if request.method == "GET":

        # 对象数据
        obj = models.ResumeInfo.objects.get(id=obj_id)
        objs= models.ResumeInfo.objects.filter(id=obj_id)

        # 格式化数据到标头
        objs_resume_source = list(objs.values("resume_source__name"))[0]["resume_source__name"]
        objs_upload_user = list(objs.values("upload_user__name"))[0]["upload_user__name"]
        objs_agent = list(objs.values("agent__name"))[0]["agent__name"]
        objs_zh_filename = list(objs.values("zh_filename__name"))[0]["zh_filename__name"]
        zh_filename_name = os.path.basename(objs_zh_filename)
        objs_en_filename = list(objs.values("en_filename__name"))[0]["en_filename__name"] if objs.values("en_filename__name") else ""
        if objs_en_filename:
            en_filename_name = os.path.basename(objs_en_filename)
        else:
            en_filename_name = ""

        # 工作/教育/项目 等经历格式化 Html 数据
        objs_work_info_ele = SetManytoManyField_inHTMLs(objs, "work_info__describe")
        objs_project_info_ele = SetManytoManyField_inHTMLs(objs, "project_info__describe")
        objs_education_info_ele = SetManytoManyField_inHTMLs(objs, "education_info__describe")
        objs_personal_assessment_ele = SetManytoManyField_inHTMLs(objs, "personal_assessment__describe")
        objs_personal_assessment_str = SetManytoManyField_inStrs(objs, "personal_assessment__describe")
        objs_comprehensive_ability_ele = SetManytoManyField_inHTMLs(objs, "comprehensive_ability__describe")

        # 获取 Resume Source Html
        obj_resume_source = models.ResumeSource.objects.all().values_list("name")
        ele = ""
        if obj_resume_source:
            for i in list(obj_resume_source):
                for j in i:
                    ele += "<option value={}>{}</option>".format(j, j)
        ele = mark_safe(ele)
        
        uid = obj_id

        form_obj = ResumeInfoFrom(instance=obj)
        
        # 评论
        comments_ele = ""
        for item in list(models.Comment.objects.filter(id__in=objs.values_list("user_comments", flat=True)).order_by("create_time").values("user", "create_time", "describe")):
            comments_ele += """<div class="inbox-item">
                <div class="inbox-item-img">
                    <img src="{}" class="rounded-circle" alt="">
                </div>
                <p class="inbox-item-author">{}</p>
                <p class="inbox-item-text"><pre>{}</pre></p>
                <p class="inbox-item-date">{}</p>
            </div>
            <hr>""".format(os.path.join("/static", models.UserProfile.objects.filter(id=item["user"]).values_list("head_portrait", flat=True)[0]), models.UserProfile.objects.get(id=item["user"]).name, item["describe"].replace("<", "&lt;").replace(">", "&gt;"),item["create_time"])
        comments_ele = mark_safe(comments_ele)

        # 订阅
        subscribe_obj = models.ResumeSubscription.objects.filter(user_id=request.user.id, resume_id=obj_id, status=True).exists()

        # 操作记录
        OperationRecords = models.EventLog.objects.filter(target_object=obj.uuid).order_by("-trigger_time").values("user__email", "trigger_time", "describe")
        
        ## 当前时间
        tz = pytz.timezone('Asia/Shanghai')
        _the_day_time = datetime.datetime.now(tz)

        ## Time 状态
        time_status = ["今天", "昨天", "三天内", "一周内", "一个月内", "三个月内", "一年内", "古老的时间"]
        operation_records_ele = ''
        operation_records_ele_the_day_time_title = """<article class="timeline-item alt">
                <div class="text-right">
                    <div class="time-show first">
                        <a href="#" class="btn btn-primary w-lg">操作时间</a>
                    </div>
                </div>
            </article>"""

        operation_records_ele += operation_records_ele_the_day_time_title
        operation_records_ele_template = """<article class="timeline-item {}">
                <div class="timeline-desk">
                    <div class="panel">
                        <div class="panel-body">
                            <span class="arrow-alt"></span>
                            <span class="timeline-icon"></span>
                            <h4 class="text-{}">{}</h4>
                            <p class="timeline-date text-muted"><small>{}</small></p>
                            <p>{}</p>
                        </div>
                    </div>
                </div>
            </article>"""

        # 调色板
        style_list = ["primary", "pink", "success", "danger", "warning", "info", "purple"]

        for index, item in enumerate(list(OperationRecords)):
            if (index % 2) == 0:
                operation_records_ele += operation_records_ele_template.format(
                    "",
                    style_list[index],
                    _TimeRange(_the_day_time, item["trigger_time"] + datetime.timedelta(hours=+8)), 
                    (item["trigger_time"] + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
                    item["describe"],
                )
            else:
                operation_records_ele += operation_records_ele_template.format(
                    "alt", 
                    style_list[index],
                    _TimeRange(_the_day_time, item["trigger_time"] + datetime.timedelta(hours=+8)), 
                    (item["trigger_time"] + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
                    item["describe"],
                )
            style_list.append(style_list[index])

        return render(request, 'resume-info.html', locals())

def DeleteCandidate(request, uid):
    ret = {"status": "seccuss", "status_code": "200"}
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    if request.method == "POST":

        obj = models.ResumeInfo.objects.filter(id=uid)
        _describe = EventCode.EventCode["Resume.Delete"]["zh"]["seccess"].format(request.user, obj.last().id, obj.last().username)
        _status = 1
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=obj.last().uuid, 
            user_id=request.user.id, 
            event_type=EventCode.EventCode["Resume.Delete"]["type"],
            label=EventCode.EventCode["Resume.Delete"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=request.user.uuid,
            target=obj.last().uuid,
        )
        obj.delete()

    return JsonResponse(ret)

def EditResumeView(request, uid):
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    data = {}
    MoreTable = {}
    for i in request.POST:
        if i == "comments":
            MoreTable[i] = request.POST.get(i, None)
        else:
            data[i] = request.POST.get(i, None)
    obj = models.ResumeInfo.objects.filter(id=uid)
    obj.update(**data)
    if 'comments' in MoreTable.keys():

        ct = models.Comment.objects.create(describe=MoreTable["comments"])
        obj.last().comments.clear()
        obj.last().comments.add(ct)

    ret = {"status": "seccuss", "status_code": "200"}
    return JsonResponse(ret)

# 评论
def SaveResumeCommands(request):
    ret = {"status": "seccuss", "status_code": "200"}
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    data = {}
    if request.method == "POST":
        for i in request.POST:
            if i in ("resume_id"):
                pass
            else:
                data[i] = request.POST.get(i)

        _query_resume = models.ResumeInfo.objects.filter(id=request.POST.get("resume_id")).first()
        
        data["uuid"] = _query_resume.uuid
        _obj = models.Comment.objects.create(**data)
        _query_resume.user_comments.add(_obj)
        
        _describe = EventCode.EventCode["Resume.Command"]["zh"]["seccess"].format(request.user,  _query_resume.username)
        _status = 1
        _event_record = tasks.CommonRecordEventLog.delay(
            uuid=_obj.uuid, 
            user_id=request.user.id, 
            event_type=EventCode.EventCode["Resume.Command"]["type"],
            label=EventCode.EventCode["Resume.Command"]["label"], 
            request=None, 
            response=None, 
            describe=_describe, 
            status=_status,
            access=_access,
            source=request.user.uuid,
            target=_obj.uuid,
        )
    else:
        ret["status_code"] = 403
        ret["status"] = "failed"
    return JsonResponse(ret)

# 收藏订阅
def ResumeSubscription(request):
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')

    ret = {"status": "seccuss", "status_code": "200", "event": "subscribe"}
    if request.method == "POST":
        unsubscribe =  True if request.POST.get("unsubscribe", False) == "True" else False
        if unsubscribe:
            obj = models.ResumeSubscription.objects.filter(user_id=request.user.id, resume_id=request.POST.get("sub_obj")).update(status=False)
            ret["event"] = "unsubscribe"
        else:
            obj = models.ResumeSubscription.objects.filter(user_id=request.user.id, resume_id=request.POST.get("sub_obj"))
            if not obj.exists():
                data = {"resume": models.ResumeInfo.objects.get(id=request.POST.get("sub_obj")), "user": request.user}
                models.ResumeSubscription.objects.create(**data)
            else:
                obj.update(status=True, trigger_time=datetime.datetime.now(tz))
    return JsonResponse(ret)
