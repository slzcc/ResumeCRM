SHELL := /bin/bash
VERSION := "4"

initialize_data:
	@docker exec -t resume_server curl http://127.0.0.1:8088/initialize/set_main

build:
	@docker build -t slzcc/resumecrm:v$(VERSION) -f ./Docker/Dockerfile . --no-cache