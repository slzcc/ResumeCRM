
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Source.views import (
    CheckPDF, upload_resume
)

# Source

urlpatterns = [
  
    re_path('^checkPDF', CheckPDF.isExistPDF, name="source-check-pdf"),
    re_path('^upload/resume', upload_resume.UploadResume, name="source-upload-resume"),

]
