# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-23 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0008_userprofile_test'),
        ('survey', '0018_auto_20161223_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initialsurveymodel',
            name='userProf',
        ),
        migrations.AddField(
            model_name='rentingsurveymodel',
            name='userProf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userAuth.UserProfile'),
            preserve_default=False,
        ),
    ]
