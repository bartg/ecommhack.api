# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
import os

import uuid
from django.db.models.fields.files import FileField
from faces.lib.django.models import AbstractModel


log = logging.getLogger(__name__)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("images", filename)


class ImageModel(AbstractModel):
    file = FileField(upload_to=get_file_path)

    @property
    def public_url(self):
        """
        :rtype: unicode
        """
        return "{}{}".format(settings.HOST_NAME, self.file.url)
