# coding: utf-8
from django.db import models
from .choices import UF
from unipath import Path
from uuid import uuid4
from .helpers import get_coordenates

def imovel_foto_path(instance, filename):
    return 'imovel/{}{}'.format(uuid4(), Path(filename).ext)

class Imovel(models.Model):

    descricao = models.TextField(blank=False, help_text="Insira aqui a descrição do imóvel")
    foto = models.ImageField(blank=False, upload_to=imovel_foto_path)
    endereco = models.CharField(blank=False, max_length=100, help_text="Exemplo: Rua Baronesa, 175")
    cep = models.CharField(blank=False, max_length=8)
    uf = models.CharField(blank=False, max_length=2, null=True, choices=UF)
    cidade = models.CharField(blank=False, max_length=50)
    endereco_formatado = models.CharField(editable=False, max_length=200)
    longitude = models.FloatField(editable=False)
    latitude = models.FloatField(editable=False)
    quartos = models.PositiveSmallIntegerField(help_text="Numero de quartos do imóvel", default=1)
    suites = models.PositiveSmallIntegerField(help_text="Numero de quartos que são suite", default=0)
    area = models.PositiveSmallIntegerField(help_text="Área em m²")
    vagas = models.PositiveSmallIntegerField(help_text="Quantas Vagas na garagem?", default=0)
    aluguel = models.DecimalField(blank=False, max_digits=8, decimal_places=2)
    condominio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iptu = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    telefone = models.CharField(blank=False, max_length=11)
    email = models.EmailField(blank=False, help_text="E-mail de contato")
    disponivel = models.BooleanField(default=True, help_text="Desmarque se o imóvel não estiver mais disponível")
    incluido = models.DateTimeField(auto_now_add=True, editable=False)
    alterado = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        #Se um dos dois nao tiver preenchido
        if not (self.latitude and self.longitude):
            endereco_busca = '%s, %s' % (self.endereco, self.cidade)
            coordenadas = get_coordenates(endereco=endereco_busca)
            if coordenadas:
                self.latitude = coordenadas[0]
                self.longitude = coordenadas[1]
                self.endereco_formatado = coordenadas[2]
        super(Imovel, self).save(*args, **kwargs)

    @classmethod
    def get_disponiveis(cls_obj):
        return Imovel.objects.filter(disponivel=True)


    class Meta:
        ordering = ('-incluido',)
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

    def __str__(self):
        return 'Imóvel em {}'.format(self.endereco)