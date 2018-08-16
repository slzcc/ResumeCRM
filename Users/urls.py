
from django.urls import path, re_path, include
from Users.views import (
    login, logout, register, lock_screen, profile, recoverpw, update
)

# Users
urlpatterns = [

    re_path('^login$', login.UserLogin, name="user-login"),
    re_path('^logout$', logout.UserLogout, name="user-logout"),
    re_path('^profile$', profile.UserProfiles, name="user-profile"),
    re_path('^lock-screen$', lock_screen.UserLockScreen, name="user-lock-screen"),
    re_path('^register$', register.UserRegistrys, name="user-register"),
    re_path('^recoverpw$', recoverpw.UserForgotPassword, name="user-recoverpw"),
    re_path('^update/password/(\d+)$', update.UpdateUserPassword, name="user-update-password"),
    re_path('^update/head-portrait$', update.UpdateUserHeadPortrait, name="user-update-head-portrait"),

]
