#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import os, time, requests, json,datetime, re
from django.utils.safestring import mark_safe

from Events import tasks, EventCode
import pytz, uuid, datetime

def TriggerStream(request):
	print(request.POST, request.GET)
	return HttpResponse("")