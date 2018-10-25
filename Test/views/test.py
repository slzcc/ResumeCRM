#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django import conf

from repository import models
import datetime, re
import os, time, requests
from django.utils.safestring import mark_safe

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from celery.result import AsyncResult


from django.conf.urls import url, include
from django.urls.resolvers import RegexPattern


from django.views import View
# from web.handlers import cors_allow_mysites

class TestView(View):

    def get(self, request, *args, **kwargs):
        # return HttpResponse('Hello, World!')
        return render(request, 'test/test.html')

# from reportlab.pdfgen import canvas
from django.http import HttpResponse


def testpdf2(request, DirName, BaseName):

	# pdf 的绝对路径
	path = os.path.join(conf.settings.BASE_DIR,'static','firmware-pdf', DirName, BaseName)

	# 打开 pdf 文件
	with open(path, 'rb') as pdfExtract:
		response = HttpResponse(pdfExtract.read(), content_type='application/pdf')

		# 直接让浏览器下载
		# response['Content-Disposition'] = 'attachment; filename="extracted_page_{}.pdf"'.format(page_num)

		# 让浏览器展示 pdf
		response['Content-Disposition'] = 'filename="{}"'.format(BaseName)

	# 返回给前端
	return response



def testpdf(request, date_pash,file_name):
    # Create the HttpResponse object with the appropriate PDF headers.
    path = os.path.join(conf.settings.BASE_DIR,'static','firmware-pdf', date_pash, file_name)
    print(path)
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename='+path
    response['Content-Disposition'] = 'filename='+path

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


from Test.tasks import add
from celery.result import AsyncResult
  
 
    

def test(request):
    # a = add.delay(123,123)
    # # a.get()                   # 直接获取数据，如果数据执行过程中较慢，则会阻塞
    # ret = AsyncResult(id=a.id)  # 间接获取数据，则需要首先获取这个任务的 id，然后通过 id 获取执行结果
    # print(ret.get())
    # location = request.get_host().split(":")[0]
    # print(location)
    path = os.path.join(conf.settings.BASE_DIR, 'static', 'firmware', "temporary", "resume", "source")
    check_list = [1, 2, 5, 6, 6, 13, 16, 17, 18, 19, 22, 23, 28, 30, 32, 34, 36, 38]

    cvs_list = [
        "username", 
        "age", 
        "phone", 
        "email", 
        "gender", 
        "place_residence", 
        "old_company", 
        "old_jobs", 
        "jobs", 
        "salary", 
        "graduated_school", 
        "degree", 
        "professional",
        "work_info",
        "project_info",
        "education_info",
        "comprehensive_ability",
        "personal_assessment",
    ]
    # cvs_title = ""

    # for index, i in enumerate(cvs_list):
    #     if not (index + 1) == len(cvs_list):
    #         cvs_title += i + ", "
    #     else:
    #         cvs_title += i

    # file_s = open(os.path.join(path, "demo.csv"), 'w+')
    # file_s.write(cvs_title)

    cvs_list_zh = ["姓名", "年龄", "电话", "邮箱", "性别", "居住地", "上家公司", "上一份工作", "应聘岗位", "所需薪资", "毕业学习", "文凭", "所学专业"]
    



    import csv
    with open(os.path.join(path, "demo.csv"), 'w', newline='') as f:
        # 标头在这里传入，作为第一行数据
        writer = csv.DictWriter(f, cvs_list)
        writer.writeheader()
        for index in range(1, 40):
            if not index in check_list:
                object_num = "1000"
                if len(str(index)) == 1:
                    object_num = object_num  + str("0" + str(index))
                else:
                    object_num = object_num + str(index)
                session = requests.get(url="http://"+ request.get_host() + "/api/resume/candidate/"+ object_num)
                data = json.loads(session.text)
                datas = {}
                datas["username"] = data["username"]
                datas["age"] = data["age"]
                datas["phone"] = data["phone"]
                datas["email"] = data["email"]
                datas["gender"] = data["gender"]
                datas["place_residence"] = data["place_residence"]
                datas["old_company"] = data["old_company"]
                datas["old_jobs"] = data["old_jobs"]
                datas["jobs"] = data["jobs"]
                datas["salary"] = data["salary"]
                datas["graduated_school"] = data["graduated_school"]
                datas["degree"] = data["degree"]
                datas["professional"] = data["professional"]
                datas["work_info"] = data["work_info"][0]["describe"] if "work_info" in data.keys() else ""
                datas["project_info"] = data["project_info"][0]["describe"] if "project_info" in data.keys() else "" 
                datas["education_info"] = data["education_info"][0]["describe"] if "education_info" in data.keys() else "" 
                datas["comprehensive_ability"] = data["comprehensive_ability"][0]["describe"] if "comprehensive_ability" in data.keys() else ""
                datas["personal_assessment"] = data["personal_assessment"][0]["describe"] if "personal_assessment" in data.keys() else ""

                writer.writerow(datas)
                # writer.writerows(datas)




    # for index in range(1, 40):
    #     if not index in check_list:
    #         object_num = "1000"
    #         if len(str(index)) == 1:
    #             object_num = object_num  + str("0" + str(index))
    #         else:
    #             object_num = object_num + str(index)
    #         session = requests.get(url="http://"+ request.get_host() + "/api/resume/candidate/"+ object_num)
    #         data = json.loads(session.text)
    #         cvs_str = ""
    #         cvs_str += str(data["username"]) + ", "
    #         cvs_str += str(data["age"]) + ", "
    #         cvs_str += str(data["phone"]) + ", "
    #         cvs_str += str(data["email"]) + ", "
    #         cvs_str += str(data["gender"]) + ", "
    #         cvs_str += str(data["place_residence"]) + ", "
    #         cvs_str += str(data["old_company"]) + ", "
    #         cvs_str += str(data["old_jobs"]) + ", "
    #         cvs_str += str(data["jobs"]) + ", "
    #         cvs_str += str(data["salary"]) + ", "
    #         cvs_str += str(data["graduated_school"]) + ", "
    #         cvs_str += str(data["degree"]) + ", "
    #         cvs_str += str(data["professional"])
    #         # cvs_str += ("\"" + str(data["work_info"][0]["describe"]) + "\"") if data["work_info"] else ""
            # cvs_str += ("\"" + str(data["project_info"][0]["describe"]) + "\"") if data["project_info"] else "" 
            # cvs_str += str(data["education_info"][0]["describe"]) if data["education_info"] else "" 
            # cvs_str += str(data["comprehensive_ability"][0]["describe"]) if data["comprehensive_ability"] else ""
            # cvs_str += str(data["personal_assessment"][0]["describe"]) if data["personal_assessment"] else ""

    #         file_s.write("\n")
    #         file_s.write(cvs_str)
                # if type(v) == list:

                #     if k == "work_info":
                #         writeData["WorkExperience"] = v[0][""describe""]

                #     if k == "project_info":
                #         writeData["ProjectExperience"] = v[0][""describe""]

                #     if k == "personal_assessment":
                #         writeData["SelfAssessment"] = v[0][""describe""]

                #     if k == "education_info":
                #         writeData["EducationExperience"] = v[0][""describe""]

                #     if k == "comprehensive_ability":
                #         writeData["ComprehensiveAbility"] = v[0][""describe""]
    return render(request, 'test.html')