# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20151201_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplinestats',
            name='rank_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subjectstats',
            name='rank_count',
            field=models.IntegerField(default=0),
        ),
    ]
