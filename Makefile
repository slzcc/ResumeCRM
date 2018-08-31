SHELL := /bin/bash
VERSION := "4"

set_data:
	@docker exec -t resume_mysql mysql -uroot -pexample.org -e "create database resume character set 'UTF8';"
	@docker exec -t resume_mysql mysql -uroot -pexample.org -e "grant all on resume.* to resume@'%' identified by 'resume';"
	@docker exec -t resume_mysql mysql -uroot -pexample.org -e "create database check_md5 character set 'UTF8';"
	@docker exec -t resume_mysql mysql -uroot -pexample.org -e "grant all on check_md5.* to check_md5@'%' identified by 'check_md5';"
	@docker exec -t resume_server python3 manage.py makemigrations
	@docker exec -t resume_server python3 manage.py migrate
	@docker exec -t resume_transcode python3 manage.py makemigrations
	@docker exec -t resume_transcode python3 manage.py migrate
initialize_data:
	@curl http://127.0.0.1:8088/initialize/set_url_name_in_database
	@curl http://127.0.0.1:8088/initialize/set_primission_in_system_perimission
	@curl http://127.0.0.1:8088/initialize/set_resume_id
	@curl http://127.0.0.1:8088/initialize/set_default_user
	@curl http://127.0.0.1:8088/initialize/set_event_type
	@curl http://127.0.0.1:8088/initialize/set_solr_full_import_cronjob
	@curl http://127.0.0.1:8088/initialize/set_resume_custom_label
	@curl http://127.0.0.1:8088/initialize/set_system_setting

build:
	@docker build -t slzcc/resumecrm:v$(VERSION) -f /Resume/Docker/Dockerfile . --no-cache