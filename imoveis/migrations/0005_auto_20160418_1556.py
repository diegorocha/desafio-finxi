# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0004_auto_20160417_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='cidade',
            field=models.CharField(max_length=50, default='Rio de Janeiro'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imovel',
            name='endereco_formatado',
            field=models.CharField(editable=False, max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imovel',
            name='endereco',
            field=models.CharField(max_length=100, help_text='Exemplo: Rua Baronesa, 175'),
        ),
    ]
