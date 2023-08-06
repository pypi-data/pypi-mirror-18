# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import yacms.pages.fields
import yacms.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='_order',
            field=yacms.core.fields.OrderField(null=True, verbose_name='Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='in_menus',
            field=yacms.pages.fields.MenusField(max_length=100, null=True, verbose_name='Show in menus', blank=True),
            preserve_default=True,
        ),
    ]
