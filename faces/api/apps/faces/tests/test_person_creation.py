# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
from faces.api.apps.faces.models import FaceModel
from faces.api.apps.faces.tasks import schedule_person_creation
from faces.api.apps.images.models import ImageModel
from faces.api.apps.users.models import User
from faces.lib.tests import with_celery

from faces.lib.tests.testcases import APITestCase


log = logging.getLogger(__name__)


class TestPersonCreation(APITestCase):

    @with_celery()
    @APITestCase.vcr.use_cassette("api/person_creation.yaml")
    def test_person_creation(self):
        hassel_root = "../static/images/"

        images = [ImageModel.objects.create(file="{}{}".format(hassel_root, image_name))
                  for image_name in ["david_hasselhoff_1.jpg", "david_hasselhoff_2.jpg", "david_hasselhoff_3.jpg"]]
        image_ids = [image.id for image in images]

        user = User.objects.create(name="David Hasselhoff",
                                   email="david@hasselhoff.com")

        # precondition
        self.assertIsNone(user.face_api_id)
        self.assertEqual(FaceModel.objects.count(), 0)

        schedule_person_creation(user_id=user.id, image_ids=image_ids)

        user.refresh_from_db()
        self.assertIsNotNone(user.face_api_id)

        faces = FaceModel.objects.all()
        self.assertEqual(faces.count(), 3)

        self.assertItemsEqual([face.image.id for face in faces], image_ids)
        [self.assertIsNotNone(face.face_api_id) for face in faces]
