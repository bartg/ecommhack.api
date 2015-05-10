# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from faces.api.apps.users.resources import MeResource
from django.conf.urls import url

urlpatterns = [
    url(r'^me/$', MeResource.as_view()),
]