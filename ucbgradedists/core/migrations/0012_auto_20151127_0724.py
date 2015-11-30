# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_subject_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='canonical',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
