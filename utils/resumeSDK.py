# coding: utf-8

import sys
import base64
import requests
import json
import traceback
import os

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(5)
File_List = []


def test_resume_parser(url, fname, uid, pwd):
    res_js = {}

    try:
        # 读取文件内容，构造请求
        cont = open(fname, 'rb').read()
        base_cont = base64.b64encode(cont)
        base_cont = base_cont.decode('utf-8') if sys.version.startswith('3') else base_cont  # 兼容python2与python3
        data = {'base_cont': base_cont,
                'fname': fname,
                'uid': uid,
                'pwd': str(pwd),
                }

        # 发送请求
        res = requests.post(url, data=json.dumps(data), auth=('admin', '2015'))

        # 解析结果
        res_js = json.loads(res.text)
        # print('result:\n%s\n' % (json.dumps(res_js, indent=2, ensure_ascii=False)))

        status = res_js['status']
        # if status['code'] == 200:
        #     print('usage_remaining: %d' % (res_js['account']['usage_remaining']))
        #     print('name: %s' % (res_js['result'].get('name', 'None')))
        #     print('parse resume <%s> succeeded' % (fname))
        # else:
        #     print('parse resume <%s> failed: code=<%d> msg=<%s>' % (fname, status['code'], status['message']))
    except:
        print('parse resume <%s> failed: %s' % (fname, traceback.format_exc()))
    # newFileName = os.path.splitext(os.path.basename(fname))[0] + '.json'
    # FilePath = os.path.dirname(fname)
    # newFilePath = os.path.join(FilePath, newFileName)
    # return write_file(newFilePath, res_js)
    return res_js


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

url = 'http://www.resumesdk.com/api/parse'
Path = '/Users/shilei/Desktop/jianli'
fname = u'/Users/shilei/Desktop/gui.pdf'  # 替换为你的文件名
fName = u"/Users/shilei/Desktop/jianli/html/resume4.json"

uid = 1805220  # 替换为你的用户名
pwd = '720683'  # 替换为你的密码（str格式）

# for fileName in File_List:
#     file_handler = open(fileName, 'rb')
#     print(file_handler, type(file_handler.read()))
    # pool.submit(requests.post("http://127.0.0.1:8088/addresume.html", data={"content": json.dumps(file_handler)}))

# res_js = test_resume_parser(url, fname, uid, pwd)
# print(res_js, type(res_js))

# print(os.path.basename(fName))


getDirJson(Path)
for fileName in File_List:
    file_handler = open(fileName, 'rb')
    a = file_handler.read()
    pool.submit(requests.post("http://127.0.0.1:8088/sdkresume.html", data={"content": a, "filename": os.path.basename(fileName)}))
pool.shutdown(wait=True)