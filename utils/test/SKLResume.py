#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
import importlib
import requests
import os
import json
import time

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

importlib.reload(sys)

Path = '/Users/shilei/Desktop/jianli.1'
SavePath = '/Users/shilei/Desktop/jianli/'

API_Path = "http://cv-extract.com/api/extract"

File_List = []

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


def upload_file(url, attr, file_path):
    files = {attr: open(file_path, 'rb')}
    result = requests.post(url, files=files, timeout=15, verify=False)
    newFileName = os.path.splitext(os.path.basename(file_path))[0] + '.json'
    FilePath = os.path.dirname(file_path)
    newFilePath = os.path.join(FilePath, newFileName)
    return  write_file(newFilePath, result.text)


def write_file(fileName, text):
    with open(fileName, 'w') as f:
        f.write(text)

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



# if __name__ == "__main__":
#     getDirFile(Path)
#     for fileName in File_List:
#         #print(fileName.encode('utf-8'))
#         if os.path.basename(fileName).startswith == "txt":
#
#             pool.submit(upload_file, API_Path, 'content',  fileName)
#         else:
#             pool.submit(upload_file, API_Path, 'resume', fileName)
#     pool.shutdown(wait=True)

b = 0
getDirJson(Path)
for fileName in File_List:
    file_handler = open(fileName, 'rb')
    a = file_handler.read()
    pool.submit(requests.post("http://127.0.0.1:8088/sklresume.html", data={"content": a, "filename": os.path.basename(fileName)}))
    b += 1
pool.shutdown(wait=True)
print(b)