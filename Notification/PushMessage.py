#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from repository import models
import os, json, uuid

def PushMessage(notice_user_id, describe, origin_id=1):
	origin_user = models.UserProfile.objects.get(id=origin_id)

	data = {"uuid": uuid.uuid1(), "user": notice_user_id, "describe": describe}
	models.Notification.objects.create(**data)