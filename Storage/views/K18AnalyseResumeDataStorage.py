#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission

import datetime, re, shutil
import os, time, requests
from django.utils.safestring import mark_safe

from utils import SKLResumes
from utils import resumeK18
from utils import update_solr_data
from utils import CheckFileAndTranscoding
from utils import FileFormatToPDF
ret = {"status": "seccuss", "status_code": "200", "event": "add"}


def K18DataStorage(request):

    if request.method == "POST":
        data = {}
        result = {"content": ""}
        MoreTable = {}
        for i in request.POST:
            if i == "content" and i :
                result[i] = json.loads(request.POST.get(i, None))
            else:
                result[i] = request.POST.get(i, None)
        
        MoreTable["raw_text"] = ""
        MoreTable["comprehensive_ability"] = ""
        data["language"] = ""

        if result["content"]:
            for k, v in result.items():
                if k == "content":
                    for j, l in v.items():
                        if l:

                            # 单表
                            data["create_time"] = datetime.datetime.now()
                            # data["cnterview_time"] = datetime.datetime.now()
                            data["modify_time"] = datetime.datetime.now()


                            if j == "Brith":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                _re_nian = re.findall("年", l)
                                _re_yue = re.findall("月", l)
                                _re_ri = re.findall("日", l)
                                if _re_nian:
                                    l = l.replace("年", '-')

                                if _re_yue:
                                    l = l.replace("月", '-')

                                if _re_ri:
                                    l = l.replace("日", '')

                                if re.findall("-$", l):
                                    l += "01"

                                data["birthday"] = l

                            if j == "Education":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["degree"] = l

                            if j == "Experience":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["work_time"] = l

                            if j == "Name":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["username"] = l

                            if j == "Married":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                if l == u"未婚":
                                    l = False
                                elif l == u"已婚":
                                    l = True
                                elif l == u"保密":
                                    l = False
                                else:
                                    l = False
                                data["marital_status"] = l

                            if j == "QQ":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["qq"] = l

                            if j == "School":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["graduated_school"] = l

                            if j == "Speciality":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["professional"] = l

                            if j == "Sex":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                if l == u"男":
                                    l = True
                                elif l == u"女":
                                    l = False

                                data["gender"] = l

                            if j == "Age":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["age"] = l

                            if j == "AimSalary":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["salary"] = l

                            if j == "Email":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["email"] = l

                            if j == "Mobile":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["phone"] = l

                            if j == "NowLocation":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["place_residence"] = l

                            if j == "Jiguan":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["origin"] = l

                            if j == "High":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["high"] = l

                            if j == "Title":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["jobs"] = l

                            if j == "LastTitle":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["old_jobs"] = l

                            if j == "StudentType":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["learning_type"] = l

                            if j == "LastCompany":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["old_company"] = l

                            if j == "Forwardlocation":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["job_addr"] = l

                            if j == "StartFrom":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                data["duty_time"] = l

                            if j == "WorkType":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                if l == "全职":
                                    l = True
                                else:
                                    l = False

                                data["nature_work"] = l

                            if j == "Switch":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + l + "\t"
                                if l == "离职":
                                    l = True
                                elif l == "正在找工作":
                                    l = True
                                elif l == "在职":
                                    l = False
                                data["current_situation"] = l

                            if j == "LanguagesSkills":
                                for o in l:
                                    for k, v in o.items():
                                        if k == "Languages":
                                            data["language"] = data["language"] + v + "\t"

                            # 多表
                            if j == "English":
                                MoreTable["comprehensive_ability"] = MoreTable["comprehensive_ability"] + l + "\t"
                                MoreTable["comprehensive_ability"] += "\n"

                            if j == "Skill":
                                MoreTable["comprehensive_ability"] = MoreTable["comprehensive_ability"] + l

                            if j == "ArrEducationDetail":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                                MoreTable["education_info"] = "".join(l)

                            if j == "ArrExpericeneDetail":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                                MoreTable["work_info"] = "".join(l)

                            if j == "ArrProjectDetail":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                                MoreTable["project_info"] = "".join(l)

                            if j == "Personal":
                                MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                                MoreTable["personal_assessment"] = "".join(l)

                            if j == "upload_user":
                                 MoreTable["upload_user"] = l
                        
            if "update_resume_id" in result.keys():
                base = models.ResumeInfo.objects.filter(id=result["update_resume_id"])
                base.update(**data)
                base = base.last()

                if "personal_assessment" in MoreTable.keys():
                    personal_assessment = models.PersonalAssessment.objects.create(describe=MoreTable["personal_assessment"])
                    base.personal_assessment.clear()
                    base.personal_assessment.add(personal_assessment)
                if "work_info" in MoreTable.keys():
                    work_info = models.WorkInfo.objects.create(describe=MoreTable["work_info"])
                    base.work_info.clear()
                    base.work_info.add(work_info)
                if "education_info" in MoreTable.keys():
                    education_info = models.EducationInfo.objects.create(describe=MoreTable["education_info"])
                    base.education_info.clear()
                    base.education_info.add(education_info)
                if "project_info" in MoreTable.keys():
                    project_info = models.ProjectInfo.objects.create(describe=MoreTable["project_info"])
                    base.project_info.clear()
                    base.project_info.add(project_info)
                if "raw_text" in MoreTable.keys():
                    raw_text = models.ResumeSourceText.objects.create(describe=MoreTable["raw_text"])
                    base.raw_text.clear()
                    base.raw_text.add(raw_text)
                if "resume_source" in result.keys():
                    data = []
                    data.append(result["resume_source"])
                    a = models.ResumeSource.objects.filter(name__in=data)[0]
                    b = models.ResumeName.objects.create(name=result["filename"], create_time=datetime.datetime.now(), source=a)

                    base.resume_source.clear()
                    base.zh_filename.clear()

                    base.zh_filename.add(b)
                    base.resume_source.add(a)

                if "comprehensive_ability" in MoreTable.keys():
                    comprehensive_ability = models.ComprehensiveAbility.objects.create(describe=MoreTable["comprehensive_ability"])
                    base.comprehensive_ability.clear()
                    base.comprehensive_ability.add(comprehensive_ability)

                if "upload_user" in MoreTable.keys():
                    upload_user = models.UserProfile.objects.get(id=MoreTable["upload_user"])

                    base.upload_user.clear()
                    base.agent.clear()
                    
                    base.upload_user.add(upload_user)
                    base.agent.add(upload_user)

            else:
                if "username" in data.keys():
                    base = models.ResumeInfo.objects.create(**data)

                    if "personal_assessment" in MoreTable.keys():
                        personal_assessment = models.PersonalAssessment.objects.create(describe=MoreTable["personal_assessment"])
                        base.personal_assessment.add(personal_assessment)
                    if "work_info" in MoreTable.keys():
                        work_info = models.WorkInfo.objects.create(describe=MoreTable["work_info"])
                        base.work_info.add(work_info)
                    if "education_info" in MoreTable.keys():
                        education_info = models.EducationInfo.objects.create(describe=MoreTable["education_info"])
                        base.education_info.add(education_info)
                    if "project_info" in MoreTable.keys():
                        project_info = models.ProjectInfo.objects.create(describe=MoreTable["project_info"])
                        base.project_info.add(project_info)
                    if "raw_text" in MoreTable.keys():
                        raw_text = models.ResumeSourceText.objects.create(describe=MoreTable["raw_text"])
                        base.raw_text.add(raw_text)
                    if "resume_source" in result:
                        data = []
                        data.append(result["resume_source"])
                        a = models.ResumeSource.objects.filter(name__in=data)[0]
                        b = models.ResumeName.objects.create(name=result["filename"], create_time=datetime.datetime.now(), source=a)
                        base.zh_filename.add(b)
                        base.resume_source.add(a)
                    if "comprehensive_ability" in MoreTable.keys():
                        comprehensive_ability = models.ComprehensiveAbility.objects.create(describe=MoreTable["comprehensive_ability"])
                        base.comprehensive_ability.add(comprehensive_ability)

                    if "upload_user" in MoreTable.keys():
                        upload_user = models.UserProfile.objects.get(id=MoreTable["upload_user"])
                        base.upload_user.add(upload_user)
                        base.agent.add(upload_user)

        else:
            if "update_resume_id" in result.keys():
                base = models.ResumeInfo.objects.filter(id=result["update_resume_id"])
                base = base.last()

                if "resume_source" in result.keys():
                    data = []
                    data.append(result["resume_source"])
                    a = models.ResumeSource.objects.filter(name__in=data)[0]
                    b = models.ResumeName.objects.create(name=result["filename"], create_time=datetime.datetime.now(), source=a)

                    base.en_filename.clear()
                    base.en_filename.add(b)
    return JsonResponse(ret)