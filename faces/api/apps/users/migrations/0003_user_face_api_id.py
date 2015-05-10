# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150509_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='face_api_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
