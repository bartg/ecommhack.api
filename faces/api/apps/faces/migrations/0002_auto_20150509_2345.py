# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facemodel',
            name='age',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='facemodel',
            name='gender',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
