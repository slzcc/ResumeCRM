from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from RestAPI.views import (
	resume 
)

# RestAPI

urlpatterns = [

    re_path('^resume/candidate/(?P<uid>\d+)', resume.OneCandidateAllInfo, name="api-resume-OneCandidate-detailed-information"),

    re_path('^user/info/(?P<uid>\d+)$', resume.GetUserProfileInfo, name="api-user-info"),

]
