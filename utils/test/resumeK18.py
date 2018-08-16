#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import requests
import os, time, json, sys
import importlib

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
importlib.reload(sys)

File_List = []

Path = '/Users/shilei/Desktop/jianli.2'
file_path = '/Users/shilei/Desktop/gui1.pdf'
username='u100049'
pwd = '49test'
url = 'http://service.ygys.net/resumeservice.asmx?WSDL'

pool = ProcessPoolExecutor(5)

def getDirFile(path):
    fileList = os.listdir(path)

    for fileName in fileList:
        if fileName.startswith('.', 0, 1):
            continue

        fileAbs = os.path.join(path, fileName)
        if os.path.isdir(fileAbs):
            getDirFile(fileAbs)
        else:
            if not os.path.splitext(fileName)[1] == '.json':
                File_List.append(fileAbs)

def getDirJson(path):
    fileList = os.listdir(path)

    for fileName in fileList:
        if fileName.startswith('.', 0, 1):
            continue

        fileAbs = os.path.join(path, fileName)
        if os.path.isdir(fileAbs):
            getDirJson(fileAbs)
        else:
            if os.path.splitext(fileName)[1] == '.json':
                File_List.append(fileAbs)

# from suds.client import Client
# def getFile(file_path):
#     fileContent = open(file_path, 'rb').read()
#     base64Str = base64.b64encode(fileContent)
#     client = Client(url)
#     result = client.service.TransResumeByJsonStringForFileBase64(username, pwd, base64Str, os.path.splitext(os.path.basename(file_path))[1])
#     newFileName = os.path.splitext(os.path.basename(file_path))[0] + '.json'
#     FilePath = os.path.dirname(file_path)
#     newFilePath = os.path.join(FilePath, newFileName)
#     return write_file(newFilePath, result)

def write_file(fileName, text):
    return fileName, text

b = 0
getDirJson(Path)
for fileName in File_List:
    file_handler = open(fileName, 'rb').read()
    # print(json.loads(file_handler))
    pool.submit(requests.post("http://127.0.0.1:8088/k18resume.html", data={"content": file_handler, "filename": os.path.basename(fileName)}))
    b += 1
pool.shutdown(wait=True)
print(b)
