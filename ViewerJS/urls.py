
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from ViewerJS.views import viewerjs


# ViewerJS

urlpatterns = [
   
    re_path('^index.html', viewerjs.ViewerJSInterface, name="viewerjs-index"),
    re_path('^AccessFiles', viewerjs.ViewerJSAccessFiles, name="viewerjs-access-files"),
  
]
