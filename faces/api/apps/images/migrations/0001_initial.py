# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import faces.api.apps.images.models
import datetime
import faces.lib.django.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='Deleted at')),
                ('file', models.FileField(upload_to=faces.api.apps.images.models.get_file_path)),
            ],
            options={
                'ordering': ('created_at', 'pk'),
                'abstract': False,
            },
            bases=(faces.lib.django.models.ModelMixins, models.Model),
        ),
    ]
