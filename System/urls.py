
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from System.views import (
    email, role, user, general, audit
)

# System
urlpatterns = [

    re_path('^user/list$', user.UserList, name="system-user-list-manage"),
    re_path('^user/(\d+)/change$', user.UserChange, name="system-user-change"),
    re_path('^user/delete$', user.UserDelete, name="system-user-delete"),
    re_path('^user/update/password/(\d+)$', user.UpdateUserPassword, name="system-system-user-update-password"),

    re_path('^role/list$', role.RoleList, name="system-role-list-manage"),
    re_path('^role/(\d+)/change$', role.RoleChange, name="system-role-change"),
    re_path('^role/delete$', role.RoleDelete, name="system-role-delete"),

    # re_path('^test-email', email.TestEmail, name="system-test-email"),
    re_path('^email/list$', email.EmailList, name="system-email-list-manage"),
    re_path('^email/(?P<obj_id>\d+)/change$', email.EmailChange, name="system-email-change"),
    re_path('^email/delete$', email.EmailDelete, name="system-email-delete"),
    re_path('^email/send/interface/(\d+)$', email.SendEmailDataInterface, name="system-email-send-nterface"),

    re_path('^general/list$', general.GeneralList, name="system-general-list-manage"),
    
    re_path('^audit/list$', audit.AuditList, name="system-audit-list-manage"),

]
