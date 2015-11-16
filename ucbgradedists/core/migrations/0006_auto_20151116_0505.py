# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_subjectstats'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subjectstats',
            options={'ordering': ['subject__name', 'division_set__name']},
        ),
    ]
