# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from faces.lib.django.models import AbstractModel
from django.db import models


log = logging.getLogger(__name__)


class FaceModel(AbstractModel):
    user = models.ForeignKey("users.User", related_name="faces")
    image = models.ForeignKey("images.ImageModel", related_name="+")
    face_api_id = models.CharField(max_length=255)

    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
