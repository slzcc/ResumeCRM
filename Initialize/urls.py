
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Initialize.views import (
	permission, url, models
)

# Initialize

urlpatterns = [
    re_path('^set_main$', models.main, name="initialize-main"),

    # re_path('^set_url_name_in_database$', url.SetUrlNameDatabaseList, name="initialize-set-url-name"),
    # re_path('^set_primission_in_system_perimission$', permission.AddPermission, name="initialize-set-system-perimission"),
    # re_path('^set_resume_id$', models.setModels_id, name="initialize-set-resume-id"),
    # re_path('^set_default_user$', models.setDefaultUser, name="initialize-default-user"),
    # re_path('^set_event_type$', models.setEventType, name="initialize-event-type"),
    # re_path('^set_solr_full_import_cronjob$', models.setCrojob_inSolrData, name="initialize-solr-cronjob"),
    # re_path('^set_resume_custom_label$', models.setResumeCustomLabel, name="initialize-resume-label"),
    # re_path('^set_system_setting$', models.setSettings, name="initialize-system-setting"),
]
