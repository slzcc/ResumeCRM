#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time

def update_solr_data():
    data = {
        "command": "full-import",
        "entity": "resume_source_text",
        "clean": "false"
    }

    url = "http://127.0.0.1:8983/solr/gettingstarted/dataimport"

    return requests.get(url=url, data=data)

# update_solr_data()