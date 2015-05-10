# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include, patterns
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings

handler500 = 'faces.lib.resources.handler500'


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('faces.api.apps.users.urls')),
    url(r'^faces/', include('faces.api.apps.faces.urls')),
    url(r'^products/', include('faces.api.apps.products.urls')),
    url(r'^auth/', include('faces.api.apps.authorization.urls', 'auth')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ckeditor/', include('ckeditor.urls')),
] + format_suffix_patterns([
])

# Debug
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
