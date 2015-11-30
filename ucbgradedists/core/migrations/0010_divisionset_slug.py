# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20151117_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='divisionset',
            name='slug',
            field=models.SlugField(default=b''),
        ),
    ]
