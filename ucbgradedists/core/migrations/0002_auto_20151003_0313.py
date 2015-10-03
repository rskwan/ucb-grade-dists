# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='letter',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='grade',
            name='points',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='instructor',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='section',
            name='number',
            field=models.CharField(max_length=10),
        ),
    ]
