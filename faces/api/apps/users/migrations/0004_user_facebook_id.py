# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_face_api_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facebook_id',
            field=models.CharField(default='', unique=True, max_length=255, verbose_name='facebook id'),
            preserve_default=False,
        ),
    ]
