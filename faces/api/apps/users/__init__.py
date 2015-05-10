# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from faces.api.apps.users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'id',
        )
