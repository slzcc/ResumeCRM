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

ret = {"status": "seccuss", "status_code": "200", "event": "add"}

def K18ResumeAnalyse(request):
    
    if request.method == "POST":

        dataDir = {"update_file_type": "zh_filename"}

        for i in request.POST:
            dataDir[i] = request.POST.get(i, None)

        file_data = request.FILES.get("file", None)
        sub_path = time.strftime("%Y-%m-%d", time.gmtime(time.time()))
        path = os.path.join(conf.settings.BASE_DIR, 'static', 'firmware', sub_path)
        isExists = os.path.exists(path)
        if not isExists: os.makedirs(path)

        # 把文件内容保存到本地
        f = open(os.path.join(path, file_data.name), 'wb')
        for line in file_data.chunks():
            f.write(line)
        f.close()

        # 检测文件是否是 GB2312，如果是转成 UTF-8
        CheckFileAndTranscoding.checkFileCoding(os.path.join(path, file_data.name))

        # 判断是否上传的是中文附件，如果是则解析，否则不解析
        if dataDir["update_file_type"] == "zh_filename":
            fileName, text = resumeK18.upload_file(os.path.join(path, file_data.name))

            if 'update_resume_id' in dataDir.keys():
                access = requests.post("http://"+ request.get_host() + "/storage/resume/k18", data={"content": text, "filename": fileName, "resume_source": dataDir["resume_source"], "update_resume_id": dataDir["update_resume_id"], "upload_user": request.user.id})

                ret["event"] = "update"
                return JsonResponse(ret)
            else:
                access = requests.post("http://"+ request.get_host() + "/storage/resume/k18", data={"content": text, "filename": fileName, "resume_source": dataDir["resume_source"], "upload_user": request.user.id})
                return JsonResponse(ret)
        else:
            access = requests.post("http://"+ request.get_host() + "/storage/resume/k18", data={"filename": os.path.join(sub_path, file_data.name), "resume_source": dataDir["resume_source"], "update_resume_id": dataDir["update_resume_id"], "upload_user": request.user.id})
            return JsonResponse(ret)

    return JsonResponse(ret)