# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-27 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape_items', '0002_auto_20180927_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapeditems',
            name='category_discount',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='scrapeditems',
            name='list_price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='scrapeditems',
            name='price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='scrapeditems',
            name='wholesale_price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]