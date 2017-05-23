# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0011_userprofile_visit_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_list', to='houseDatabase.RentDatabase'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='visit_list',
            field=models.ManyToManyField(related_name='visit_list', to='houseDatabase.RentDatabase'),
        ),
    ]