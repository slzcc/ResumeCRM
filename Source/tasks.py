from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests, os, json, datetime, shutil
from utils import resumeK18
from Storage import K18AnalyseResumeDataStorage, upload_nginx
from django import conf
from repository import models
from Events.controller import common 
import pytz, uuid
from Events import tasks, EventCode
tz = pytz.timezone('Asia/Shanghai')

@shared_task
def AnalyseResume(filePath, resume_source, upload_user_id, access, isAnalyse=True, update_id=None):
	if isAnalyse:
		filePath, text = resumeK18.upload_file(filePath)
		if update_id:
			data={"content": json.loads(text[0]), "filePath": filePath, "resume_source": resume_source, "update_resume_id": update_id, "upload_user": upload_user_id, "access": access}
		else:
			data={"content": json.loads(text[0]), "filePath": filePath, "resume_source": resume_source, "upload_user": upload_user_id, "access": access}
		return AnalyseResumeStorageDatabase(data)
	else:
		data={"filePath": filePath, "resume_source": resume_source, "update_resume_id": update_id, "upload_user": upload_user_id, "access": access}
		return AnalyseResumeStorageDatabase(data)

@shared_task
def AnalyseResumeStorageDatabase(data):
    
    # 存储数据到数据库
	if "content" in data.keys():
		base = K18AnalyseResumeDataStorage.K18DataStorage(data)
		
		if base and not "update_resume_id" in data.keys():
			_describe = EventCode.EventCode["Resume.Create"]["zh"]["seccess"].format(models.UserProfile.objects.get(id=int(data["upload_user"])),  base.id, base.username)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=base.uuid, 
				user_id=data["upload_user"], 
				event_type=EventCode.EventCode["Resume.Create"]["type"],
				label=EventCode.EventCode["Resume.Create"]["label"],
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=data["access"],
				source=models.UserProfile.objects.get(id=data["upload_user"]).uuid,
				target=base.uuid,
			)
		else:
			_describe = EventCode.EventCode["Resume.Update.ZH.Attachment"]["zh"]["seccess"].format(models.UserProfile.objects.get(id=int(data["upload_user"])),  base.id, base.username)
			_status = 1
			_event_record = tasks.CommonRecordEventLog.delay(
				uuid=base.uuid,
				user_id=data["upload_user"], 
				event_type=EventCode.EventCode["Resume.Update.ZH.Attachment"]["type"],
				label=EventCode.EventCode["Resume.Update.ZH.Attachment"]["label"],
				request=None, 
				response=None, 
				describe=_describe, 
				status=_status,
				access=data["access"],
				source=models.UserProfile.objects.get(id=data["upload_user"]).uuid,
				target=base.uuid,
			)

	else:
		base = models.ResumeInfo.objects.filter(id=data["update_resume_id"]).last()

	# 目标文件名，统一文件名
	suffix = os.path.splitext(os.path.basename(data["filePath"]))[1]
	# 暂不支持中文你文件名
	# targetFileName = base.username + suffix
	targetFileName = str(base.id) + suffix

	# 把本地文件名称进行修改，为上传后的文件名作统一规划
	targetPath = os.path.join(os.path.dirname(data["filePath"]), str(base.id))

	if not os.path.exists(targetPath):
		os.makedirs(targetPath)

	targetFilePath = os.path.join(targetPath, targetFileName)
	shutil.move(data["filePath"], targetFilePath)
	
	if "content" in data.keys():
		storagePath = os.path.join("firmware/resume", str(base.id), "zh")
	else:
		storagePath = os.path.join("firmware/resume", str(base.id), "en")

	# 上传文件
	session = upload_nginx.UploadNginx(url=conf.settings.NGINX_UPLOAD_ADDRESS, fileName=targetFileName, filePath=targetFilePath, storagePath=storagePath)
	_url = "/".join(json.loads(session)["account_url"].split("/")[3:])

	# 回写上传地址到数据库
	if "content" in data.keys():
		if not "update_resume_id" in data.keys():
			_data = []
			_data.append(data["resume_source"])
			a = models.ResumeSource.objects.filter(name__in=_data)[0]
			b = models.ResumeName.objects.create(name=_url, create_time=datetime.datetime.now(), source=a)
			base.zh_filename.add(b)
			base.resume_source.add(a)
		else:
			_data = []
			_data.append(data["resume_source"])
			a = models.ResumeSource.objects.filter(name__in=_data)[0]
			b = models.ResumeName.objects.create(name=_url, create_time=datetime.datetime.now(), source=a)

			base.resume_source.clear()
			base.zh_filename.clear()

			base.zh_filename.add(b)
			base.resume_source.add(a)

	else:
		_data = []
		_data.append(data["resume_source"])
		a = models.ResumeSource.objects.filter(name__in=_data)[0]
		b = models.ResumeName.objects.create(name=_url, create_time=datetime.datetime.now(), source=a)

		base.en_filename.clear()
		base.en_filename.add(b)

		_describe = EventCode.EventCode["Resume.Update.EN.Attachment"]["zh"]["seccess"].format(models.UserProfile.objects.get(id=int(data["upload_user"])),  base.id, base.username)
		_status = 1
		_event_record = tasks.CommonRecordEventLog.delay(
			uuid=base.uuid, 
			user_id=data["upload_user"], 
			event_type=EventCode.EventCode["Resume.Update.EN.Attachment"]["type"],
			label=EventCode.EventCode["Resume.Update.EN.Attachment"]["label"],
			request=None, 
			response=None, 
			describe=_describe, 
			status=_status,
			access=data["access"],
			source=models.UserProfile.objects.get(id=data["upload_user"]).uuid,
			target=base.uuid,
		)
