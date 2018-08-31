#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import conf
from repository import models
from django.contrib.auth.decorators import login_required
from Permission.Authentication import check_permission
from HttpCode.StatusCode import StatusCode

import datetime, re, os, time, requests, json

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

def AddPermission(request):
	content_type = ContentType.objects.get_for_model(models.SystemPermission)
	
	Permission.objects.all().delete()

	# ************************************ Resume ************************************************************
	Permissions = Permission.objects.create(
		codename="resume_uplaod_attachment",
		name=u"简历-上传-附件",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="analyse-resume-k18").id,
		"name": "resume_uplaod_attachment",
		"describe": u"允许在简历页面上传附件后进行解析.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="resume_candidate_info",
		name=u"简历-候选人-详情页",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-candidate-info").id,
		"name": "resume_candidate_info",
		"describe": u"允许访问候选人的详细页面.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="resume_candidate_info_origin_manage",
		name=u"简历-候选人-详情页-原件管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": "",
		"name": "resume_candidate_info_origin_manage",
		"describe": u"允许访问候选人的详细页面的原始简历管理.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_list",
		name=u"简历-列表",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-list-manage").id,
		"name": "resume_list",
		"describe": u"允许访问简历列表.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_source_list_manage",
		name=u"简历来源-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-source-list-manage").id,
		"name": "resume_source_list_manage",
		"describe": u"允许访问/添加简历来源.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_source_change",
		name=u"简历来源-编辑页面",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-source-change").id,
		"name": "resume_source_change",
		"describe": u"允许访问/修改简历来源的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)


	Permissions = Permission.objects.create(
		codename="resume_candidate_info_download_origin_attachment",
		name=u"简历-候选人-详情页-下载-原始附件",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": "",
		"name": "resume_candidate_info_download_origin_attachment",
		"describe": u"允许对候选人详情页面下载原始简历",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_export_template",
		name=u"简历-候选人-详情页-导出模板简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="documents-export-word").id,
		"name": "resume_candidate_info_export_template",
		"describe": u"允许对候选人详情页导出简历模板.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_view_pdf",
		name=u"简历-候选人-详情页-查看PDF",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="viewerjs-index").id,
		"name": "resume_candidate_info_view_pdf",
		"describe": u"允许对候选人详情页进行查看 PDF 格式源简历信息.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_delete",
		name=u"简历-候选人-详情页-删除简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-candidate-info-delete").id,
		"name": "resume_candidate_info_delete",
		"describe": u"允许对候选人详情页进行删除操作.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_comment",
		name=u"简历-候选人-详情页-评论",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-candidate-info-comment").id,
		"name": "resume_candidate_info_comment",
		"describe": u"允许对候选人详情页添加评论信息.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_again_upload",
		name=u"简历-候选人-详情页-重新上传简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="analyse-resume-k18").id,
		"name": "resume_candidate_info_again_upload",
		"describe": u"允许对候选人详情页上传新简历覆盖原始简历内容信息.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_template_list_manage",
		name=u"简历模板-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-template-list-manage").id,
		"name": "resume_template_list_manage",
		"describe": u"允许对简历模板进行添加与删除.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_template_change",
		name=u"简历模板-编辑页面",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-template-change").id,
		"name": "resume_template_change",
		"describe": u"允许对简历模板进行编辑.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_batch_operation",
		name=u"简历模板-编辑页面",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": "",
		"name": "resume_batch_operation",
		"describe": u"允许对简历页面进行批量修改等操作.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="resume_list_search",
		name=u"简历-列表-搜索",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": "",
		"name": "resume_list_search",
		"describe": u"允许在简历列表页面进行搜索.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_candidate_info_collection",
		name=u"简历-候选人-详情页-收藏简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": "",
		"name": "resume_candidate_info_collection",
		"describe": u"允许在候选人页面进行收藏.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="resume_related_tracking_list_manage",
		name=u"简历-相关-我追踪的简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-related-tracking-list-manage").id,
		"name": "resume_related_tracking",
		"describe": u"允许查看自己追踪的简历页面.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_related_upload_list_manage",
		name=u"简历-相关-我上传的简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-related-upload-list-manage").id,
		"name": "resume_related_upload_list_manage",
		"describe": u"允许查看自己上传的简历页面.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_related_download_list_manage",
		name=u"简历-相关-我收藏的简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-related-download-list-manage").id,
		"name": "resume_related_download_list_manage",
		"describe": u"允许查看自己下载的简历页面.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="resume_related_subscribe_list_manage",
		name=u"简历-相关-我收藏的简历",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="resume-related-subscribe-list-manage").id,
		"name": "resume_related_subscribe_list_manage",
		"describe": u"允许查看自己收藏的简历页面.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)


	# ************************************ Permissions ************************************************************
	Permissions = Permission.objects.create(
		codename="permission_link_manage",
		name=u"权限-分配-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="permission-link-manage").id,
		"name": "permission_link_manage",
		"describe": u"允许访问/修改权限的分配.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="permission_list_manage",
		name=u"权限-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="permission-list-manage").id,
		"name": "permission_list_manage",
		"describe": u"允许访问/修改/添加权限.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="permission_link_setting",
		name=u"权限-分配-功能",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="permission-link-setting").id,
		"name": "permission_link_setting",
		"describe": u"允许访问/修改权限的功能.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="permission_list_change",
		name=u"权限-列表-配置",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="permission-list-change").id,
		"name": "permission_list_change",
		"describe": u"允许访问/修改权限的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)


	# ************************************ System ************************************************************
	Permissions = Permission.objects.create(
		codename="system_user_list_manage",
		name=u"系统-用户-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-user-list-manage").id,
		"name": "system_user_list_manage",
		"describe": u"允许访问/添加系统用户.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="system_role_list_manage",
		name=u"系统-角色-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-role-list-manage").id,
		"name": "system_role_list_manage",
		"describe": u"允许访问/添加系统角色.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="system_role_change",
		name=u"系统-角色-配置",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-role-change").id,
		"name": "system_role_change",
		"describe": u"允许访问/修改系统角色的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="system_email_list_manage",
		name=u"系统-邮件-列表-管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-email-list-manage").id,
		"name": "system_email_list_manage",
		"describe": u"允许访问/添加系统 SMTP.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="system_email_change",
		name=u"系统-邮件-配置",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-email-change").id,
		"name": "system_email_change",
		"describe": u"允许访问/修改系统 SMTP 的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="system_user_change",
		name=u"系统-用户-配置",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-user-change").id,
		"name": "system_user_change",
		"describe": u"允许访问/修改系统用户的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="system_general_list_manage",
		name=u"系统-全局-配置",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="system-general-list-manage").id,
		"name": "system_general_list_manage",
		"describe": u"允许访问/修改系统全局的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	# ************************************ User ************************************************************
	Permissions = Permission.objects.create(
		codename="user_profile",
		name=u"用户-配置管理",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="user-profile").id,
		"name": "user_profile",
		"describe": u"允许访问/修改用户的配置.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="user_register",
		name=u"用户-注册",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="user-register").id,
		"name": "user_register",
		"describe": u"允许注册用户.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	Permissions = Permission.objects.create(
		codename="user_profile_set_password",
		name=u"用户-配置管理-修改密码",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="user-update-password").id,
		"name": "user_profile_set_password",
		"describe": u"允许用户修改自己的密码.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)
	
	Permissions = Permission.objects.create(
		codename="user_notification",
		name=u"用户-配置管理-修改密码",
		content_type=content_type,
	)
	data = {
		"per_method": 3,
		"argument_list": "*",
		"permissions_id": Permissions.id,
		"url_id": models.Menu.objects.get(url_name="user-notification").id,
		"name": "user_notification",
		"describe": u"允许用户查看通知.",
	}
	SystemPermissions = models.SystemPermission.objects.create(**data)

	return HttpResponse("")
