import json

# from django.core.urlresolvers import resolve
from django.urls import resolve
from django import conf
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.db.models import Q

from repository import models

def perm_check(request, *args, **kwargs):
    try:
        if conf.settings.CLOSE_PERMISSION:

            url_obj = resolve(request.path_info)
            url_name = url_obj.url_name
            perm_name = ''

            #权限必须和urlname配合使得
            if url_name:

                #获取请求方法，和请求参数
                url_method = request.method
                if request.method == "GET":
                    url_args = request.GET

                elif request.method == "POST":
                    url_args = request.POST
                
                # 获取发送的数据
                url_args_list = []
                for k, v in url_args.items():
                    url_args_list.append(k)

                url_args_list = ','.join(url_args_list)

                # 获取访问的 url 具有的权限
                _query_argument_list = models.SystemPermission.objects.filter(url__name=url_name)

                # 访问 url 所使用的访问类型
                _query_url_method = _query_argument_list.last().get_per_method_display()
                if _query_url_method == "*":
                    url_method = "*"

                # 因数据的存储数据是 1、2、3 等，不是 GET/POST 等值，所以需要找出数据库中所定义的 key，并重新赋值
                _query_url_method_type = models.SystemPermission._meta.get_field("per_method")
                _query_url_method_type_list = _query_url_method_type.flatchoices

                for i in _query_url_method_type_list:
                    if url_method == i[1]:
                        url_method = i[0]


                if list(_query_argument_list.values("argument_list"))[0]["argument_list"] == "*":
                    get_perm = models.SystemPermission.objects.filter(url__name=url_name, per_method=url_method).values("permissions__codename","url__name")
                    if get_perm:
                        for i in list(get_perm):
                            for k,v in i.items():
                                if k == "permissions__codename":
                                    perm_name = v
                            perm_str = 'repository.%s' % perm_name

                            if request.user.has_perm(perm_str):
                                return True
                        else:
                            return False
                    else:
                        return False
                else:
                    get_perm = models.SystemPermission.objects.filter(url__name=url_name,per_method=url_method,argument_list=url_args_list)
                    if get_perm:
                        for i in get_perm:
                            perm_name = i.name
                            perm_str = 'repository.%s' % perm_name

                            if request.user.has_perm(perm_str):
                                return True
                        else:
                            return False
                    else:
                        return False

            else:
                # 没有权限设置，默认不放过
                return False   
                
    except AttributeError as e:
        return False

def check_permission(StatusCode=None):
    def check_permission_sub(fun):
        def wapper(request, *args, **kwargs):
            try:
                if request.user.is_staff:
                    return fun(request, *args, **kwargs)
                elif perm_check(request, *args, **kwargs):
                    return fun(request, *args, **kwargs)
                obj = models.UserProfile.objects.filter(is_staff=True).last()
                email = obj.email
                return render(request, '401.html', {"StatusCode": StatusCode, "email": email})
            except:
                return render(request, '401.html', {"StatusCode": StatusCode})
        return wapper
    return check_permission_sub
