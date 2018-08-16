from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from Notification import views

# Notification
urlpatterns = [
    re_path('^message/check$', views.TriggerStream, name="notification-message-check"),
]
