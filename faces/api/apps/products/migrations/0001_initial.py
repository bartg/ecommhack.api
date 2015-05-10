# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import faces.lib.django.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='Deleted at')),
                ('zalando_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('brand_name', models.CharField(default='', max_length=255, null=True, blank=True)),
                ('brand_key', models.CharField(max_length=255, null=True, blank=True)),
                ('image_url', models.CharField(max_length=1000)),
                ('gender_female', models.BooleanField(default=False)),
                ('gender_male', models.BooleanField(default=False)),
                ('age_group_baby', models.BooleanField(default=False)),
                ('age_group_child', models.BooleanField(default=False)),
                ('age_group_teen', models.BooleanField(default=False)),
                ('age_group_adult', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('created_at', 'pk'),
                'abstract': False,
            },
            bases=(faces.lib.django.models.ModelMixins, models.Model),
        ),
    ]
