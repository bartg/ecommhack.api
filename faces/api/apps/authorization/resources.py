# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from django.shortcuts import redirect

import facebook

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from faces.api.apps.authorization.services import FacebookAuthService, FacebookAuthServiceException
from faces.api.apps.faces.tasks import schedule_person_creation
from faces.api.apps.users.serializers import DetailedUserModelSerializer
from faces.lib.authentication import JWTAuthentication
from faces.lib.resources import GenericAPIView, BadRequest


class AuthResource(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = DetailedUserModelSerializer

    def post(self, request):
        if 'access_token' not in request.DATA:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': {'key': 'missing.field', 'description':
                'Missing access_token in request'
            }})
        try:
            service = FacebookAuthService(request.DATA['access_token'])
            user, token = service.authorize()
        except FacebookAuthServiceException as e:
            raise BadRequest(data=e.data)

        user_data = self.get_serializer(instance=user).data
        user_data['access_token'] = token

        if user.avatar and not user.face_api_id:
            schedule_person_creation(user.pk, [user.avatar.pk])
        return Response(data=user_data, status=status.HTTP_200_OK)


class AuthRedirectResource(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = DetailedUserModelSerializer

    def get(self, request):
        if 'access_token' not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': {'key': 'missing.field', 'description':
                'Missing access_token in request'
            }})

        try:
            service = FacebookAuthService(request.query_params['access_token'])
            user, token = service.authorize()
        except FacebookAuthServiceException as e:
            raise BadRequest(data=e.data)

        return redirect(settings.BACKOFFICE_URL_LOGIN_SUCCESS.format(token=token))