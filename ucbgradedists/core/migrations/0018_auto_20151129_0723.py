# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20151129_0658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='grade_average',
            new_name='mean',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='grade_stdev',
            new_name='stdev',
        ),
    ]
