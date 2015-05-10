# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from faces.api.apps.products.models import ProductModel
from faces.api.apps.products.recommender import ProductRecommender
from faces.api.apps.products.serializers import ProductModelSerializer
from faces.api.apps.users.models import User
from faces.lib.resources import APIListResource, APIResource


log = logging.getLogger(__name__)


class ProductListResource(APIListResource):
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        return ProductModel.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductRecommendationResource(APIResource):
    serializer_class = ProductModelSerializer

    def post(self, request):
        user_id = request.GET.get("user_id", None)

        if user_id is None:
            age = request.GET.get("age", None)
            gender = request.GET.get("gender", None)

            product = ProductRecommender.anonymous_recommendation(age=age, gender=gender)
        else:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound()

            recommender = ProductRecommender(user=user)
            product = recommender.recommend()

        serializer = self.get_serializer(product)
        return Response(data=serializer.data)

    def get(self, request):
        user_id = request.GET.get("user_id", None)
        if user_id is None:
            raise ValidationError("Missing query param: user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound()

        if user.recommendation is None:
            raise NotFound()

        serializer = self.get_serializer(user.previous_recommendation)
        return Response(data=serializer.data)
