# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='image_url',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='images',
            field=django_extensions.db.fields.json.JSONField(),
        ),
    ]
