#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from repository import models
import datetime, re, os, time, requests, json, urllib
import uuid

ret = {"status": "seccuss", "status_code": "200", "event": "", "describe": ""}


def CommonRecordEventLog(uuid, user_id, event_type, label, describe, status=1, request=None, response=None):
	_event_type = models.StoredEventType.objects.filter(name=event_type)
	_user = models.UserProfile.objects.get(id=int(user_id))
	if not _event_type.exists():
		ret["status"] = "failed"
		ret["status_code"] = "404"
		ret["event"] = event_type + "." + label
		ret["describe"] = "Incorrect event logging"
		ret["uuid"] = uuid
		return ret
	data = {
		"uuid": uuid,
		"event_type": _event_type.last(),
		"label": label,
		"status": status,
		"user": _user,
		"describe": describe,
		"request": request,
		"response": response,
	}
	models.EventLog.objects.create(**data)
	ret["event"] = event_type + "." + label
	ret["describe"] = describe
	return ret