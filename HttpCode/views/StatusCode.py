#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
from Permission.Authentication import check_permission
import datetime, re, os, time, requests, json

def HttpCode_401(request):
	obj = models.UserProfile.objects.filter(is_staff=True).last()
	email = obj.email
	return render(request, 'http-code/pages-401.html', {"email": email})

def HttpCode_404(request):

	return render(request, 'http-code/pages-404.html')


def BasicConfiguration(request):
	return render(request, 'http-code/pages-404.html')

