from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests, os, json, datetime, shutil
from utils import resumeK18
from Storage import K18AnalyseResumeDataStorage, upload_nginx
from django import conf
from repository import models
from Events.controller import common 
import pytz, uuid, requests
from Events import tasks, EventCode
from Notification import PushMessage

tz = pytz.timezone('Asia/Shanghai')

@shared_task
def AnalyseResume(location, filePath, resume_source, upload_user_id, access, isAnalyse=True, update_id=None):
	if isAnalyse:
		filePath, text = resumeK18.upload_file(filePath)
		if update_id:
			data={"location": location, "content": json.loads(text[0]), "filePath": filePath, "resume_source": resume_source, "update_resume_id": update_id, "upload_user": upload_user_id, "access": access}
		else:
			data={"location": location, "content": json.loads(text[0]), "filePath": filePath, "resume_source": resume_source, "upload_user": upload_user_id, "access": access}
		return AnalyseResumeStorageDatabase(data)
	else:
		data={"location": location, "filePath": filePath, "resume_source": resume_source, "update_resume_id": update_id, "upload_user": upload_user_id, "access": access}
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
			
			# 发送提示信息
			_SendNotification_Message = {"auth": models.UserProfile.objects.get(id=1).uuid, "target": models.UserProfile.objects.get(id=int(data["upload_user"])).uuid, "content": "custom|发现新的简历|{}上传了一份{}的简历，请刷新页面查阅新添加的简历.".format(models.UserProfile.objects.get(id=int(data['upload_user'])).email, base.username)}
			session = requests.get(url="http://{}{}".format(data["location"], "/notification/message/send"), params=_SendNotification_Message)
			
			# 发送通知
			_PushMessageData = {
				"to_user_id": int(data["upload_user"]),
				"from_user_id": 1,
				"title": "上传简历 {} 成功!".format(base.username),
				"describe": "简历 {} 上传成功，<a href='/resume/candidate/{}/change' target='_blank'>点击链接</a> 进入详细页面!".format(base.username, base.id)
			}
			PushMessage.PushMessage(to_user_id=_PushMessageData["to_user_id"], from_user_id=_PushMessageData["from_user_id"], title=_PushMessageData["title"], describe=_PushMessageData["describe"])
		
			# 默认简历有锁定期，则在一定时间内对简历进行默认解锁。
			run_time = models.SystemSetting.objects.get(name="AutoUnlockResume").num_value
			ResumeUnlock.apply_async((base.id,), countdown=run_time)

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
			_SendNotification_Message = {"auth": models.UserProfile.objects.get(id=1).uuid, "target": models.UserProfile.objects.get(id=int(data["upload_user"])).uuid, "content": "info|发现更新的简历|请刷新页面查阅新添加的简历."}
			session = requests.get(url="http://{}{}".format(data["location"], "/notification/message/send"), params=_SendNotification_Message)

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
	_file_md5 = json.loads(session)["md5"]

	# 回写上传地址到数据库
	if "content" in data.keys():
		if not "update_resume_id" in data.keys():
			_data = []
			_data.append(data["resume_source"])
			a = models.ResumeSource.objects.filter(name__in=_data)[0]
			b = models.ResumeName.objects.create(name=_url, create_time=datetime.datetime.now(), source=a, uuid=base.uuid, md5=_file_md5)
			base.zh_filename.add(b)
			base.resume_source.add(a)
		else:
			_data = []
			_data.append(data["resume_source"])
			a = models.ResumeSource.objects.filter(name__in=_data)[0]
			b = models.ResumeName.objects.create(name=_url, create_time=datetime.datetime.now(), source=a, uuid=base.uuid, md5=_file_md5)

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

		base.custom_label.add(2)

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

@shared_task
def ResumeUnlock(resume_id):
	
	objs = models.ResumeInfo.objects.filter(id=resume_id)
	for i in list(objs.values("agent__email")):
		if i["agent__email"] == None:
			objs[0].custom_label.remove(1)
			objs[0].custom_label.add(3)

