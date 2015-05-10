# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from celery.canvas import group
from django.conf import settings

from faces.api.apps.faces.models import FaceModel
from faces.api.apps.images.models import ImageModel
from faces.lib.celery import faces_task

from faces.api.apps.users.models import User
from faces.lib.faces_api.api import FaceAPI


log = logging.getLogger(__name__)


@faces_task()
def create_person_task(self, user_id):
    """
    :type self: faces.lib.celery.FacesTask
    :type user_id: int
    """
    user = User.objects.get(id=user_id)
    if user.face_api_id is not None:
        return

    face_api = FaceAPI()
    person_id = face_api.persons.create(group_id=settings.FACE_API_PERSON_GROUP_ID,
                                        name=user.name)

    user.face_api_id = person_id
    user.save()


@faces_task()
def add_face_from_image_task(self, user_id, image_id):
    """
    :type self: faces.lib.celery.FacesTask
    :type user_id: int
    :type image_id: int
    """
    user = User.objects.get(id=user_id)
    image = ImageModel.objects.get(id=image_id)

    face_api = FaceAPI()
    face = face_api.faces.detect(image_url=image.public_url)

    face_id = face["faceId"]
    gender = face["attributes"]["gender"]
    age = int(face["attributes"]["age"])

    FaceModel.objects.get_or_create(face_api_id=face_id,
                                    defaults=dict(user=user, image=image, gender=gender, age=age))

    user.age = age
    user.gender = gender
    user.save()

    face_api.persons.add_face(group_id=settings.FACE_API_PERSON_GROUP_ID,
                              person_id=user.face_api_id,
                              face_id=face_id)


@faces_task()
def add_face_task(self, user_id, face_id):
    """
    :type self: faces.lib.celery.FacesTask
    :type user_id: int
    :type face_id: int
    """
    user = User.objects.get(id=user_id)
    face = FaceModel.objects.get(id=face_id)

    face_api = FaceAPI()
    face_api.persons.add_face(group_id=settings.FACE_API_PERSON_GROUP_ID,
                              person_id=user.face_api_id,
                              face_id=face.face_api_id)


@faces_task()
def train_group_task(self):
    """
    :type self: faces.lib.celery.FacesTask
    """
    face_api = FaceAPI()
    face_api.person_groups.train(group_id=settings.FACE_API_PERSON_GROUP_ID)


def schedule_person_creation(user_id, image_ids):
    """
    :type user_id: int
    :type image_ids: list[int]
    """
    create_person = create_person_task.si(user_id)
    add_faces = group(add_face_from_image_task.si(user_id, image_id) for image_id in image_ids)
    train_group = train_group_task.si()

    (create_person | add_faces | train_group)()


def schedule_user_training(user_id, face_id):
    """
    :type user_id: int
    :type face_id: int
    """
    add_face = add_face_task.si(user_id, face_id)
    train_group = train_group_task.si()

    (add_face | train_group)()
