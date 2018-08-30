#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django import conf
from django.utils.safestring import mark_safe

from repository import models
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode
from Public.service.resume import table_config

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import os, json, re, requests, datetime

def SearchResumeList(request):
    url = conf.settings.SOLR_SERVER_URL + "solr/gettingstarted/select?" 
    local_url_getData = request.get_full_path().split("?")[1]
    q_list = []
    rlt = {}
    for i in table_config:
        if not i['q']:
            continue

        if type(i['q']) == list:
            for j in i['q']:
                q_list.append(j)
        else:
            q_list.append(i['q'])

    if request.method == "GET":
        data_list = []
        for k, v in request.GET.items():
            if k == "searchType":
                rlt["q_type"] = request.GET.get(k, "_so")
            else:
                rlt[k] = json.loads(request.GET.get(k))

        if rlt["q_type"] == "_so":
            solrData_dict = {}

            for a, b in rlt["solrData"].items():
                solrData_dict[a] = b

            access = requests.get(url, data=solrData_dict)

            solr_datas = json.loads(access.text)["response"]["docs"]
            values = []
            for i in solr_datas:
                for o, p in i.items():
                    values.append(p)

            datas = models.ResumeInfo.objects.filter(id__in=values).order_by("-create_time").values(*q_list)
        else:
            datas = models.ResumeInfo.objects.all().order_by("-create_time").values(*q_list)

        
        sqlData_dict = {}
        for a, b in rlt["sqlData"].items():
            if a == "gender":
                if b == "false":
                    b = False
                else:
                    b = True
            sqlData_dict[a] = b

        dataList = list(datas.filter(**sqlData_dict))

        # heavy
        _dataList = []
        _checklist = []
        for item in dataList:
            _sub_custom_label = {
                "name": item["custom_label__name"],
                "code": item["custom_label__code"],
                "priority": item["custom_label__priority"],
                "agent": item["agent"],
            }
            _sub_user_comments = {
                "describe": item["user_comments__describe"],
                "user_id": item["user_comments__user"],
                "user_name": item["user_comments__user__email"],
                "create_time": item["user_comments__create_time"],
                "portrait": item["user_comments__user__head_portrait"],
            }
            try:
                _sub_user_comments["create_time"] = (_sub_user_comments["create_time"] + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M:%S')
            except:
                pass
            if not item["id"] in _checklist:
                # custom_label
                custom_label__name = item.pop("custom_label__name")
                custom_label__code = item.pop("custom_label__code")
                custom_label__priority = item.pop("custom_label__priority")
                item["custom_label"] = {}
                if custom_label__name:
                    item["custom_label"][custom_label__name] = _sub_custom_label

                # user_comments
                item.pop("user_comments__describe")
                item.pop("user_comments__user")
                item.pop("user_comments__create_time")
                item.pop("user_comments__user__email")
                item.pop("user_comments__user__head_portrait")
                item["user_comments"] = []
                if custom_label__name:
                    item["user_comments"].append(_sub_user_comments)

                _dataList.append(item)
                _checklist.append(item["id"])
            else:
                for items in _dataList:
                    if items["id"] == item["id"]:
                        items["custom_label"][item["custom_label__name"]] = _sub_custom_label
                        items["user_comments"].append(_sub_user_comments)

        paginator = Paginator(_dataList, 20)

        page = int(request.GET.get('_page', 1))
        contacts = paginator.get_page(page)

        ele = '<nav><ul class="pagination pagination-split">'

        if page == 1:
            ele += '''<li class="page-item"><a class="page-link" href="#" aria-label="Previous"> <span aria-hidden="true">«</span><span class="sr-only">Previous</span></a></li>'''
        else:
            ele += '''<li class="page-item"><a class="page-link" href="?{}" aria-label="Previous"> <span aria-hidden="true">«</span><span class="sr-only">Previous</span></a></li>'''.format(re.sub("_page=\d+", "_page=" + str(page - 1), local_url_getData))

        for i in paginator.page_range:

            if (abs(page) - i) < 2:
                active = ""
                if page == i:
                    active = "active"

                p = re.sub("_page=\d+", "_page={}", local_url_getData).format(i)
                p_ele = '<li class="paginate_button page-item {}" ><a id="auto_paginate" href="?{}" aria-controls="datatable" data-dt-idx="2" tabindex="0" class="page-link">{}</a></li>'.format(active, p, i)
                # p_ele = '<li class="paginate_button page-item {}" ><a id="auto_paginate" href="?_page={}#" aria-controls="datatable" data-dt-idx="2" tabindex="0" class="page-link">{}</a></li>'.format(active, i, i)

                ele += p_ele

        if paginator.num_pages == page:
            ele += '''<li class="page-item"><a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">»</span><span class="sr-only">Next</span></a></li>'''
        else:
            ele += '''<li class="page-item"><a class="page-link" href="?{}" aria-label="Next"><span aria-hidden="true">»</span><span class="sr-only">Next</span></a></li>'''.format(re.sub("_page=\d+", "_page=" + str(page + 1), local_url_getData))

        ele += "</ul></nav>"

        for i in contacts:
            try:
                i["create_time"] = i["create_time"] + datetime.timedelta(hours=+8)
                i["create_time"] = i["create_time"].strftime('%y/%m/%d %H:%M')
                data_list.append(i)
            except:
                pass

        result = {
            'ele': ele,
            'table_config': table_config,
            'data_list': data_list,
            'global_list': {
                'resume_status_choices': models.ResumeInfo.resume_status_choices,
            },
        }
        return JsonResponse(result)


    return HttpResponse("Not Data!")