# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imoveis.models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0002_auto_20160417_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='foto',
            field=models.ImageField(upload_to=imoveis.models.imovel_foto_path, blank=True),
        ),
    ]
