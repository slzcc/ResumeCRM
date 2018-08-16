#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
import importlib
import requests
import os
import json
import time
import random
import string
import shutil
from django import conf

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

importlib.reload(sys)

File_List = []
pool = ProcessPoolExecutor(5)

def copy_file(fileSource):
    fileSuffix = os.path.splitext(os.path.basename(fileSource))[1]
    fileName = ''.join(random.sample(string.ascii_letters + string.digits, 16)) + fileSuffix

    filePath = os.path.dirname(fileSource)
    newFilePath = os.path.join(filePath, fileName)
    shutil.copyfile(fileSource, newFilePath)
    return newFilePath

def upload_file(fileName):
    attr = 'resume'
    url = "http://cv-extract.com/api/extract"
    file_path = copy_file(fileName)
    if os.path.basename(file_path).startswith == "txt":
        attr = 'content'


    files = {attr: open(file_path, 'rb')}
    result = requests.post(url, files=files, timeout=15, verify=False)
    os.remove(file_path)
    # fileName = os.path.join(os.path.basename(os.path.dirname(fileName)), os.path.basename(fileName))
    fileName = os.path.join(os.path.basename(os.path.dirname(fileName)), os.path.basename(fileName))

    return  webhook_resume(fileName, result.text)


def webhook_resume(fileName, text):
    # access = requests.post("http://resume.shileizcc.com/sklresume.html", data={"content": text, "filename": fileName})
    # access = requests.post("http://127.0.0.1:8088/sklresume.html", data={"content": text, "filename": fileName})
    # access = requests.post("http://127.0.0.1:8088/sklresume.html", data={"content": text})
    return fileName,text
