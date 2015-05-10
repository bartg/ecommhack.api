# encoding: utf-8
from __future__ import absolute_import, unicode_literals
# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import mock

import os
import logging
import vcr
import unittest
from mock import patch

from django.utils.datetime_safe import datetime
from django.conf import settings
from django.test.testcases import TestCase
from rest_framework import test
from faces.api.apps.users.models import User
from faces.lib.authentication import JWTAuthentication


log = logging.getLogger(__name__)


class APIClient(test.APIClient):
    pass


class PatchMixin(object):

    def patch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()


class APITestCase(PatchMixin, test.APITestCase):
    ping_spotify_for_auth = False
    maxDiff = None
    client_class = APIClient
    vcr = vcr.VCR(
        serializer='yaml',
        record_mode='once',
        cassette_library_dir=settings.CASSETTES_DIR
    )

    def setUp(self):
        super(APITestCase, self).setUp()

        self.user1 = self.create_user('michal@hernas.pl', "michal", '1')

        self.user2 = self.create_user('bartosz@hernas.pl', "bartosz", '2')

    def create_user(self, email, username, facebook_id):
        user, c = User.objects.get_or_create(email=email, username=username, defaults={"facebook_id": facebook_id})
        return user

    def authenticate(self, user):
        """
        Authenticates the given user

        :param user: User to authenticate
        :type user: inventorum.ebay.apps.accounts.models.EbayUserModel
        """
        self.token = JWTAuthentication.get_token(user)
        credentials = {
            'HTTP_AUTHORIZATION': 'JWT %s' % self.token
        }
        self.client.credentials(**credentials)

    def switch_to_user1(self):
        self.user = self.user1
        self.user.refresh_from_db()
        self.authenticate(self.user)

    def switch_to_user2(self):
        self.user = self.user2
        self.user.refresh_from_db()
        self.authenticate(self.user)


class AuthenticatedAPITestCase(APITestCase, PatchMixin):

    def setUp(self):
        super(AuthenticatedAPITestCase, self).setUp()
        self.switch_to_user1()


class UnitTestCase(PatchMixin, TestCase):
    pass
