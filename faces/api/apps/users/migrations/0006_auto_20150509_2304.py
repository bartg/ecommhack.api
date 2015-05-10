# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[('male', 'male'), ('female', 'female')]),
        ),
    ]
