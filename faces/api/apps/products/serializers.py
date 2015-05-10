# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.serializers import json

from rest_framework import serializers
from faces.api.apps.products.models import ProductModel


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta():
        model = ProductModel
        fields = ('id', 'name', 'price', 'brand', 'images')

    brand = serializers.CharField(source="brand_name")
    images = serializers.SerializerMethodField()

    def get_images(self, product):
        """
        :type product: ProductModel
        """
        return list(product.images)
