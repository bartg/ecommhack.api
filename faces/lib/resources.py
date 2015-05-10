# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView as RestGenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GenericAPIView(RestGenericAPIView):
    authentication_classes = ()
    permission_classes = ()


class APIResource(GenericAPIView):
    pass


class APIListResource(GenericAPIView, ListModelMixin):
    pass


class HttpException(APIException):
    status_code = 500

    def __init__(self, data=None, key=None):
        self.data = data
        self.key = key
        self.detail = {
            'message': data,
            'key': key
        }


class NotFound(HttpException):
    status_code = 404


class BadRequest(HttpException):
    status_code = 400

def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))


class APIPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "total": self.page.paginator.count,
            "data": data
        })
