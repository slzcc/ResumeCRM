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
    print(data)
    obj = data.values()
    head_template = """
    <ul class="nav click_properties">
        <li class="nav-item">
            <a href="#v-home" class="nav-link" data-toggle="tab" aria-expanded="false">
                <div class="inbox-item">
            
                    <p class="inbox-item-author">Chadengle</p>
                    <p class="inbox-item-text">Hey! there I'm available...</p>
                    <p class="inbox-item-date">13:40 PM</p>
                </div>
            </a>
        </li>
    </ul>"""
    # print(obj)
    # for item in obj:
    #     print(item)

    head_ele = ''
    return mark_safe(head_ele)

@register.simple_tag
def SetNotificationBody(data):
    # print(data)
    body_template = """
    <div class="tab-pane" id="v-home">
        <h4 class="m-t-0 font-18"><b>Hi Bro, How are you?</b></h4>
        <hr>
        <div class="media m-b-30">
            <div class="media-body">
                <span class="media-meta pull-right">07:23 AM</span>
                <h4 class="text-primary font-16 m-0">Jonathan Smith</h4>
                <small class="text-muted">From: jonathan@domain.com</small>
            </div>
        </div>

        <p><b>Hi Bro...</b></p>
        <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem.</p>
        <p>Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi.</p>
        <p>Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar,</p>
    </div>"""

    body_ele = ''
    return mark_safe(body_ele)

