from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
 
@shared_task
def full_update_solr(url):
	session = requests.get(url)
	return session.status_code