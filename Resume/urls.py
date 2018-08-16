
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Resume.views import (
    resume_info, resume, source, resume_template, my_related
)

# Resume
urlpatterns = [
    
    # 简历列表
    re_path('^list$', resume.ResumeView, name="resume-list-manage"),
    # re_path('^resume-config-json.html$', resume.ResumeJsonView, name="resume-config"),
    # # re_path('^resume/(?P<uid>\d+)-info.html$', resume_info.GetResumeInfoView, name="resume-user-info-view"),
    
    # 与我相关的
    re_path('^related/tracking/list$', my_related.IamTrackingResume, name="resume-related-tracking-list-manage"),
    re_path('^related/upload/list$', my_related.IUploadResume, name="resume-related-upload-list-manage"),
    re_path('^related/download/list$', my_related.IDownloadResume, name="resume-related-download-list-manage"),
    re_path('^related/subscribe/list$', my_related.ISubscribeResume, name="resume-related-subscribe-list-manage"),

    # 详细简历
    re_path('^candidate/(?P<obj_id>\d+)/change$', resume_info.GetResumeInfoView, name="resume-candidate-info"),
    # re_path('^add_resume.html$', resume_info.AddResumeView, name="resume-user-add"),
    # re_path('^upload_skl_resume.html$', resume_info.UploadSKLResume),
    # re_path('^upload_k18_resume.html$', resume_info.UploadK18Resume, name="resume-upload"),
    # re_path('^sdkresume.html$', resume_info.interfaceResumeSDK),
    # re_path('^sklresume.html$', resume_info.interfaceSKLResume),
    # re_path('^k18resume.html$', resume_info.interfaceResumeK18, name="resume-k18parsing-storage"),
    re_path('^list/delete$', resume.DeleteResumeList, name="resume-delete-resume-list"),
    re_path('^candidate/delete/(\d+)$', resume_info.DeleteCandidate, name="resume-candidate-info-delete"),
    re_path('^candidate/subscription$', resume_info.ResumeSubscription, name="resume-candidate-info-subscription"),
    # re_path('^delete-(?P<uid>\d+)-resume.html$', resume_info.DeleteResumeInfoView),
    # re_path('^edit-(?P<uid>\d+)-resume.html$', resume_info.EditResumeView, name="resume-user-info-edit"),

    # 评论
    re_path('^candidate/commands/save$', resume_info.SaveResumeCommands, name="resume-candidate-info-comment"),

    # 简历来源
    re_path('^source/list$', source.ResumeSource, name="resume-source-list-manage"),
    re_path('^source/(\d+)/change$', source.ResumeSourceChange, name="resume-source-change"),
    re_path('^source/delete$', source.ResumeSourceDelete, name="resume-source-delete"),

    # 模板
    re_path('^template/list$', resume_template.ResumeTemplate, name="resume-template-list-manage"),
    re_path('^template/(\d+)/change$', resume_template.ResumeTemplateChange, name="resume-template-change"),
    re_path('^template/delete$', resume_template.ResumeTemplateDelete, name="resume-template-delete"),

]
