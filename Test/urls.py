
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from Test.views import test


# Test 
urlpatterns = [
    
    re_path('^index$', test.test, name="test-html"),
    # re_path('^test/(\w+\-\w+\-\w+)/(\w+\-\w+\-\w+\-\w+.pdf)$', test.testpdf2, name="testpdf"),
    # re_path('^test/test.html$', test.test, name="test"),
]
