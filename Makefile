SHELL := /bin/bash
VERSION := "4"

set_data:
	@docker exec -t resume_server python3 manage.py migrate
	@docker exec -t resume_transcode python3 manage.py migrate
initialize_data:
	@docker exec -t resume_server curl http://127.0.0.1:8088/initialize/set_main

build:
	@docker build -t slzcc/resumecrm:v$(VERSION) -f ./Docker/Dockerfile . --no-cache