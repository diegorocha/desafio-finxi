# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='condominio',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='iptu',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
        ),
    ]
