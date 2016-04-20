# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import imoveis.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('descricao', models.TextField(help_text='Insira aqui a descrição do imóvel')),
                ('foto', models.ImageField(upload_to=imoveis.models.imovel_foto_path)),
                ('endereco', models.CharField(help_text='Exemplo: Rua Baronesa, 175, Rio de Janeiro', max_length=100)),
                ('cep', models.CharField(max_length=8)),
                ('uf', models.CharField(choices=[('', 'Escolha uma opção'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MT', 'Mato Grosso'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True)),
                ('longitude', models.FloatField(editable=False)),
                ('latitude', models.FloatField(editable=False)),
                ('quartos', models.PositiveSmallIntegerField(help_text='Numero de quartos do imóvel', default=1)),
                ('suites', models.PositiveSmallIntegerField(help_text='Numero de quartos que são suite', default=0)),
                ('area', models.PositiveSmallIntegerField(help_text='Área em m²')),
                ('vagas', models.PositiveSmallIntegerField(help_text='Quantas Vagas na garagem?', default=0)),
                ('aluguel', models.DecimalField(max_digits=8, decimal_places=2)),
                ('condominio', models.DecimalField(max_digits=8, decimal_places=2)),
                ('iptu', models.DecimalField(max_digits=8, decimal_places=2)),
                ('telefone', models.CharField(max_length=11)),
                ('email', models.EmailField(help_text='E-mail de contato', max_length=254)),
                ('disponivel', models.BooleanField(help_text='Desmarque se o imóvel não estiver mais disponível', default=True)),
                ('incluido', models.DateTimeField(auto_now_add=True)),
                ('alterado', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-incluido',),
                'verbose_name_plural': 'Imóveis',
                'verbose_name': 'Imóvel',
            },
        ),
    ]
