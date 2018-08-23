#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.safestring import mark_safe

from repository import models
from Permission.Authentication import check_permission

import datetime, re, shutil, os, time, requests, json

from utils import SKLResumes
from utils import resumeK18
from utils import update_solr_data
from utils import CheckFileAndTranscoding
from utils import FileFormatToPDF
from Source import tasks

ret = {"status": "seccuss", "status_code": "200", "event": "add"}

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

        # 检测文件是否是 GB2312，如果是转成 UTF-8
        # CheckFileAndTranscoding.checkFileCoding(os.path.join(path, file_data.name))

        # 判断是否上传的是中文附件，如果是则解析，否则不解析
        if dataDir["update_file_type"] == "zh_filename":
            

            if 'update_resume_id' in dataDir.keys():
                tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), update_id=dataDir["update_resume_id"], resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=True, access=_access)
            else:
                tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=True, access=_access)
        else:
            tasks.AnalyseResume.delay(location=location, filePath=os.path.join(path, file_data.name), update_id=dataDir["update_resume_id"], resume_source=dataDir["resume_source"], upload_user_id=request.user.id, isAnalyse=False, access=_access)


    return JsonResponse(ret)