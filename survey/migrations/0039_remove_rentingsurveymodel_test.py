# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-06 00:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0038_merge_20170503_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentingsurveymodel',
            name='test',
        ),
    ]
