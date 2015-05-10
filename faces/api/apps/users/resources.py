# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework.response import Response
from faces.api.apps.users.serializers import DetailedUserModelSerializer
from faces.lib.resources import GenericAPIView


log = logging.getLogger(__name__)


class MeResource(GenericAPIView):
    serializer_class = DetailedUserModelSerializer

    def get(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data, status=200)
