from django.template import Library
from django.utils.safestring import mark_safe
import datetime ,time, json
from repository import models

register = Library()

@register.simple_tag
def MenuButtonAuthentication(request, permission_name):
	if request.user.is_staff:
		return True
	else:
		return request.user.has_perm("repository.{}".format(permission_name))
