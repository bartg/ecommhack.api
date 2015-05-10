# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from django.conf import settings
from faces.lib.sphere_api.api import SphereAPIAuthenticator


log = logging.getLogger(__name__)


def run(*args):
    authenticator = SphereAPIAuthenticator(client_id=settings.SPHERE_API_CLIENT_ID,
                                           client_secret=settings.SPHERE_API_CLIENT_SECRET,
                                           project_key=settings.SPHERE_API_PROJECT_KEY)
    auth = authenticator.auth()

    log.info(auth)
