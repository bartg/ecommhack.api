# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import faces.lib.django.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='Deleted at')),
                ('face_api_id', models.CharField(max_length=255)),
                ('image', models.ForeignKey(related_name='+', to='images.ImageModel')),
                ('user', models.ForeignKey(related_name='faces', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at', 'pk'),
                'abstract': False,
            },
            bases=(faces.lib.django.models.ModelMixins, models.Model),
        ),
    ]
