# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from django.conf.urls import patterns, include, url
from faces.api.apps.authorization.resources import AuthResource, AuthRedirectResource


urlpatterns = patterns('',
                       url(r'^$', AuthResource.as_view(), name='login'),
                       url(r'^redirect/$', AuthRedirectResource.as_view(), name='redirect'),
)