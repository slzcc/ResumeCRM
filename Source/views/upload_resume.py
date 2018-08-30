#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.safestring import mark_safe

from repository import models
from Permission.Authentication import check_permission

import datetime, re, shutil, os, time, requests, json, hashlib

from utils import SKLResumes
from utils import resumeK18
from utils import update_solr_data
from utils import CheckFileAndTranscoding
from utils import FileFormatToPDF
from Source import tasks
from Notification import PushMessage

ret = {"status": "seccuss", "status_code": "200", "event": "add"}

def get_FileMD5(filePath):
    MD5_Object = hashlib.md5()
    maxbuf = 8192
    f = open(filePath,'rb')
    while True:
        buf = f.read(maxbuf)
        if not buf:
            break
        MD5_Object.update(buf)
    f.close()
    md5Code = MD5_Object.hexdigest()
    return  md5Code

def UploadResume(request):
    _access = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_REMOTE_ADD') or request.META.get('REMOTE_ADDR')
    location = request.get_host()
    
    if request.method == "POST":

        dataDir = {"update_file_type": "zh_filename"}

        for i in request.POST:
            dataDir[i] = request.POST.get(i, None)

        file_data = request.FILES.get("file", None)
        path = os.path.join(conf.settings.BASE_DIR, 'static', 'firmware', "temporary")

        # 如果目录不存在则创建
        if not os.path.exists(path): os.makedirs(path)

        # 把文件内容保存到本地
        f = open(os.path.join(path, file_data.name), 'wb')
        for line in file_data.chunks():
            f.write(line)
        f.close()

        # Check File MD5
        md5Str = get_FileMD5(os.path.join(path, file_data.name))
        _RESUME_NAME_DATABASE_QUERY = models.ResumeName.objects.filter(md5=md5Str)
        if _RESUME_NAME_DATABASE_QUERY.exists():
            ret["status_code"] = "307"
            ret["error"] = {}
            ret["error"]["title"] = "重复简历上传"
            ret["describe"] = "已发现此简历已经被上传过,文件为{},冲突简历ID为{}".format(file_data.name, _RESUME_NAME_DATABASE_QUERY[0].fne.values_list("id", flat=True)[0])
            
            # 发送提示信息
            _SendNotification_Message = {"auth": models.UserProfile.objects.get(id=1).uuid, "target": request.user.uuid, "content": "error|{}|{}".format(ret["error"]["title"], ret["describe"])}
            session = requests.get(url="http://{}{}".format(location, "/notification/message/send"), params=_SendNotification_Message)
            
            # 发送通知
            _PushMessageData = {
                "to_user_id": request.user.id,
                "from_user_id": 1,
                "title": ret["error"]["title"],
                "describe": ret["describe"] + ", <a href='/resume/candidate/{}/change' target='_blank'>点击链接</a> 跳转页面后进行查阅!".format(_RESUME_NAME_DATABASE_QUERY[0].fne.values_list("id", flat=True)[0])
            }
            PushMessage.PushMessage(to_user_id=_PushMessageData["to_user_id"], from_user_id=_PushMessageData["from_user_id"], title=_PushMessageData["title"], describe=_PushMessageData["describe"], notification_type=2)

            return JsonResponse(ret)
        
        # 检测文件是否是 GB2312，如果是转成 UTF-8
        # CheckFileAndTranscoding.checkFileCoding(os.path.join(path, file_data.name))

        if 'update_resume_id' in dataDir.keys():
            objs= models.ResumeInfo.objects.filter(id=int(dataDir["update_resume_id"]))
            if objs.values_list("agent", flat=True)[0]:
                owner = list(objs.values_list("agent__email", flat=True))[0]
                if not request.user.email == owner:
                    ret["status_code"] = "201"
                    ret["event"] = "edit"
                    ret["describe"] = "此份简历属于 {} , 操作被禁止!".format(owner)
                    ret["owner"] = owner
            return JsonResponse(ret)


        # 判断是否上传的是中文附件，如果是则解析，否则不解析
        if dataDir["update_file_type"] == "zh_filename":
            

            if 'update_resume_id' in dataDir.keys():
                tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), update_id=dataDir["update_resume_id"], resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=True, access=_access)
            else:
                tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=True, access=_access)
        else:
            tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), update_id=dataDir["update_resume_id"], resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=False, access=_access)


    return JsonResponse(ret)