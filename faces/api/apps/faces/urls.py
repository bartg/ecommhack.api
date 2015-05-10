# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from faces.api.apps.faces.resources import FaceDetectionResource
from django.conf.urls import url

urlpatterns = [
    url(r'^detect/$', FaceDetectionResource.as_view()),
]
