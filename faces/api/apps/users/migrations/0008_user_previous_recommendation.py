# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150509_2224'),
        ('users', '0007_user_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='previous_recommendation',
            field=models.ForeignKey(related_name='previous_reccomendation', blank=True, to='products.ProductModel', null=True),
        ),
    ]
