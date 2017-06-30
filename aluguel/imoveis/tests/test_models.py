from django.db.utils import IntegrityError
from django.test import TestCase
from model_mommy import mommy
from requests import get

from aluguel.imoveis.helpers import get_coordenates
from aluguel.imoveis.models import Imovel


class ImovelTest(TestCase):
    def setUp(self):
        self.imovel = mommy.make(Imovel)
        for i in range(9):
            imovel = mommy.make(Imovel)
            # Corrige para um endereço de verdade
            imovel.endereco = 'Rua Baronesa, 175'
            imovel.cidade = 'Rio de Janeiro'
            imovel.latitude = -22.8950148
            imovel.longitude = -43.3542673
            # Remove metade dos anúncios
            if i % 2 == 0:
                imovel.disponivel = False
            imovel.save()

    def test_get_disponiveis_qtd(self):
        """Garante que tem 5 imóveis disponíveis apenas"""
        imoveis = Imovel.get_disponiveis()
        self.assertEqual(5, len(imoveis))

    def test_get_disponiveis_value(self):
        """Garante que todos os imóveis retornados estão com disponível True"""
        imoveis = Imovel.get_disponiveis()
        self.assertEqual([True] * len(imoveis), [i.disponivel for i in imoveis])

    def test_get_proximos_a_vazio(self):
        imoveis = Imovel.get_proximos_a(latitude=0, longitude=0)
        self.assertEqual(0, len(imoveis))

    def test_get_proximos(self):
        coordenadas = get_coordenates("Rua Baronesa, 300, Rio de Janeiro")
        imoveis = Imovel.get_proximos_a(latitude=coordenadas[0], longitude=coordenadas[1])
        self.assertLess(0, len(imoveis))

    def test_custom_save_erro(self):
        imovel = mommy.make(Imovel)
        imovel.latitude = None
        imovel.longitude = None
        with self.assertRaises(IntegrityError):
            imovel.save()

    def test_custom_save(self):
        imovel = mommy.make(Imovel)
        imovel.latitude = None
        imovel.longitude = None
        imovel.endereco = 'Rua Baronesa, 175'
        imovel.cidade = 'Rio de Janeiro'
        imovel.save()
        self.assertIsNotNone(imovel.latitude)
        self.assertIsNotNone(imovel.longitude)
        self.assertIsNotNone(imovel.endereco_formatado)

    def test_remover_anuncio(self):
        self.imovel.remover_anuncio()
        self.assertFalse(self.imovel.disponivel)

    def test_url_foto(self):
        retornos = []
        for imovel in Imovel.objects.all():
            r = get(imovel.foto.url)
            # Salva o retorno das chamadas http da url das imagens ou None se não tiver
            retornos.append(r.status_code if r else None)
        self.assertEqual([200] * len(retornos), retornos)

    def test_str(self):
        self.assertTrue('Imóvel em %s' % self.imovel.endereco, str(self.imovel))
