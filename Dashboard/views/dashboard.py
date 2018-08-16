#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import datetime, re, shutil, json, os, time, requests
from django.utils.safestring import mark_safe

@login_required
def GetDashboard(request):
    if request.method == "GET":

        return render(request, 'dashboard.html', locals())
