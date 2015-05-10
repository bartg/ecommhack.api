# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging
from PIL import Image
import tempfile
from rest_framework import status
from faces.api.apps.users.models import User
from faces.api.apps.users.serializers import DetailedUserModelSerializer

from faces.lib.tests.testcases import AuthenticatedAPITestCase, APITestCase


log = logging.getLogger(__name__)


class TestFaceDetection(AuthenticatedAPITestCase):

    def _get_test_image_file(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        return tmp_file

    @APITestCase.vcr.use_cassette("api/face_ident.yaml")
    def test_detection(self):
        # personId returned in the cassette
        self.user.face_api_id = "8cc7e621-478f-4bc1-a3d1-161ec4710373"
        self.user.save()

        image = self._get_test_image_file()
        response = self.client.post('/faces/detect/', {'image': image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user = User.objects.get(pk=self.user.pk)
        expected_response_data = DetailedUserModelSerializer(self.user).data
        self.assertEqual(response.data, expected_response_data)

    @APITestCase.vcr.use_cassette("api/face_ident.yaml")
    def test_undetected(self):
        image = self._get_test_image_file()
        response = self.client.post('/faces/detect/', {'image': image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {"age": 29, "gender": "male"})

    def test_request_without_image(self):
        response = self.client.post('/faces/detect/', {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
