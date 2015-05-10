# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150509_2224'),
        ('users', '0006_auto_20150509_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='recommendation',
            field=models.ForeignKey(blank=True, to='products.ProductModel', null=True),
        ),
    ]
