from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Solr.views import (
	solr 
)

# Solr
urlpatterns = [

    re_path('^search/resume/list$', solr.SearchResumeList, name="solr-search-resume-list"),

]
