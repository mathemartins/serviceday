# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-16 01:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0005_auto_20171209_0740'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curatedskills',
            options={'verbose_name': 'Curated Skill', 'verbose_name_plural': 'Curated Skills'},
        ),
    ]