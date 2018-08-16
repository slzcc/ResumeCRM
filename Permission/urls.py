
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Permission.views import permission

# Permission

urlpatterns = [

    re_path('^link$', permission.LinkPermission, name="permission-link-manage"),
    re_path('^list$', permission.ListPermission, name="permission-list-manage"),
    re_path('^(\d+)/change$', permission.PermissionChange, name="permission-list-change"),
    re_path('^(\w+)/setting$', permission.SettingPermission, name="permission-link-setting"),
    re_path('^delete$', permission.PermissionDelete, name="permission-delete"),

]
