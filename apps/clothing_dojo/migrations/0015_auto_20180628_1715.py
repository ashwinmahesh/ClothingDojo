# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-28 17:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothing_dojo', '0014_auto_20180628_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='clothing_admin.Color'),
        ),
    ]