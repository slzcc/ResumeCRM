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
    location = request.get_host().split(":")[0]
    print(location)
    
    return render(request, 'test.html')