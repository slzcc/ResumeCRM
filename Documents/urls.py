
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from Documents.views import (
	export, download
)

# Documents
urlpatterns = [
    re_path('^export/word/(\d+)$', export.GenerateWordDocument, name="documents-export-word"),
    re_path('^download/word$', download.DownloadWordFile, name="documents-download-word"),
    re_path('^download/resume/source$', download.DownloadSourceResume, name="documents-download-source-resume"),

]
