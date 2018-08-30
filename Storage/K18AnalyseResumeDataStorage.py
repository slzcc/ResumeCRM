#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models
import datetime, re, shutil, os, time, requests, json, uuid
import pytz
tz = pytz.timezone('Asia/Shanghai')

def K18DataStorage(SourceData):

    data = {}
    data["language"] = ""
    if "update_resume_id" in SourceData.keys():
        base = models.ResumeInfo.objects.filter(id=SourceData["update_resume_id"])
        data["uuid"] = base[0].uuid
    else:
        data["uuid"] = uuid.uuid1()
    

    MoreTable = {}
    MoreTable["raw_text"] = ""
    MoreTable["comprehensive_ability"] = ""
   
                    
    if "content" in SourceData.keys():
        for j, l in SourceData["content"].items():
            if l:
                # 单表
                data["create_time"] = datetime.datetime.now(tz)
                # data["cnterview_time"] = datetime.datetime.now(tz)
                data["modify_time"] = datetime.datetime.now(tz)

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
                    MoreTable["comprehensive_ability"] = MoreTable["comprehensive_ability"].replace("\r", '').replace("\n\n", '\n')
                    
                if j == "ArrEducationDetail":
                    MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                    MoreTable["education_info"] = "".join(l)
                    MoreTable["education_info"] = MoreTable["education_info"].replace("\r", '').replace("\n\n", '\n')

                if j == "ArrExpericeneDetail":
                    MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                    MoreTable["work_info"] = "".join(l)
                    MoreTable["work_info"] = MoreTable["work_info"].replace("\r", '').replace("\n\n", '\n')

                if j == "ArrProjectDetail":
                    MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                    MoreTable["project_info"] = "".join(l)
                    MoreTable["project_info"] = MoreTable["project_info"].replace("\r", '').replace("\n\n", '\n')

                if j == "Personal":
                    MoreTable["raw_text"] = MoreTable["raw_text"] + "".join(l) + "\t"
                    MoreTable["personal_assessment"] = "".join(l)
                    MoreTable["personal_assessment"] = MoreTable["personal_assessment"].replace("\r", '').replace("\n\n", '\n')
                    
        if "upload_user" in SourceData.keys():
            MoreTable["upload_user"] = SourceData["upload_user"]
            # print("MoreTable", MoreTable["upload_user"])

        if "update_resume_id" in SourceData.keys():
            
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

            if "comprehensive_ability" in MoreTable.keys():
                comprehensive_ability = models.ComprehensiveAbility.objects.create(describe=MoreTable["comprehensive_ability"])
                base.comprehensive_ability.clear()
                base.comprehensive_ability.add(comprehensive_ability)

            if "upload_user" in MoreTable.keys():
                upload_user = models.UserProfile.objects.get(id=MoreTable["upload_user"])

                base.upload_user.clear()
                # base.agent.clear()
                
                base.upload_user.add(upload_user)
                # base.agent.add(upload_user)

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
                if "comprehensive_ability" in MoreTable.keys():
                    comprehensive_ability = models.ComprehensiveAbility.objects.create(describe=MoreTable["comprehensive_ability"])
                    base.comprehensive_ability.add(comprehensive_ability)

                if "upload_user" in MoreTable.keys():
                    upload_user = models.UserProfile.objects.get(id=MoreTable["upload_user"])
                    base.upload_user.add(upload_user)
                    # base.agent.add(upload_user) 

                base.custom_label.set([1])

    return base