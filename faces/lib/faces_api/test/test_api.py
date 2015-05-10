# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging

from django.conf import settings
from django.test.testcases import TestCase
from faces.lib.faces_api.api import FaceAPI
from faces.lib.tests.testcases import APITestCase


log = logging.getLogger(__name__)


class TestFaceAPI(TestCase):
    TEST_IMAGE_URL = "http://i.imgur.com/OFrzDjU.jpg"

    def setUp(self):
        super(TestFaceAPI, self).setUp()
        self.api = FaceAPI()

    @APITestCase.vcr.use_cassette('face_api/face_detection.yaml')
    def test_face_detection(self):
        face = self.api.faces.detect(image_url=self.TEST_IMAGE_URL)

        self.assertIsNotNone(face.get("faceId"))
        self.assertIsInstance(face.get("attributes"), dict)
        self.assertIsNotNone(face["attributes"].get("age"))
        self.assertIsNotNone(face["attributes"].get("gender"))

    def test_basic_logic(self):
        self.assertIsNotNone(self.api.client)
        self.assertEqual(self.api.client.subscription_key, settings.FACE_API_SUBSCRIPTION_KEY)
