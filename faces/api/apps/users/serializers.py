# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.fields import CharField, IntegerField, DateTimeField, SerializerMethodField
from faces.api.apps.users import UserModelSerializer
from faces.api.apps.users.models import User
from faces.lib.authentication import JWTAuthentication


class DetailedUserModelSerializer(UserModelSerializer):
    avatar = SerializerMethodField(read_only=True)

    class Meta(UserModelSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'name',
            'avatar',
            'age',
            'gender'
        )

    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['view'].request.build_absolute_uri(obj.avatar.file.url)
        return None
