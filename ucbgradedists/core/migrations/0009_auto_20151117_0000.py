# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_subjectstats_grade_counts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectstats',
            old_name='term_averages',
            new_name='yearly_averages',
        ),
    ]
