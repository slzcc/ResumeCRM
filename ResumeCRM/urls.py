"""ResumeCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from Dashboard.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^resume/', include('Resume.urls')),
    re_path('^api/', include('RestAPI.urls')),
    re_path('^user/', include('Users.urls')),
    re_path('^storage/', include('Storage.urls')),
    re_path('^solr/', include('Solr.urls')),
    re_path('^analyse/', include('Analyse.urls')),
    re_path('^system/', include('System.urls')),
    re_path('^permission/', include('Permission.urls')),
    re_path('^ViewerJS/', include('ViewerJS.urls')),
    re_path('^source/', include('Source.urls')),
    re_path('^documents/', include('Documents.urls')),
    re_path('^initialize/', include('Initialize.urls')),
    re_path('^test/', include('Test.urls')),
    re_path('^dashboard', dashboard.GetDashboard),
    re_path('^notification/', include('Notification.urls')),
]
