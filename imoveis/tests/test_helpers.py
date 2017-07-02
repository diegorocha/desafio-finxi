from random import randrange, choice

from django.test import TestCase

from imoveis import helpers
from imoveis.helpers import LAT_DELTA
from imoveis.helpers import LNG_DELTA


class HelpersTest(TestCase):

    def setUp(self):
        self.lat_delta = LAT_DELTA
        self.lng_delta = LNG_DELTA

    def test_get_min_max_coordenates(self):
        """ Garante que os valores retornados estão corretos."""
        bounds = helpers.get_min_max_coordenates()
        self.assertEqual((-self.lat_delta, self.lat_delta, -self.lng_delta, self.lng_delta), bounds)

    def test_get_min_max_coordenates_2(self):
        """ Garante que os valores retornados estão corretos."""
        lat = randrange(-45, 45)
        lng = randrange(-45, 45)
        bounds = helpers.get_min_max_coordenates(lat, lng)
        self.assertEqual((lat - self.lat_delta, lat + self.lat_delta, lng - self.lng_delta, lng + self.lng_delta), bounds)

    def test_get_coordenates_endereco_invalido(self):
        coordenadas = helpers.get_coordenates("")
        self.assertEqual(None, coordenadas)

    def test_get_coordenates_endereco_valido(self):
        cases = [
            ('Rua da Quitanda, 86, Rio de Janeiro', (-22.9026854, -43.1769713, 'R. da Quitanda, 86 - Centro, Rio de Janeiro - RJ, Brasil')),
            ('Rua da Baronesa, 175, Rio de Janeiro', (-22.8950398, -43.3541986, 'R. Baronesa, 175 - Praça Seca, Rio de Janeiro - RJ, Brasil')),
            ('Avenida Celia Ribeiro, 100 Rio de Janeiro', (-22.9951457, -43.3800536, 'Av. Célia Ribeiro da Silva Mendes, 100 - Barra da Tijuca, Rio de Janeiro - RJ, Brasil')),
        ]
        selected_case = choice(cases)
        coordenadas = helpers.get_coordenates(selected_case[0])
        expected = selected_case[1]
        self.assertEqual(expected, coordenadas)
