# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db.models.query_utils import Q
from faces.api.apps.products.models import ProductModel
from faces.api.apps.users.models import Gender


log = logging.getLogger(__name__)


class ProductRecommender(object):

    def __init__(self, user):
        self.user = user

    def recommend(self):
        """
        :rtype: faces.api.apps.products.models.ProductModel
        """
        recommendation = self._recommend(age=self.user.age, gender=self.user.gender)
        self.user.previous_recommendation = self.user.recommendation
        self.user.recommendation = recommendation
        self.user.save()

        return recommendation

    @classmethod
    def anonymous_recommendation(cls, age=None, gender=None):
        """
        :rtype: faces.api.apps.products.models.ProductModel
        """
        return cls._recommend(age, gender)

    @classmethod
    def _recommend(cls, age=None, gender=None):
        """
        :rtype: faces.api.apps.products.models.ProductModel
        """
        q = Q()

        if gender is not None:
            if gender == Gender.MALE:
                q &= Q(gender_male=True)
            else:
                q &= Q(gender_female=True)

        if age is not None:
            if 0 < age <= 2:
                q &= Q(age_group_baby=True)
            elif 2 < age <= 12:
                q &= Q(age_group_child=True)
            elif 12 < age <= 19:
                q &= Q(age_group_teen=True)
            else:
                q &= Q(age_group_adult=True)

        return ProductModel.objects.filter(q).order_by('?').first()
