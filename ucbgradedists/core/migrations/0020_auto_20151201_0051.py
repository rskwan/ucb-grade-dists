# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20151130_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='disciplinestats',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subjectstats',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
