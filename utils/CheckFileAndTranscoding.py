#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import os, time, json, sys
import importlib
import chardet
import shutil

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
importlib.reload(sys)


# Path = "/Users/shilei/Desktop/jianli5"

# checkFileListPath= "/Users/shilei/Documents/PyCharm/Django/ResumeCRM/utils/.check_file_list.txt"
# processedFileListPath = "/Users/shilei/Documents/PyCharm/Django/ResumeCRM/utils/.processed_file_list.txt"
# FileList = []

# ProcessedFile = []

# def checkFileList(checkFileListPath, processedFileListPath):
# 	with open(processedFileListPath) as pf:
# 		processedFileList = pf.read().strip().split("\n")
# 	with open(checkFileListPath, 'r+') as cf:
# 		for FileName in cf.read().strip().split("\n"):
# 			if not FileName in processedFileList:
# 				checkFileCoding(FileName)
# 				with open(processedFileListPath, 'a') as pf:
# 					pf.write(FileName + "\n")

def checkFileCoding(file):
	if os.path.splitext(os.path.basename(file))[1] in [".txt"]:
		try:
			with open(file, 'r', encoding='gbk') as f:
				SourceContent = f.read()
			os.remove(file)
			with open(file, 'w', encoding='utf-8') as f:
				f.write(SourceContent)
		except UnicodeDecodeError:
			pass
	else:
		return

		# with open(i, 'rb') as f:
		# 	SourceContent = f.read()
		# 	# chardet.detect(f.read()) = {'confidence': 0.99, 'encoding': 'GB2312', 'language': 'Chinese'}
		# print("FileName: {} Coding: {}".format(i,chardet.detect(SourceContent)["encoding"]))
		# # if chardet.detect(SourceContent)["encoding"] != "utf-8":
		# if chardet.detect(SourceContent)["encoding"] and chardet.detect(SourceContent)["encoding"] in ("GB2312"):
		# 	with open(i, 'wb') as f:
		# 		f.write(SourceContent.decode("utf-8")) 
		# 		ProcessedFile.append(i)


# checkFileList(checkFileListPath, processedFileListPath)



	    

