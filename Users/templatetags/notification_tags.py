#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()


def getNotificationTypeChoicesValue_inHTML(value, location_type="body", uuid=None, title=None, trigger_time=None):

    style_list = ["dark", "success", "danger", "warning", "info", "purple"]
    icon = {
        "system": "mdi mdi-settings", 
        "email": "mdi mdi-email-outline", 
        "event": "mdi mdi-alert-circle-outline", 
        "user": "mdi mdi-account",
        "notification": "mdi mdi-test-tube",
        "other": "mdi mdi-airplane",
    }

    notification_type_choices = models.Notification._meta.get_field("notification_type")
    for index, item in enumerate(notification_type_choices.choices):
        if item[0] == value:
            style = style_list[index]
            type_name = item[1]

    if location_type == "title":
        template = """
        <a href="{}" class="dropdown-item notify-item">
            <div class="notify-icon bg-{}">
                <i class="{}"></i>
            </div>
            <p class="notify-details">{}
                <small class="text-muted">{}</small>
            </p>
        </a>
        """.format(
            "/user/notification?view=" + uuid,
            style,
            icon[type_name],
            title,
            (trigger_time + datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
        )

    else:
        
        template = """
        <div class="notify-icon bg-{}">
            <i class="{}"></i>
        </div>""".format(style, icon[type_name])
    
    return template

@register.simple_tag
def SetNotificationTitle(data, urlParameter):
    head_ele = ''

    obj = data.values()
    head_template = """
    
        <li class="nav-item">
            <a href="?view={}" value="{}" class="nav-link {}" data-toggle="tab" aria-expanded="true">
                <div class="inbox-item ">
                    <div class="inbox-item-img">
                        {}
                    </div>

                    <p class="inbox-item-author">{}</p>
                    <p class="inbox-item-text">{}</p>
                    <p class="inbox-item-date">{}</p>
                    <p class="inbox-item-author text-right">
                        <span class="badge badge-{}">{}</span>
                    </p>
                </div>
            </a>
        </li>
    """
    for index, item in enumerate(obj):
        active = ''
        try:
            if item["uuid"] == urlParameter.split("=")[1]:
                active = "active show"
        except:
            pass
        if item["read"]:
            label = "warning"
            label_content = "已读"
        else:
            label = "purple"
            label_content = "未读"

        head_ele += head_template.format(
            item["uuid"],
            item["uuid"],
            active,
            getNotificationTypeChoicesValue_inHTML(item["notification_type"]),
            item["title"],
            item["describe"][:11] + " ...",
            (item["trigger_time"]+ datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
            label,
            label_content,
        )

    
    return mark_safe(head_ele)

@register.simple_tag
def SetNotificationBody(data, urlParameter):
    body_ele = ''
    user = data.values_list("from_user__name", flat=True)[0]
    email = data.values_list("from_user__email", flat=True)[0]
    
    body_template = """
    <div class="tab-pane active show" id="{}">
        <h4 class="m-t-0 font-18"><b>{}</b></h4>
        <hr>
        <div class="media m-b-30">
            <div class="media-body">
                <span class="media-meta pull-right">{}</span>
                <h4 class="text-primary font-16 m-0">{}</h4>
                <small class="text-muted">From: {}</small>
            </div>
        </div>

        <p><b>Hi ~<b></p>
        <p>{}</p>
    </div>"""
    try:
        obj = data.filter(uuid=urlParameter.split("=")[1]).last()
        body_ele += body_template.format(
            obj.uuid,
            obj.title,
            (obj.trigger_time+ datetime.timedelta(hours=+8)).strftime('%y/%m/%d %H:%M'),
            str.capitalize(user),
            email,
            obj.describe,
        )
    except:
        pass
    
    
    return mark_safe(body_ele)

@register.simple_tag
def SetNotificationBellModels(request):
    data = models.Notification.objects.filter(to_user=request.user).order_by("-trigger_time")
    not_read_number = data.filter(read=False).count()
    if int(not_read_number) >= 100:
        not_read_number = "99+"
        
    obj = data.filter(read=False).values()[:5]
    ele = ''
    for index, item in enumerate(list(obj)):
        ele += getNotificationTypeChoicesValue_inHTML(item["notification_type"], location_type="title", uuid=item["uuid"], title=item["title"], trigger_time=item["trigger_time"])

    if not ele:
        ele = """
        <div class="row">
            <div class="col-md-12 portlets">
                <!-- Your awesome content goes here -->
                <div class="m-b-30">
                    <div action="#" class="notification_body dz-clickable" id="wrapper_location">
                        <div class="dz-default dz-message" id="cell_location">
                            <span>没有新消息!</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    template = """
    <a class="nav-link dropdown-toggle arrow-none waves-light waves-effect" data-toggle="dropdown" href="#" role="button" aria-haspopup="false" aria-expanded="false">
        <i class="mdi mdi-bell noti-icon"></i>
        <span class="badge badge-pink noti-icon-badge not-read-number">{}</span>
    </a>
    <div class="dropdown-menu dropdown-menu-right dropdown-arrow dropdown-menu-lg" aria-labelledby="Preview">
        <!-- item-->
        <div class="dropdown-item noti-title">
            <h5 class="font-16"><span class="badge badge-danger float-right not-read-number">{}</span>消息通知</h5>
        </div>

        <!-- item-->
        {}

        <!-- All-->
        <a href="/user/notification" class="dropdown-item notify-item notify-all">
            查看全部
        </a>

    </div>
    """.format(
        not_read_number,
        not_read_number,
        ele,
    )



    return mark_safe(template)
