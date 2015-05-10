# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
import logging

from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from faces.api.apps.faces.services import FaceIdentService, UnrecognizedIdentity

from faces.api.apps.images.models import ImageModel
from faces.api.apps.users.serializers import DetailedUserModelSerializer

from faces.lib.resources import GenericAPIView


log = logging.getLogger(__name__)


class FaceDetectionResource(GenericAPIView):
    parser_classes = (FileUploadParser,)
    serializer_class = DetailedUserModelSerializer

    def post(self, request):
        incoming_image = request.data.get("image")
        if incoming_image is None:
            raise ValidationError("image is required")

        image = ImageModel.objects.create(file=incoming_image)

        face_ident_service = FaceIdentService()

        try:
            identity = face_ident_service.identify(from_image=image)
        except UnrecognizedIdentity as e:
            return Response(status=status.HTTP_200_OK, data={"gender": e.gender, "age": e.age})

        if not identity:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user, confidence = identity

        serializer = self.get_serializer(user)
        return Response(data=serializer.data,
                        headers={"X-Faces-Confidence": confidence})
