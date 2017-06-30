# coding: utf-8
from uuid import uuid4

from django.core.urlresolvers import reverse
from django.db import models
from unipath import Path

from imoveis.choices import UF
from imoveis.helpers import get_min_max_coordenates, get_coordenates


def imovel_foto_path(instance, filename):
    return 'imovel/{}{}'.format(uuid4(), Path(filename).ext)


class Imovel(models.Model):
    class Meta:
        ordering = ('-incluido',)
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

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

    @classmethod
    def get_disponiveis(cls_obj):
        return Imovel.objects.filter(disponivel=True)

    @classmethod
    def get_proximos_a(cls_obj, latitude, longitude):
        """
        Calculos com latitude e longitude são complicados.
        O ideal seria usar a https://pt.wikipedia.org/wiki/F%C3%B3rmula_de_Haversine
        para testar a distancia de cada imóvel ao endereço de busca.
        Mas, além de complicado de implementar numa consultado do django seria problematico
        quando o banco de dados ficasse cheio de imóveis.

        Resolvi usar a seguinte abordagem:
        A função get_min_max_coordenates calcula as latitudes e longitudes
        mínimas e máximas com n km de distancia (aproximada).
        Nesse caso n=1 km

        Assim, eu filtro os imoveis cujas latitude e longitude fiquem dentro desse quadrado.
        É claro que essa lista pode retornar imoveis que estejam a mais de 1km de distância
        do endereço, afinal, geramos um quadrado ao invés de um circulo.

        Como o conjunto de imóveis já foi reduzido, uma solução para isso seria filtrar os imóveis
        retornado pelo orm novamente, testando a distância entre cada um e ponto através da formula.
        Os imóveis fora do circúlo, mas retornados pela consulta seriam eliminados,
        ficando apenas os dentro do circulo.

        """
        bounds = get_min_max_coordenates(latitude, longitude)
        return Imovel.get_disponiveis().filter(latitude__gte=bounds[0],
                                               latitude__lte=bounds[1],
                                               longitude__gte=bounds[2],
                                               longitude__lte=bounds[3])

    def get_absolute_url(self):
        return reverse('imoveis:detalhe', kwargs={'imovel_id': self.pk})

    def save(self, *args, **kwargs):
        # Se um dos dois nao tiver preenchido
        if not (self.latitude and self.longitude):
            endereco_busca = '%s, %s' % (self.endereco, self.cidade)
            coordenadas = get_coordenates(endereco=endereco_busca)
            if coordenadas:
                self.latitude = coordenadas[0]
                self.longitude = coordenadas[1]
                self.endereco_formatado = coordenadas[2]
        super(Imovel, self).save(*args, **kwargs)

    def remover_anuncio(self):
        self.disponivel = False
        self.save()

    def __str__(self):
        return 'Imóvel em {}'.format(self.endereco)
