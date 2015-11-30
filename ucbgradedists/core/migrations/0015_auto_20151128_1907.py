# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_disciplinestats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disciplinestats',
            old_name='division',
            new_name='division_set',
        ),
    ]
