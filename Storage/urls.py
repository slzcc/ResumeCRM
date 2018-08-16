
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Storage.views import K18AnalyseResumeDataStorage

## Storage
urlpatterns = [
    re_path('^resume/k18$', K18AnalyseResumeDataStorage.K18DataStorage, name="storage-analyse-resume-k18"),

]
