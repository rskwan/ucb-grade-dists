# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151128_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disciplinestats',
            old_name='average',
            new_name='mean',
        ),
    ]
