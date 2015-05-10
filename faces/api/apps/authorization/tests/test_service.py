# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
from faces.api.apps.authorization import facebook_download_image
from faces.lib.tests import with_celery

from faces.lib.tests.testcases import APITestCase


log = logging.getLogger(__name__)


class TestFacebookService(APITestCase):

    @with_celery()
    @APITestCase.vcr.use_cassette("api/downloading_facebook_avatar.yaml")
    def test_downloading_facebook_avatar(self):
        image = facebook_download_image('10202937621320306')
        self.assertTrue(image)
        self.assertTrue(image.file)

# 10202937621320306