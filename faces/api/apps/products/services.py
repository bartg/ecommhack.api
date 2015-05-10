# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db.models.query_utils import Q
from faces.api.apps.products.models import ProductModel


log = logging.getLogger(__name__)


class RecommendationService(object):

    def __init__(self, user):
        self.user = user

    def recommend(self):
        """
        :rtype: faces.api.apps.products.models.ProductModel
        """
        q = Q()

        if self.user.has_gender:
            if self.user.is_male:
                q &= Q(gender_male=True)
            else:
                q &= Q(gender_female=True)

        if self.user.age:
            age = self.user.age

            if 0 < age <= 2:
                q &= Q(age_group_baby=True)
            elif 2 < age <= 12:
                q &= Q(age_group_child=True)
            elif 12 < age <= 19:
                q &= Q(age_group_teen=True)
            else:
                q &= Q(age_group_adult=True)

        recommendation = ProductModel.objects.filter(q).order_by('?').first()

        self.user.recommendation = recommendation
        self.user.save()

        return recommendation
