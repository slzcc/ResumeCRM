#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from repository import models
import os, json, uuid

def PushMessage(to_user_id, describe, title, from_user_id=1):
	
	if to_user_id:
		to_user = models.UserProfile.objects.get(id=to_user_id)
	else:
		to_user = models.UserProfile.objects.get(id=1)
	from_user = models.UserProfile.objects.get(id=from_user_id)

	data = {
		"uuid": uuid.uuid1(), 
		"to_user": to_user, 
		"from_user": from_user, 
		"describe": describe, 
		"title": title
	}
	try:
		obj = models.Notification.objects.create(**data)
		return obj
	except:
		return False