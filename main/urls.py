from django.urls import path,include
from . import views
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings
from django.template import RequestContext
from django.conf.urls import handler404



urlpatterns = [
    path('',views.homepage,name="homepage"),
    
]