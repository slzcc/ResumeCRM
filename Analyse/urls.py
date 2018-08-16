
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Analyse.views import k18

# Analyse

urlpatterns = [

    re_path('^resume/k18$', k18.K18ResumeAnalyse, name="analyse-resume-k18"),
 
]
