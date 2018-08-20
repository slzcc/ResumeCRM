#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import conf
from repository import models
from celery import shared_task
from websocket import create_connection

@shared_task
def SendWebSocketNotificationTasks(url, content=None):
	ws = create_connection(url)
	ws.send(content)
	ws.close()
