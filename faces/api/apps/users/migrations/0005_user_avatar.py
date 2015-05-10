# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('users', '0004_user_facebook_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(related_name='+', blank=True, to='images.ImageModel', null=True),
        ),
    ]
