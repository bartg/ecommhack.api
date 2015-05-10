# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import facebook
from django.conf import settings
from faces.api.apps.users.models import User
from faces.lib.authentication import JWTAuthentication

from django.core import files


class FacebookAuthServiceException(Exception):
    def __init__(self, data):
        self.data = data


class FacebookAuthService(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def authorize(self):
        try:
            graph = facebook.GraphAPI(self.access_token)
            response = graph.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
            profile = graph.get_object("me")
        except facebook.GraphAPIError as e:
            raise FacebookAuthServiceException({'error': {'description': e.message, 'key': 'graphapi.error'}})

        defaults = {
            'name': '{0} {1}'.format(profile['first_name'], profile['last_name']),
            'email': profile['email'],
            'facebook_id': profile['id'],
            'facebook_access_token': response.get('access_token', None)
        }
        user, created = User.objects.get_or_create(username='fb_%s' % profile['id'], defaults=defaults)

        if not created:
            for key, value in defaults.iteritems():
                setattr(user, key, value)
            user.save()

        token = JWTAuthentication.get_token(user)
        return user, token
