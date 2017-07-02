from itertools import cycle

from django.db.utils import IntegrityError
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe

from imoveis.helpers import get_coordenates
from imoveis.models import Imovel


class ImovelTest(TestCase):
    def setUp(self):
        self.endereco_base = 'Rua Baronesa, 175'
        self.cidade_base = 'Rio de Janeiro'
        self.lat_base = -22.8950148
        self.lng_base = -43.3542673
        self.imovel = mommy.make(Imovel)
        self.basic_imovel_recipe = Recipe(Imovel, latitude=None, longitude=None)
        imoveis_recipe = Recipe(Imovel,
                                endereco=self.endereco_base,
                                cidade=self.cidade_base,
                                latitude=self.lat_base,
                                longitude=self.lng_base,
                                disponivel=cycle([False, True])
                                )
        # Cria 9 imóveis alterando disponíveis e indisponíveis
        imoveis_recipe.make(_quantity=9)

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
        imovel = self.basic_imovel_recipe.prepare()
        with self.assertRaises(IntegrityError):
            imovel.save()

    def test_custom_save(self):
        imovel = self.basic_imovel_recipe.prepare(endereco=self.endereco_base, cidade=self.cidade_base)
        imovel.save()
        self.assertIsNotNone(imovel.latitude)
        self.assertIsNotNone(imovel.longitude)
        self.assertIsNotNone(imovel.endereco_formatado)

    def test_remover_anuncio(self):
        self.imovel.remover_anuncio()
        self.assertFalse(self.imovel.disponivel)

    def test_str(self):
        self.assertTrue('Imóvel em %s' % self.imovel.endereco, str(self.imovel))
