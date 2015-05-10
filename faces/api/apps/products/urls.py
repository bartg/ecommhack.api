# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from faces.api.apps.products.resources import ProductListResource, ProductRecommendationResource

urlpatterns = [
    url(r'^recommendation/$', ProductRecommendationResource.as_view()),
    url(r'^$', ProductListResource.as_view()),
]
