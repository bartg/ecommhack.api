# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.conf import settings
from faces.api.apps.faces.models import FaceModel
from faces.api.apps.faces.tasks import add_face_task, schedule_user_training
from faces.api.apps.users.models import User
from faces.lib.faces_api.api import FaceAPI


log = logging.getLogger(__name__)


class UnrecognizedIdentity(Exception):

    def __init__(self, face_id, gender, age):
        self.face_id = face_id
        self.gender = gender
        self.age = age


class FaceIdentService(object):

    def __init__(self):
        self.face_api = FaceAPI()

    def identify(self, from_image):
        """
        :type from_image: faces.api.apps.images.models.ImageModel
        :rtype (User, decimal.Decimal) | None

        :raises requests.exceptions.RequestException
        """
        # 1. detect a face
        face = self.face_api.faces.detect(image_url=from_image.public_url)
        if not face:
            return None

        log.info("Detected face: {}".format(face))

        face_id = face["faceId"]
        gender = face["attributes"]["gender"]
        age = int(face["attributes"]["age"])

        # 2. identify the detected face
        identity = self.face_api.faces.identify(face_id=face_id,
                                                person_group_id=settings.FACE_API_PERSON_GROUP_ID)
        if not identity:
            raise UnrecognizedIdentity(face_id=face_id, gender=gender, age=age)

        log.info("Detected identity: {}".format(identity))

        # 3. match the identified person
        person_id, confidence = identity

        try:
            user = User.objects.get(face_api_id=person_id)
        except User.DoesNotExist:
            log.info("User with `face_api_id={}` does not exist".format(person_id))
            raise UnrecognizedIdentity(face_id=face_id, gender=gender, age=age)

        face = FaceModel.objects.create(user=user,
                                        image=from_image,
                                        face_api_id=face_id,
                                        gender=gender,
                                        age=age)

        # lazy data migration
        if user.gender is None or user.age is None:
            user.gender = gender
            user.age = age
            user.save()

        # train user with face, whaaaaaaat uuuupppp??
        schedule_user_training(user_id=user.id, face_id=face.id)

        return user, confidence
