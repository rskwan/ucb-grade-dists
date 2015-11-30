# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151127_0724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('slug', models.SlugField(default=b'')),
            ],
        ),
        migrations.RemoveField(
            model_name='subject',
            name='category',
        ),
        migrations.AddField(
            model_name='subject',
            name='discipline',
            field=models.ForeignKey(to='core.Discipline', null=True),
        ),
    ]
