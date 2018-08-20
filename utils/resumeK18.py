#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import requests
import os, time, json, sys
import importlib

import http.client as httplib
# import html2text
from lxml import html

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
importlib.reload(sys)

File_List = []

Path = '/Users/shilei/Desktop/jianli.2'
file_path = '/Users/shilei/Desktop/gui1.pdf'
username='u100049'
pwd = 'test20180621'
# username='u100207'
# pwd = 'hb20180810'
url = 'http://service.ygys.net/resumeservice.asmx?WSDL'

pool = ProcessPoolExecutor(5)

def upload_file(file_path):

    fileContent = open(file_path, 'rb').read()
    base64Str = base64.b64encode(fileContent).decode("utf-8")
    suffix = os.path.splitext(os.path.basename(file_path))[1]

    Data = '<?xml version="1.0" encoding="utf-8"?>'
    Data += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    Data += '<soap:Body>'
    Data += '<TransResumeByJsonStringForFileBase64 xmlns="http://tempuri.org/">'  # Interface name
    Data += '<username>{}</username>'.format(username)
    # username
    Data += '<pwd>{}</pwd>'.format(pwd)
    Data += '<content>' + base64Str + '</content>'  # The base64 string of the file
    Data += '<ext>' + suffix + '</ext>'
    # Extension name
    Data += '</TransResumeByJsonStringForFileBase64>'
    Data += '</soap:Body>'
    Data += '</soap:Envelope>'

    url = 'http://service.ygys.net/resumeservice.asmx?WSDL'
    headerdata = {'SOAPAction': 'http://tempuri.org/TransResumeByJsonStringForFileBase64',
                  'Content-Type': 'text/xml; charset=utf-8'}

    conn = httplib.HTTPConnection("service.ygys.net", 80)
    conn.request('POST', url, Data, headerdata)
    response = conn.getresponse()

    result = response.read()
    # result = response.read().decode('utf-8')
    # text = html2text.html2text(result)

    selector = html.fromstring(result)
    text = selector.xpath("//*/*/text()")

    filePath = file_path
    return write_file(filePath, text)

def write_file(filePath, text):
    # text = json.dumps(text)
    # print(type(text), "text")
    # print(json.loads(text))
    # requests.post("http://127.0.0.1:8088/k18resume.html", data={"content": json.loads(text), "filename": os.path.basename(fileName)})
    return filePath, text