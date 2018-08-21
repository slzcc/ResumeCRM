#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()


def getStatusTypeChoicesValue(value):

	style_list = ["pink", "success", "danger", "warning", "info", "purple"]
	download_type_choices = models.EventLog._meta.get_field("status")
	for index, item in enumerate(download_type_choices.choices):
		if item[0] == value:
			return style_list[index], item[1]

def getResumeInfoChoicesValue(value):
	Resume_status_choices = models.ResumeInfo._meta.get_field("resume_status")
	for item in Resume_status_choices.choices:
		if item[0] == value:
			return item[1]

@register.simple_tag
def SetNotificationTitle(data):
    head_ele = ''

    obj = data.values()
    head_template = """
    
        <li class="nav-item">
            <a href="#{}" class="nav-link {}" data-toggle="tab" aria-expanded="{}">
                <div class="inbox-item">
            
                    <p class="inbox-item-author">{}</p>
                    <p class="inbox-item-text">{}</p>
                    <p class="inbox-item-date">{}</p>
                </div>
            </a>
        </li>
    """
    # print(url)
    for index, item in enumerate(obj):
        active = ""
        _isView = "false"
        if index == "0":
            active = "active show"
            _isView = "true"
        head_ele += head_template.format(
            item["uuid"],
            active,
            _isView,
            item["title"],
            item["describe"][:11] + " ...",
            (item["trigger_time"]+ datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
        )

    
    return mark_safe(head_ele)

@register.simple_tag
def SetNotificationBody(data):
    body_ele = ''
    user = data.values_list("from_user__name", flat=True)[0]
    email = data.values_list("from_user__email", flat=True)[0]
    obj = data.values()
    body_template = """
    <div class="tab-pane" id="{}">
        <h4 class="m-t-0 font-18"><b>{}</b></h4>
        <hr>
        <div class="media m-b-30">
            <div class="media-body">
                <span class="media-meta pull-right">{}</span>
                <h4 class="text-primary font-16 m-0">{}</h4>
                <small class="text-muted">From: {}</small>
            </div>
        </div>

        <p><b>Hi Bro...</b></p>
        <p>{}</p>
    </div>"""

    for index, item in enumerate(obj):
        body_ele += body_template.format(
            item["uuid"],
            item["title"],
            
            (item["trigger_time"]+ datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
            user,
            email,
            item["describe"],
        )
    
    return mark_safe(body_ele)

