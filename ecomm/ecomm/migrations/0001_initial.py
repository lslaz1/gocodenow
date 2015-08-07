# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(to='ecomm.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('orderproducts', models.ManyToManyField(to='ecomm.Order', through='ecomm.OrderProduct')),
            ],
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(to='ecomm.Product'),
        ),
    ]
