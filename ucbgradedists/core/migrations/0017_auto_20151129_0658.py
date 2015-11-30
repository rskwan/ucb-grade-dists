# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151128_1947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subjectstats',
            options={},
        ),
        migrations.RenameField(
            model_name='subjectstats',
            old_name='grade_counts',
            new_name='distribution',
        ),
        migrations.RenameField(
            model_name='subjectstats',
            old_name='grade_average',
            new_name='mean',
        ),
        migrations.RenameField(
            model_name='subjectstats',
            old_name='grade_median',
            new_name='median',
        ),
        migrations.RenameField(
            model_name='subjectstats',
            old_name='grade_stdev',
            new_name='stdev',
        ),
        migrations.RemoveField(
            model_name='subjectstats',
            name='yearly_averages',
        ),
    ]
