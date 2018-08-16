#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf

from repository import models
import datetime, re, os, time, requests, json



def get_filter_result(request, querysets):

    filter_conditions = {}
    for key, val in request.GET.items():
        if key in ('_page', '_o', '_q'):
            continue
        if val:
            filter_conditions[key] = val

    # print("filter_conditions", filter_conditions)
    return querysets.filter(**filter_conditions), filter_conditions

def get_orderby_result(request, querysets, admin_class):
    """排序"""

    current_ordered_column = {}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key =  admin_class.list_display[abs(int(orderby_index))]

        # 为了让前端知道当前排序的列
        current_ordered_column[orderby_key] = orderby_index

        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key

        return querysets.order_by(orderby_key),current_ordered_column
    else:
        return querysets, current_ordered_column


def get_serached_result(request, querysets, admin_class):

    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_key))


        return querysets.filter(q)
    return querysets

def table_obj_delete(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admins[app_name][model_name]

    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        obj.delete()
        return redirect("/generaladmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))
    return render(request, 'generaladmin/table_obj_delete.html', locals())