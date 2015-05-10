# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from django.utils.datetime_safe import datetime

import jwt
import logging
import json

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from faces.api.apps.users.models import User

log = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'jwt':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            log.warn('Invalid token header: "%s" No credentials provided.', auth)
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            log.warn('Invalid token header: "%s" Token string should not contain spaces.', auth)
            raise AuthenticationFailed(msg)

        token = auth[1]
        try:
            data = jwt.decode(token, settings.FACES_SECRET)
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(e)

        user_id = data['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser(), token

        return user, data

    def authenticate_header(self, request):
        return 'JWT'

    @classmethod
    def get_token(cls, user):
        return jwt.encode({'user_id': user.id}, settings.FACES_SECRET, algorithm='HS256')


    @classmethod
    def encode_jwt_token(cls, user, refresh_token):
        token = JWTAuthentication.get_token(user)
        refresh_token = json.dumps({
            'refresh_token': refresh_token,
            'token': token
        })
        return refresh_token