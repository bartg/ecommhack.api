# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
import logging
from django_extensions.db.fields.json import JSONField

from faces.lib.django.models import AbstractModel
from django.db import models
from faces.lib.zalando_api import Genders, AgeGroups


log = logging.getLogger(__name__)


class ProductModel(AbstractModel):
    zalando_id = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    brand_name = models.CharField(max_length=255, null=True, blank=True, default="")
    brand_key = models.CharField(max_length=255, null=True, blank=True)

    images = JSONField()

    gender_female = models.BooleanField(default=False)
    gender_male = models.BooleanField(default=False)

    age_group_baby = models.BooleanField(default=False)
    age_group_child = models.BooleanField(default=False)
    age_group_teen = models.BooleanField(default=False)
    age_group_adult = models.BooleanField(default=False)

    @classmethod
    def from_zalando_article(cls, article):
        """
        :type article: dict
        :rtype: (ProductModel, bool)
        """
        return cls.objects.get_or_create(
            zalando_id=article["id"],
            defaults=dict(
                zalando_id=article["id"],
                name=article["name"],
                price=Decimal(article["units"][0]["price"]["value"]),
                brand_name=article["brand"]["name"],
                brand_key=article["brand"]["key"],
                images=article["media"]["images"],

                gender_male=Genders.MALE in article["genders"],
                gender_female=Genders.FEMALE in article["genders"],

                age_group_baby=AgeGroups.BABY in article["ageGroups"],
                age_group_child=AgeGroups.CHILD in article["ageGroups"],
                age_group_teen=AgeGroups.TEEN in article["ageGroups"],
                age_group_adult=AgeGroups.ADULT in article["ageGroups"]
            )
        )
